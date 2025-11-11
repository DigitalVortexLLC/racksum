"""
WebAuthn/Passkey Authentication Views
"""

import os
import base64
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model, login, logout
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    PublicKeyCredentialDescriptor,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier

from .models import Passkey, PasskeyChallenge

User = get_user_model()

# WebAuthn configuration
RP_ID = os.getenv("WEBAUTHN_RP_ID", "localhost")
RP_NAME = os.getenv("WEBAUTHN_RP_NAME", "RackSum")
ORIGIN = os.getenv("WEBAUTHN_ORIGIN", "http://localhost:3000")

# Authentication requirement
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "false").lower() == "true"


@extend_schema(
    summary="Get authentication configuration",
    description="Retrieve authentication settings and ensure CSRF cookie is set for the session",
    tags=["Authentication"],
    responses={
        200: {
            "description": "Authentication configuration",
            "content": {"application/json": {"example": {"require_auth": False, "passkey_supported": True}}},
        }
    },
)
@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def auth_config(request):
    """
    Get authentication configuration and ensure CSRF cookie is set
    """
    return Response(
        {
            "require_auth": REQUIRE_AUTH,
            "passkey_supported": True,
        }
    )


@extend_schema(
    summary="Begin passkey registration",
    description="Start the WebAuthn passkey registration process. Creates a new user if needed and generates registration options.",
    tags=["Authentication"],
    request={"application/json": {"example": {"username": "john_doe", "email": "john@example.com"}}},
    responses={
        200: {
            "description": "Registration options for WebAuthn ceremony",
            "content": {"application/json": {"example": {"options": "...", "user_id": 1}}},
        }
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def begin_registration(request):
    """
    Start passkey registration process
    Generates WebAuthn registration options
    """
    username = request.data.get("username")
    email = request.data.get("email", f"{username}@racksum.local")

    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user exists, create if not
    user, created = User.objects.get_or_create(username=username, defaults={"email": email})

    if not created and Passkey.objects.filter(user=user).exists():
        # User already has passkeys, require authentication first
        pass  # Allow adding additional passkeys

    # Get existing passkeys for this user (to exclude them)
    existing_passkeys = Passkey.objects.filter(user=user)
    exclude_credentials = [
        PublicKeyCredentialDescriptor(id=base64.b64decode(pk.credential_id)) for pk in existing_passkeys
    ]

    # Generate registration options
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=str(user.id).encode("utf-8"),
        user_name=user.username,
        user_display_name=user.get_full_name() or user.username,
        exclude_credentials=exclude_credentials,
        authenticator_selection=AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.PLATFORM,
            resident_key=ResidentKeyRequirement.PREFERRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.ECDSA_SHA_256,
            COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
        ],
    )

    # Store challenge
    challenge_b64 = base64.b64encode(options.challenge).decode("utf-8")
    PasskeyChallenge.objects.create(
        user=user,
        challenge=challenge_b64,
        challenge_type="registration",
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    # Convert options to JSON format for frontend
    options_json = options_to_json(options)

    return Response(
        {
            "options": options_json,
            "user_id": user.id,
        }
    )


@extend_schema(
    summary="Complete passkey registration",
    description="Complete the WebAuthn passkey registration by verifying the credential and storing it. Automatically logs the user in.",
    tags=["Authentication"],
    request={"application/json": {"example": {"user_id": 1, "credential": {}, "name": "My Laptop"}}},
    responses={
        200: {
            "description": "Registration successful",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Passkey registered successfully",
                        "passkey_id": 1,
                        "user": {"id": 1, "username": "john_doe", "email": "john@example.com"},
                    }
                }
            },
        }
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def complete_registration(request):
    """
    Complete passkey registration
    Verifies the registration response and stores the credential
    """
    user_id = request.data.get("user_id")
    credential = request.data.get("credential")
    passkey_name = request.data.get("name", "My Passkey")

    if not user_id or not credential:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the challenge
    try:
        challenge_obj = PasskeyChallenge.objects.filter(
            user=user, challenge_type="registration", expires_at__gt=timezone.now()
        ).latest("created_at")
    except PasskeyChallenge.DoesNotExist:
        return Response({"error": "Challenge not found or expired"}, status=status.HTTP_400_BAD_REQUEST)

    challenge = base64.b64decode(challenge_obj.challenge)

    try:
        # Verify the registration response
        verification = verify_registration_response(
            credential=credential,
            expected_challenge=challenge,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
        )

        # Store the passkey
        credential_id_b64 = base64.b64encode(verification.credential_id).decode("utf-8")
        public_key_b64 = base64.b64encode(verification.credential_public_key).decode("utf-8")

        passkey = Passkey.objects.create(
            user=user,
            credential_id=credential_id_b64,
            public_key=public_key_b64,
            sign_count=verification.sign_count,
            aaguid=str(verification.aaguid) if verification.aaguid else "",
            name=passkey_name,
        )

        # Clean up used challenge
        challenge_obj.delete()

        # Log the user in
        login(request, user)

        return Response(
            {
                "success": True,
                "message": "Passkey registered successfully",
                "passkey_id": passkey.id,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )

    except Exception as e:
        return Response({"error": f"Registration verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Begin passkey authentication",
    description="Start the WebAuthn passkey authentication process. Optionally provide username to authenticate a specific user.",
    tags=["Authentication"],
    request={"application/json": {"example": {"username": "john_doe"}}},
    responses={
        200: {
            "description": "Authentication options for WebAuthn ceremony",
            "content": {"application/json": {"example": {"options": "..."}}},
        }
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def begin_authentication(request):
    """
    Start passkey authentication process
    Generates WebAuthn authentication options
    """
    username = request.data.get("username")

    # Generate authentication options
    # If username provided, get their passkeys
    # Otherwise, allow discoverable credentials
    allow_credentials = []
    user = None

    if username:
        try:
            user = User.objects.get(username=username)
            passkeys = Passkey.objects.filter(user=user)

            if not passkeys.exists():
                return Response({"error": "No passkeys found for this user"}, status=status.HTTP_404_NOT_FOUND)

            allow_credentials = [
                PublicKeyCredentialDescriptor(id=base64.b64decode(pk.credential_id)) for pk in passkeys
            ]
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Generate authentication options
    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    # Store challenge
    challenge_b64 = base64.b64encode(options.challenge).decode("utf-8")
    PasskeyChallenge.objects.create(
        user=user,
        challenge=challenge_b64,
        challenge_type="authentication",
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    # Convert options to JSON format for frontend
    options_json = options_to_json(options)

    return Response(
        {
            "options": options_json,
        }
    )


@extend_schema(
    summary="Complete passkey authentication",
    description="Complete the WebAuthn passkey authentication by verifying the credential. Logs the user in on success.",
    tags=["Authentication"],
    request={"application/json": {"example": {"credential": {}}}},
    responses={
        200: {
            "description": "Authentication successful",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Authentication successful",
                        "user": {"id": 1, "username": "john_doe", "email": "john@example.com"},
                    }
                }
            },
        }
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def complete_authentication(request):
    """
    Complete passkey authentication
    Verifies the authentication response and logs the user in
    """
    credential = request.data.get("credential")

    if not credential:
        return Response({"error": "Missing credential"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract credential ID to find the passkey
    try:
        credential_id = credential.get("id") or credential.get("rawId")
        if not credential_id:
            raise ValueError("Credential ID not found")

        # Find the passkey
        passkey = Passkey.objects.get(credential_id=credential_id)
        user = passkey.user

    except Passkey.DoesNotExist:
        return Response({"error": "Passkey not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Invalid credential: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Get the challenge
    try:
        challenge_obj = (
            PasskeyChallenge.objects.filter(challenge_type="authentication", expires_at__gt=timezone.now())
            .filter(models.Q(user=user) | models.Q(user__isnull=True))
            .latest("created_at")
        )
    except PasskeyChallenge.DoesNotExist:
        return Response({"error": "Challenge not found or expired"}, status=status.HTTP_400_BAD_REQUEST)

    challenge = base64.b64decode(challenge_obj.challenge)
    public_key = base64.b64decode(passkey.public_key)

    try:
        # Verify the authentication response
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=challenge,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
            credential_public_key=public_key,
            credential_current_sign_count=passkey.sign_count,
        )

        # Update sign count
        passkey.sign_count = verification.new_sign_count
        passkey.last_used_at = timezone.now()
        passkey.save()

        # Clean up used challenge
        challenge_obj.delete()

        # Log the user in
        login(request, user)

        return Response(
            {
                "success": True,
                "message": "Authentication successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )

    except Exception as e:
        return Response({"error": f"Authentication verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="List user's passkeys",
    description="Retrieve all passkeys registered for the authenticated user",
    tags=["Authentication"],
    responses={
        200: {
            "description": "List of passkeys",
            "content": {
                "application/json": {
                    "example": {
                        "passkeys": [
                            {
                                "id": 1,
                                "name": "My Laptop",
                                "created_at": "2024-11-09T10:00:00Z",
                                "last_used_at": "2024-11-09T12:00:00Z",
                                "aaguid": "...",
                            }
                        ]
                    }
                }
            },
        }
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_passkeys(request):
    """
    List all passkeys for the current user
    """
    passkeys = Passkey.objects.filter(user=request.user)

    return Response(
        {
            "passkeys": [
                {
                    "id": pk.id,
                    "name": pk.name,
                    "created_at": pk.created_at,
                    "last_used_at": pk.last_used_at,
                    "aaguid": pk.aaguid,
                }
                for pk in passkeys
            ]
        }
    )


@extend_schema(
    summary="Delete a passkey",
    description="Delete a specific passkey belonging to the authenticated user",
    tags=["Authentication"],
    parameters=[OpenApiParameter(name="passkey_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)],
    responses={
        200: {
            "description": "Passkey deleted successfully",
            "content": {"application/json": {"example": {"success": True, "message": "Passkey deleted successfully"}}},
        }
    },
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_passkey(request, passkey_id):
    """
    Delete a passkey
    """
    try:
        passkey = Passkey.objects.get(id=passkey_id, user=request.user)
        passkey.delete()

        return Response({"success": True, "message": "Passkey deleted successfully"})
    except Passkey.DoesNotExist:
        return Response({"error": "Passkey not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    summary="Logout user",
    description="Logout the current authenticated user and end their session",
    tags=["Authentication"],
    responses={
        200: {
            "description": "Logged out successfully",
            "content": {"application/json": {"example": {"success": True, "message": "Logged out successfully"}}},
        }
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout the current user
    """
    logout(request)
    return Response({"success": True, "message": "Logged out successfully"})


@extend_schema(
    summary="Get current user",
    description="Retrieve information about the current authenticated user",
    tags=["Authentication"],
    responses={
        200: {
            "description": "Current user information",
            "content": {
                "application/json": {
                    "example": {"user": {"id": 1, "username": "john_doe", "email": "john@example.com"}}
                }
            },
        }
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user
    """
    return Response(
        {
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        }
    )

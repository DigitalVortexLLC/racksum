import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Site, RackConfiguration
from .serializers import (
    SiteSerializer,
    RackConfigurationSerializer,
    RackConfigurationCreateSerializer
)


class SiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Site CRUD operations
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new site
        """
        name = request.data.get('name')
        description = request.data.get('description')

        if not name or not isinstance(name, str) or not name.strip():
            return Response(
                {'error': 'Site name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            site = Site.objects.create(
                name=name.strip(),
                description=description or None
            )
            serializer = self.get_serializer(site)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'error': 'A site with this name already exists'},
                status=status.HTTP_409_CONFLICT
            )

    def update(self, request, *args, **kwargs):
        """
        Update an existing site
        """
        name = request.data.get('name')
        description = request.data.get('description')

        if not name or not isinstance(name, str) or not name.strip():
            return Response(
                {'error': 'Site name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            instance = self.get_object()
            instance.name = name.strip()
            instance.description = description or None
            instance.save()

            return Response({
                'success': True,
                'message': 'Site updated successfully'
            })
        except IntegrityError:
            return Response(
                {'error': 'A site with this name already exists'},
                status=status.HTTP_409_CONFLICT
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a site
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Site deleted successfully'
        })


@api_view(['GET', 'POST'])
def rack_operations_view(request, site_id):
    """
    Combined view for GET (list racks) and POST (save rack) operations
    """
    if request.method == 'GET':
        try:
            site = get_object_or_404(Site, id=site_id)
            racks = RackConfiguration.objects.filter(site=site)
            serializer = RackConfigurationSerializer(racks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch rack configurations', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        try:
            site = get_object_or_404(Site, id=site_id)

            name = request.data.get('name')
            config_data = request.data.get('configData')
            description = request.data.get('description')

            if not name or not isinstance(name, str) or not name.strip():
                return Response(
                    {'error': 'Rack name is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not config_data or not isinstance(config_data, dict):
                return Response(
                    {'error': 'Configuration data is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update or create
            rack, created = RackConfiguration.objects.update_or_create(
                site=site,
                name=name.strip(),
                defaults={
                    'config_data': config_data,
                    'description': description or None
                }
            )

            return Response(
                {
                    'id': rack.id,
                    'siteId': site.id,
                    'name': rack.name,
                    'description': rack.description
                },
                status=status.HTTP_201_CREATED
            )
        except Site.DoesNotExist:
            return Response(
                {'error': 'Site not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to save rack configuration', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def get_rack_configuration(request, site_id, rack_name):
    """
    Get a specific rack configuration
    """
    try:
        site = get_object_or_404(Site, id=site_id)
        rack = RackConfiguration.objects.filter(
            site=site,
            name=rack_name
        ).first()

        if not rack:
            return Response(
                {'error': 'Rack configuration not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RackConfigurationSerializer(rack)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch rack configuration', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_rack_configuration(request, rack_id):
    """
    Delete a rack configuration
    """
    try:
        rack = get_object_or_404(RackConfiguration, id=rack_id)
        rack.delete()
        return Response({
            'success': True,
            'message': 'Rack configuration deleted successfully'
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to delete rack configuration', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_all_racks(request):
    """
    Get all rack configurations across all sites
    """
    try:
        racks = RackConfiguration.objects.select_related('site').all()
        serializer = RackConfigurationSerializer(racks, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch rack configurations', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def load_rack_config(request):
    """
    Load rack configuration endpoint (matches Express /api/load)
    """
    try:
        rack_config = request.data

        if not rack_config or not isinstance(rack_config, dict):
            return Response(
                {'error': 'Invalid rack configuration data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'success': True,
            'message': 'Configuration received successfully',
            'config': rack_config,
            'redirectUrl': '/?loadConfig=true'
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to process rack configuration', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_devices(request):
    """
    Serve devices.json file
    """
    try:
        devices_path = os.path.join(settings.BASE_DIR.parent, 'src', 'data', 'devices.json')
        with open(devices_path, 'r') as f:
            devices = json.load(f)
        return Response(devices)
    except FileNotFoundError:
        return Response(
            {'error': 'Devices file not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to load devices', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

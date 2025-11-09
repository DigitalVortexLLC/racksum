import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Site, RackConfiguration, Device, Rack, RackDevice
from .serializers import (
    SiteSerializer,
    RackConfigurationSerializer,
    RackConfigurationCreateSerializer,
    DeviceSerializer,
    RackSerializer,
    RackCreateSerializer,
    RackDeviceSerializer,
    RackDeviceCreateSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="List all sites",
        description="Retrieve a list of all datacenter sites",
        tags=["Sites"]
    ),
    retrieve=extend_schema(
        summary="Get site details",
        description="Retrieve details of a specific datacenter site by ID",
        tags=["Sites"]
    ),
    create=extend_schema(
        summary="Create a new site",
        description="Create a new datacenter site with a unique name",
        tags=["Sites"],
        examples=[
            OpenApiExample(
                "Site creation example",
                value={"name": "Data Center East", "description": "Primary east coast facility"},
                request_only=True
            )
        ]
    ),
    update=extend_schema(
        summary="Update a site",
        description="Update an existing datacenter site",
        tags=["Sites"]
    ),
    partial_update=extend_schema(
        summary="Partially update a site",
        description="Partially update an existing datacenter site",
        tags=["Sites"]
    ),
    destroy=extend_schema(
        summary="Delete a site",
        description="Delete a datacenter site and all associated racks",
        tags=["Sites"]
    )
)
class SiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Site CRUD operations
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [AllowAny]

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


@extend_schema(
    summary="List or create rack configurations",
    description="GET: List all rack configurations for a site. POST: Create or update a rack configuration",
    tags=["Legacy"],
    parameters=[
        OpenApiParameter(
            name="site_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Site ID"
        )
    ],
    examples=[
        OpenApiExample(
            "Create rack configuration",
            value={
                "name": "Rack A1",
                "description": "Production rack",
                "configData": {"devices": [], "height": 42}
            },
            request_only=True
        )
    ]
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
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


@extend_schema(
    summary="Get specific rack configuration",
    description="Retrieve a specific rack configuration by site ID and rack name",
    tags=["Legacy"],
    parameters=[
        OpenApiParameter(name="site_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name="rack_name", type=OpenApiTypes.STR, location=OpenApiParameter.PATH)
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
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


@extend_schema(
    summary="Delete rack configuration",
    description="Delete a rack configuration by ID",
    tags=["Legacy"],
    parameters=[OpenApiParameter(name="rack_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)]
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
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


@extend_schema(
    summary="Get all rack configurations",
    description="Retrieve all rack configurations across all sites",
    tags=["Legacy"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
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


@extend_schema(
    summary="Load rack configuration",
    description="Load and process rack configuration data (legacy compatibility endpoint)",
    tags=["Legacy"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
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


@extend_schema(
    summary="Get devices from JSON file",
    description="Retrieve device templates from the static devices.json file (legacy compatibility)",
    tags=["Legacy"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
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


# ==================== Device Management Endpoints ====================

@extend_schema_view(
    list=extend_schema(
        summary="List all devices",
        description="Retrieve a list of all device templates from the database",
        tags=["Devices"]
    ),
    retrieve=extend_schema(
        summary="Get device details",
        description="Retrieve details of a specific device template by ID",
        tags=["Devices"]
    ),
    create=extend_schema(
        summary="Create a new device",
        description="Create a new device template with specifications",
        tags=["Devices"],
        examples=[
            OpenApiExample(
                "Device creation example",
                value={
                    "device_id": "custom-server-01",
                    "name": "Custom Server",
                    "category": "server",
                    "ru_size": 2,
                    "power_draw": 500,
                    "color": "#4CAF50",
                    "description": "Custom 2U server"
                },
                request_only=True
            )
        ]
    ),
    update=extend_schema(
        summary="Update a device",
        description="Update an existing device template",
        tags=["Devices"]
    ),
    partial_update=extend_schema(
        summary="Partially update a device",
        description="Partially update an existing device template",
        tags=["Devices"]
    ),
    destroy=extend_schema(
        summary="Delete a device",
        description="Delete a device template from the database",
        tags=["Devices"]
    )
)
class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Device CRUD operations
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create a new device
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            device = serializer.save()
            return Response(
                DeviceSerializer(device).data,
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {'error': 'A device with this device_id already exists'},
                status=status.HTTP_409_CONFLICT
            )


# ==================== Rack Management Endpoints ====================

@extend_schema_view(
    list=extend_schema(
        summary="List all racks",
        description="Retrieve a list of all racks, optionally filtered by site",
        tags=["Racks"],
        parameters=[
            OpenApiParameter(
                name="site_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter racks by site ID",
                required=False
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Get rack details",
        description="Retrieve details of a specific rack including all devices",
        tags=["Racks"]
    ),
    update=extend_schema(
        summary="Update a rack",
        description="Update an existing rack",
        tags=["Racks"]
    ),
    partial_update=extend_schema(
        summary="Partially update a rack",
        description="Partially update an existing rack",
        tags=["Racks"]
    ),
    destroy=extend_schema(
        summary="Delete a rack",
        description="Delete a rack and all associated device placements",
        tags=["Racks"]
    )
)
class RackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Rack CRUD operations
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter by site_id if provided"""
        queryset = Rack.objects.select_related('site').prefetch_related(
            'rack_devices__device'
        )
        site_id = self.request.query_params.get('site_id')
        if site_id:
            queryset = queryset.filter(site_id=site_id)
        return queryset


@extend_schema(
    summary="Create a rack for a site",
    description="Create a new rack for a specific site",
    tags=["Racks"],
    request=RackCreateSerializer,
    parameters=[OpenApiParameter(name="site_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)],
    examples=[
        OpenApiExample(
            "Rack creation example",
            value={"name": "Rack A1", "ru_height": 42, "description": "Production rack"},
            request_only=True
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_rack(request, site_id):
    """
    Create a new rack for a specific site
    """
    try:
        site = get_object_or_404(Site, id=site_id)

        serializer = RackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rack = Rack.objects.create(
            site=site,
            **serializer.validated_data
        )

        return Response(
            RackSerializer(rack).data,
            status=status.HTTP_201_CREATED
        )
    except IntegrityError:
        return Response(
            {'error': 'A rack with this name already exists at this site'},
            status=status.HTTP_409_CONFLICT
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to create rack', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Add device to rack",
    description="Place a device in a specific rack at a given position",
    tags=["Rack Devices"],
    request=RackDeviceCreateSerializer,
    parameters=[OpenApiParameter(name="rack_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)],
    examples=[
        OpenApiExample(
            "Add device example",
            value={"device_id": 1, "position": 1, "instance_name": "Web Server 01"},
            request_only=True
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def add_device_to_rack(request, rack_id):
    """
    Add a device to a specific rack at a given position
    """
    try:
        rack = get_object_or_404(Rack, id=rack_id)

        serializer = RackDeviceCreateSerializer(
            data=request.data,
            context={'rack': rack}
        )
        serializer.is_valid(raise_exception=True)

        rack_device = RackDevice.objects.create(
            rack=rack,
            **serializer.validated_data
        )

        return Response(
            RackDeviceSerializer(rack_device).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': 'Failed to add device to rack', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Remove device from rack",
    description="Remove a device placement from a rack",
    tags=["Rack Devices"],
    parameters=[OpenApiParameter(name="rack_device_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)]
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_device_from_rack(request, rack_device_id):
    """
    Remove a device from a rack
    """
    try:
        rack_device = get_object_or_404(RackDevice, id=rack_device_id)
        rack_device.delete()
        return Response({
            'success': True,
            'message': 'Device removed from rack successfully'
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to remove device from rack', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== Resource Usage Endpoints ====================

@extend_schema(
    summary="Get site resource usage",
    description="Calculate total power draw and HVAC load for all racks in a site",
    tags=["Resource Usage"],
    parameters=[OpenApiParameter(name="site_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)],
    responses={
        200: {
            "description": "Resource usage data",
            "content": {
                "application/json": {
                    "example": {
                        "site_id": 1,
                        "site_name": "Data Center East",
                        "total_power_draw": 15000,
                        "total_hvac_load": 51150,
                        "rack_count": 5,
                        "racks": []
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_site_resource_usage(request, site_id):
    """
    Get resource usage (power and HVAC) for a specific site
    """
    try:
        site = get_object_or_404(Site, id=site_id)
        racks = Rack.objects.filter(site=site).prefetch_related(
            'rack_devices__device'
        )

        total_power = 0
        total_hvac = 0
        rack_data = []

        for rack in racks:
            rack_power = rack.get_power_utilization()
            rack_hvac = rack.get_hvac_load()

            total_power += rack_power
            total_hvac += rack_hvac

            rack_data.append({
                'id': rack.id,
                'name': rack.name,
                'power_draw': rack_power,
                'hvac_load': rack_hvac,
                'device_count': rack.rack_devices.count()
            })

        return Response({
            'site_id': site.id,
            'site_name': site.name,
            'total_power_draw': total_power,
            'total_hvac_load': total_hvac,
            'rack_count': racks.count(),
            'racks': rack_data
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to calculate resource usage', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Get rack resource usage",
    description="Calculate power draw and HVAC load for all devices in a rack",
    tags=["Resource Usage"],
    parameters=[OpenApiParameter(name="rack_id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH)],
    responses={
        200: {
            "description": "Rack resource usage data",
            "content": {
                "application/json": {
                    "example": {
                        "rack_id": 1,
                        "rack_name": "Rack A1",
                        "site_name": "Data Center East",
                        "total_power_draw": 3000,
                        "total_hvac_load": 10230,
                        "ru_height": 42,
                        "devices": []
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_rack_resource_usage(request, rack_id):
    """
    Get resource usage (power and HVAC) for a specific rack
    """
    try:
        rack = get_object_or_404(
            Rack.objects.prefetch_related('rack_devices__device'),
            id=rack_id
        )

        devices = []
        for rd in rack.rack_devices.all():
            devices.append({
                'id': rd.id,
                'device_name': rd.instance_name or rd.device.name,
                'position': rd.position,
                'ru_size': rd.device.ru_size,
                'power_draw': rd.device.power_draw,
                'hvac_load': rd.device.power_draw * 3.41
            })

        return Response({
            'rack_id': rack.id,
            'rack_name': rack.name,
            'site_name': rack.site.name,
            'total_power_draw': rack.get_power_utilization(),
            'total_hvac_load': rack.get_hvac_load(),
            'ru_height': rack.ru_height,
            'devices': devices
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to calculate rack resource usage', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

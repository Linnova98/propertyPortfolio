from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Property
from .serializer import (PropertyListSerializer, PropertyReadSerializer, PropertyEditSerializer)
from .filters import PropertyFilter
from django.views.decorators.csrf import csrf_exempt

class PropertyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

@api_view(['GET'])
def PropertyOverview(request):
    queryset = Property.objects.select_related("portfolio")

    filtered_properties = PropertyFilter(request.GET, queryset=queryset).qs

    sort_usable_area = request.GET.get('sort_usable_area')
    sort_zip_place = request.GET.get('sort_zip_place')
    sort_address = request.GET.get('sort_address')
    min_value = request.GET.get('min_value')
    max_value = request.GET.get('max_value')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    portfolio = request.GET.get('portfolio')

    if sort_usable_area:
        filtered_properties = filtered_properties.order_by(
            "usable_area" if sort_usable_area == "asc" else "-usable_area"
        )

    if sort_zip_place:
        filtered_properties = filtered_properties.order_by(
            "zip_place" if sort_zip_place == "asc" else "-zip_place"
        )

    if sort_address:
        filtered_properties = filtered_properties.order_by(
            "address" if sort_address == "asc" else "-address"
        )

    if min_value:
        filtered_properties = filtered_properties.filter(value__gte=min_value)
    if max_value:
        filtered_properties = filtered_properties.filter(value__lte=max_value)
    if min_year:
        filtered_properties = filtered_properties.filter(year__gte=min_year)
    if max_year:
        filtered_properties = filtered_properties.filter(year__lte=max_year)
    if portfolio:
        filtered_properties = filtered_properties.filter(portfolio=portfolio)

    if min_value or max_value or min_year or max_year or sort_address or portfolio or sort_usable_area:
        serializer_class = PropertyReadSerializer
    else:
        serializer_class = PropertyListSerializer

    paginator = PropertyPagination()
    paginated_properties = paginator.paginate_queryset(filtered_properties, request)

    serializer = serializer_class(paginated_properties, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def view_items(request):
    if request.query_params:
        property = Property.objects.filter(**request.query_params.dict()).select_related("portfolio")
    else:
        property = Property.objects.select_related("portfolio").all()

    if property:
        serializer = PropertyReadSerializer(property, many=True)
        # serializer = PropertyListSerializer(property, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_item(request, pk):
    property_item = get_object_or_404(Property.objects.select_related("portfolio"), pk=pk)

    serializer = PropertyReadSerializer(property_item)

    return Response(serializer.data)

@api_view(['POST'])
def add_items(request):
    portfolio_id = request.data.get('portfolio')

    if not portfolio_id:
        return Response({"error": "Portfolio is required."}, status=status.HTTP_400_BAD_REQUEST)

    item = PropertyEditSerializer(data=request.data)

    if Property.objects.filter(
        address=request.data.get("address"),
        zip_code=request.data.get("zip_code"),
        zip_place=request.data.get("zip_place"),
        estimated_value=request.data.get("estimated_value"),
        construction_year=request.data.get("construction_year"),
        usable_area=request.data.get("usable_area"),
        portfolio_id=portfolio_id
    ).exists():
        return Response({"error": "This property already exists."})
    
    if item.is_valid():
        item.save()
        return Response(item.data, status=status.HTTP_201_CREATED)
    else:
        return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def update_items(request, pk):
    item = get_object_or_404(Property, pk=pk)

    if request.method == 'GET':
        serializer = PropertyEditSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PropertyEditSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "updated_data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Temporarily added csrf exempt to be able to delete in browser would use permission normally
@csrf_exempt
@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Property, pk=pk)
    item.delete()
    return Response({"message": "Property deleted successfully"}, status=status.HTTP_202_ACCEPTED)

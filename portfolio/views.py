from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Portfolio
from .serializer import PortfolioListSerializer, PortfolioReadSerializer, PortfolioEditSerializer
from .filters import PortfolioFilter
from django.views.decorators.csrf import csrf_exempt

class PropertyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def getPortfolios(request):
    portfolio = Portfolio.objects.all()
    serializer = PortfolioListSerializer(portfolio, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def PorfolioOverview(request):
    queryset = Portfolio.objects.all()

    filtered_portfolios = PortfolioFilter(request.GET, queryset=queryset).qs

    name = request.GET.get('name')
    owner_of_portfolio = request.GET.get('owner_of_portfolio')
    geographic_region = request.GET.get('geographic_region')

    if name:
        filtered_portfolios = filtered_portfolios.order_by(
            "name" if name == "asc" else "-name"
        )
    
    if owner_of_portfolio:
        filtered_portfolios = filtered_portfolios.order_by(
            "owner_of_portfolio" if owner_of_portfolio == "asc" else "-owner_of_portfolio"
        )
    
    if geographic_region:
        filtered_portfolios = filtered_portfolios.order_by(
            "geographic_region" if geographic_region == "asc" else "-geographic_region"
        )

    if name or owner_of_portfolio or geographic_region:
        serializer_class = PortfolioReadSerializer
    else:
        serializer_class = PortfolioListSerializer

    paginator = PropertyPagination()
    paginated_porfolios = paginator.paginate_queryset(filtered_portfolios, request)

    serializer = serializer_class(paginated_porfolios, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def view_instances(request):
    if request.query_params:
        portfolio = Portfolio.objects.filter(**request.query_params.dict())
    else:
        portfolio = Portfolio.objects.all()
    
    if portfolio:
        serializeer = PortfolioReadSerializer(portfolio, many=True)
        # serializeer = PortfolioListSerializer(portfolio, many=True)
        return Response(serializeer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_instance(request, pk):
    portfolio_instance = get_object_or_404(Portfolio, pk=pk)

    serializer = PortfolioReadSerializer(portfolio_instance)

    return Response(serializer.data)

@api_view(['POST'])
def add_instances(request):
    instance = PortfolioEditSerializer(data=request.data)

    if Portfolio.objects.filter(name=request.data.get('name')).exists():
        return Response({"error": "This portfolio already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if instance.is_valid():
        instance.save()
        return Response(instance.data, status=status.HTTP_201_CREATED)
    else:
        return Response(instance.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def update_instances(request, pk):
    instance = get_object_or_404(Portfolio, pk=pk)

    if request.method == 'GET':
        serializer = PortfolioEditSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PortfolioEditSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "updated_data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Temporarily added csrf exempt to be able to delete in browser would use permission normally
@csrf_exempt
@api_view(['DELETE'])
def delete_instances(request, pk):
    instance = get_object_or_404(Portfolio, pk=pk)
    instance.delete()
    return Response({"message": "Portfolio deleted successfully"}, status=status.HTTP_202_ACCEPTED)

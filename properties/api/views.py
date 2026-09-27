from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Property
from ..serializers import PropertySerializer

from .permissions import IsAgentOrAdmin, IsPropertyOwnerOrAdmin

from rest_framework.pagination import PageNumberPagination

class PropertyListAPIView(APIView):

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsAgentOrAdmin()]

        return []

    def get(self, request):

        properties = Property.objects.all()

        city = request.query_params.get("city")

        if city:
            properties = properties.filter(city__icontains=city)

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price:
            properties = properties.filter(price__gte=min_price)

        if max_price:
            properties = properties.filter(price__lte=max_price)

        property_type = request.query_params.get("property_type")

        if property_type:
            properties = properties.filter(
                property_type=property_type
            )

        min_bedrooms = request.query_params.get("min_bedrooms")

        if min_bedrooms:
            properties = properties.filter(
            bedrooms__gte=min_bedrooms
        )

        search = request.query_params.get("search")

        if search:
            properties = properties.filter(
                title__icontains=search
            )

        paginator = PageNumberPagination()
        paginator.page_size = 6

        page = paginator.paginate_queryset(
            properties,
            request
        )


        serializer = PropertySerializer(
            properties,
            many=True
        )

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = PropertySerializer(
            data=request.data
        )

        if serializer.is_valid():

            property = serializer.save(
                owner=request.user
            )

            return Response(
                PropertySerializer(property).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

    
class PropertyDetailAPIView(APIView):

    def get_permissions(self):

        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [
                IsAgentOrAdmin(),
                IsPropertyOwnerOrAdmin(),
            ]

        return []

    def get(self, request, pk):

        property = get_object_or_404(
            Property,
            pk=pk
        )

        serializer = PropertySerializer(property)

        return Response(serializer.data)

    def delete(self, request, pk):

        property = get_object_or_404(
            Property,
            pk=pk
        )

        self.check_object_permissions(request, property)

        property.delete()

        return Response(
            status=204
        )

    def patch(self, request, pk):

        property = get_object_or_404(
            Property,
            pk=pk
        )

        self.check_object_permissions(request, property)

        serializer = PropertySerializer(
            property,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

def put(self, request, pk):

    property = get_object_or_404(
        Property,
        pk=pk
    )

    self.check_object_permissions(request, property)

    serializer = PropertySerializer(
        property,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data
        )

    return Response(
        serializer.errors,
        status=400
    )
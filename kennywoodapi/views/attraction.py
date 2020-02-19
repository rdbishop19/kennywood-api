#imports
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction


#serializer class inherited from HyperlinkedSomething
class AttractionSerializer(serializers.HyperlinkedModelSerializer):
    '''Serialize the Attraction model'''

    class Meta:
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'area')
        depth = 2

#itinerary class inherited from ViewSet
class Attractions(ViewSet):
    '''Attractions within the Kennywood Amusement Park'''

    def create(self, request):
        '''POST
        
        Returns:
            Response -- JSON serialized instance
        '''
        attraction = Attraction()
        attraction.name = request.data['name']
        attraction.area_id = request.data['area_id']
        attraction.save()

        serializer = AttractionSerializer(attraction, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''GET

        Returns:
            Response -- JSON serialized instance
        '''
        try:
            attraction = Attraction.objects.get(pk=pk)
            print(attraction)
            serializer = AttractionSerializer(attraction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        '''PUT request

        Returns:
            response -- Empty body with 204 status code
        '''
        attraction = Attraction.objects.get(pk=pk)
        attraction.name = request.data['name']
        attraction.area_id = request.data['area_id']
        attraction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """

        attractions = Attraction.objects.all()

        area = self.request.query_params.get('area', None)
        if area is not None:
            attractions = attractions.filter(area__id=area)

        serializer = AttractionSerializer(attractions, many=True, context={'request': request})

        return Response(serializer.data)
from django.http import HttpResponseServerError
from rest_framework import serializers
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer

class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    '''JSON serializer for itineraries

    Arguments:
        serializers
    '''
    # Pattern: model, url, fields, depth
    class Meta:
        # model = provide the model
        model = Itinerary
        # url = provide a linkable url path
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        # fields = provide the query params
        fields = ('id', 'url', 'starttime', 'attraction',)
        # depth = provide the nested level
        depth = 2

class ItineraryItems(ViewSet):
    '''CRUD for itinerary items'''

    def create(self, request):
        '''POST request: single itinerary

        '''
        new_itinerary = Itinerary()
        new_itinerary.starttime = request.data['starttime']
        new_itinerary.customer_id = request.auth.user.id
        new_itinerary.attraction_id = request.data['attraction_id']

        new_itinerary.save()

        serializer = ItinerarySerializer(new_itinerary, context={'request': request})

        return Response(serializer.data)

    # retrieve takes 3 args
    def retrieve(self, request, pk=None):
        '''GET request: single itinerary

        '''
        try:
            # save ORM single object 'GET' to var 'itinerary'
            itinerary = Itinerary.objects.get(pk=pk)
            # serialize the data for the Response
            serializer = ItinerarySerializer(itinerary, context={'request': request})
            # return the damned thing
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # update takes 3 args
    def update(self, request, pk=None):
        '''PUT requests

        Returns:
            Response -- Empty body with 204 status code
        '''
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data['starttime']
        itinerary.customer_id = request.auth.user.id
        itinerary.attraction_id = request.data['attraction_id']
        itinerary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''DELETE requests
        
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        '''GET requests to itinerary items resource

        Returns:
            Response -- JSON serialized list of itinerary items
        '''
        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            itineraries,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from address.documents import AddressDocument
from address.serializers import AddressSerializer
import json

class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request):
        #try:
            query = request.GET.get('query')
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            # print all the hits
            for hit in search:
                print(hit.fullAddress)
                print(hit.uploadFile)
                

            results = self.paginate_queryset(response, request, view=self)

            print(results)

            serializer = self.serializer_class(results, many=True)

            return self.get_paginated_response(serializer.data)
        #except Exception as e:
        #    return HttpResponse(e, status=500)

class SearchAddresses(PaginatedElasticSearchAPIView):
    serializer_class = AddressSerializer
    document_class = AddressDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'fullAddress',
                ], fuzziness='auto', operator='and')

class QueryAddressesSuggestion(PaginatedElasticSearchAPIView):
    serializer_class = AddressSerializer
    document_class = AddressDocument

    def generate_q_expression(self, query):
        return Q(
                'multi_match', query=query,
                fields=[
                    'fullAddress1',
                ], operator='and')

def elasticsearch_address(query):
    q = Q(
        'multi_match', query=query,
        fields=[
            'fullAddress',
        ], fuzziness='auto', operator='and')
    search = AddressDocument.search().query(q)
    response = search.execute()
    serializer = AddressSerializer(response, many=True)

    return json.loads(json.dumps(serializer.data))

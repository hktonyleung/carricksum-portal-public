from django_elasticsearch_dsl import Document, Text, Date, Nested, Index, fields
from elasticsearch_dsl.analysis import token_filter, analyzer
from django_elasticsearch_dsl.registries import registry

from address.models import Address

autocomplete_filter = token_filter('autocomplete_filter', 'edge_ngram', min_gram=2, max_gram=20)
synonym_filter = token_filter('synonym_filter', 'synonym', synonyms=[
        "road, rd",
        "wan chai, wc"
    ],
)

autocomplete = analyzer('autocomplete',
    tokenizer='standard',
    filter=["lowercase", synonym_filter, autocomplete_filter],
)

standard_search = analyzer('standard_search',
    tokenizer='standard',
    filter=["lowercase", synonym_filter],
)

@registry.register_document
class AddressDocument(Document):

    fullAddress = fields.TextField(analyzer=autocomplete, copy_to=[ "fullAddress1"], attr="fullAddress")
    buildingName = fields.TextField(copy_to=[ "fullAddress1"], attr="buildingName")
    streetName = fields.TextField(copy_to=[ "fullAddress1"], attr="streetName")
    buildingNoFrom = fields.TextField(copy_to=[ "fullAddress1"], attr="buildingNoFrom")
    buildingNoTo = fields.TextField(copy_to=[ "fullAddress1"], attr="buildingNoTo")
    district = fields.TextField(copy_to=[ "fullAddress1"], attr="district")
    fullAddress1 = Text(analyzer=autocomplete, search_analyzer=standard_search)
    

    class Index:
        name = 'address'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Address
        fields = [
            'relatedDocument', 'uploadFile'
        ]
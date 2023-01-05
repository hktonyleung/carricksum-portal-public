from django.urls import path

from search.views import SearchAddresses, QueryAddressesSuggestion

app_name = 'search'

urlpatterns = [
    path('address/', SearchAddresses.as_view(), name="address"),
    path('address-suggestion/', QueryAddressesSuggestion.as_view(), name="address-suggestion"),
]
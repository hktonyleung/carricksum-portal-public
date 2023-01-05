from django.urls import path, include
from rest_framework import routers
from address.views import AddressViewSet, index, search_address, AddressListView, AddressCreateView, AddressUpdateView, AddressDeleteView



router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)

app_name = 'address'

urlpatterns = [
    path('', include(router.urls)),
    path('search', index, name="search-index"),
    path('search_address', search_address, name="search-address"),

    path("addresses", AddressListView.as_view(), name="address-manage"),
    path("addresses/create", AddressCreateView.as_view(), name="address-create"),
    path("addresses/<str:pk>/update", AddressUpdateView.as_view(), name="address-update"),
    path("addresses/<str:pk>/delete", AddressDeleteView.as_view(), name="address-delete"),

]
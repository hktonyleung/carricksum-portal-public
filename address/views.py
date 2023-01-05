import json
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from address.models import Address
from address.serializers import AddressSerializer
import requests
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from address.forms import AddressForm
from portal.base._mixin import SuperUserMixin
from django.views import generic
from search.views import elasticsearch_address
import json

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

def index(request):
    context = {}
    return render(request, "address/index.html", context) 

def search_address(request):
    context = {}
    query = request.GET.get('query')

    addresses = elasticsearch_address(query)

    data = dict()
    if (len(addresses) > 0):
        print(len(addresses))
        context['addresses'] = addresses
        data['form_is_valid'] = True
        data['html_form'] = render_to_string("address/result.html", context, request=request)
    else:
        data['form_is_valid'] = False
    return JsonResponse(data)

def save_address_form(request, form, template_name):
    user = request.user
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = user

            # TODO: catch exception?
            #try:
            instance = form.save()
            #except IntegrityError as e:
            #    return render(request, "portal/error.html", {"message": e.__cause__})
            
            data['form_is_valid'] = True
            addresses = Address.objects.get_queryset()
            data['html_partial_addresses_management'] = render_to_string('address/partial/addresses.html', {
                'addresses': addresses
            })
        else:
            print ('form is valid - false')
            data['form_is_valid'] = False
    
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

class AddressListView(SuperUserMixin, generic.ListView):
    
    #model = Room
    context_object_name = 'addresses'   # your own name for the list as a template variable
    queryset = Address.objects.get_queryset()
    template_name = 'address/address_index.html'  # Specify your own template name/location

class AddressCreateView(SuperUserMixin, generic.CreateView):
    #logger.debug('Enter Room Create View')
    name = "Create Address"
    # specify the model you want to use
    model = Address
    template_name = 'address/partial/create.html'
    # specify the form
    form_class = AddressForm

    def get(self, request):
        return save_address_form(request, super().get_form_class(), super().get_template_names())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print('form_valid')
        print(self.request.FILES)
        form = AddressForm(self.request.POST, self.request.FILES)
        return save_address_form(self.request, form, super().get_template_names())

    def form_invalid(self, form):
        print('form_invalid')
        print(self.request.FILES)
        form = AddressForm(self.request.POST, self.request.FILES)
        return save_address_form(self.request, form, super().get_template_names())

class AddressUpdateView(SuperUserMixin, generic.UpdateView):
    name = "Edit Address"
    # specify the model you want to use
    model = Address
    template_name = 'address/partial/update.html'

    # specify the form    
    form_class = AddressForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("address:address-manage")

    def get(self, request, pk):
        room = get_object_or_404(Address, pk=pk)
        form = AddressForm(instance=room)
        data = dict()
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        instance = form.save(commit=False)
        #if not instance.created_by:
        #instance.created_by = self.request.user
        instance.save()
        #res = super().form_valid(form)
        data = dict()
        data['form_is_valid'] = True
        addresses = Address.objects.all()
        data['html_partial_addresses_management'] = render_to_string('address/partial/addresses.html', {
                'addresses': addresses
        })
        return JsonResponse(data)   
        #return res

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        return JsonResponse(data)

class AddressDeleteView(SuperUserMixin, generic.DeleteView):
    name = "Delete Address"
    # specify the model you want to use
    model = Address
    template_name = 'address/partial/delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object
    #success_url = reverse("address:address-manage")

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        data = dict()
        context = {'address': address}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def delete(self, *args, **kwargs):
        #self.get_object().delete()
        self.get_object().hard_delete()
        data = dict()
        data['form_is_valid'] = True
        addresses = Address.objects.all()
        data['html_partial_addresses_management'] = render_to_string('address/partial/addresses.html', {
                'addresses': addresses
        })
        return JsonResponse(data) 

from django.shortcuts import render, get_object_or_404
from .models import Branch
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from branches.forms import BranchesForm, BranchesSpatialForm
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.serializers import serialize
from portal.base._mixin import SuperUserMixin
from .managers import BranchManager
#import json

# Create your views here.
def index(request):
    branches = Branch.objects.get_active_branches()
    context = {'branches':branches}
    response =  render(request, "branches/index.html", context) 
    return response

'''
def manage(request):
    branches = serialize('geojson', Branch.objects.get_active_branches(),
        geometry_field='geo',
        fields=('pk','name','desc',))
    context = {'branches':branches}
    response =  render(request, "branches/branch/manage.html", context) 
    return response

class BranchesListView(SuperUserMixin, generic.ListView):
    
    context_object_name = 'branches'   # your own name for the list as a template variable
    template_name = 'branches/branch/manage.html'  # Specify your own template name/location

    def get_queryset(self):
        queryset = serialize('geojson', Branch.objects.get_active_branches(),
            geometry_field='geo',
            fields=('pk','name','desc',))
        return queryset
'''
class BranchesListView(SuperUserMixin, generic.ListView):
    
    context_object_name = 'branches'   # your own name for the list as a template variable
    template_name = 'branches/branch/manage.html'  # Specify your own template name/location
    queryset = Branch.objects.get_active_branches()

class BranchesCreateView(LoginRequiredMixin, FormView):
    name = "Create Branches"
    # specify the model you want to use
    model = Branch
    template_name = "branches/branch/partial/create.html"
    # specify the form
    form_class = BranchesForm

    def get(self, request):
        data = dict()
        data['form_is_valid'] = True
        context = {'form': super().get_form_class()}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print('form_valid')
        name = form.cleaned_data['name'] 
        desc = form.cleaned_data['desc'] 
        #wkt = form.cleaned_data['wkt'] 
        #geo = GEOSGeometry(wkt)

        branch = Branch()
        branch.name = name
        branch.desc = desc
        #branch.geo = geo
        branch.active = True
        branch.created_by = self.request.user
        branch.save()
        data = dict()
        data['form_is_valid'] = True

        #new_branch = serialize('geojson', [branch,],
        #    geometry_field='geo',
        #    fields=('pk','name','desc',))

        branches = Branch.objects.get_active_branches()
        data['html_partial_branches_management'] = render_to_string('branches/branch/partial/branches.html', {
                'branches': branches
        })

        return JsonResponse(data) 

    def form_invalid(self, form): 
        print('form_INvalid')
        name = form.data['name'] 
        desc = form.data['desc'] 
        #wkt = form.data['wkt'] 
        #geo = GEOSGeometry(wkt)

        branch = Branch()
        branch.name = name
        branch.desc = desc
        #branch.geo = geo
        #geojson_branch = serialize('geojson', [branch,],
        #    geometry_field='geo',
        #    fields=('name','desc',))    

        data = dict()
        #context = {'form': form, 'geojson_branch': geojson_branch}
        context = {'form': form}
        print(form)
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        #data['html_form'] = form
        data['form_is_valid'] = False
        return JsonResponse(data)

class BranchUpdateSpatialView(SuperUserMixin, FormView):
    name = "Edit Branch"
    # specify the model you want to use
    model = Branch
    template_name = 'branches/branch/partial/update-spatial.html'

    # specify the form    
    form_class = BranchesSpatialForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        form = super().get_form_class()
        data = dict()
        form.instance = branch

        geojson_branch = None
        wkt = None
        if (branch.geo is not None):
            geojson_branch = serialize('geojson', [branch,],
                geometry_field='geo',
                fields=('pk','name','desc',))
            wkt = (GEOSGeometry(branch.geo)).wkt
            
        context = {'form': form, 'geojson_branch': geojson_branch, 'wkt': wkt}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        print('pk is: ' + pk)
        name = form.cleaned_data['name'] 
        desc = form.cleaned_data['desc'] 
        wkt = form.cleaned_data['wkt'] 
        geo = GEOSGeometry(wkt)
        branch = get_object_or_404(Branch, pk=pk)
        branch.name = name
        branch.desc = desc
        branch.geo = geo
        branch.save()
        data = dict()
        data['form_is_valid'] = True
        #edited_branch = serialize('geojson', [branch,],
        #    geometry_field='geo',
        #    fields=('pk','name','desc',))

        #data['branch'] = edited_branch
        branches = Branch.objects.get_active_branches()
        data['html_partial_branches_management'] = render_to_string('branches/branch/partial/branches.html', {
                'branches': branches
        })
        return JsonResponse(data)   

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        return JsonResponse(data)

class BranchDeleteView(SuperUserMixin, generic.DeleteView):
    name = "Delete Branch"
    # specify the model you want to use
    model = Branch
    template_name = 'branches/branch/partial/delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        data = dict()
        context = {'branch': branch}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def delete(self, *args, **kwargs):
        self.get_object().delete()
        data = dict()
        data['form_is_valid'] = True
        branches = Branch.objects.get_active_branches()
        data['html_partial_branches_management'] = render_to_string('branches/branch/partial/branches.html', {
            'branches': branches
        })
        return JsonResponse(data) 

class BranchUpdateView(SuperUserMixin, FormView):
    name = "Edit Branch"
    # specify the model you want to use
    model = Branch
    template_name = 'branches/branch/partial/update.html'

    # specify the form    
    form_class = BranchesForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    def get(self, request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        form = super().get_form_class()
        data = dict()
        form.instance = branch

        #geojson_branch = serialize('geojson', [branch,],
        #    geometry_field='geo',
        #    fields=('pk','name','desc',))
        
        #wkt = (GEOSGeometry(branch.geo)).wkt
        #context = {'form': form, 'geojson_branch': geojson_branch, 'wkt': wkt}
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        print('pk is: ' + pk)
        name = form.cleaned_data['name'] 
        desc = form.cleaned_data['desc'] 
        #wkt = form.cleaned_data['wkt'] 
        #geo = GEOSGeometry(wkt)
        branch = get_object_or_404(Branch, pk=pk)
        branch.name = name
        branch.desc = desc
        #branch.geo = geo
        branch.save()
        data = dict()
        data['form_is_valid'] = True
        #edited_branch = serialize('geojson', [branch,],
        #    geometry_field='geo',
        #    fields=('pk','name','desc',))

        #data['branch'] = edited_branch
        branches = Branch.objects.get_active_branches()
        data['html_partial_branches_management'] = render_to_string('branches/branch/partial/branches.html', {
                'branches': branches
        })
        return JsonResponse(data)   

    def form_invalid(self, form):
        data = dict()
        name = form.data['name'] 
        desc = form.data['desc'] 

        branch = Branch()
        branch.name = name
        branch.desc = desc
        form.instance = branch

        data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        return JsonResponse(data)
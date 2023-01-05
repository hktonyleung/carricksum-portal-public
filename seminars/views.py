from django.shortcuts import render, get_object_or_404
from .models import Room, Seminar, Booking
from .forms import RoomForm, SeminarForm, BookingForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import generic
from portal.base._mixin import SuperUserMixin
from django.utils.crypto import get_random_string
from django.views.generic.edit import FormView
from portal.utils import generate_qrcode
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError, transaction

# Create your views here.
class RoomListView(SuperUserMixin, generic.ListView):
    
    #model = Room
    context_object_name = 'rooms'   # your own name for the list as a template variable
    queryset = Room.objects.get_queryset()
    template_name = 'seminars/room_index.html'  # Specify your own template name/location
    #paginate_by = 5

class RoomUpdateView(SuperUserMixin, generic.UpdateView):
    name = "Edit Room"
    # specify the model you want to use
    model = Room
    template_name = 'seminars/room/partial/update.html'

    # specify the form    
    form_class = RoomForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("seminars:room-index")

    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        form = RoomForm(instance=room)
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
        rooms = Room.objects.all()
        data['html_partial_rooms_management'] = render_to_string('seminars/room/partial/rooms.html', {
                'rooms': rooms
        })
        return JsonResponse(data)   
        #return res

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        return JsonResponse(data)


class RoomCreateView(SuperUserMixin, generic.CreateView):
    #logger.debug('Enter Room Create View')
    name = "Create Room"
    # specify the model you want to use
    model = Room
    template_name = 'seminars/room/partial/create.html'
    # specify the form    
    form_class = RoomForm
    
    def get(self, request):
        data = dict()
        context = {'form': super().get_form_class()}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        return reverse("seminars:room-index")

    def form_valid(self, form):
        instance = form.save(commit=False)
        #if not instance.created_by:
        instance.created_by = self.request.user
        instance.save()
        res = super().form_valid(form)
        data = dict()
        data['form_is_valid'] = True
        rooms = Room.objects.all()
        data['html_partial_rooms_management'] = render_to_string('seminars/room/partial/rooms.html', {
                'rooms': rooms
        })
        return JsonResponse(data)   
        #return res

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=self.request)
        return JsonResponse(data)


class RoomDeleteView(SuperUserMixin, generic.DeleteView):
    name = "Delete Room"
    # specify the model you want to use
    model = Room
    template_name = 'seminars/room/partial/delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = reverse_lazy('seminars:room-index')

    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        data = dict()
        context = {'room': room}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def delete(self, *args, **kwargs):
        self.get_object().delete()
        data = dict()
        data['form_is_valid'] = True
        rooms = Room.objects.all()
        data['html_partial_rooms_management'] = render_to_string('seminars/room/partial/rooms.html', {
                'rooms': rooms
        })
        return JsonResponse(data)         

class SeminarListView(SuperUserMixin, generic.ListView):
    
    context_object_name = 'seminars'   # your own name for the list as a template variable
    queryset = Seminar.objects.get_active_seminar()
    template_name = 'seminars/seminar_index.html'  # Specify your own template name/location
    #paginate_by = 5


def save_seminar_form(request, form, template_name):
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
            seminars = Seminar.objects.get_active_seminar()
            data['html_partial_seminars_management'] = render_to_string('seminars/seminar/partial/seminars.html', {
                'seminars': seminars
            })
        else:
            data['form_is_valid'] = False
    
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

'''
def seminar_create(request):
    if request.method == 'POST':
        form = SeminarForm(request.POST)
    else:
        form = SeminarForm()
    return save_seminar_form(request, form, 'seminar/partial/create.html')
'''
class SeminarCreateView(SuperUserMixin, generic.CreateView):
    #logger.debug('Enter Room Create View')
    name = "Create Seminar"
    # specify the model you want to use
    model = Seminar
    template_name = 'seminars/seminar/partial/create.html'
    # specify the form
    form_class = SeminarForm

    def get(self, request):
        return save_seminar_form(request, super().get_form_class(), super().get_template_names())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return save_seminar_form(self.request, form, super().get_template_names())

    def form_invalid(self, form):
        return save_seminar_form(self.request, form, super().get_template_names())


'''
def seminar_update(request, pk):
    seminar = get_object_or_404(Seminar, pk=pk)
    if request.method == 'POST':
        form = SeminarForm(request.POST, instance=seminar)
    else:
        form = SeminarForm(instance=seminar)
    return save_seminar_form(request, form, 'seminar/partial/update.html')
'''
class SeminarUpdateView(SuperUserMixin, generic.UpdateView):
    name = "Edit Seminar"
    # specify the model you want to use
    model = Seminar
    template_name = 'seminars/seminar/partial/update.html'

    # specify the form    
    form_class = SeminarForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    # can specify success url
    # url to redirect after successfully
    # updating details
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("seminars:room-index")

    def get(self, request, pk):
        seminar = get_object_or_404(Seminar, pk=pk)
        form = SeminarForm(instance=seminar)
        return save_seminar_form(request, form, super().get_template_names())

    def form_valid(self, form):
        #seminar = get_object_or_404(Seminar, pk=pk)
        #form = SeminarForm(self.request.POST, instance=seminar)
        #form = SeminarForm(self.request.POST)
        return save_seminar_form(self.request, form, super().get_template_names())


    def form_invalid(self, form):
        #form = SeminarForm(self.request.POST)
        return save_seminar_form(self.request, form, super().get_template_names())


def seminar_delete(request, pk):
    seminar = get_object_or_404(Seminar, pk=pk)
    data = dict()
    if request.method == 'POST':
        seminar.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        seminars = Seminar.objects.get_active_seminar()
        data['html_partial_seminars_management'] = render_to_string('seminar/partial/management.html', {
            'seminars': seminars
        })
    else:
        context = {'seminar': seminar}
        data['html_form'] = render_to_string('seminar/partial/delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

class SeminarDeleteView(SuperUserMixin, generic.DeleteView):
    name = "Seminar Room"
    # specify the model you want to use
    model = Seminar
    template_name = 'seminars/seminar/partial/delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = reverse_lazy('seminars:seminar-index')

    def get(self, request, pk):
        seminar = get_object_or_404(Seminar, pk=pk)
        data = dict()
        context = {'seminar': seminar}
        data['html_form'] = render_to_string(super().get_template_names(), context, request=request)
        return JsonResponse(data)

    def delete(self, *args, **kwargs):
        self.get_object().delete()
        data = dict()
        data['form_is_valid'] = True
        seminars = Seminar.objects.get_active_seminar()
        data['html_partial_seminars_management'] = render_to_string('seminars/seminar/partial/seminars.html', {
            'seminars': seminars
        })
        return JsonResponse(data) 



class BookingListView(LoginRequiredMixin, generic.ListView):
    
    context_object_name = 'seminars'   # your own name for the list as a template variable
    template_name = 'seminars/booking_index.html'  # Specify your own template name/location
    #paginate_by = 5
    def get_queryset(self):
        seminars = Seminar.objects.get_active_seminar()
        for seminar in seminars:
            try:
                booking = Booking.objects.get_active_booking().get(seminar=seminar, attendee=self.request.user)
            except Booking.DoesNotExist:
                booking = None

            if (booking is not None):
                seminar.isBooked = True
                seminar.booking_id = booking.id
            else:
                seminar.isBooked = False
        return seminars

class BookingCreateView(LoginRequiredMixin, FormView):
    #logger.debug('Enter Room Create View')
    name = "Create Booking"
    # specify the model you want to use
    model = Booking
    template_name = 'seminars/booking/create.html'
    # specify the form
    form_class = BookingForm

    def get(self, request, seminar_id):
        seminar = Seminar.objects.get(pk=seminar_id)  
        form = BookingForm() 
        context = {'seminar':seminar,'form': form }
        return render(request, super().get_template_names(), context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        seminar_id = form.cleaned_data['seminar_id'] 

        with transaction.atomic():
            #Deduct 1 on seminar available seat
            seminar = Seminar.objects.select_for_update().get(pk=seminar_id)
            seminar.no_of_available_seat = seminar.no_of_available_seat -1
            seminar.save()
            #Make a booking record
            booking = Booking()
            booking.attendee = self.request.user
            booking.created_by = self.request.user
            booking.seminar = seminar
            unique_string = get_random_string(length=32)
            booking.unique_string = unique_string
            booking.save()  
            booking_id = booking.id

        return HttpResponseRedirect(reverse('seminars:booking-result', args=[booking_id]))

        #return save_seminar_form(self.request, form, super().get_template_names())

    def form_invalid(self, form): 
        #seminar_id = form.cleaned_data['seminar_id'] 
        #seminar = Seminar.objects.get(pk=seminar_id)
        context = {'form':form}
        return render(self.request, "seminars/booking/create.html", context)
        #return save_seminar_form(self.request, form, super().get_template_names())

class BookingDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    permission_denied_message = 'Permission denied; You are not the owner of the ticket'

    def test_func(self):
        booking = Booking.objects.get(pk=self.kwargs['booking_id'])
        return booking.attendee == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("no-permission"))
    
    def get(self, request, booking_id):
        #user = request.user
        booking = Booking.objects.get(pk=booking_id)
        #if booking.attendee == user:
        context = {'seminar':booking.seminar}
        context["svg"] = generate_qrcode(booking.unique_string)
        context["booking_id"] = booking.id
        return render(request, "seminars/booking/result.html", context)

def booking_result(request, booking_id):
    user = request.user
    booking = Booking.objects.get(pk=booking_id)
    if booking.attendee == user:
        context = {'seminar':booking.seminar}
        context["svg"] = generate_qrcode(booking.unique_string)
        context["booking_id"] = booking.id
        return render(request, "seminars/booking/result.html", context)


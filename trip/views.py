from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView

from trip.models import NoteModel, TripModel


class HomeView(TemplateView):
    template_name = 'trip/index.html'


def trips_list(request):
    trips = TripModel.objects.filter(owner=request.user)
    context = {
        "trips": trips
    }
    return render(request, 'trip/trip_list.html', context=context)


class TripCreateView(CreateView):
    model = TripModel
    success_url = reverse_lazy('trips-list')
    fields = ['city', 'country', 'start_date', 'end_date', 'trip_img']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TripDetailView(DetailView):
    model = TripModel

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        trip = context["object"]
        notes = trip.NoteModel_trip.all()
        context['notes'] = notes
        return context


class NoteDetailView(DetailView):
    model = NoteModel


class NoteListView(ListView):
    model = NoteModel

    def get_queryset(self) -> QuerySet[Any]:
        queryset = NoteModel.objects.filter(trip__owner=self.request.user)
        return queryset


class NoteCreateView(CreateView):
    model = NoteModel
    success_url = reverse_lazy('note-list-view')
    fields = "__all__"

    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        trips = TripModel.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form


class NoteUpdateView(UpdateView):
    model = NoteModel
    success_url = reverse_lazy('note-list-view')
    fields = "__all__"

    def get_form_class(self):
        form = super(NoteUpdateView, self).get_form()
        trips = TripModel.objects.filter(owner=self.request.user)
        form.fields['trip'].queryset = trips
        return form


class NoteDeleteView(DeleteView):
    model = NoteModel
    success_url = reverse_lazy('note-list-view')


class TripUpdateView(UpdateView):
    model = TripModel
    success_url = reverse_lazy('trips-list')
    fields = ["city", "country", "start_date", "end_date"]


class TripDeleteView(DeleteView):
    model = TripModel
    success_url = reverse_lazy("trips-list")

from django.http import HttpResponse
from django.shortcuts import render

from django.views import View

from cars.models import Car
from django.views.generic import TemplateView

# Create your views here.

class ShowCarsView(TemplateView):
    template_name = "cars/show_cars.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:

        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all()

        return context
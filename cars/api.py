from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from cars.models import Car, Mark, CarClass, BodyType, Country
from cars.serializers import CarCreateSerializer, CarSerializer, MarkSerializer, CarClassSerializer, BodyTypeSerializer, CountrySerializer

class CarsViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_serializer_class(self):
        if self.action in ('update', 'create'):
            return CarCreateSerializer
        return super().get_serializer_class()

class MarksViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):

    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

class CarClassesViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):

    queryset = CarClass.objects.all()
    serializer_class = CarClassSerializer

class BodyTypesViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):

    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer

class CountriesViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin, 
    GenericViewSet
    ):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response

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
    
    def get_queryset(self):
        qs = super().get_queryset()

        if (self.request.user.is_superuser):
            resQs = qs
        else:
            # фильтруем по текущему юзеру
            resQs = qs.filter(user=self.request.user)

        return resQs

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

class UserProfileViewset(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_url(self, request, *args, **kwargs):
        user = request.user
        data = {
            "is_authentificated": user.is_authenticated
        }
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser, 
                "name": user.username
            })
        return Response(data)
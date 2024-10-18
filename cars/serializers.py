from rest_framework import serializers

from cars.models import Car, Mark, CarClass, BodyType, Country

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"

class CarClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarClass
        fields = "__all__"

class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    mark_name = MarkSerializer(read_only=True)
    car_class = CarClassSerializer(read_only=True)
    body_type = BodyTypeSerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'model', 'mark_name', 'car_class', 'body_type', 'country', 'picture']



class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'mark_name', 'car_class', 'body_type', 'country', 'picture']
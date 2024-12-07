from django.contrib import admin

from cars.models import Car, Mark, CarClass, BodyType, Country, UserPhoto

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'mark_name', 'car_class', 'body_type', 'country']

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CarClass)
class CarClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Country)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(UserPhoto)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'picture']
"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cars import views

from rest_framework.routers import DefaultRouter

from cars.api import CarsViewset, MarksViewset, CarClassesViewset, BodyTypesViewset, CountriesViewset, UserProfileViewset, UsersPhotoViewset

router = DefaultRouter()
router.register("cars", CarsViewset, basename="cars")
router.register("marks", MarksViewset, basename="marks")
router.register("car-classes", CarClassesViewset, basename="car_classes")
router.register("body-types", BodyTypesViewset, basename="body_types")
router.register("countries", CountriesViewset, basename="countries")
router.register("user", UserProfileViewset, basename="user")
router.register("user_photo", UsersPhotoViewset, basename="user_photo")

urlpatterns = [
    path('', views.ShowCarsView.as_view()), 
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

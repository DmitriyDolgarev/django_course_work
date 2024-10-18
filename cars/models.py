from django.db import models

# Create your models here.

class Mark(models.Model):
    name = models.TextField("Марка")

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"

    def __str__(self) -> str:
        return self.name

class Car(models.Model):
    model = models.TextField("Модель")

    mark_name = models.ForeignKey("Mark", on_delete=models.CASCADE, null=True)

    car_class = models.ForeignKey("CarClass", on_delete=models.CASCADE, null=True)

    body_type = models.ForeignKey("BodyType", on_delete=models.CASCADE, null=True)

    country = models.ForeignKey("Country", on_delete=models.CASCADE, null=True)

    picture = models.ImageField("Изображение", null=True, upload_to="cars")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class CarClass(models.Model):
    name = models.TextField("Класс автомобиля")

    class Meta:
        verbose_name = "Класс автомобиля"
        verbose_name_plural = "Классы автомобиля"

    def __str__(self) -> str:
        return self.name
    
class BodyType(models.Model):
    name = models.TextField("Тип кузова автомобиля")

    class Meta:
        verbose_name = "Тип кузова"
        verbose_name_plural = "Типы кузова"

    def __str__(self) -> str:
        return self.name
    
class Country(models.Model):
    name = models.TextField("Страна производства автомобиля")

    class Meta:
        verbose_name = "Страна производства"
        verbose_name_plural = "Страны производства"

    def __str__(self) -> str:
        return self.name
from django.db import models
from django.utils import timezone


class Rentproperty(models.Model):
    property_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    rent = models.FloatField(blank=True, null=True)
    kanrihi = models.FloatField(blank=True, null=True)
    sikikin = models.FloatField(blank=True, null=True)
    reikin = models.FloatField(blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longititude = models.FloatField(blank=True, null=True)
    close_station = models.IntegerField(blank=True, null=True)
    floor_plan = models.CharField(max_length=50, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    orientation = models.CharField(max_length=5, blank=True, null=True)
    bath_toilet = models.BooleanField(blank=True, null=True)
    auto_lock = models.BooleanField(blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    predicted_rent = models.FloatField(blank=True, null=True)
    rent_diff = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = 'realestate'
        # db_table = 'rentproperty'
        unique_together = (('date', 'url'),)
    
    @property
    def rent_diff(self):
        return round(self.rent_diff, 1)


class AddressCoordinate(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField(blank=True, null=False)
    longititude = models.FloatField(blank=True, null=False)

    class Meta:
        app_label = 'realestate'
    #     db_table = 'addresscoordinate'

    def __str__(self):
        return self.address

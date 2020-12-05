from django.db import models
from django.utils import timezone


def _yield_area_choice():
    area_list = ()
    for i in range(3, 11):
        area = i*5
        temp = (str(area), str(area))
        area_list += temp
    return area_list

FLOOR_CHOICE = (
    ('ワンルーム', 'ワンルーム'),
    ('1K', '1K'),
    ('1DK', '1DK'),
    ('1LDK', '1LDK'),
    ('2LDK', '2LDK'),
    ('3LDK', '3LDK'),
)

AREA_CHOICE = (
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
    ('30', '30'),
    ('35', '35'),
    ('40', '40'),
    ('45', '45'),
    ('50', '50')
)

BATH_CHOICE = (
    ('バストイレ別', 'バストイレ別'),
    ('ユニットバス', 'ユニットバス')
)

AUTOLOCK_CHOICE = (
    ('オートロック有り', 'オートロック有り'),
    ('オートロックなし', 'オートロックなし')
)

class Rentproperty(models.Model):
    property_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)
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
    def rent_diff_round(self):
        if self.rent_diff:
            return round(self.rent_diff, 1)
        else:
            return

    @property
    def area_round(self):
        if self.area:
            return int(self.area)
        else:
            return

    @property
    def bath_toilet_ja(self):
        if self.bath_toilet == None:
            return
        else:
            if self.bath_toilet:
                return 'バストイレ別'
            else:
                return 'ユニットバス'

    @property
    def auto_lock_ja(self):
        if self.auto_lock == None:
            return
        else:
            if self.auto_lock:
                return 'オートロック有り'
            else:
                return 'オートロックなし'


class AddressCoordinate(models.Model):
    address = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField(blank=True, null=False)
    longititude = models.FloatField(blank=True, null=False)

    class Meta:
        app_label = 'realestate'
    #     db_table = 'addresscoordinate'

    def __str__(self):
        return self.address


class SearchCondition(models.Model):
    # 賃料下限
    min_rent = models.FloatField()

    # 賃料上限
    max_rent = models.FloatField()

    # 間取り
    floor_plan = models.CharField(choices=FLOOR_CHOICE, max_length=10)

    # 面積下限
    min_area = models.CharField(choices=AREA_CHOICE, max_length=10)

    # バス・トイレ別
    bath_toilet = models.CharField(choices=BATH_CHOICE, max_length=10)

    # オートロック
    autolock = models.CharField(choices=AUTOLOCK_CHOICE, max_length=10)

    class Meta:
        app_label = 'realestate'

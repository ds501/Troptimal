from django.db import models

# Create your models here.

class trop_request(models.Model):
    request_number = models.PositiveIntegerField(primary_key=True, default=0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_time = models.TimeField(null=True)
    finish_time = models.TimeField(null=True)
    attract_list_nums = models.CharField(max_length=50, null=True, default='')
    def __str__(self):
        return str(self.request_number)

class attraction(models.Model):
    attraction_number = models.PositiveIntegerField(primary_key=True, default=0)
    attraction_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=500, null=True, default='')
    attraction_city = models.CharField(max_length=100, default='')
    attraction_state = models.CharField(max_length=100, default='')
    attraction_country = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, null=True, default='')
#    hour_open = models.TimeField
#    hour_close = models.TimeField
    def __str__(self):
        return 'Name:' + ' ' + self.attraction_name + ', ' + 'City:'+ ' ' + self.attraction_city

class attraction_pair(models.Model):
    user_trop_request = models.ForeignKey(trop_request)
    attraction_pair = models.CharField(max_length=30, default='')
    attraction = models.ForeignKey(attraction, default=None)
    attraction_second_num = models.PositiveIntegerField(null=True, default=0)
    duration = models.PositiveIntegerField(null=True, default=0)
    value = models.FloatField(null=True, default=0)
    def __str__(self):
        return 'Startpoint:' + ' ' + str(self.attraction.attraction_number) + ', ' + 'Endpoint:'+ ' ' + str(self.attraction_second_num)

class output(models.Model):
    user_trop_request = models.ForeignKey(trop_request)
    period = models.PositiveIntegerField(null=True, default=1000)
    attraction_pair = models.ForeignKey(attraction_pair)

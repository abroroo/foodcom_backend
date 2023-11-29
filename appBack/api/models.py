from django.db import models
from django.forms.models import model_to_dict
import json
from django import forms
from rest_framework import serializers
from multiselectfield import MultiSelectField

event_types = (
    ('wedding', '가족 개인행사'),
    ('business', '기업 이벤트'),
    ('public', '사회 단체행사'),
    ('festival', '기관, 축제등'),
    ('birthday', '스몰웨딩, 야외결혼'),
    ('steak', '스테이크 행사'),
    ('fingerFood', '핑거푸드')
)

event_places = (
    ('실내', '실내'),
    ('야외', '야외'),
    ('체육관', '체육관'),
    ('연회장', '연회장'),
    ('호텔', '호텔'),
    ('미정', '미정')
)

class Tool(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)

    event_type = models.CharField(max_length=200, choices=event_types, blank=True, null=True)
    custom_event_type = models.CharField(max_length=200, blank=True, null=True)
    event_place = models.CharField(max_length=200, choices=event_places, blank=True, null=True)
    custom_event_place = models.CharField(max_length=200, blank=True, null=True)
    people_count = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    meal_cost = models.IntegerField(blank=True, null=True)
    tool = models.ManyToManyField(Tool, blank=True, null=True)
    custom_tool = models.CharField(max_length=200, blank=True, null=True)

    date_registered = models.DateTimeField(auto_now_add=True)
    ticket_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.ticket_number)

class CustomerSerializer(serializers.ModelSerializer):
    tool = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(), many=True)
    class Meta:
        model = Customer
        fields = '__all__'
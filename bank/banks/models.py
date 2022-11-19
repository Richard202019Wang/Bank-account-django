from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.contrib.auth.models import User


class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(verbose_name='Email Address', default="admin@utoronto.ca")
    capacity = models.PositiveIntegerField(null=True)
    last_modified = models.DateTimeField(auto_now=True)
    auto_increment = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name, self.transit_num, self.address


class Bank(models.Model):
    name = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    bank = models.ForeignKey(to=User, on_delete=SET_NULL, null=True)
    auto_increment = models.AutoField(primary_key=True)
    branches = models.ManyToManyField(Branch)

    def __str__(self):
        return self.name, self.swift_code, self.inst_num, self.description

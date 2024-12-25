from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    Bolt,
    BoltJoint,
    Nut,
    Order,
    Washer,
)


@admin.register(Bolt)
class BoltAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'diameter',
        'length',
        'weight',
        'accuracy_class',
        'cost',
        'strength_class',
        'size',
    ]
    search_fields = ['diameter']
    list_filter = ['diameter']


@admin.register(BoltJoint)
class BoltJointAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'bolt',
        'bolt_washer',
        'material',
        'nut_washer',
        'nut',
        'locknut',
        'weight',
    ]
    search_fields = ['bolt__diameter']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'created_at',
        'weight',
        'edited_at',
        'cost',
    ]
    search_fields = ['created_at', 'customer']
    list_filter = ['created_at', 'customer', 'edited_at']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Nut)
class NutAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'diameter',
        'weight',
        'accuracy_class',
        'cost',
        'strength_class',
        'size',
    ]
    search_fields = ['diameter']
    list_filter = ['diameter']


@admin.register(Washer)
class WasherAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'diameter',
        'weight',
        'accuracy_class',
        'cost',
        'strength_class',
    ]
    search_fields = ['diameter']
    list_filter = ['diameter']

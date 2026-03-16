from django.contrib import admin
from .models import (
    Brand,
    Combiner,
    CombinerCondition,
    CombinerImage,
    CombinerType,
    Sprayer,
    SprayerCondition,
    SprayerImage,
    SprayerType,
    Tractor,
    TractorCondition,
    TractorImage,
    TractorType,
)

admin.site.site_header = 'Combiner Shop Admin'
admin.site.site_title = 'Combiner Shop'
admin.site.index_title = 'Керування каталогом і замовленнями'


class CombinerImageInline(admin.TabularInline):
    model = CombinerImage
    extra = 3
    fields = ('image', 'order')


class TractorImageInline(admin.TabularInline):
    model = TractorImage
    extra = 3
    fields = ('image', 'order')


class SprayerImageInline(admin.TabularInline):
    model = SprayerImage
    extra = 3
    fields = ('image', 'order')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CombinerType)
class CombinerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CombinerCondition)
class CombinerConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Combiner)
class CombinerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'year',
        'condition',
        'working_hours',
        'price',
        'is_available',
    )
    search_fields = ('name', 'brand__name', 'seller_name')
    list_filter = (
        'brand',
        'combiner_type',
        'condition',
        'fuel_type',
        'year',
        'is_available',
        'created_at',
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'short_description', 'description'),
        }),
        ('Класифікація', {
            'fields': ('brand', 'combiner_type', 'condition'),
        }),
        ('Технічні характеристики', {
            'fields': ('year', 'working_hours', 'fuel_type', 'engine_power'),
        }),
        ('Ціна та статус', {
            'fields': ('price', 'is_available'),
        }),
        ('Зображення', {
            'fields': ('image',),
        }),
        ('Додаткова інформація', {
            'fields': ('features', 'documents'),
        }),
        ('Контакти продавця', {
            'fields': ('seller_name', 'seller_phone', 'seller_email'),
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [CombinerImageInline]


@admin.register(TractorType)
class TractorTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TractorCondition)
class TractorConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tractor)
class TractorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'year',
        'condition',
        'working_hours',
        'price',
        'is_available',
    )
    search_fields = ('name', 'brand__name', 'seller_name')
    list_filter = (
        'brand',
        'tractor_type',
        'condition',
        'fuel_type',
        'year',
        'is_available',
        'created_at',
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'short_description', 'description'),
        }),
        ('Класифікація', {
            'fields': ('brand', 'tractor_type', 'condition'),
        }),
        ('Технічні характеристики', {
            'fields': ('year', 'working_hours', 'fuel_type', 'engine_power'),
        }),
        ('Ціна та статус', {
            'fields': ('price', 'is_available'),
        }),
        ('Зображення', {
            'fields': ('image',),
        }),
        ('Додаткова інформація', {
            'fields': ('features', 'documents'),
        }),
        ('Контакти продавця', {
            'fields': ('seller_name', 'seller_phone', 'seller_email'),
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [TractorImageInline]


@admin.register(SprayerType)
class SprayerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SprayerCondition)
class SprayerConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Sprayer)
class SprayerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'year',
        'condition',
        'working_hours',
        'price',
        'is_available',
    )
    search_fields = ('name', 'brand__name', 'seller_name')
    list_filter = (
        'brand',
        'sprayer_type',
        'condition',
        'fuel_type',
        'year',
        'is_available',
        'created_at',
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'short_description', 'description'),
        }),
        ('Класифікація', {
            'fields': ('brand', 'sprayer_type', 'condition'),
        }),
        ('Технічні характеристики', {
            'fields': (
                'year',
                'working_hours',
                'fuel_type',
                'tank_volume',
                'spray_width',
            ),
        }),
        ('Ціна та статус', {
            'fields': ('price', 'is_available'),
        }),
        ('Зображення', {
            'fields': ('image',),
        }),
        ('Додаткова інформація', {
            'fields': ('features', 'documents'),
        }),
        ('Контакти продавця', {
            'fields': ('seller_name', 'seller_phone', 'seller_email'),
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [SprayerImageInline]

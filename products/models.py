from django.db import models
from django.utils.text import slugify

class Brand(models.Model):
    """Марка комбайна"""
    name = models.CharField(max_length=255, verbose_name="Назва марки")
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    description = models.TextField(blank=True, verbose_name="Опис")
    logo = models.URLField(blank=True, verbose_name="Логотип")
    
    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class CombinerType(models.Model):
    """Тип комбайна (зерноуборочний, кормоуборочний тощо)"""
    name = models.CharField(max_length=255, verbose_name="Тип комбайна")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-ім'я")
    description = models.TextField(blank=True, verbose_name="Опис")
    
    class Meta:
        verbose_name = "Тип комбайна"
        verbose_name_plural = "Типи комбайнів"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class CombinerCondition(models.Model):
    """Стан комбайна"""
    CONDITION_CHOICES = [
        ('excellent', 'Відмінний стан'),
        ('good', 'Хороший стан'),
        ('normal', 'Задовільний'),
        ('poor', 'Потребує ремонту'),
    ]
    
    name = models.CharField(max_length=50, choices=CONDITION_CHOICES, unique=True, verbose_name="Стан")
    
    class Meta:
        verbose_name = "Стан комбайна"
        verbose_name_plural = "Стани комбайнів"
    
    def __str__(self):
        return self.get_name_display()


class Combiner(models.Model):
    """Основна модель комбайна"""
    FUEL_CHOICES = [
        ('diesel', 'Дизель'),
        ('gasoline', 'Бензин'),
        ('gas', 'Газ'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Модель комбайна")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL-ім'я")
    description = models.TextField(verbose_name="Опис")
    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Короткий опис"
    )
    
    # Основна інформація
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='combiners',
        verbose_name="Марка"
    )
    combiner_type = models.ForeignKey(
        CombinerType,
        on_delete=models.CASCADE,
        related_name='combiners',
        verbose_name="Тип комбайна"
    )
    condition = models.ForeignKey(
        CombinerCondition,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Стан"
    )
    
    # Технічні характеристики
    year = models.PositiveIntegerField(verbose_name="Рік випуску")
    working_hours = models.PositiveIntegerField(verbose_name="Годин роботи")
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        verbose_name="Тип палива"
    )
    engine_power = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Потужність двигуна (л.с.)"
    )
    
    # Зображення
    # основне фото (стане полем для завантаження файлу)
    image = models.ImageField(upload_to='combiners/', verbose_name="Основне зображення", blank=True)
    # додаткові фото як кома‑розділені URL'и або шляхи
    images = models.TextField(
        blank=True,
        help_text="URLs або шляхи зображень, розділені комами",
        verbose_name="Додаткові зображення"
    )
    
    # Ціна
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Ціна"
    )
    
    # Додаткова інформація
    features = models.TextField(
        blank=True,
        verbose_name="Особливості та переваги"
    )
    documents = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Наявні документи"
    )
    seller_name = models.CharField(
        max_length=255,
        verbose_name="Ім'я продавця"
    )
    seller_phone = models.CharField(
        max_length=20,
        verbose_name="Телефон продавця"
    )
    seller_email = models.EmailField(
        blank=True,
        verbose_name="Email продавця"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Місцезнаходження"
    )
    
    # Системні поля
    is_available = models.BooleanField(default=True, verbose_name="Доступний")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Комбайн"
        verbose_name_plural = "Комбайни"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Combiner.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class TractorType(models.Model):
    """Тип трактора"""
    name = models.CharField(max_length=255, verbose_name="Тип трактора")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-ім'я")
    description = models.TextField(blank=True, verbose_name="Опис")
    
    class Meta:
        verbose_name = "Тип трактора"
        verbose_name_plural = "Типи тракторів"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class TractorCondition(models.Model):
    """Стан трактора"""
    CONDITION_CHOICES = [
        ('excellent', 'Відмінний стан'),
        ('good', 'Хороший стан'),
        ('normal', 'Задовільний'),
        ('poor', 'Потребує ремонту'),
    ]
    
    name = models.CharField(max_length=50, choices=CONDITION_CHOICES, unique=True, verbose_name="Стан")
    
    class Meta:
        verbose_name = "Стан трактора"
        verbose_name_plural = "Стани тракторів"
    
    def __str__(self):
        return self.get_name_display()


class Tractor(models.Model):
    """Модель трактора"""
    FUEL_CHOICES = [
        ('diesel', 'Дизель'),
        ('gasoline', 'Бензин'),
        ('gas', 'Газ'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Модель трактора")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL-ім'я")
    description = models.TextField(verbose_name="Опис")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Короткий опис")
    
    # Основна інформація
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='tractors', verbose_name="Марка")
    tractor_type = models.ForeignKey(TractorType, on_delete=models.CASCADE, related_name='tractors', verbose_name="Тип трактора")
    condition = models.ForeignKey(TractorCondition, on_delete=models.SET_NULL, null=True, verbose_name="Стан")
    
    # Технічні характеристики
    year = models.PositiveIntegerField(verbose_name="Рік випуску")
    working_hours = models.PositiveIntegerField(verbose_name="Годин роботи")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, verbose_name="Тип палива")
    engine_power = models.CharField(max_length=100, blank=True, verbose_name="Потужність двигуна (л.с.)")
    
    # Зображення
    image = models.ImageField(upload_to='tractors/', verbose_name="Основне зображення", blank=True)
    images = models.TextField(blank=True, help_text="URLs або шляхи зображень, розділені комами", verbose_name="Додаткові зображення")
    
    # Ціна
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ціна")
    
    # Додаткова інформація
    features = models.TextField(blank=True, verbose_name="Особливості та переваги")
    documents = models.CharField(max_length=255, blank=True, verbose_name="Наявні документи")
    seller_name = models.CharField(max_length=255, verbose_name="Ім'я продавця")
    seller_phone = models.CharField(max_length=20, verbose_name="Телефон продавця")
    seller_email = models.EmailField(blank=True, verbose_name="Email продавця")
    location = models.CharField(max_length=255, blank=True, verbose_name="Місцезнаходження")
    
    # Системні поля
    is_available = models.BooleanField(default=True, verbose_name="Доступний")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Трактор"
        verbose_name_plural = "Трактори"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Tractor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SprayerType(models.Model):
    """Тип обприскувача"""
    name = models.CharField(max_length=255, verbose_name="Тип обприскувача")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL-ім'я")
    description = models.TextField(blank=True, verbose_name="Опис")
    
    class Meta:
        verbose_name = "Тип обприскувача"
        verbose_name_plural = "Типи обприскувачів"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class SprayerCondition(models.Model):
    """Стан обприскувача"""
    CONDITION_CHOICES = [
        ('excellent', 'Відмінний стан'),
        ('good', 'Хороший стан'),
        ('normal', 'Задовільний'),
        ('poor', 'Потребує ремонту'),
    ]
    
    name = models.CharField(max_length=50, choices=CONDITION_CHOICES, unique=True, verbose_name="Стан")
    
    class Meta:
        verbose_name = "Стан обприскувача"
        verbose_name_plural = "Стани обприскувачів"
    
    def __str__(self):
        return self.get_name_display()


class Sprayer(models.Model):
    """Модель обприскувача"""
    FUEL_CHOICES = [
        ('diesel', 'Дизель'),
        ('gasoline', 'Бензин'),
        ('electric', 'Електричний'),
        ('battery', 'Акумулятор'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Модель обприскувача")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL-ім'я")
    description = models.TextField(verbose_name="Опис")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Короткий опис")
    
    # Основна інформація
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='sprayers', verbose_name="Марка")
    sprayer_type = models.ForeignKey(SprayerType, on_delete=models.CASCADE, related_name='sprayers', verbose_name="Тип обприскувача")
    condition = models.ForeignKey(SprayerCondition, on_delete=models.SET_NULL, null=True, verbose_name="Стан")
    
    # Технічні характеристики
    year = models.PositiveIntegerField(verbose_name="Рік випуску")
    working_hours = models.PositiveIntegerField(verbose_name="Годин роботи")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, blank=True, verbose_name="Тип палива")
    tank_volume = models.PositiveIntegerField(verbose_name="Об'єм бака (літри)")
    spray_width = models.CharField(max_length=100, blank=True, verbose_name="Ширина розпилювання (м)")
    
    # Зображення
    image = models.ImageField(upload_to='sprayers/', verbose_name="Основне зображення", blank=True)
    images = models.TextField(blank=True, help_text="URLs або шляхи зображень, розділені комами", verbose_name="Додаткові зображення")
    
    # Ціна
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ціна")
    
    # Додаткова інформація
    features = models.TextField(blank=True, verbose_name="Особливості та переваги")
    documents = models.CharField(max_length=255, blank=True, verbose_name="Наявні документи")
    seller_name = models.CharField(max_length=255, verbose_name="Ім'я продавця")
    seller_phone = models.CharField(max_length=20, verbose_name="Телефон продавця")
    seller_email = models.EmailField(blank=True, verbose_name="Email продавця")
    location = models.CharField(max_length=255, blank=True, verbose_name="Місцезнаходження")
    
    # Системні поля
    is_available = models.BooleanField(default=True, verbose_name="Доступний")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    
    class Meta:
        verbose_name = "Обприскувач"
        verbose_name_plural = "Обприскувачі"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Sprayer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CombinerImage(models.Model):
    combiner = models.ForeignKey(Combiner, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='combiners/', verbose_name='Фото')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Додаткове фото'
        verbose_name_plural = 'Додаткові фото'

    def __str__(self):
        return f'Фото для {self.combiner}'


class TractorImage(models.Model):
    tractor = models.ForeignKey(Tractor, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='tractors/', verbose_name='Фото')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Додаткове фото'
        verbose_name_plural = 'Додаткові фото'

    def __str__(self):
        return f'Фото для {self.tractor}'


class SprayerImage(models.Model):
    sprayer = models.ForeignKey(Sprayer, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='sprayers/', verbose_name='Фото')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Додаткове фото'
        verbose_name_plural = 'Додаткові фото'

    def __str__(self):
        return f'Фото для {self.sprayer}'
from django.core.management.base import BaseCommand
from decimal import Decimal
from products.models import (
    Brand, 
    CombinerType, CombinerCondition, Combiner,
    TractorType, TractorCondition, Tractor,
    SprayerType, SprayerCondition, Sprayer
)


class Command(BaseCommand):
    help = 'Створити 2 категорії (CombinerType) і 5 товарів (Combiner) для тестування'

    def handle(self, *args, **options):
        self.stdout.write('Починаю створення даних...')

        # Бренди
        brands = {}
        for name in ['John Deere', 'New Holland']:
            b, created = Brand.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'Офіційний дилер {name}',
                    'logo': ''
                }
            )
            brands[name] = b
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено бренд: {name}'))

        # Типи (категорії)
        types = {}
        for tname in ['Зерноуборочний', 'Кормоуборочний']:
            t, created = CombinerType.objects.get_or_create(
                name=tname,
                defaults={'description': f'Тип: {tname}'}
            )
            types[tname] = t
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено тип: {tname}'))

        # Стани (використовуємо наявні choices)
        conditions = {}
        for key, label in CombinerCondition.CONDITION_CHOICES:
            c, created = CombinerCondition.objects.get_or_create(name=key)
            conditions[key] = c
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено стан: {key}'))

        # Створити 5 комбайнів
        products_data = [
            {
                'name': 'JD S700',
                'brand': brands['John Deere'],
                'combiner_type': types['Зерноуборочний'],
                'condition': conditions.get('excellent'),
                'year': 2019,
                'working_hours': 1200,
                'fuel_type': 'diesel',
                'engine_power': '350',
                'image': 'https://via.placeholder.com/800x600?text=JD+S700',
                'images': 'https://via.placeholder.com/800x600?text=JD+1,https://via.placeholder.com/800x600?text=JD+2',
                'price': Decimal('85000.00'),
                'features': 'Розширений зерновий бункер, GPS',
                'documents': 'Паспорт, сервісна книжка',
                'seller_name': 'Петро',
                'seller_phone': '+380501112233',
                'seller_email': 'petro@example.com',
            },
            {
                'name': 'NH CX5000',
                'brand': brands['New Holland'],
                'combiner_type': types['Зерноуборочний'],
                'condition': conditions.get('good'),
                'year': 2016,
                'working_hours': 2400,
                'fuel_type': 'diesel',
                'engine_power': '320',
                'image': 'https://via.placeholder.com/800x600?text=NH+CX5000',
                'images': 'https://via.placeholder.com/800x600?text=NH+1',
                'price': Decimal('62000.00'),
                'features': 'Широкий комбайн, підвищена продуктивність',
                'documents': 'Паспорт',
                'seller_name': 'Олег',
                'seller_phone': '+380671234567',
                'seller_email': 'oleg@example.com',
            },
            {
                'name': 'JD F400 (кормоуборочний)',
                'brand': brands['John Deere'],
                'combiner_type': types['Кормоуборочний'],
                'condition': conditions.get('normal'),
                'year': 2012,
                'working_hours': 3600,
                'fuel_type': 'diesel',
                'engine_power': '220',
                'image': 'https://via.placeholder.com/800x600?text=JD+F400',
                'images': '',
                'price': Decimal('27000.00'),
                'features': 'Підходить для корму і сіна',
                'documents': '',
                'seller_name': 'Іван',
                'seller_phone': '+380631234000',
                'seller_email': 'ivan@example.com',
            },
            {
                'name': 'NH FR Forage',
                'brand': brands['New Holland'],
                'combiner_type': types['Кормоуборочний'],
                'condition': conditions.get('good'),
                'year': 2018,
                'working_hours': 1800,
                'fuel_type': 'diesel',
                'engine_power': '260',
                'image': 'https://via.placeholder.com/800x600?text=NH+Forage',
                'images': 'https://via.placeholder.com/800x600?text=Forage+1,https://via.placeholder.com/800x600?text=Forage+2',
                'price': Decimal('41000.00'),
                'features': 'Оптимізований для кормозаготівлі',
                'documents': 'Сервісна книжка',
                'seller_name': 'Марія',
                'seller_phone': '+380661112233',
                'seller_email': 'maria@example.com',
            },
            {
                'name': 'JD X9 Demo',
                'brand': brands['John Deere'],
                'combiner_type': types['Зерноуборочний'],
                'condition': conditions.get('excellent'),
                'year': 2021,
                'working_hours': 400,
                'fuel_type': 'diesel',
                'engine_power': '450',
                'image': 'https://via.placeholder.com/800x600?text=JD+X9',
                'images': '',
                'price': Decimal('230000.00'),
                'features': 'Новітня модель, мінімальні годинники',
                'documents': 'Гарантія',
                'seller_name': 'Сергій',
                'seller_phone': '+380501234999',
                'seller_email': 'serhii@example.com',
            },
        ]

        created_count = 0
        for pdata in products_data:
            product, created = Combiner.objects.get_or_create(
                name=pdata['name'],
                defaults={
                    'description': pdata.get('features', ''),
                    'short_description': pdata.get('features', '')[:200],
                    'brand': pdata['brand'],
                    'combiner_type': pdata['combiner_type'],
                    'condition': pdata['condition'],
                    'year': pdata['year'],
                    'working_hours': pdata['working_hours'],
                    'fuel_type': pdata['fuel_type'],
                    'engine_power': pdata['engine_power'],
                    'image': pdata['image'],
                    'images': pdata['images'],
                    'price': pdata['price'],
                    'features': pdata.get('features', ''),
                    'documents': pdata.get('documents', ''),
                    'seller_name': pdata.get('seller_name', ''),
                    'seller_phone': pdata.get('seller_phone', ''),
                    'seller_email': pdata.get('seller_email', ''),
                    'is_available': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Створено комбайн: {product.name}'))

        # ===== ТРАКТОРИ =====
        tractor_types = {}
        for tname in ['Колісний', 'Гусеничний']:
            t, created = TractorType.objects.get_or_create(
                name=tname,
                defaults={'description': f'Тип трактора: {tname}'}
            )
            tractor_types[tname] = t
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено тип трактора: {tname}'))

        tractor_conditions = {}
        for key, label in TractorCondition.CONDITION_CHOICES:
            c, created = TractorCondition.objects.get_or_create(name=key)
            tractor_conditions[key] = c
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено стан трактора: {key}'))

        tractors_data = [
            {
                'name': 'JD 7R330',
                'brand': brands['John Deere'],
                'tractor_type': tractor_types['Колісний'],
                'condition': tractor_conditions.get('excellent'),
                'year': 2020,
                'working_hours': 800,
                'fuel_type': 'diesel',
                'engine_power': '330',
                'image': 'https://via.placeholder.com/800x600?text=JD+7R330',
                'images': '',
                'price': Decimal('95000.00'),
                'features': 'Потужний трактор для великих земельних ділянок',
                'documents': 'Паспорт, сервісна книжка',
                'seller_name': 'Максим',
                'seller_phone': '+380501234567',
                'seller_email': 'maksym@example.com',
            },
            {
                'name': 'NH T7.240',
                'brand': brands['New Holland'],
                'tractor_type': tractor_types['Колісний'],
                'condition': tractor_conditions.get('good'),
                'year': 2017,
                'working_hours': 1600,
                'fuel_type': 'diesel',
                'engine_power': '240',
                'image': 'https://via.placeholder.com/800x600?text=NH+T7',
                'images': '',
                'price': Decimal('68000.00'),
                'features': 'Надійний економічний трактор',
                'documents': 'Паспорт',
                'seller_name': 'Анна',
                'seller_phone': '+380661234567',
                'seller_email': 'anna@example.com',
            },
        ]

        tractors_created = 0
        for tdata in tractors_data:
            tractor, created = Tractor.objects.get_or_create(
                name=tdata['name'],
                defaults={
                    'description': tdata.get('features', ''),
                    'short_description': tdata.get('features', '')[:200],
                    'brand': tdata['brand'],
                    'tractor_type': tdata['tractor_type'],
                    'condition': tdata['condition'],
                    'year': tdata['year'],
                    'working_hours': tdata['working_hours'],
                    'fuel_type': tdata['fuel_type'],
                    'engine_power': tdata['engine_power'],
                    'image': tdata['image'],
                    'images': tdata['images'],
                    'price': tdata['price'],
                    'features': tdata.get('features', ''),
                    'documents': tdata.get('documents', ''),
                    'seller_name': tdata.get('seller_name', ''),
                    'seller_phone': tdata.get('seller_phone', ''),
                    'seller_email': tdata.get('seller_email', ''),
                    'is_available': True,
                }
            )
            if created:
                tractors_created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Створено трактор: {tractor.name}'))

        # ===== ОБПРИСКУВАЧІ =====
        sprayer_types = {}
        for sname in ['Польовий', 'Навісний']:
            s, created = SprayerType.objects.get_or_create(
                name=sname,
                defaults={'description': f'Тип обприскувача: {sname}'}
            )
            sprayer_types[sname] = s
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено тип обприскувача: {sname}'))

        sprayer_conditions = {}
        for key, label in SprayerCondition.CONDITION_CHOICES:
            c, created = SprayerCondition.objects.get_or_create(name=key)
            sprayer_conditions[key] = c
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Створено стан обприскувача: {key}'))

        sprayers_data = [
            {
                'name': 'Amazone UX6200',
                'brand': brands['John Deere'],
                'sprayer_type': sprayer_types['Навісний'],
                'condition': sprayer_conditions.get('excellent'),
                'year': 2021,
                'working_hours': 300,
                'fuel_type': 'diesel',
                'tank_volume': 6200,
                'spray_width': '42',
                'image': 'https://via.placeholder.com/800x600?text=Amazone+UX',
                'images': '',
                'price': Decimal('125000.00'),
                'features': 'Сучасна гідравлічна система, точне дозування',
                'documents': 'Гарантія, інструкція',
                'seller_name': 'Дмитро',
                'seller_phone': '+380501234123',
                'seller_email': 'dmytro@example.com',
            },
            {
                'name': 'Hardi Commander 4000',
                'brand': brands['New Holland'],
                'sprayer_type': sprayer_types['Польовий'],
                'condition': sprayer_conditions.get('good'),
                'year': 2018,
                'working_hours': 900,
                'fuel_type': 'diesel',
                'tank_volume': 4000,
                'spray_width': '38',
                'image': 'https://via.placeholder.com/800x600?text=Hardi+Commander',
                'images': '',
                'price': Decimal('78000.00'),
                'features': 'Надійний обприскувач для рядків',
                'documents': 'Паспорт',
                'seller_name': 'Ігор',
                'seller_phone': '+380671234123',
                'seller_email': 'igor@example.com',
            },
        ]

        sprayers_created = 0
        for sdata in sprayers_data:
            sprayer, created = Sprayer.objects.get_or_create(
                name=sdata['name'],
                defaults={
                    'description': sdata.get('features', ''),
                    'short_description': sdata.get('features', '')[:200],
                    'brand': sdata['brand'],
                    'sprayer_type': sdata['sprayer_type'],
                    'condition': sdata['condition'],
                    'year': sdata['year'],
                    'working_hours': sdata['working_hours'],
                    'fuel_type': sdata['fuel_type'],
                    'tank_volume': sdata['tank_volume'],
                    'spray_width': sdata['spray_width'],
                    'image': sdata['image'],
                    'images': sdata['images'],
                    'price': sdata['price'],
                    'features': sdata.get('features', ''),
                    'documents': sdata.get('documents', ''),
                    'seller_name': sdata.get('seller_name', ''),
                    'seller_phone': sdata.get('seller_phone', ''),
                    'seller_email': sdata.get('seller_email', ''),
                    'is_available': True,
                }
            )
            if created:
                sprayers_created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Створено обприскувач: {sprayer.name}'))

        total = created_count + tractors_created + sprayers_created
        self.stdout.write(self.style.SUCCESS(f'\n✅ Готово — створено {total} товарів (комбайнів: {created_count}, тракторів: {tractors_created}, обприскувачів: {sprayers_created}).'))
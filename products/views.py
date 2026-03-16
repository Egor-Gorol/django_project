from django.shortcuts import render
from django.db import models
from .models import Combiner, Tractor, Sprayer, Brand, CombinerType, TractorType, SprayerType



def get_all_products(search_query='', brand_filter=None):
	"""Отримати всі товари (комбайни, трактори, обприскувачі)"""
	products = []

	# Комбайни
	combiners = Combiner.objects.filter(is_available=True)
	if search_query:
		combiners = combiners.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
	if brand_filter:
		combiners = combiners.filter(brand=brand_filter)
	
	for c in combiners:
		c.model_type = 'Комбайн'
		products.append(c)

	# Трактори
	tractors = Tractor.objects.filter(is_available=True)
	if search_query:
		tractors = tractors.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
	if brand_filter:
		tractors = tractors.filter(brand=brand_filter)
	
	for t in tractors:
		t.model_type = 'Трактор'
		products.append(t)

	# Обприскувачі
	sprayers = Sprayer.objects.filter(is_available=True)
	if search_query:
		sprayers = sprayers.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
	if brand_filter:
		sprayers = sprayers.filter(brand=brand_filter)
	
	for s in sprayers:
		s.model_type = 'Обприскувач'
		products.append(s)

	# Сортуємо за датою створення (новіші першими)
	products.sort(key=lambda x: x.created_at, reverse=True)
	return products


def home(request):
	categories = Brand.objects.all()
	products = get_all_products()[:6]
	return render(request, 'projects/home.html', {
		'products': products,
		'categories': categories,
		'selected_category': None,
		'search_query': '',
	})


def contact(request):
	return render(request, 'projects/contact.html')


def product_list(request):
	categories = Brand.objects.all()
	search_query = request.GET.get('search', '').strip()
	equipment_type = request.GET.get('type', '').strip()
	
	brand_filter = None
	selected_category = request.GET.get('category')
	if selected_category:
		try:
			brand_filter = Brand.objects.filter(slug=selected_category).first()
			if not brand_filter:
				brand_filter = Brand.objects.filter(id=selected_category).first()
		except Exception:
			brand_filter = None
		if brand_filter:
			selected_category = brand_filter.slug

	# Фільтруємо по типу товару
	if equipment_type == 'combiner':
		products = Combiner.objects.filter(is_available=True)
		if search_query:
			products = products.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
		if brand_filter:
			products = products.filter(brand=brand_filter)
		for p in products:
			p.model_type = 'Комбайн'
		products = sorted(products, key=lambda x: x.created_at, reverse=True)
	elif equipment_type == 'tractor':
		products = Tractor.objects.filter(is_available=True)
		if search_query:
			products = products.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
		if brand_filter:
			products = products.filter(brand=brand_filter)
		for p in products:
			p.model_type = 'Трактор'
		products = sorted(products, key=lambda x: x.created_at, reverse=True)
	elif equipment_type == 'sprayer':
		products = Sprayer.objects.filter(is_available=True)
		if search_query:
			products = products.filter(models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query))
		if brand_filter:
			products = products.filter(brand=brand_filter)
		for p in products:
			p.model_type = 'Обприскувач'
		products = sorted(products, key=lambda x: x.created_at, reverse=True)
	else:
		products = get_all_products(search_query=search_query, brand_filter=brand_filter)

	return render(request, 'projects/product_list.html', {
		'products': products,
		'categories': categories,
		'selected_category': selected_category,
		'search_query': search_query,
		'equipment_type': equipment_type,
	})


def product_detail(request, slug):
	# Спробуємо знайти товар у кожній моделі
	product = None
	
	product = Combiner.objects.filter(slug=slug).first()
	if product:
		product.model_type = 'Комбайн'
	else:
		product = Tractor.objects.filter(slug=slug).first()
		if product:
			product.model_type = 'Трактор'
		else:
			product = Sprayer.objects.filter(slug=slug).first()
			if product:
				product.model_type = 'Обприскувач'
	
	if not product:
		from django.http import Http404
		raise Http404("Товар не знайдено")

	extra_images = list(product.extra_images.all())
	return render(request, 'projects/product_detail.html', {
		'product': product,
		'extra_images': extra_images,
	})

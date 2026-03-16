
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from products.models import Combiner, Tractor, Sprayer
from .models import Cart, CartItem

# Вспомогательная функция для поиска товара по slug или id
def find_product(slug=None, pk=None):
    product = None
    model_type = ''
    if slug is not None:
        product = Combiner.objects.filter(slug=slug).first()
        if product:
            model_type = 'Комбайн'
        else:
            product = Tractor.objects.filter(slug=slug).first()
            if product:
                model_type = 'Трактор'
            else:
                product = Sprayer.objects.filter(slug=slug).first()
                if product:
                    model_type = 'Обприскувач'
    elif pk is not None:
        for model, name in ((Combiner, 'Комбайн'), (Tractor, 'Трактор'), (Sprayer, 'Обприскувач')):
            try:
                product = model.objects.get(pk=pk)
                model_type = name
                break
            except model.DoesNotExist:
                continue
    if product:
        product.model_type = model_type
    return product

# Работа с корзиной в сессии
def _get_session_cart(request):
    return request.session.get('cart', {})
def _save_session_cart(request, cart):
    request.session['cart'] = cart

# Добавить товар в корзину
def add_to_cart(request, slug):
    product = find_product(slug=slug)
    if not product:
        messages.error(request, 'Товар не знайдено')
        return redirect('products:product_list')
    key = f"{product._meta.model_name}:{product.id}"
    if request.user.is_authenticated:
        cart_obj, _ = Cart.objects.get_or_create(user=request.user.profile)
        ct = ContentType.objects.get_for_model(product)
        item, created = CartItem.objects.get_or_create(
            cart=cart_obj, content_type=ct, object_id=product.id
        )
        if not created:
            item.quantity += 1
            item.save()
    else:
        cart = _get_session_cart(request)
        if key in cart:
            cart[key]['quantity'] += 1
        else:
            cart[key] = {
                'name': str(product),
                'price': float(product.price),
                'image': product.image.url if product.image else '',
                'model_type': product.model_type,
                'quantity': 1,
            }
        _save_session_cart(request, cart)
    messages.success(request, 'Товар додано до кошика')
    return redirect('card:cart_details')

# Просмотр корзины
def cart_details(request):
    cart_dict = {}
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user.profile).first()
        if cart_obj:
            for item in cart_obj.items.select_related('content_type'):
                prod = item.product
                if not prod:
                    continue
                model_name = prod._meta.model_name
                model_type = 'Комбайн' if isinstance(prod, Combiner) else (
                    'Трактор' if isinstance(prod, Tractor) else 'Обприскувач')
                cart_dict[f"{model_name}:{prod.id}"] = {
                    'name': str(prod),
                    'price': float(prod.price),
                    'image': prod.image.url if prod.image else '',
                    'model_type': model_type,
                    'quantity': item.quantity,
                }
    else:
        cart_dict = _get_session_cart(request)
    item_count = sum(entry['quantity'] for entry in cart_dict.values())
    total_price = sum(entry['quantity'] * entry['price'] for entry in cart_dict.values())
    return render(request, 'card/cart_details.html', {
        'cart': cart_dict,
        'item_count': item_count,
        'total_price': total_price,
    })

# Обновить количество товара
def update_cart(request, product_key):
    qty = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user.profile).first()
        if cart_obj:
            try:
                model_name, pk = product_key.split(':')
                ct = ContentType.objects.get(model=model_name)
                item = CartItem.objects.filter(cart=cart_obj, content_type=ct, object_id=pk).first()
                if item:
                    if qty > 0:
                        item.quantity = qty
                        item.save()
                    else:
                        item.delete()
            except Exception:
                pass
    else:
        cart = _get_session_cart(request)
        if product_key in cart:
            if qty > 0:
                cart[product_key]['quantity'] = qty
            else:
                del cart[product_key]
            _save_session_cart(request, cart)
    return redirect('card:cart_details')

# Удалить товар из корзины
def remove_from_cart(request, product_key):
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user.profile).first()
        if cart_obj:
            try:
                model_name, pk = product_key.split(':')
                ct = ContentType.objects.get(model=model_name)
                CartItem.objects.filter(cart=cart_obj, content_type=ct, object_id=pk).delete()
            except Exception:
                pass
    else:
        cart = _get_session_cart(request)
        if product_key in cart:
            del cart[product_key]
            _save_session_cart(request, cart)
    return redirect('card:cart_details')

# Очистить корзину
def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user.profile).delete()
    else:
        request.session['cart'] = {}
    return redirect('card:cart_details')

# Оформление заказа (заглушка)
def checkout(request):
    cart_dict = {}
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user.profile).first()
        if cart_obj:
            for item in cart_obj.items.select_related('content_type'):
                prod = item.product
                if not prod:
                    continue
                model_name = prod._meta.model_name
                model_type = 'Комбайн' if isinstance(prod, Combiner) else (
                    'Трактор' if isinstance(prod, Tractor) else 'Обприскувач')
                cart_dict[f"{model_name}:{prod.id}"] = {
                    'name': str(prod),
                    'price': float(prod.price),
                    'image': prod.image.url if prod.image else '',
                    'model_type': model_type,
                    'quantity': item.quantity,
                }
    else:
        cart_dict = _get_session_cart(request)
    item_count = sum(entry['quantity'] for entry in cart_dict.values())
    total_price = sum(entry['quantity'] * entry['price'] for entry in cart_dict.values())
    return render(request, 'card/checkout.html', {
        'cart': cart_dict,
        'item_count': item_count,
        'total_price': total_price,
    })


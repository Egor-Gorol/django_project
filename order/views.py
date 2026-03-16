from django.shortcuts import render, redirect, get_object_or_404

from card.models import CartItem, Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def _get_cart_items(request):
    items = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user.profile).first()
        if not cart:
            return []
        for item in cart.items.select_related('content_type'):
            prod = item.product
            if not prod:
                continue
            items.append({
                'name': str(prod),
                'price': prod.price,
                'quantity': item.quantity,
            })
        return items

    cart = request.session.get('cart', {})
    if not cart:
        return []
    for key, entry in cart.items():
        items.append({
            'name': entry.get('name', 'Товар'),
            'price': entry.get('price', 0),
            'quantity': entry.get('quantity', 1),
        })
    return items


def checkout(request):
    cart_items = _get_cart_items(request)
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_phone=form.cleaned_data['phone'],
                shipping_sity=form.cleaned_data['shipping_city'],
                shipping_street=form.cleaned_data['shipping_street'],
                coment=form.cleaned_data.get('comment', ''),
                total_price=total_price,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    quantity=item['quantity'],
                    price=item['price'],
                )

            if request.user.is_authenticated:
                CartItem.objects.filter(cart__user=request.user.profile).delete()
            else:
                request.session['cart'] = {}

            return redirect('order:order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    return render(request, 'orders/confirmation.html', {'order': order, 'items': items})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # allow only owner or anonymous orders
    if order.user and request.user != order.user:
        return redirect('order:order_history')
    items = order.items.all()
    return render(request, 'orders/detail.html', {'order': order, 'items': items})


def order_history(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})


def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = []
    return render(request, 'orders/history.html', {'orders': orders})
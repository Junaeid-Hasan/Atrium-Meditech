from django.shortcuts import render
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

@staff_member_required
def admin_order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/invoice.html',
                  {'order': order})

def order_create(request):
    """
    Function-Based view for handling order creations. We use FBV here because handling
    forms manually, associating them with cart sessions, and generating records inline
    is straightforward and clear here compared to chaining multiple CBV mixins.
    """
    cart = Cart(request)
    if len(cart) == 0:
        return render(request, 'cart/detail.html', {'cart': cart, 'error': 'Your cart is empty'})
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         color=item['color'])
            # clear the cart
            cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

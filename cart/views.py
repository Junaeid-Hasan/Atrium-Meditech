from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """
    Function-Based View representing custom action to add to Cart. FBV is preferred over CBV
    when defining very simple controller logic that does not render typical 'views', and just manipulates data before redirecting.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        color = cd.get('color')
        
        # Check if we should redirect to checkout
        if request.POST.get('next') == 'checkout':
            cart.clear() # Clear existing cart items to ensure immediate checkout applies only to this product
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'],
                     color=color)
            return redirect('orders:order_create')
            
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'],
                 color=color)
        
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Displays cart contents and handles form presentation for item quantity logic.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})

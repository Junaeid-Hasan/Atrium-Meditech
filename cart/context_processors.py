from .cart import Cart

def cart(request):
    """Provide the 'cart' object globally to templates."""
    return {'cart': Cart(request)}

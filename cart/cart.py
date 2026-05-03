from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, color=None):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        # Create a unique key for product + color combination
        item_key = f"{product_id}_{color}" if color else product_id
        
        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0, 
                'price': str(product.price),
                'color': color,
                'product_id': product.id
            }
        
        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database."""
        # Get all unique product IDs from the keys (keys are like "id_color" or just "id")
        # Fallback to key if 'product_id' is missing (for backward compatibility with old sessions)
        product_ids = []
        for key, item in self.cart.items():
            if 'product_id' not in item:
                # Old format: key was the product_id
                item['product_id'] = int(key.split('_')[0])
            product_ids.append(item['product_id'])
            
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            # Match products to all items that have this product ID
            for item in cart.values():
                if item.get('product_id') == product.id:
                    item['product'] = product
        
        for key, item in list(cart.items()):
            if 'product' not in item:
                # Remove product from session if it no longer exists in database
                if key in self.cart:
                    del self.cart[key]
                    self.save()
                continue
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.cart = self.session[settings.CART_SESSION_ID] = {}
        self.save()

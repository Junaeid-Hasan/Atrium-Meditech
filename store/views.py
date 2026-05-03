from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

class ProductListView(ListView):
    """
    Class-based view for displaying a list of products. Using CBV here is ideal because
    Django provides robust generic views for rendering list pages, pagination etc. out of the box
    which drastically reduces boilerplate compared to Function-Based Views (FBV).
    """
    model = Product
    template_name = 'store/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query) | qs.filter(description__icontains=query)
        
        # Quick filters
        if self.request.GET.get('in_stock') == 'on':
            qs = qs.filter(stock__gt=0)
        
        if self.request.GET.get('cod') == 'on':
            # Assuming COD is a feature of the item or availability, but here we'll just handle it as a filter if needed.
            # If there's no COD field, we can ignore or assume all have it for now.
            pass

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=self.category)
        else:
            self.category = None
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    """
    Class-based view for displaying product details. Similar to ListView,
    CBVs provide clean handling of object retrieval (404 errors natively).
    """
    model = Product
    template_name = 'store/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass a cart add form to place items into the cart directly from details page.
        context['cart_product_form'] = CartAddProductForm()
        return context

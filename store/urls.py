from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('about/', TemplateView.as_view(template_name='store/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='store/contact.html'), name='contact'),
    path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

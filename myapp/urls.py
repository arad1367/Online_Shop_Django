from django.contrib import admin
from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.index),   # localhost:8000/myapp/
    path('products/', views.products, name='products'), # localhost:8000/myapp/products/
    # path('products/', views.ProductListView.as_view(), name='products'), # We used Class list view
    # path('products/<int:id>/', views.product_details, name='product_details'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_details'), # class based detail view
    path('products/add/', views.add_product, name='add_product'),
    # path('products/add/', views.ProductCreateView.as_view(), name='add_product'), # Class based create view
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    # path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'), # Class based Update view
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    # path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'), # Class based Delete view
    path('products/mylistings/', views.my_listings, name='my_listings'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'), # Class based Success view
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
    path('api/checkout-session/<id>',views.create_checkout_session,name='api_checkout_session'),
]
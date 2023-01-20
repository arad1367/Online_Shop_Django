from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products, OrderDetail
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator

from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe


# Create your views here.
def index(request):
    return HttpResponse('<h1>Hellllo Pejman :)</h1>')

# Function based view
def products(request):
    if request.method == 'POST':
        page_obj = searched_item = request.POST['search']
        if searched_item != "" and searched_item is not None:
            page_obj = Products.objects.filter(name__contains=searched_item)
        #Pagination
        per_page = request.GET.get("per_page", 3)
        paginator = Paginator(page_obj, per_page)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj':page_obj
        }
        return render(request, 'myapp/index.html', context=context)
        
    products = Products.objects.get_queryset().order_by('name')
    #Pagination
    per_page = request.GET.get("per_page", 3)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj
    }
    return render(request, 'myapp/index.html', context=context)

# Class based view for above products view [ListView]
class ProductListView(ListView):
    model = Products
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 3

def product_details(request, id):
    product = Products.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'myapp/details.html', context=context)

# Class based view for above product detail view [DetailView]
class ProductDetailView(DetailView):
    model = Products
    template_name = 'myapp/details.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_context_data(self,**kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


@login_required
def add_product(request):
    if request.method == 'POST':
        # Get data from form
        seller_name = request.user
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        # Add data to databse
        product = Products(name=name, price=price, description=description, image=image, seller_name=seller_name)
        product.save()
        return redirect('/myapp/products/') # redirect to url not template
    return render(request, 'myapp/addproduct.html')

# Class based view for creating product
@login_required
class ProductCreateView(CreateView):
    model = Products
    fields = ['name', 'price', 'description', 'image', 'seller_name']
    # Now we need to create template for it, the name come from model name >> products_form.html


@login_required
def update_product(request, id):
    product = Products.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.image = request.FILES['upload']
        product.save()
        return redirect('/myapp/products/') # redirect to url not template name
    context = {
        'product':product
    }
    return render(request, 'myapp/updateproduct.html', context=context)

# Class based view for Update a product
@login_required
class ProductUpdateView(UpdateView):
    model = Products
    fields = ['name', 'price', 'description', 'image', 'seller_name']
    template_name_suffix = '_update_form' # then just make product_update_form.html

@login_required
def delete_product(request, id):
    product = Products.objects.get(id=id)
    context = {
        'product':product
    }
    
    if request.method == 'POST':
        product.delete()
        return redirect('/myapp/products/')
    return render(request, 'myapp/delete.html', context=context)

# Class based view for Delete a product
@login_required
class ProductDeleteView(DeleteView):
    model = Products # then just create a template products_confirm_delete.html
    success_url = reverse_lazy('myapp:products')

def my_listings(request):
    products = Products.objects.filter(seller_name=request.user)
    context = {
        'products': products
    }
    return render(request, 'myapp/my_listings.html', context=context)


@csrf_exempt
def create_checkout_session(request,id):
    product = get_object_or_404(Products,pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price *100),
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('myapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url= request.build_absolute_uri(
            reverse('myapp:failed')),
    )
    
    order = OrderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name ='myapp/payment_success.html'
    
    def get(self,request,*args,**kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request,self.template_name)
    
class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'
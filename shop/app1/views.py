from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from .models import Contact
from django.contrib import messages


# Create your views here.

#class ProductView(View):
  #def get(self,request):
    #totalitem=0
    #products = Product.objects.all()

    #data={
      #"products":products 
    #}
    #if request.user.is_authenticated:
      #totalitem=len(Cart.objects.filter(user=request.user))
    #return render(request, 'home.html', data, {'totalitem':totalitem})

class ProductView(View):
    def get(self, request):
        totalitem = 0
        products = Product.objects.all()

        data = {
            "products": products,
            "totalitem": totalitem,
        }

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        
        data["totalitem"] = totalitem

        return render(request, 'home.html', data)


#def product_detail(request):
    #return render(request, 'productdetail.html')
 
class ProductDetailView(View):
  def get(self,request,pk):
   totalitem = 0
   product=Product.objects.get(pk=pk)
   item_already_in_cart = False
   if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

   return render(request, 'productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
  totalitem=0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   user=request.user
   cart=Cart.objects.filter(user=user)
   print(cart)
   amount=0.0
   shipping_amount=70.0
   total_amount=0.0
   cart_product=[p for p in Cart.objects.all() if p.user == user ]
   #print(cart_product)
  if cart_product:
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
     totalamount = amount + shipping_amount
    return render(request, 'addtocart.html', {'carts': cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
  else:
    return render(request, 'emptycart.html')
   
def plus_cart(request):
  if request.method == "GET":
    prod_id= request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
     
   

    data={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount

     }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == "GET":
    prod_id= request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
     
   

    data={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount +shipping_amount

     }
    return JsonResponse(data)
  

def remove_cart(request):
  if request.method == "GET":
    prod_id= request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
  
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
     
   

    data={
      'amount':amount,
      'totalamount':amount+shipping_amount

     }
    return JsonResponse(data)


def buy_now(request):

 return render(request, 'buynow.html')

#def login(request):
 #return render(request, 'login.html')

#def profile(request):
 #return render(request, 'profile.html')

@login_required
def address(request):
 totalitem=0
 add=Customer.objects.filter(user=request.user)
 totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'address.html', {'add':add,'active':'btn-primary', 'totalitem':totalitem})

#def passwordchange(request):
 #return render(request, 'passwordchange.html')

#def customerregistration(request):
 #return render(request, 'customerregistration.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form=CustomerRegistrationForm()
  return render(request, 'customerregistration.html', {'form':form})
 def post(self,request):
  form=CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Registered Successfully..! ')
   form.save()
  return render(request, 'customerregistration.html', {'form':form})
 

   

@login_required
def checkout(request):
 totalamount=0
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user == request.user]
 totalitem = len(Cart.objects.filter(user=request.user))
 if cart_product:
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
  totalamount=amount+shipping_amount
 return render(request, 'checkout.html', {'add':add, 'totalamount': totalamount, 'cart_items':cart_items, 'totalitem':totalitem})


@login_required
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders")
 


@login_required
def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'orders.html', {'order_placed':op, 'totalitem':totalitem})



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
   totalitem=0
   form=CustomerProfileForm()
   totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
  
  def post(self,request):
    form =CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request,'Congratulations Profile Updated Successfully..!')
    return render(request, 'profile.html', {'form':form, 'active':'btn-primary'})
  
@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('description')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
        return redirect('contact')
    
    return render(request, 'contact.html')

       
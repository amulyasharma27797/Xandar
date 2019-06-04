from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response

from core.get_data import get_data
from core.models import OrderedItems, DeliveryAddresses, Customer, Wishlist, Cart, CartItems, ProductImage
from django.views.generic import ListView
# Create your views here.


def show_ordered_items(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        if request.user.is_authenticated:
            try:
                current_cart = Cart.objects.get(user_id=request.user.id)
                orders = CartItems.objects.filter(cart_id=current_cart)
                delivery_addresses = DeliveryAddresses.objects.filter(customer=request.user)
                context = {
                    'orders':orders,
                    'addresses': delivery_addresses
                }
            except Cart.DoesNotExist:
                context = {
                    'orders': False
                }
            return render(request, 'orders/checkout.html', context)
        else:
            return redirect('accounts:login_app')



def apply_coupon(request):
    coupon = request.GET['coupon']
    total = int(request.GET['total'])
    if coupon == 'FIRST':
        discount = 0.10 * total
    else:
        discount  = 0
    total = total-discount
    return HttpResponse(total)


def place_order(request):
    address_dict={}
    for key, values in request.GET.items():
        address_dict[key] = values
    UserAddress = DeliveryAddresses()
    for key, values in request.GET.items():
            setattr(UserAddress, key, request.GET[key])
    UserAddress.customer = request.user
    address_exists = get_data(DeliveryAddresses,
             receiver_name=UserAddress.receiver_name,
             customer=UserAddress.customer,
             phone_number=UserAddress.phone_number,
             city=UserAddress.city,
             pincode=UserAddress.pincode,
             state=UserAddress.state
             )
    if address_exists is None:
        UserAddress.save()
    request.session['order_context'] = request.GET
    return HttpResponse('Order Placed Successful')


class get_delivery_addresses(ListView):
    template_name = 'orders/delivery_address.html'
    context_object_name = "address"

    def get_queryset(self):
        queryset = DeliveryAddresses.objects.filter(customer=self.request.user)
        return queryset

    def post(self,id):
        pass

def order_successful_page(request):
    context = request.session.get('order_context')
    current_cart = Cart.objects.get(user_id=request.user.id)
    orders = CartItems.objects.filter(cart_id=current_cart)
    for order in orders:
        OrderedItems.objects.create(customer=request.user, product=order.product)
    context['orders']=orders
    current_cart.delete()
    return render(request, 'orders/order_confirmed.html', context)

class GetOrderedItems(ListView):
    template_name = 'orders/ordered_items.html'
    
    def get_queryset(self):
        queryset = OrderedItems.objects.filter(customer=self.request.user).order_by('-order_date')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for order in context['object_list']:
            order.product.product_image = ProductImage.objects.filter(product=order.product).first()
        return context

def add_address(request):

    if request.user.is_authenticated:

        if request.method == "POST":
            name = request.POST['name']
            phone = request.POST['phone']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            pin = request.POST['pin']
            state = request.POST.get('state')

            user = DeliveryAddresses.objects.create(customer=request.user, receiver_name=name, street_address=address1,
                                                    city=city, phone_number=phone, pincode=pin, state=state)

            return redirect('orders:delivery_address')

    return render(request, 'orders/add_address.html',)



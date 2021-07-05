from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem,Order,ShippingAddress
from account.models import Profile
from addkabaad.models import Product
import datetime
import json
from django.views.decorators.csrf import csrf_exempt



def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.products.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('addkabaad:list')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
    
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('addkabaad:list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'order_summary.html', context)

@login_required()
def checkout(request):  
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
    }

    return render(request, 'checkout.html', context)

@csrf_exempt
@login_required
def processOrder(request):
    if request.method=='POST':
        data=json.loads(request.body)
        user_profile = get_object_or_404(Profile, user=request.user)
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        total=data['form']['total']
        if str(total)==str(user_order.get_cart_total()):
            order_items=user_order.items.all()
            for item in order_items:
                product=item.product
                product.available=False
                product.save()
            user_order.is_ordered=True
        user_order.save()
        ShippingAddress.objects.create(
            owner=user_profile,
            order=user_order,
            is_ordered = True,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
        return JsonResponse('Order placed',safe=False)

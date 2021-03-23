from django.shortcuts import render, redirect
from .forms	import	ProductCreateForm
from django.contrib	import	messages
from django.contrib.auth.decorators	import login_required
from django.shortcuts import get_object_or_404
from .models import	Product,Category
from django.core.paginator	import	Paginator,	EmptyPage,	\
	PageNotAnInteger
from django.http	import	HttpResponse
from shopping_cart.models import Order
# Create your views here.

@login_required
def	product_create(request,**kwargs):
    
    if	request.method	==	'POST':
	#	form	is	sent
        form = ProductCreateForm(request.POST,request.FILES)
        if form.is_valid():
            #form data is valid
            cd=form.cleaned_data
            print("hey",cd)
            new_item=form.save(commit=False)
            #assign	current	user to	the	item
            new_item.user = request.user
            typo = kwargs.get('decision', "")
            if typo=="sell":
                new_item.decision=False
            else:
                new_item.decision=True
            new_item.save()
           
            
            messages.success(request,	'Product	added	successfully')
            # redirect	to	new	created	item	detail	view
            return redirect(new_item.get_absolute_url())
        print("hh")
    else:
	# build	form	with	data	provided	by	the	bookmarklet	via	GET
        form = ProductCreateForm(data=request.GET)
    return render(request,
    'products/product/create.html',
    {'section':	'products',
    'form':	form})

@login_required
def	product_detail(request,id,slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    print(filtered_orders)
    if filtered_orders.exists():
        print("heuu")
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]
    context = {
        'object_list': object_list,
        'current_order_products': current_order_products,
        'section':'products',
        'product': product
    }
   
    return render(request,'products/product/detail.html',context)

@login_required
def	product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products=Product.objects.all()
    products = products.filter(decision=False)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category,decision=False)
    paginator = Paginator(products,	8)
    page = request.GET.get('page')
    try:
        products	=	paginator.page(page)
    except	PageNotAnInteger:
        products	=	paginator.page(1)
    except	EmptyPage:
        if	request.is_ajax():
	        return	HttpResponse('')
        products=paginator.page(paginator.num_pages)
    if request.is_ajax():
            return	render(request,'products/product/list_ajax.html',{'category': category,'categories': categories,'section':'products','products': products})
    return	render(request,'products/product/list.html',{'category': category,'categories': categories,'section':'products','products': products})
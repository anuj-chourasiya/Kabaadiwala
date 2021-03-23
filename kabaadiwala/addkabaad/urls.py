from django.urls	import	path
from . import	views
app_name =	'addkabaad'
urlpatterns	=	[
	path('create-sell/',	views.product_create,kwargs={'decision': 'sell'},	name='create-sell'),
	path('create-donate/',	views.product_create,kwargs={'decision': 'donate'},	name='create-donate'),
	path('detail/<int:id>/<slug:slug>/',views.product_detail, name='detail'),
	path('',views.product_list,	name='list'),
    path('<slug:category_slug>/', views.product_list,
    name='product_list_by_category'),

]
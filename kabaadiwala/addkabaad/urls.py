from django.urls	import	path
from . import	views
app_name =	'addkabaad'
urlpatterns	=	[
	path('create/',	views.product_create,	name='create'),
	path('detail/<int:id>/<slug:slug>/',views.product_detail, name='detail'),
	path('',views.product_list,	name='list'),
    path('<slug:category_slug>/', views.product_list,
    name='product_list_by_category'),

]
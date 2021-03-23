from	django.db	import	models
from	django.conf	import	settings
from	django.contrib.auth.models	import	User
from addkabaad.models import Product
from django.db.models.signals import post_save



class	Profile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,
			on_delete=models.CASCADE)
	date_of_birth =	models.DateField(blank=True,	null=True)
	photo	=	models.ImageField(upload_to='users/%Y/%m/%d/',
	blank=True)
	products=models.ManyToManyField(Product,blank=True)
	def	__str__(self):
	    return	'Profile	for	user	{}'.format(self.user.username)
def post_save_profile_create(sender, instance, created, *args, **kwargs):
   		user_profile, created = Profile.objects.get_or_create(user=instance)




post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

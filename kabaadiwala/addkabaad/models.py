from django.db	import	models
from django.conf import	settings
from django.utils.text	import	slugify
from django.urls import	reverse

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def	save(self,*args,**kwargs):
        if	not	self.slug:
            self.slug=slugify(self.name)
        super(Category,self).save(*args,**kwargs)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('kabaad:product_list_by_category',args=[self.slug])



class Product(models.Model):
    user	=	models.ForeignKey(settings.AUTH_USER_MODEL,
    related_name='product_created',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='product/')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    def	save(self,*args,**kwargs):
        if	not	self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)
    def	get_absolute_url(self):
        return	reverse('addkabaad:detail',args=[self.id,self.slug])
    

  
    
    
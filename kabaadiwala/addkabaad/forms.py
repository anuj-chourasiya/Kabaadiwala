from	django	import	forms
from	.models	import	Product
from	urllib	import	request
from	django.core.files.base	import	ContentFile
from	django.utils.text	import slugify

class	ProductCreateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('name','category','image','description','price','available')
        
  
    
   
   
    
    
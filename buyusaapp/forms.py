from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gig, Profile, Product
from .widgets import ImagePreviewInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Accordion, AccordionGroup, Alert
from django.core.exceptions import ValidationError

class GigForm(ModelForm):

    title = forms.CharField(label=u'Brand Name', max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=2000,label=u'Description', required=True)
    BrandLink = forms.CharField(label=u'Website', required=True)
    BrandCustomerServicePhone = forms.CharField(label=u'Customer Service Phone', required=False)
    BrandSearch = forms.CharField(widget=forms.Textarea, max_length=400,label=u'Search Keywords', required=True)
    BrandWhereToBuy = forms.CharField(label=u'Where To Buy', max_length=200, required=True)

    # BrandLogo = forms.ImageField(widget=ImagePreviewInput(),label=u'Logo',required=False)

    #BrandCaption1 = forms.CharField(label=u'Brand Caption 1', max_length=200, required=False)
    #BrandPicture1 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 1',required=False)

    #BrandCaption2 = forms.CharField(label=u'Brand Caption 2', max_length=200, required=False)
    #BrandPicture2 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 2',required=False)

    #BrandCaption3 = forms.CharField(label=u'Brand Caption 3', max_length=200, required=False)
    #BrandPicture3 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 3',required=False)

    #BrandCaption4 = forms.CharField(label=u'Brand Caption 4', max_length=200, required=False)
    #BrandPicture4 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 4',required=False)
    
    #BrandCaption5 = forms.CharField(label=u'Brand Caption 5', max_length=200, required=False)
    #BrandPicture5 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 5',required=False)
    
    #BrandCaption6 = forms.CharField(label=u'Brand Caption 6', max_length=200, required=False)
    #BrandPicture6 = forms.ImageField(widget=ImagePreviewInput(),label=u'Brand Image 6',required=False)    
    
    Publish = forms.ChoiceField(choices=[(True,'Published'),(False,'Unpublished')])
    
    class Meta:
        model = Gig
        # *** BEGIN - Update fields - TCG - 1/28/18 ***
        # fields = ['title', 'category', 'description', 'price', 'photo', 'status']
        #fields = ['title', 'description', 'BrandLogo', 
        #          'BrandLink', 'BrandCustomerServicePhone',
        #          'BrandSearch', 'BrandWhereToBuy', 
        #          'BrandCaption1', 'BrandPicture1', 
        #          'BrandCaption2', 'BrandPicture2', 
        #          'BrandCaption3', 'BrandPicture3', 
        #          'BrandCaption4', 'BrandPicture4', 
        #          'BrandCaption5', 'BrandPicture5',
        #          'BrandCaption6', 'BrandPicture6',
        #          'Publish']

        fields = ['title', 'description', 'BrandLink', 'BrandCustomerServicePhone', 'BrandSearch', 'BrandWhereToBuy', 'Publish']

    def __init__(self, *args, **kwargs):
        self.edit = kwargs.pop('edit', None)
        super(GigForm, self).__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.helper.form_id = 'id-gigForm'
        self.helper.form_class = 'gigForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'create_gig'
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            
            Fieldset('Brand Details', 
                Field('title'), 
                Field('description'),
                # Field('BrandLogo'),
                Field('BrandLink'), 
                Field('BrandCustomerServicePhone'), 
                Field('BrandSearch'),
                Field('BrandWhereToBuy'),
            ),

            
            #Fieldset('Brand Images',
            #    Accordion(
            #        AccordionGroup('',                        
            #            Field('BrandCaption1'), 
            #            Field('BrandPicture1'),
            #           Alert(content='<strong>Keep total image uploads less than 50MB...</strong>'),
            #            css_id = "first_gig_image",
            #            css_class='button white'
            #        ),
            #        AccordionGroup('Add More Images', 
            #            Field('BrandCaption2'), 
            #            Field('BrandPicture2'),
            #            Field('BrandCaption3'), 
            #            Field('BrandPicture3'),
            #            Field('BrandCaption4'), 
            #            Field('BrandPicture4'),
            #            Field('BrandCaption5'), 
            #            Field('BrandPicture5'),
            #            Field('BrandCaption6'), 
            #            Field('BrandPicture6')
            #        ),
            #    ),                
            #),

            Fieldset('Submit Brand',                 
                Field('Publish'),
            ),
        )

        # if self.edit:
        #    self.fields['BrandLogo'].required = False
        #    self.fields['BrandPicture1'].required = False        


class SignUpForm(UserCreationForm):
    #avatar = forms.ImageField()
    #about = forms.CharField()
    #slogan = forms.CharField()
    #CompanyName = forms.CharField()
    #CompanyCategory = forms.ChoiceField(choices=Profile.COMPANYCATEGORY_CHOICES)
    #CompanyType = forms.ChoiceField(choices=Profile.COMPANYTYPE_CHOICES)
    #CompanyLogo = forms.FileField()
    #CompanyLink = forms.CharField()
    #CompanyContactName = forms.CharField()
    #CompanyContactPhone = forms.CharField()
    CompanyContactEmail = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class ProfileForm(ModelForm):    
    #avatar = forms.ImageField(widget=ImagePreviewInput(),label=u'avatar')
    #CompanyLogo = forms.ImageField(widget=ImagePreviewInput(),label=u'CompanyLogo')
    Publish = forms.ChoiceField(choices=[(True,'Published'),(False,'Unpublished')])
    class Meta:
        model = Profile
        #fields = ('avatar', 'about', 'slogan', 'CompanyName', 'CompanyCategory', 'CompanyType',
        #          'CompanyLogo', 'CompanyLink', 'CompanyContactName', 'CompanyContactPhone',
        #          'CompanyContactEmail','Publish')
        
        fields = ('about', 'slogan', 'CompanyName', 'CompanyCategory', 'CompanyType',
                  'CompanyLink', 'CompanyContactName', 'CompanyContactPhone',
                  'CompanyContactEmail','Publish')
        

class ImportDataForm(forms.Form):
    source = forms.CharField(label=u'What is the source of this import?', required=True)    
    file = forms.FileField(label=u'data file(Excel file)',required=True)



class ProductForm(ModelForm):

    title = forms.CharField(label=u'Product Name', max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=2000,label=u'Description', required=True)
    search_keywords = forms.CharField(widget=forms.Textarea, max_length=400,label=u'Search Keywords', required=False)
    brand = forms.ModelChoiceField(queryset=Gig.objects.all()[:30], label=u'Brand', required=True, initial=0)

    #caption1 = forms.CharField(label=u'Caption 1', max_length=200, required=True)
    #image1 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 1',required=True)

    #caption2 = forms.CharField(label=u'Caption 2', max_length=200, required=False)
    #image2 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 2',required=False)

    #caption3 = forms.CharField(label=u'Caption 3', max_length=200, required=False)
    #image3 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 3',required=False)

    #caption4 = forms.CharField(label=u'Caption 4', max_length=200, required=False)
    #image4 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 4',required=False)
    
    #caption5 = forms.CharField(label=u'Caption 5', max_length=200, required=False)
    #image5 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 5',required=False)
    
    #caption6 = forms.CharField(label=u'Caption 6', max_length=200, required=False)
    #image6 = forms.ImageField(widget=ImagePreviewInput(),label=u'Image 6',required=False)
    
    publish = forms.ChoiceField(choices=[(True,'Published'),(False,'Unpublished')])
    
    class Meta:
        model = Product        
        #fields = ['title', 'description', 'brand', 'search_keywords',
        #          'caption1', 'image1',
        #          'caption2', 'image2',
        #          'caption3', 'image3',
        #          'caption4', 'image4',
        #          'caption5', 'image5',
        #          'caption6', 'image6',                  
        #          'publish']

        fields = ['title', 'description', 'brand', 'search_keywords', 'publish']

    def __init__(self, *args, **kwargs):
        self.user_obj = kwargs.pop('user_obj', None)
        self.edit = kwargs.pop('edit', None)
        super(ProductForm, self).__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.helper.form_id = 'id-gigForm'
        self.helper.form_class = 'gigForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'create_product'
        self.helper.form_show_errors = True
        self.helper.error_text_inline = True
        self.helper.help_text_inline = False
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            
            Fieldset('Product Details', 
                Field('title'), 
                Field('brand'), 
                Field('description'),
                Field('search_keywords'),
            ),

            #Fieldset('Product Images',
            #    Accordion(
            #        AccordionGroup('',                        
            #            Field('caption1'), 
            #           Field('image1'),
            #           Alert(content='<strong>Keep total image uploads less than 50MB...</strong>'),
            #            css_id = "first_gig_image",
            #            css_class='button white'
            #        ),
            #        AccordionGroup('Add More Images', 
            #            Field('caption2'), 
            #            Field('image2'),
            #            Field('caption3'), 
            #            Field('image3'),
            #            Field('caption4'), 
            #            Field('image4'),
            #            Field('caption5'), 
            #            Field('image5'),
            #            Field('caption6'), 
            #            Field('image6')
            #        ),
            #    ),                
            #),

            Fieldset('Submit Product',                 
                Field('publish'),
            ),
        )

        #if self.edit:
        #    self.fields['image1'].required = False

        if self.user_obj:
            gig_ids = [gig.id for gig in Gig.objects.filter(user=self.user_obj)[:30]] # workaround bcuz u cant slice and then filter a queryset            
            self.fields['brand'].queryset = Gig.objects.filter(user=self.user_obj, id__in=gig_ids)

    '''
    def clean_brand(self):
        brand = self.cleaned_data['brand']
        possible_brands = Gig.objects.filter(user=self.user)
        for bran in possible_brands:
            if bran.title == brand:
                return brand
        raise ValidationError("Brand does not exist for user")
        return None
    '''
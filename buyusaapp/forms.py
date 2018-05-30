from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gig, Profile
from .widgets import ImagePreviewInput

class GigForm(ModelForm):
    BrandLogo = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandLogo',required=False)
    BrandPicture1 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture1',required=False)
    BrandPicture2 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture2',required=False)
    BrandPicture3 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture3',required=False)
    BrandPicture4 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture4',required=False)
    BrandPicture5 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture5',required=False)
    BrandPicture6 = forms.ImageField(widget=ImagePreviewInput(),label=u'BrandPicture6',required=False)
    
    Publish = forms.ChoiceField(choices=[(True,'Published'),(False,'Unpublished')])
    class Meta:
        model = Gig
        # *** BEGIN - Update fields - TCG - 1/28/18 ***
        # fields = ['title', 'category', 'description', 'price', 'photo', 'status']
        fields = ['title', 'category', 'description', 'BrandLogo', 'BrandLink', 'BrandCustomerServicePhone', 'BrandSearch',
                  'BrandWhereToBuy', 'BrandPicture1', 'BrandPicture2', 'BrandPicture3', 'BrandPicture4', 'BrandPicture5', 
                  'BrandPicture6','BrandCaption1','BrandCaption2','BrandCaption3','BrandCaption4','BrandCaption5',
                  'BrandCaption6','Publish']
        
        

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
    #avatar = forms.ImageField()
    #CompanyLogo = forms.ImageField()
    avatar = forms.ImageField(widget=ImagePreviewInput(),label=u'avatar')
    CompanyLogo = forms.ImageField(widget=ImagePreviewInput(),label=u'CompanyLogo')
    Publish = forms.ChoiceField(choices=[(True,'Published'),(False,'Unpublished')])
    class Meta:
        model = Profile
        fields = ('avatar', 'about', 'slogan', 'CompanyName', 'CompanyCategory', 'CompanyType',
                  'CompanyLogo', 'CompanyLink', 'CompanyContactName', 'CompanyContactPhone',
                  'CompanyContactEmail','Publish')
        
class ImportDataForm(forms.Form):
    source = forms.CharField(label=u'What is the source of this import?',required=True)
    file = forms.FileField(label=u'data file(Excel file)',required=True)
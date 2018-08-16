from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):
    # *** BEGIN - Choices added for BuyUSA - TCG - 1/19/18***
    COMPANYCATEGORY_CHOICES = {
        ("b2b", "Business-to-Business"),
        ("b2c", "Business-to-Consumer")
    }

    COMPANYTYPE_CHOICES = {
        ("manufacturer", "Manufacturer"),
        ("wholesale", "Wholesale"),
        ("retail", "Retail"),
        ("service", "Service"),
        ("independent", "Independent")
    }
    # *** END - Choices added for BuyUSA - TCG - 1/19/18 ***

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500)
    about = models.CharField(max_length=1000, default='')
    slogan = models.CharField(max_length=500, default='')
    # *** BEGIN - Fields added for BuyUSA - TCG - 1/19/18 ***
    CompanyName = models.CharField(max_length=50, default='')
    CompanyCategory = models.CharField(max_length=3, choices=COMPANYCATEGORY_CHOICES, default='b2c')
    CompanyType = models.CharField(max_length=12, choices=COMPANYTYPE_CHOICES, default='manufacturer')
    CompanyLogo = models.FileField(upload_to='profile', default='')
    CompanyLink = models.CharField(max_length=50, default='')
    BBB = models.BooleanField(default=True)
    CompanyContactName = models.CharField(max_length=50, default='')
    CompanyContactPhone = models.CharField(max_length=50, default='')
    CompanyContactEmail = models.CharField(max_length=50, default='')
    CompanyJoined = models.DateTimeField(default=timezone.now)
    # *** END - Fields added for BuyUSA - TCG - 1/19/18 ***
    ImportedCompanyID = models.CharField(max_length=50, default='') 
    # 1-126 (This id will be the concatenation of the read-only table’s ImportID field, a “-“, and the companyID from the import. 
    # The reason is this: what if we have 3 sources that all use the same company ID number? This way we can differentiate them.)
    CompanyID = models.IntegerField(null=True)  # This is an auto generated incrementing number (per company, not per row)
    flag = models.BooleanField(default=False) 
    # A flag should be added to the user table for each of these users created from new imported records as a boolean of whether 
    # or not the user has logged into the site yet
    LoginLink = models.CharField(max_length=50, default='') 
    # Also, a link should be created and added to a new column called “LoginLink”. 
    # This url will be sent to new users (using the address listed in the “Email” column) 
    # so they can log in one time and then change their password and begin using the site, 
    # updating their profile, adding new gigs, etc.
    # *** END - Fields added for BuyUSA - Dan Kwok - 5/5/18 ***
    Publish = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username
    
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Gig(models.Model):
    CATEGORY_CHOICES = {
        ("C1", "Category 1"),
        ("C2", "Category 2"),
        ("C3", "Category 3"),
        ("C4", "Category 4"),
        ("C5", "Category 5")
    }

    title = models.CharField(max_length=500)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='')
    description = models.CharField(max_length=1000, default='') # RichTextField(max_length=1000, default='')
    BrandLogo = models.FileField(upload_to='gigs')
    BrandLink = models.CharField(max_length=50, default='')
    BrandCustomerServicePhone = models.CharField(max_length=50, default='')
    BrandSearch = models.CharField(max_length=500, default='')
    BrandWhereToBuy = models.CharField(max_length=200, default='')
    # price = models.IntegerField(default=6)
    # photo = models.FileField(upload_to='gigs', default='')
    BrandPicture1 =  models.FileField(upload_to='gigs')
    BrandPicture2 =  models.FileField(upload_to='gigs')
    BrandPicture3 =  models.FileField(upload_to='gigs')
    BrandPicture4 =  models.FileField(upload_to='gigs')
    BrandPicture5 =  models.FileField(upload_to='gigs')
    BrandPicture6 =  models.FileField(upload_to='gigs') #　added by guolei 02/23/2017
    BrandCaption1 = models.CharField(max_length=200, default='')
    BrandCaption2 = models.CharField(max_length=200, default='')
    BrandCaption3 = models.CharField(max_length=200, default='')
    BrandCaption4 = models.CharField(max_length=200, default='')
    BrandCaption5 = models.CharField(max_length=200, default='')
    BrandCaption6 = models.CharField(max_length=200, default='')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    # *** BEGIN - Fields added for BuyUSA - Dan Kwok - 5/5/18 ***
    BrandID = models.IntegerField(null=True)
    # BrandID: This is an auto generated incrementing number (per row). So for the three brands in companyID=126, 
    # there will be three records sharing the same CompanyID (parent), but unique Brand IDs (children).
    CompanyID = models.IntegerField(null=True)
    # *** END - Fields added for BuyUSA - Dan Kwok - 5/5/18 ***
    Publish = models.BooleanField(default=True)
    # i thought of something… i can’t remember if this is in there or not, but if you can add it if it is not, 
    # I’d really appreciate it. can you add a “Publish” checkmark for the gig (brands/products), 
    # as well as for the user/company profile? If Publish is selected, then it is made available to public for search results,
    # public display, etc. Otherwise, it remains a private draft. also if the user/company profile is not published, 
    # then I suppose the gigs (brands/products) should be disabled too. 
    def __str__(self):
        return self.title
    def get_Publish(self):
        rst = 'Published'
        if not self.Publish:
            rst = 'Unpublished'
        return rst

class Purchase(models.Model):
    gig = models.ForeignKey(Gig,on_delete=models.CASCADE)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.gig.title

class Review(models.Model):
    gig = models.ForeignKey(Gig,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content

class Donate(models.Model):
    username = models.CharField(verbose_name='User name',max_length=200)
    donatevalue = models.FloatField(verbose_name='Donate value')
    cardtype = models.CharField(verbose_name='Card type',max_length=200)
    cc_number = models.CharField(verbose_name='Card number',max_length=200)
    cc_exp_date = models.CharField(verbose_name='Expire date',max_length=200)
    cc_ccv = models.CharField(verbose_name='Card ccv',max_length=200)
    holdername = models.CharField(verbose_name='Card holdername',max_length=200)
    
    def __str__(self):
        return '%s,%s' % (self.holdername,self.donatevalue)
    
class ImportData(models.Model):
    companyid = models.CharField(max_length=20)
    company = models.CharField(max_length=200)
    employees = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    psic = models.CharField(max_length=20)
    brandnames = models.CharField(max_length=500)
    salutation = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    middlename = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    suffix = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    titleext = models.CharField(max_length=500)
    ImportSource = models.CharField(max_length=200)
    # Every new record being imported should have the value of "3rd Party - XYZ Data” in the ImportSource column.
    ImportTimestamp = models.DateTimeField(auto_now_add=True)
    # Additionally, a time-date stamp of the import should be added as a new column in the table.
    # The column name should be ImportTimestamp. This should be listed on every record of this specific import.
    ImportID = models.IntegerField(default=1)
    # One final new column called “ImportID" should be added. This will simply be a number (start with 1). 
    # Every time there is a new import, the number will be incremented by 1. 
    # Every record from that import will have whatever the latest incremented number is listed in this column. 
    # For example, for our first import, the number 1 will be in Import ID for every record brought in during the import.
    def __str__(self):
        return self.company


class Product(models.Model):

    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Gig,on_delete=models.SET_NULL, null=True)
    search_keywords = models.CharField(max_length=500, default='')
    image1 =  models.FileField(upload_to='products')
    image2 =  models.FileField(upload_to='products')
    image3 =  models.FileField(upload_to='products')
    image4 =  models.FileField(upload_to='products')
    image5 =  models.FileField(upload_to='products')
    image6 =  models.FileField(upload_to='products')
    caption1 = models.CharField(max_length=200, default='')
    caption2 = models.CharField(max_length=200, default='')
    caption3 = models.CharField(max_length=200, default='')
    caption4 = models.CharField(max_length=200, default='')
    caption5 = models.CharField(max_length=200, default='')
    caption6 = models.CharField(max_length=200, default='')
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField(default=timezone.now)
    publish = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        ''' On save, update timestamps '''
        if not self.id:
            self.create_time = timezone.now()
        self.modified_time = timezone.now()
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_Publish(self):
        rst = 'Published'
        if not self.publish:
            rst = 'Unpublished'
        return rst

    
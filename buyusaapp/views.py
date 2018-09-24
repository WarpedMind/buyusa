from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q, Max
from django.db import transaction, connection
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import RequestContext
from crispy_forms.utils import render_crispy_form
from itertools import chain
from django.db import connection
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from .models import Gig, Profile, Purchase, Review, Donate, ImportData, Product
from .forms import GigForm, SignUpForm, ProfileForm, ImportDataForm


import os,random, threading, re, datetime, sys
import xlrd
import braintree
import csv
braintree.Configuration.configure(braintree.Environment.Sandbox, merchant_id="7968vwncy9mkmwv6", public_key="5k6r27pfddhdx4wb", private_key="3a6cfa52f4b1d37475125a7a5b5117eb")

import payeezy
import logging
logger = logging.getLogger("buyusa")

# Create your views here.
def home(request):
    title = request.GET.get('title')
    #gigs = Gig.objects.filter(status=True,Publish=True,user__profile__Publish=True)
    gigs = None
    return render(request, 'home.html', {"gigs": gigs, "MEDIA_URL" : settings.MEDIA_URL, 'title': title})

def gig_detail(request, id):
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], gig_id=id, user=request.user )
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        logger.exception("Error GIG DOES NOT EXIST...")
        return redirect('/')
    
    if request.user.is_anonymous or \
        Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
        Review.objects.filter(gig=gig, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0
    reviews = Review.objects.filter(gig=gig)
    client_token = braintree.ClientToken.generate()

    products = Product.objects.filter(brand=gig, publish=True).order_by('create_time')
    paginator_prods = Paginator(products, settings.SEARCH_RESULTS_PER_PAGE)
    profile = Profile.objects.get(user=gig.user)
    return render(request, 'gig_detail.html', {"show_post_review": show_post_review, "reviews": reviews, "gig": gig, "products": paginator_prods.get_page("1"), 
                                                "profile": profile, "client_token": client_token , "MEDIA_URL" : settings.MEDIA_URL, })


@login_required(login_url="/login")
def create_gig(request):
    
    if request.method == 'POST':        
        form = GigForm(request.POST, request.FILES)        
        if form.is_valid():
            gig = form.save(commit=False)
            gig.user = request.user
            gig.CompanyID=gig.user.profile.CompanyID
            gig.save()
            gig.BrandID = gig.id
            gig.save(update_fields=['BrandID',])
            return redirect('my_gigs')
    else:
        form = GigForm()

    errors = form.errors
    errors_non = form.non_field_errors
    
    return render(request, 'create_gig.html', {'gig_form': form, 'gig_errors':errors, 'errors_non':errors_non})


@login_required(login_url="/login")
def edit_gig(request, id):
    try:        
        gig = Gig.objects.get(id=id, user=request.user)
        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig, edit=True)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
        else:
            gig_form = GigForm(instance=gig, edit=True)

        errors = gig_form.errors
        errors_non = gig_form.non_field_errors    
        
        gig_form.helper.form_action = "/edit_gig/" + str(gig.id) + "/"
        return render(request, 'edit_gig.html', {"gig": gig, "gig_form":gig_form, 'gig_errors':errors, 'errors_non':errors_non})
    except Gig.DoesNotExist:
        return redirect('/')

@login_required(login_url="/login")
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    products = Product.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs, "products":products})

#@login_required(login_url="/login")
def profile(request, username):
    profile_form=None
    update_msg = None
    if request.method == 'POST' :
        profile = Profile.objects.get(user=request.user)
        #oldprofileflag = profile.Publish
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            #profile.avatar = file_save_to_media(profile_form.cleaned_data.get('avatar'))        
            profile.save()
            update_msg = True
            #if oldprofileflag != profile.Publish:
                #Gig.objects.filter(user=profile.user,Publish=oldprofileflag).update(Publish=profile.Publish)
    else:
        try:
            profile = Profile.objects.get(user__username=username)
            profile_form = ProfileForm(instance=profile)
        except Profile.DoesNotExist:
            redirect('/')

    gigs = Gig.objects.filter(user=profile.user, status=True, Publish=True).order_by('create_time')
    gigs_paginator = Paginator(gigs, settings.SEARCH_RESULTS_PER_PAGE)
    products = Product.objects.filter(user=profile.user, publish=True).order_by('create_time')
    paginator_prods = Paginator(products, settings.SEARCH_RESULTS_PER_PAGE)
    return render(request, 'profile.html', {"profile":profile, "brands": gigs_paginator.get_page("1"), "products": paginator_prods.get_page("1"), 'profile_form': profile_form,
                                            "MEDIA_URL" : settings.MEDIA_URL, "update_msg":update_msg})


#@login_required(login_url="/login")
def create_purchase(request):
        if request.method == 'POST':
            gig=None
            try:
                gig = Gig.objects.get(id = request.POST.get('gig_id'))
            except Gig.DoesNotExist:
                pass
            if gig:
                nonce = request.POST["payment_method_nonce"]
                result = braintree.Transaction.sale({
                    "amount": gig.price,
                    "payment_method_nonce": nonce
                })    
    
                if result.is_success:
                    Purchase.objects.create(gig=gig, buyer=request.user)
            else:
                nonce = request. POST["payment_method_nonce"]
                result = braintree.Transaction.sale({
                    "amount": request.POST.get('amount'),
                    "payment_method_nonce": nonce
                })    
        return HttpResponse('<script>alert("Thank you!");location.href="/";</script>')
        #return redirect('/')

@login_required(login_url="/login")
def my_sales(request):
    purchases = Purchase.objects.filter(gig__user=request.user)
    return render(request, 'my_sales.html', {"purchases": purchases})

@login_required(login_url="/login")
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'my_purchases.html', {"purchases": purchases})

def category(request, link):
    title = request.GET.get('title')
    categories = {
        "category-1": "C1",
        "category-2": "C2",
        "category-3": "C3",
        "category-4": "C4",
        "category-5": "C5",
    }
    try:
        gigs = Gig.objects.filter(category=categories[link])
        return render(request, 'home.html', {"gigs": gigs,"MEDIA_URL" : settings.MEDIA_URL, 'title': title})
    except KeyError:
        return redirect('home')


def query_brands(title, page):
    qset = Q(title__icontains=title) | Q(category__icontains=title) \
            | Q(description__icontains=title) | Q(BrandLink__icontains=title) \
            | Q(BrandCustomerServicePhone__icontains=title) | Q(BrandSearch__icontains=title) \
            | Q(BrandWhereToBuy__icontains=title) \
            | Q(BrandCaption1__icontains=title) | Q(BrandCaption2__icontains=title) \
            | Q(BrandCaption3__icontains=title) | Q(BrandCaption4__icontains=title) \
            | Q(BrandCaption5__icontains=title) | Q(BrandCaption6__icontains=title)
    gigs = Gig.objects.filter(qset, Publish=True).order_by('create_time')
    paginator = Paginator(gigs, settings.SEARCH_RESULTS_PER_PAGE)
    return paginator.get_page(page)


def query_products(title, page):
    product_qset = Q(title__icontains=title) \
            | Q(description__icontains=title) | Q(search_keywords__icontains=title) \
            | Q(caption1__icontains=title) | Q(caption2__icontains=title) \
            | Q(caption3__icontains=title) | Q(caption4__icontains=title) \
            | Q(caption5__icontains=title) | Q(caption6__icontains=title)

    products = Product.objects.filter(product_qset, publish=True).order_by('create_time')
    paginator_prods = Paginator(products, settings.SEARCH_RESULTS_PER_PAGE)
    return paginator_prods.get_page(page)



def search_show_more(request):
    
    title = request.GET.get('title')
    obj_type = request.GET.get('obj_type')
    page = request.GET.get('page')

    if title and obj_type and page:
        try:
            results = query_brands(title, page) if obj_type == "brand" else query_products(title, page)
            result_string = render_to_string('search_items_display.html', {'results': results, 'title': title})
            return JsonResponse(result_string, safe=False)
        except Exception as ex:
            return JsonResponse({'error':str(ex)})
    else:
        return JsonResponse({'error':'title, page or object type missing from url query...'})
        

def search(request):
    qset=Q()
    title = request.GET.get('title')
    page = request.GET.get('page')

    if title:
        gigs_page = query_brands(title, '1')
        prods_page = query_products(title, '1')
        return render(request, 'search.html', {"brands": gigs_page, "products": prods_page, "MEDIA_URL" : settings.MEDIA_URL, 'title': title })
    else:
        return redirect('home')


def file_save_to_media(photo,photoname='avatar'):
    if type(photo) == str:
        return photo
    fname =  photo.name
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT,photoname)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT,photoname))                 
    f = open(os.path.join(settings.MEDIA_ROOT,photoname, fname), 'wb+')
    for chunk in photo.chunks():
        f.write(chunk)
    f.close()
    return '%s%s/%s' % (settings.MEDIA_URL, photoname, fname)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        donate = request.POST.get('donate') # 'on' or None
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #for field in ['about','slogan','CompanyName','CompanyCategory',
                          #'CompanyType','CompanyLogo','CompanyLink','CompanyContactName',
                          #'CompanyContactPhone','CompanyContactEmail']:
                #setattr(user.profile,field,form.cleaned_data.get(field))
            user.profile.CompanyContactEmail = form.cleaned_data.get('CompanyContactEmail')
            user.profile.CompanyID = user.profile.id
            user.email = user.profile.CompanyContactEmail
            #user.profile.avatar = file_save_to_media(form.cleaned_data.get('avatar'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            if donate == 'on':
                return redirect('donate')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')

MAIL_HOST="smtp.handctrl.com"  
MAIL_USER="postmaster"   
MAIL_PASS="Zkwl85622611"   
MAIL_POSTFIX="handctrl.com"

def generate_token(length=32, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))

def sendmailbythread(to_list,sub,content=None):
    t = threading.Thread( target=sendmail,args=[to_list,sub,content])
    t.start()  
    
import smtplib  
from email.mime.text import MIMEText  

def sendmail(to_list,sub,content=None):
    if not content:
        content = sub
    me=u"buyusa"+"<"+MAIL_USER+"@"+MAIL_POSTFIX+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(MAIL_HOST)  
        server.login(MAIL_USER+"@"+MAIL_POSTFIX,MAIL_PASS)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close() 
        #log.error((to_list,sub))
        return True  
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        #log.error('%s %s Exception: %s' % (exc_tb.tb_lineno,sys._getframe().f_code.co_name, ex) ) 
        return False 

def resetpassword(request):
    alertmsg,email,token,password,confirm_password = ('',)*5
    ajax = request.POST.get('ajax','')
    oper = request.POST.get('oper','')
    if ajax:
        if oper == 'sendmail':
            email = request.POST.get('email','')
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
            if match == None:
                return JsonResponse({'result':False,'msg':u'Your email is not valid.'})
            token = generate_token()
            cache.set('email_email_%s' % token,email,86400)
            #sendmailbythread([email,], u'[buyusa] Reset your password',u'Your token is：%s' % (token,))
            send_mail('Welcome to BuyUSA.support - Login Info', 'Token: ' + token, 'support@buyusa.support', [email], fail_silently=False, )

            return JsonResponse({'result':True,'msg':u'Your token has sent to your email, please check your email.',})
    
    if request.method == 'POST':
        email = request.POST.get('email','').strip()
        token = request.POST.get('token','').strip()
        password = request.POST.get('password','').strip()
        confirm_password = request.POST.get('confirm_password','').strip()
        tokenemail = cache.get('email_email_%s' % token) 

        if not token and not password and not confirm_password:
            alertmsg = u'Token, password and confirmed password are required'
        else:
            if len(password)<6:
                alertmsg = 'The length of the password can not less than 6.'
            else:
                if password != confirm_password:
                    alertmsg = 'Password and confirmed password are not matched.'
                else:
                    if not tokenemail:
                        alertmsg = 'Token is wrong.'
                        token=''
        if alertmsg:
            return render(request, 'resetpassword.html', {'alertmsg': alertmsg,'email':email,'token':token,
                                                          'password':password,'confirm_password':confirm_password})
        users = User.objects.filter(profile__CompanyContactEmail=tokenemail)
        if users:
            theuser = users[0]
            theuser.set_password(password)
            theuser.save()
            cache.delete('email_email_%s' % token) 
            alertmsg = u'Reset password successfully. Please login.'
            email,token,password,confirm_password = ('',)*4
        else:
            alertmsg = u'User does not exist, please check you email address'

    return render(request, 'resetpassword.html', {'alertmsg': alertmsg, 'email':email,'token':token,
                                                  'password':password,'confirm_password':confirm_password})

def donate(request):
    #client_token = braintree.ClientToken.generate()
    years = [datetime.datetime.now().year + x for x in range(15)]
    errmsg=''
    donatevalue = request.POST.get('donatevalue','')
    cardtype = request.POST.get('cardtype','')
    cc_number = request.POST.get('cc_number','')
    cc_exp_month = request.POST.get('cc_exp_month','')
    cc_exp_year = request.POST.get('cc_exp_year','')
    cc_ccv = request.POST.get('cc_ccv','')
    holdername = request.POST.get('holdername','')
    username = ''
    if request.user.id:
        username = request.user.username
    if request.method == 'POST':
        
        # Declare your API_Key, API_SECRET and TOKEN
        API_KEY = 'y6pWAJNyJyjGv66IsVuWnklkKUPFbb0a'
        API_SECRET = '86fbae7030253af3cd15faef2a1f4b67353e41fb6799f576b5093ae52901e6f7'
        TOKEN = 'fdoa-a480ce8951daa73262734cf102641994c1e55e7cdf4c02b6'
        #API_KEY = 'RTLAWyPFO20bRXs0oXaHwIDACx8snAZ8'
        #API_SECRET = '494854913193382354b35aa4738e724da17347cea5b8377ea0675743bd41d50d'
        #TOKEN = 'fdoa-01709db6a11f49b6a77686efb5d67a0101709db6a11f49b6'  
        URL = 'https://api-cert.payeezy.com/v1/transactions'
        
        payeezy.apikey = "y6pWAJNyJyjGv66IsVuWnklkKUPFbb0a"
        payeezy.apisecret = "86fbae7030253af3cd15faef2a1f4b67353e41fb6799f576b5093ae52901e6f7"
        payeezy.token = "fdoa-cbea924f98fb80517325dfbc516883b9cbea924f98fb8051"

        
        payeezy.apikey = "A7dRIA89gemn5NydADZ2Irhq3UFjQ0qq"
        payeezy.apisecret = "5f3bfc342c1a00bf14930568504fbcded21dd725671114f17294ed2efe68695d"
        payeezy.token = "fdoa-40894fd3ea9249ef0e62343b86c219ae40894fd3ea9249ef"

        # environment - sandbox
        payeezy.url = "https://api-cert.payeezy.com/v1/transactions"
        payeezy.tokenurl = "https://api-cert.payeezy.com/v1/securitytokens"
        
        # environment - live
        #payeezy.url = "https://api.payeezy.com/v1/transactions"
        #payeezy.tokenurl = "https://api.payeezy.com/v1/securitytokens"
        
        #token = payeezy.transactions.getTokenPostCall()
        
        #pz = payeezy.http_authorization.PayeezyHTTPAuthorize(payeezy.apikey,payeezy.apisecret,payeezy.token,payeezy.url,payeezy.tokenurl)
        #pz.getTokenPostCall(token_payload)
    
        responseAuthorize =  payeezy.transactions.purchase( amount=donatevalue,
                                                             currency_code='usd',
                                                             card_type=cardtype,
                                                             cardholder_name=holdername,
                                                             card_number=cc_number,
                                                             card_expiry=cc_exp_month+cc_exp_year[-2:],
                                                             card_cvv=cc_ccv,
                                                             description='donate to buyusa'
                                                             )  
        print(responseAuthorize)
        rst = responseAuthorize.json()
        transaction_approved = None
        if rst.get('gateway_resp_code') == '00':
            transaction_approved = rst.get('transaction_status') == 'approved'
        
        if transaction_approved:
            print('Thank you for your purchase')
            d = Donate()
            d.username = username
            d.donatevalue = donatevalue
            d.cardtype = cardtype
            d.cc_number = cc_number
            d.cc_exp_date = cc_exp_month+cc_exp_year[-2:]
            d.cc_ccv = cc_ccv
            d.holdername = holdername
            d.save()
            return HttpResponse('<script>alert("Thank you for your donation.");location.href="/";</script>')
        else:
            error = rst.get('Error',{}).get('messages','')
            if not error:
                error = rst.get('message')
            if type(error) == list:
                error = ''.join([x.get('description','') for x in error])
            if not error:
                error = rst.get('faultstring')
            if not error:
                error = rst.get('fault',{}).get('faultstring','')

            print(error)
            errmsg = error
        
        
    return render(request, 'donate.html', {"years": years,"errmsg": errmsg,"donatevalue": donatevalue,"cardtype":cardtype,
                                           "cc_number":cc_number, "cc_exp_month":cc_exp_month,"cc_exp_year":cc_exp_year,
                                           "cc_ccv":cc_ccv,"holdername":holdername,"username":username,"cc_exp_year2":int(cc_exp_year or 0)})

"""
task list:
1.login/signup function (done)
2.HTML field area (done)
3.small gallery function (done)
4.edit image bug (fixed)
5.change payment to Wells Fargo
6.membership function
7.receiving data from a 3rd party provider (need 3rd party info)
membership function 
I need a scratch.( draft)
"""

def add_brand_import_data(impdata, user):
    # Update or add brand data
    brands = impdata.brandnames.split('*')
    for b in brands:
        brand_title = b.strip()
        found_gigs = Gig.objects.filter(title=brand_title)
        if len(found_gigs) <= 0:
            gig = Gig()
            gig.category = 'C1'
            gig.title = brand_title
            gig.user = user
            gig.CompanyID = user.profile.id
            gig.save()
            gig.BrandID = gig.id
            gig.save(update_fields=['BrandID',])
        

            
        #email = impdata.email
        #site = get_current_site(request)
        #msg_plain = render_to_string('registration/firstlogin_email.txt', {'username': user.username, "login_link": user.profile.LoginLink, "site": site})
        #msg_html = render_to_string('registration/firstlogin_email.html', {'username': user.username, "login_link": user.profile.LoginLink, "site": site})
        #send_mail('BuyUSA.Support Account Setup', msg_plain, 'support@buyusa.support', [email],html_message=msg_html)
        #sendmailbythread([email,], u'[buyusa] Please do your first login and change password',
        #                 u'Please do your first login and change password：%s/firstlogin/%s' % (settings.SITE_URL,user.profile.LoginLink,))

def process_importdata(impdata, request):
    importedid = '%s-%s' % (impdata.ImportID,impdata.companyid)
    #haveprofile = Profile.objects.filter(ImportedCompanyID=importedid)
    user_profile = Profile.objects.filter(CompanyContactEmail=impdata.email)
    if len(user_profile) <= 0: # If no profile for this company found then create a new user
        raw_password = u'%s%s' % (impdata.company.replace(' ','') ,impdata.companyid)
        user = User()
        user.username = generate_token()
        user.set_password(raw_password)
        user.email = impdata.email
        user.save()
        user.refresh_from_db()
        user.profile.CompanyContactEmail = user.email 
        user.profile.CompanyID = user.profile.id
        user.username = 'user%s' % (user.profile.id)
        user.profile.LoginLink = user.username    
        #user.profile.about = impdata.phone
        user.profile.CompanyName = impdata.company
        user.profile.CompanyLink = impdata.url
        user.profile.CompanyContactName = '%s %s' % (impdata.firstname, impdata.lastname)
        user.profile.CompanyContactPhone = impdata.phone
        user.profile.ImportedCompanyID = importedid
        user.profile.profile_updated = False
        user.save()        
        add_brand_import_data(impdata, user)
    else:
        user_profile = user_profile[0]
        if user_profile.CompanyName != impdata.company or \
        user_profile.CompanyLink !=  impdata.url or \
        user_profile.CompanyContactName != '%s %s' % (impdata.firstname, impdata.lastname) or \
        user_profile.CompanyContactPhone != impdata.phone:
            user_profile.profile_updated = True

        user_profile.CompanyName = impdata.company
        user_profile.CompanyLink = impdata.url
        user_profile.CompanyContactName = '%s %s' % (impdata.firstname, impdata.lastname)
        user_profile.CompanyContactPhone = impdata.phone
        user_profile.ImportedCompanyID = importedid
        user_profile.save()
        add_brand_import_data(impdata, user_profile.user)



@login_required(login_url="/login")
@transaction.atomic
def importdata(request):
    #site = get_current_site(request)
    #ink = "mEvzv86u8K5pxxDGn1llPy0LCGqmAscv"
    #email = "batousai_de@hotmail.com"
    #msg_plain = render_to_string('registration/firstlogin_email.txt', {'username': request.user.username, "login_link": link, "site": site})
    #msg_html = render_to_string('registration/firstlogin_email.html', {'username': request.user.username, "login_link": link, "site": site})
    #send_mail('BuyUSA.Support Account Setup', msg_plain, 'support@buyusa.support', [email],html_message=msg_html)

    form = None
    errmsg = ''
    errlist=[]
    sucess=0
    try:
        if request.method == 'POST':
            form = ImportDataForm(request.POST,request.FILES)
            if form.is_valid():
                res = ImportData.objects.filter().aggregate(max_id=Max('ImportID'))
                importid = res.get('max_id')
                if importid == None:
                    importid = 1
                else:
                    importid += 1                
                file_ = form.cleaned_data['file']
                bk = xlrd.open_workbook(file_contents=file_.read())
                #bk = xlrd.open_workbook(file_contents=file_.file.getvalue())
                if len(bk.sheets()) > 0:
                    col_set={
                        'COMPANYID':{'col':None,'cache':{},'errcache':[],'required':True},
                        'COMPANY':{'col':None,'cache':{},'errcache':[],'required':True},
                        'EMPLOYEES':{'col':None,'cache':{},'errcache':[],'required':True},
                        'PHONE':{'col':None,'cache':{},'errcache':[],'required':True},
                        'URL':{'col':None,'cache':{},'errcache':[],'required':True},
                        'EMAIL':{'col':None,'cache':{},'errcache':[],'required':True},
                        'PSIC':{'col':None,'cache':{},'errcache':[],'required':True},
                        'BRANDNAMES':{'col':None,'cache':{},'errcache':[],'required':True},
                        'SALUTATION':{'col':None,'cache':{},'errcache':[],'required':True},
                        'FIRSTNAME':{'col':None,'cache':{},'errcache':[],'required':True},
                        'MIDDLENAME':{'col':None,'cache':{},'errcache':[],'required':True},
                        'LASTNAME':{'col':None,'cache':{},'errcache':[],'required':True},
                        'SUFFIX':{'col':None,'cache':{},'errcache':[],'required':True},
                        'GENDER':{'col':None,'cache':{},'errcache':[],'required':True},
                        'TITLEEXT':{'col':None,'cache':{},'errcache':[],'required':True},
                    }
                    sh = bk.sheets()[0]
                    for i in range(sh.nrows):
                        if i == 0:                        
                            for j in range(sh.ncols):
                                cell_data = str(sh.row(i)[j].value)
                                logger.info(cell_data)
                                v = cell_data.strip().upper()
                                xxx = [key for key, value in col_set.items() if v==key]
                                if len(xxx) > 0:
                                    col_set[xxx[0]]['col'] = j
                            for k,v in col_set.items():                                
                                if v['required'] and v['col'] == None:
                                    err= u'Error: no  “%s” column' % k
                                    logger.info(cell_data)
                                    raise Exception(err)
                                    
                            continue
                        try:
                            tempval = col_set['COMPANYID']['col']
                            compid = sh.row(i)[tempval].value
                            comp = sh.row(i)[col_set['COMPANY']['col']].value
                            # impdata = ImportData.objects.filter(companyid=compid, company=comp)
                            # impdata = ImportData() if len(impdata) <= 0 else impdata[0]
                            impdata = ImportData()
                            impdata.companyid=sh.row(i)[col_set['COMPANYID']['col']].value
                            impdata.company=sh.row(i)[col_set['COMPANY']['col']].value
                            impdata.employees=sh.row(i)[col_set['EMPLOYEES']['col']].value
                            impdata.phone=sh.row(i)[col_set['PHONE']['col']].value
                            impdata.url=sh.row(i)[col_set['URL']['col']].value
                            impdata.email=sh.row(i)[col_set['EMAIL']['col']].value
                            impdata.psic=sh.row(i)[col_set['PSIC']['col']].value
                            impdata.brandnames=sh.row(i)[col_set['BRANDNAMES']['col']].value
                            impdata.salutation=sh.row(i)[col_set['SALUTATION']['col']].value
                            impdata.firstname=sh.row(i)[col_set['FIRSTNAME']['col']].value
                            impdata.middlename=sh.row(i)[col_set['MIDDLENAME']['col']].value
                            impdata.lastname=sh.row(i)[col_set['LASTNAME']['col']].value
                            impdata.suffix=sh.row(i)[col_set['SUFFIX']['col']].value
                            impdata.gender=sh.row(i)[col_set['GENDER']['col']].value
                            impdata.titleext=sh.row(i)[col_set['TITLEEXT']['col']].value
                            impdata.ImportSource=request.POST.get('source','')
                            impdata.ImportID=importid
                            process_importdata(impdata, request)
                            impdata.save()
                            sucess+=1
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            err = '%s Exception. %s' % (exc_tb.tb_lineno, e)
                            logger.exception(err)
                            errlist.append((err,u'line %s,%s' % ((i+1),','.join([str(sh.row(i)[col_set[x]['col']].value).strip() for x in col_set.keys()]))))

                        
        else:
            form = ImportDataForm() 
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        #log.error('%s %s Exception: %s' % (exc_tb.tb_lineno,sys._getframe().f_code.co_name, ex) ) 
        errmsg = '%s Exception: %s' % (exc_tb.tb_lineno,ex)
        logger.exception(errmsg)
    return render(request, 'importdata.html',{'form':form,'errmsg':errmsg,'errlist':errlist, 'sucess':sucess,'fail':len(errlist)})


def firstlogin(request, token):
    haveone = Profile.objects.filter(LoginLink=token,flag=False)
    profile=None
    alertmsg=''
    if haveone:
        profile = haveone[0]
    if request.method == 'POST':
        password = request.POST.get('password','').strip()
        confirm_password = request.POST.get('confirm_password','').strip()

        if not password and not confirm_password:
            alertmsg = u'Password and confirmed password are required.'
        else:
            if len(password)<6:
                alertmsg = 'The length of the password can not be less than 6.'
            else:
                if password != confirm_password:
                    alertmsg = 'Password and confirmed password do not match.'
        if alertmsg:
            return render(request, 'firstlogin.html', {'alertmsg': alertmsg,'profile':profile,
                                                       'password':password,'confirm_password':confirm_password})
        profile.user.set_password(password)
        profile.flag=True
        profile.user.save()
        login(request, profile.user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    return render(request, 'firstlogin.html', {'profile':profile})


def export_import_data(request):
    # data = download_csv(request, ImportData.objects.all())
    if not request.user.is_staff:
        raise PermissionDenied
    queryset = ImportData.objects.all()
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=buyusa_profile_export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field, None) for field in field_names])
    return response

def export_profile_data(request):
    # data = download_csv(request, ImportData.objects.all())
    if not request.user.is_staff:
        raise PermissionDenied
    queryset = Profile.objects.all()
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=buyusa_export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        row = []
        for field in field_names:
            attr = getattr(obj, field, None)
            if field == "LoginLink":
                attr = get_current_site(request).domain + "/firstlogin/" + attr
            row.append(attr)
        writer.writerow(row)

    return response

@login_required(login_url="/login")
def exportdata(request):
    if not request.user.is_staff:
        raise PermissionDenied        
    ex_type = request.GET.get('type')
    if ex_type == "profile":
        return export_profile_data(request)
    elif ex_type == "import":
        return export_import_data(request)
    else:
        return render(request, 'exportdata.html')
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

from .models import Gig, Profile, Purchase, Review, Donate, ImportData, Product
from .forms import GigForm, SignUpForm, ProfileForm, ImportDataForm, ProductForm

import os,random, threading, re, datetime, sys
import xlrd
import braintree
import csv
braintree.Configuration.configure(braintree.Environment.Sandbox, merchant_id="7968vwncy9mkmwv6", public_key="5k6r27pfddhdx4wb", private_key="3a6cfa52f4b1d37475125a7a5b5117eb")

import payeezy
import logging
logger = logging.getLogger("buyusa")


def product_detail(request, id):
    '''
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], gig_id=id, user=request.user )
    '''
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        logger.exception("Error Product DOES NOT EXIST...")
        return redirect('/')
    '''
    if request.user.is_anonymous or \
        Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
        Review.objects.filter(gig=gig, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0
    reviews = Review.objects.filter(gig=gig)
    
    client_token = braintree.ClientToken.generate()
    return render(request, 'product_detail.html', {"show_post_review": show_post_review, "reviews":reviews, "product": product, 
                                               "client_token": client_token , "MEDIA_URL" : settings.MEDIA_URL, })
    '''
    return render(request, 'product_detail.html', {"product": product, "MEDIA_URL" : settings.MEDIA_URL })

@login_required(login_url="/login")
def create_product(request):
    
    if request.method == 'POST':        
        form = ProductForm(request.POST, request.FILES, user_obj=request.user)        
        try:
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect('my_gigs')
        except Exception as ex:
            try:
                raise TypeError("Again !?!")
            except:
                pass
            import traceback
            traceback.print_exc()

    else:
        form = ProductForm(user_obj=request.user)

    errors = form.errors
    errors_non = form.non_field_errors
    
    return render(request, 'create_product.html', {'product_form': form, 'product_errors':errors, 'errors_non':errors_non})



@login_required(login_url="/login")
def edit_product(request, id):
    try:
        product = Product.objects.get(id=id)
        if not product.brand.user == request.user:
            raise PermissionDenied
            
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product, user_obj=request.user, edit=True)            
            if product_form.is_valid():
                product.save()
                return redirect('my_gigs')
        else:
            product_form = ProductForm(instance=product, user_obj=request.user, edit=True)

        errors = product_form.errors
        errors_non = product_form.non_field_errors            
        product_form.helper.form_action = "/edit_product/" + str(product.id) + "/"
        return render(request, 'edit_product.html', {"product": product, "product_form":product_form, 'product_errors':errors, 'errors_non':errors_non})
    except Product.DoesNotExist:
        return redirect('/')

def my_products(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})


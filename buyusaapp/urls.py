from django.conf.urls import url
from buyusaapp import views, views_product
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.home, name='home'),    
    url(r'^terms/$', TemplateView.as_view(template_name="terms.html", content_type="text/html"), name="terms"),
    url(r'^faqs/$', TemplateView.as_view(template_name="faqs.html", content_type="text/html"), name="faqs"),
    url(r'^contact/$', TemplateView.as_view(template_name="contact.html", content_type="text/html"), name="contact"),
    url(r'^coming_soon/$', TemplateView.as_view(template_name="coming_soon.html", content_type="text/html"), name="coming_soon"),
    url(r'^videos/$', TemplateView.as_view(template_name="videos.html", content_type="text/html"), name="videos"),
    url(r'^disclaimer/$', TemplateView.as_view(template_name="disclaimer.html", content_type="text/html"), name="disclaimer"),
    url(r'^gigs/(?P<id>[0-9]+)/$', views.gig_detail, name='gig_detail'),
    url(r'^products/(?P<id>[0-9]+)/$', views_product.product_detail, name='product_detail'),
    url(r'^my_gigs/$', views.my_gigs, name='my_gigs'),
    url(r'^create_gig/$', views.create_gig, name='create_gig'),
    url(r'^edit_gig/(?P<id>[0-9]+)/$', views.edit_gig, name='edit_gig'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^checkout/$', views.create_purchase, name='create_purchase'),
    url(r'^my_sales/$', views.my_sales, name='my_sales'),
    url(r'^my_purchases/$', views.my_purchases, name='my_purchases'),
    url(r'^category/(?P<link>[\w|-]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_show_more/$', views.search_show_more, name='search_show_more'),

    url(r'^create_product/$', views_product.create_product, name='create_product'),
    url(r'^edit_product/(?P<id>[0-9]+)/$', views_product.edit_product, name='edit_product'),
    url(r'^my_products/$', views_product.my_products, name='my_products'),
    
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    #url(r'^signup/$', views.signup, name='signup'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^contribute/$', views.donate, name='donate'),
    
    url(r'^importdata/$', views.importdata, name='importdata'),
    url(r'^exportdata$', views.exportdata, name='exportdata'),    
    url(r'^firstlogin/(?P<token>[\w|-]+)/$', views.firstlogin, name='firstlogin'),    
]
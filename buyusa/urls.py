"""buyusa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^social/', include('social.apps.django_app.urls', namespace = 'social')),
    url('^auth/', include(('django.contrib.auth.urls','django.contrib.auth'), namespace = 'auth')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url('', include('buyusaapp.urls'))
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

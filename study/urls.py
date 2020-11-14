from django.contrib import admin
from django.urls import path , re_path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    re_path("^$", views.index, name='index'),
    path("layout/" , views.layout , name='layout'),
    path("accounts/", include('accounts.urls')),
    path("accounts/", include("allauth.urls")),

    path("post/" , include("post.urls" , namespace="post")),
    path("" , lambda r: redirect("post:post_list") , name='root'), 

    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)
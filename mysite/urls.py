from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # localhost:8000/admin/
    path('myapp/', include('myapp.urls')), # localhost:8000/myapp/
    path('users/', include('users.urls')), # localhost:8000/usrs/
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
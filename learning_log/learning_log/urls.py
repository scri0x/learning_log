from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learn_log.urls')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
]

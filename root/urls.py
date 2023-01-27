from django.contrib import admin
from django.urls import path, include

from apps.views import mainView
urlpatterns = [
    # path('', mainView),
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from stocks import views as stocks_views

urlpatterns = [
    path('', stocks_views.home, name='home'),

    path('logout/', stocks_views.user_logout, name='logout'),

    path('parse/', stocks_views.parse, name='parse'),

    path('share/', stocks_views.edit_share, name='share/add'),
    path('share/<str:share_id>/', stocks_views.edit_share, name='share/edit'),

    path('admin/', admin.site.urls),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

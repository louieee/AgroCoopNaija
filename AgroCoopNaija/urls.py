from django.contrib import admin
from django.urls import path, include
from .views import handler404, handler500
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import home, about
from django.conf.urls import handler404, handler500

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('about/', about, name='about'),
                  path('account/', include('core.urls')),
                  path('cooperative/', include('cooperative.urls')),
                  path('post/', include('post.urls')),
                  path('partner/', include('partner.urls')),
                  path(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404

handler500 = handler500

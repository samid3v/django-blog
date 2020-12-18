from django.contrib import admin
from django.urls import include, path
import home
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('logout',views.logout_user, name='logout'),
    path('login',views.login_user, name='login'),
    path('profile/<int:id>/<slug:slug>',views.user_profile, name='profile'),
    path('register',views.register_user, name='register'),
    path('post/', include('home.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

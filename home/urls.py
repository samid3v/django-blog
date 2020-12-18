from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create_post', views.post, name='create_post'),
    path('search_post', views.search_post, name='search'),
    path('category/<int:id>', views.category_view, name='category' ),
    path('view_post/<int:id>/<slug:slug>', views.view_post, name='view_post' ),
    path('delete_post/<int:id>/<slug:slug>', views.delete_post, name='delete_post' ),
    path('update_post/<int:id>/<slug:slug>', views.update_post, name='update_post' )
]
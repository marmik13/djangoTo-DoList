from django.urls import path
from todo_list import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('delete/<int:list_id>', views.delete, name='delete'),
    path('cross_off/<int:list_id>', views.cross_off, name='cross_off'),
    path('uncross/<int:list_id>', views.uncross, name='uncross'),
    path('edit/<int:list_id>', views.edit, name='edit'),
]

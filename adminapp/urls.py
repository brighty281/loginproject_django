from django.urls import path
from . import views

urlpatterns=[
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('user_list/',views.user_list,name='user_list'),

    # path('edit_user/<int:uid>/',views.edit_user,name='edit_user'),
    path('delete/<int:uid>/',views.delete_user,name='delete'),
    path('edit_user/<int:uid>/', views.edit_user, name='edit_user'),
    path('search_user/', views.search_user, name='search_user'),
    path('add_user/', views.add_user, name='add_user')

]
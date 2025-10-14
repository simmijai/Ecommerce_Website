from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='dashboard'),
     path('login/', views.admin_login_view, name='admin-login'),
    path('logout/', views.admin_logout_view, name='admin-logout'),
        path('edit-stock/', views.edit_stock_view, name='edit-stock'),  # ← add this
path('users/', views.users_list_view, name='users-list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user-detail'),
        path('users/<int:user_id>/edit/', views.user_edit_view, name='user-edit'),  # 👈 add this

]

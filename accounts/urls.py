from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('money-tracker/', views.money_tracker_view, name='money-tracker'),
    path('weather/', views.weather_view, name='weather'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('addBank/', views.add_bank, name='add_bank'),
    path('account/<int:id>', views.view_account, name='view_account'),
    path('transaction/<int:id>', views.add_transaction, name='add_transaction'),
    path('money-tracker-bal/<int:id>/<str:newbal>', views.money_tracker_bal, name='money-tracker-bal'),
    path('delete-account/<int:id>', views.delete_account, name='delete_account')
]

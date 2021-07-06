from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.FirstView.as_view(), name="first_view"),
    path('home/', views.HomeView.as_view(), name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('inventory/', views.IngredientsList.as_view(), name="inventory"),
    path('inventory/delete_ingredient/<pk>', views.IngredientsDelete.as_view(), name="ingredient_delete"),
    path('inventory/update_ingredient/<pk>', views.IngredientUpdate.as_view(), name="ingredient_update"),
    path('inventory/add_ingredient', views.IngredientsAdd.as_view(), name="ingredient_add"),
    path('menu/', views.MenuList.as_view(), name="menu_list"),
    path('menu/delete_item/<pk>', views.MenuDelete.as_view(), name="menu_delete"),
    path('menu/add_item', views.MenuAdd.as_view(), name="menu_add"),
    path('menu/add_required_ingredients/', views.RequiredIngredientsAdd.as_view(), name="add_req_ingredients"),
    path('purchase_log/', views.Purchase_Log.as_view(), name="purchase_log"),
    path('purchase/delete_item/<pk>', views.PurchaseDelete.as_view(), name="purchase_delete"),
    path('purchase/add_item', views.PurchaseAdd.as_view(), name="purchase_add"),
    path('report/', views.ReportView.as_view(), name="report")
]
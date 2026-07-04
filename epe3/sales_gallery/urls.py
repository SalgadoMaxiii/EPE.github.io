from django.contrib import admin
from django.urls import path
from gallery import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("register/", views.register_view, name="register"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("sales/new/", views.new_sale, name="new_sale"),
    path("sales/", views.sales_list, name="sales_list"),
]

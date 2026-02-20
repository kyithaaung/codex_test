from django.urls import path

from . import views

urlpatterns = [
    path("internal/login/", views.internal_login, name="internal-login"),
    path("internal/home/", views.internal_home, name="internal-home"),
    path("internal/customers/create/", views.create_customer, name="create-customer"),
    path("customer/login/", views.customer_login, name="customer-login"),
    path("customer/home/", views.customer_home, name="customer-home"),
    path("logout/", views.logout, name="logout"),
]

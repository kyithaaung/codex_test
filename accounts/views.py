from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomerCreateForm, LoginForm
from .models import Customer, InternalUser


SESSION_INTERNAL = "internal_user_id"
SESSION_CUSTOMER = "customer_user_id"


def _internal_logged_in(request: HttpRequest) -> bool:
    return bool(request.session.get(SESSION_INTERNAL))


def _customer_logged_in(request: HttpRequest) -> bool:
    return bool(request.session.get(SESSION_CUSTOMER))


def internal_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = InternalUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            request.session[SESSION_INTERNAL] = user.id
            request.session.pop(SESSION_CUSTOMER, None)
            return redirect("internal-home")
        error = "Invalid internal user credentials."
    return render(request, "internal/login.html", {"form": form, "error": error})


def customer_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)
    error = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        customer = Customer.objects.filter(username=username).first()
        if customer and customer.check_password(password):
            request.session[SESSION_CUSTOMER] = customer.id
            request.session.pop(SESSION_INTERNAL, None)
            return redirect("customer-home")
        error = "Invalid customer credentials."
    return render(request, "customer/login.html", {"form": form, "error": error})


def internal_home(request: HttpRequest) -> HttpResponse:
    if not _internal_logged_in(request):
        return redirect("internal-login")
    return render(request, "internal/home.html")


def customer_home(request: HttpRequest) -> HttpResponse:
    if not _customer_logged_in(request):
        return redirect("customer-login")
    return render(request, "customer/home.html")


def create_customer(request: HttpRequest) -> HttpResponse:
    if not _internal_logged_in(request):
        return redirect("internal-login")

    form = CustomerCreateForm(request.POST or None)
    message = ""
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        if Customer.objects.filter(username=username).exists():
            message = "Customer username already exists."
        else:
            internal_user = InternalUser.objects.filter(
                id=request.session[SESSION_INTERNAL]
            ).first()
            customer = Customer(username=username, created_by=internal_user)
            customer.set_password(password)
            customer.save()
            message = "Customer created successfully."
            form = CustomerCreateForm()

    return render(
        request,
        "internal/create_customer.html",
        {"form": form, "message": message},
    )


def logout(request: HttpRequest) -> HttpResponse:
    request.session.pop(SESSION_INTERNAL, None)
    request.session.pop(SESSION_CUSTOMER, None)
    return redirect("internal-login")

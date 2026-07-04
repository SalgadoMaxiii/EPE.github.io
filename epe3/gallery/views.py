from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from .models import Sale
from .forms import SaleForm


def home(request):
    return render(request, "home.html")


def custom_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Inicio de sesión correcto")
            return redirect("dashboard")
        messages.error(request, "Correo o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe")
        else:
            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(f"/activate/{uid}/{token}/")
            try:
                send_mail(
                    "Activa tu cuenta",
                    f"Haz clic en el siguiente enlace para activar tu cuenta: {activation_link}",
                    "noreply@example.com",
                    [email],
                    fail_silently=False,
                )
            except Exception as exc:
                print(f"No se pudo enviar el correo de activación: {exc}")

            print(f"Enlace de activación: {activation_link}")
            messages.success(request, f"Activa tu cuenta. Revisa tu correo o usa este enlace: {activation_link}")
            return redirect("login")
    return render(request, "register.html")


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Cuenta activada correctamente")
        return redirect("login")
    messages.error(request, "El enlace de activación es inválido")
    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")
            try:
                send_mail(
                    "Recupera tu contraseña",
                    f"Haz clic en el siguiente enlace para recuperar tu contraseña: {reset_link}",
                    "noreply@example.com",
                    [email],
                    fail_silently=False,
                )
            except Exception as exc:
                print(f"No se pudo enviar el correo de recuperación: {exc}")
            print(f"Enlace de recuperación: {reset_link}")
            messages.success(request, f"Si no llega el correo, usa este enlace para recuperar tu contraseña: {reset_link}")
        else:
            messages.error(request, "No existe un usuario con ese correo")
        return redirect("login")
    return render(request, "forgot_password.html")


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if request.method == "POST" and user is not None and default_token_generator.check_token(user, token):
        password = request.POST.get("password")
        user.set_password(password)
        user.save()
        messages.success(request, "Contraseña actualizada correctamente")
        return redirect("login")
    return render(request, "reset_password.html", {"validlink": user is not None})


@login_required
def dashboard(request):
    sales = Sale.objects.filter(user=request.user).order_by("-sale_date")
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    total_sales = sales.aggregate(total=Sum("amount"))["total"] or 0
    today_sales = sales.filter(sale_date=today).aggregate(total=Sum("amount"))["total"] or 0
    month_sales = sales.filter(sale_date__gte=start_of_month, sale_date__lte=today).aggregate(total=Sum("amount"))["total"] or 0
    year_sales = sales.filter(sale_date__gte=start_of_year, sale_date__lte=today).aggregate(total=Sum("amount"))["total"] or 0

    chart_data = list(
        sales.annotate(day=TruncDay("sale_date")).values("day").annotate(total=Sum("amount")).order_by("day")
    )
    return render(
        request,
        "dashboard.html",
        {
            "sales": sales[:5],
            "total_sales": total_sales,
            "today_sales": today_sales,
            "month_sales": month_sales,
            "year_sales": year_sales,
            "chart_data": chart_data,
        },
    )


@login_required
def new_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            messages.success(request, "Venta registrada correctamente")
            return redirect("sales_list")
    else:
        form = SaleForm()
    return render(request, "new_sale.html", {"form": form})


@login_required
def sales_list(request):
    sales = Sale.objects.filter(user=request.user).order_by("-sale_date")
    return render(request, "sales_list.html", {"sales": sales})

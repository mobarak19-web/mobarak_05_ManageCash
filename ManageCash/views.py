from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import CustomUser, AddCash, Expense
from .forms import (
    RegistrationForm,
    LoginForm,
    ChangePasswordForm,
    AddCashForm,
    ExpenseForm,
)


# =========================
# Registration View
# =========================
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Registration successful! You can now log in.'
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {
        'page': 'User Registration',
        'form': form,
    })


# =========================
# Login View
# =========================
def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            messages.success(
                request,
                f'Welcome, {user.username}!'
            )
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'page': 'User Login',
        'form': form,
    })


# =========================
# Logout View
# =========================
@login_required(login_url='login')
def logout(request):
    auth_logout(request)

    messages.success(request, 'Logout successful!')
    return redirect('login')


# =========================
# Change Password View
# =========================
@login_required(login_url='login')
def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            form.save()

            # Update session after password change
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)

            messages.success(
                request,
                'Password updated successfully!'
            )
            return redirect('dashboard')
    else:
        form = ChangePasswordForm(request.user)

    return render(request, 'change_pass.html', {
        'page': 'Change Password',
        'form': form,
    })


# =========================
# Dashboard View
# =========================
@login_required(login_url='login')
def dashboard(request):
    user_income = AddCash.objects.filter(user=request.user)
    user_expenses = Expense.objects.filter(user=request.user)

    total_income = (
        user_income.aggregate(total=Sum('amount'))['total'] or 0
    )

    total_expense = (
        user_expenses.aggregate(total=Sum('amount'))['total'] or 0
    )

    net_balance = total_income - total_expense

    context = {
        'page': 'Dashboard',
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'incomes': user_income.order_by('-datetime')[:5],
        'expenses': user_expenses.order_by('-datetime')[:5],
    }

    return render(request, 'dashboard.html', context)


# =========================
# Add Cash View
# =========================
@login_required(login_url='login')
def addcash(request):
    if request.method == 'POST':
        form = AddCashForm(request.POST)

        if form.is_valid():
            cash = form.save(commit=False)
            cash.user = request.user
            cash.save()

            messages.success(
                request,
                'Income/Cash added successfully!'
            )
            return redirect('dashboard')
    else:
        form = AddCashForm()

    return render(request, 'addcash.html', {
        'page': 'Add Cash',
        'title': 'Add Cash / Income',
        'form': form,
    })


# =========================
# Add Expense View
# =========================
@login_required(login_url='login')
def addexpense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            messages.success(
                request,
                'Expense added successfully!'
            )
            return redirect('dashboard')

    else:
        form = ExpenseForm()

    return render(request, 'addexpense.html', {
        'page': 'Add Expense',
        'title': 'Add Expense',
        'form': form,
    })
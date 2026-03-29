from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import LoginForm, WithdrawalForm
from .models import Account, Transaction

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')[:5]
    return render(request, 'accounts/dashboard.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
def balance(request):
    account = get_object_or_404(Account, user=request.user)
    return render(request, 'accounts/balance.html', {'account': account})

@login_required
def withdraw(request):
    account = get_object_or_404(Account, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            if amount > account.balance:
                messages.error(request, 'Insufficient funds.')
            else:
                # Use database transaction to ensure data consistency
                with transaction.atomic():
                    # Update account balance
                    account.balance -= amount
                    account.save()
                    
                    # Create transaction record
                    Transaction.objects.create(
                        account=account,
                        transaction_type='withdrawal',
                        amount=amount,
                        description='Cash withdrawal'
                    )
                
                messages.success(request, f'Successfully withdrew ${amount:.2f}')
                return redirect('dashboard')
    else:
        form = WithdrawalForm()
    
    return render(request, 'accounts/withdraw.html', {
        'form': form,
        'account': account
    })
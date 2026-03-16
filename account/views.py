from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, AddressForm
from .models import Profile, Address


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('account:profile')
    else:
        form = LoginForm(request)
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('products:home')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрацію завершено! Ласкаво просимо до Крамниці!')
            return redirect('products:home')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    # Ensure address object exists so forms have an instance
    if profile.address is None:
        address = Address.objects.create(
            profile=profile, street='', city=''
        )
        profile.address = address
        profile.save()
    else:
        address = profile.address

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=address)
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user_form.save()
            profile_form.save()
            address_form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('account:profile')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        address_form = AddressForm(instance=address)

    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
    })


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Ваш акаунт видалено.')
        return redirect('products:home')
    return render(request, 'account/delete_account.html')
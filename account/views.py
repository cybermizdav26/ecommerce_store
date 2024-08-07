from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView

from account.forms import SignUpForm, UserUpdateProfileForm
from account.tasks import send_email
from account.utils import generate_code

User = get_user_model()


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email = user.email
            code = generate_code()
            cache.set(f"{user.pk}", code, timeout=180)
            print(cache.get(f"{user.pk}"))
            redirect_url = f"http://127.0.0.1:8000/account/verify-code?code={code}&user_id={user.pk}"
            send_email.delay(email, code, redirect_url)
            messages.success(request, 'Siz ruyxatdan o`tdingiz')
            return redirect('account:login')
        messages.warning(request, 'qayta urinib kuring')

    form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'account/register.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, "User not found")
            return render(request, 'account/login.html')
        login(request, user)
        messages.info(request, 'Login successfull!')
        return redirect('product:home')
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have logout successfully!')
    return redirect(reverse('account:login'))


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo')

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'account/profile_update.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_code(request):
    code = request.GET.get('code')
    user_id = request.GET.get('user_id')
    if not code:
        return redirect('account:register')
    if not user_id:
        return redirect('account:register')
    user = User.objects.get(pk=user_id)
    code_cache = cache.get(user_id)
    print(code_cache, 'cache')
    if code_cache is not None and code == code_cache:
        user.is_active = True
        user.save()
        return redirect('account:login')
    return redirect('account:register')

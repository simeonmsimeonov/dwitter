from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import login
from web.forms import RegistrationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignUpView(views.CreateView):
    form_class = RegistrationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error('password', e)
                return render(self.request, self.template_name, {'form': form})
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(self.request, user)
            result = super().form_valid(form)
            return result
        else:
            return form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(auth_views.LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('dashboard')

class UserLogoutView(auth_views.LogoutView):
    success_url = reverse_lazy('login')

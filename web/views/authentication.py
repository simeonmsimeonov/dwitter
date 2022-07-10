from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import login
from web.forms import RegistrationForm
from django.contrib.auth import views as auth_views 

class SignUpView(views.CreateView):
        form_class = RegistrationForm
        template_name = 'authentication/signup.html'
        success_url = reverse_lazy('dashboard')
        
        def form_valid(self, form):
            result = super().form_valid(form)
            if form.is_valid():
                login(self.request, self.object)
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

   def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(auth_views.LogoutView):
    success_url = reverse_lazy('login')


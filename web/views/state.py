from multiprocessing.dummy import current_process
from django.urls import reverse_lazy
from web.models import Dweet, Profile, User
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect, render


class StateDeleteView(DeleteView):
    model = Dweet
    success_url = reverse_lazy("dashboard")
    template_name = "dwitter/dweet_confirm_delete.html"

    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        elif not request.user.id == pk:
            return redirect('dashboard')
    
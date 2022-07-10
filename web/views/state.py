from django.urls import reverse_lazy
from web.models import Dweet, User
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect


class StateDeleteView(DeleteView):
    model = Dweet
    success_url = reverse_lazy("dashboard")
    template_name = "statter/dweet_confirm_delete.html"

    def dispatch(self, request, pk):
        current_dweet = Dweet.objects.filter(pk=pk)
        if not request.user.is_authenticated:
            return redirect('login')
        elif not current_dweet[0].user.id == self.request.user.id:
            return redirect('dashboard')
        return super().dispatch(request)
    
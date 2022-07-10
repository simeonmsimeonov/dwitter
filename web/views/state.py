from django.urls import reverse_lazy
from web.models import Dweet
from django.views.generic.edit import DeleteView


class DweetDeleteView(DeleteView):
    model = Dweet
    success_url = reverse_lazy("dashboard")
    template_name = "dwitter/dweet_confirm_delete.html"
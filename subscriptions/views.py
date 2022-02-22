from django.views.generic import CreateView
from .models import Subscriptions
from .forms import SubscriptionsForm


class SubscriptionsView(CreateView):
    model = Subscriptions
    form_class = SubscriptionsForm
    success_url = '/'



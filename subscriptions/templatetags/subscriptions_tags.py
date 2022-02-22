from atexit import register
from django import template
from subscriptions.forms import SubscriptionsForm

register = template.Library()


@register.inclusion_tag('subscriptions/tags/form.html')
def subscriptions_form():
    return{'subscriptions_form': SubscriptionsForm()}
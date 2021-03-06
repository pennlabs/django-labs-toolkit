from django.urls import path

from pennlabs.options.views import OptionListView


app_name = "options"

urlpatterns = [
    path("", OptionListView.as_view(), name="option-list"),
]

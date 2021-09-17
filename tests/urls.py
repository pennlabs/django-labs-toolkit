from django.urls import include, path


urlpatterns = [
    path("", include("pennlabs.options.urls", namespace="django-labs-toolkit"))
]

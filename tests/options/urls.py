from django.urls import include, path


urlpatterns = [
    path("options/", include("options.urls", namespace="options")),
]

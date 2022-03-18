from django.urls import include, path


urlpatterns = [
    path("options/", include("pennlabs.options.urls", namespace="options")),
    path("shortener/", include("pennlabs.shortener.urls", namespace="shortener")),
    path("email/", include("pennlabs.emailtools.urls", namespace="email_tools"))
]

from django.urls import include, path


urlpatterns = [
    path("/options", include("pennlabs.options.urls", namespace="options"))
]

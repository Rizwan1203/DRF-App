from django.urls import path

from .views import MeView, ObtainTokenView, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("me/", MeView.as_view(), name="user-me"),
    path("token-create/", ObtainTokenView.as_view(), name="create-token"),
]

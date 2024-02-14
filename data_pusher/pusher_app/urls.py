# Standard imports here:

# Third party imports here:
from django.urls import path
from rest_framework.routers import DefaultRouter

# Local imports here:
from .views import AccountViewSet, DestinationViewSet, TriggerView

router = DefaultRouter()

router.register(r"account", AccountViewSet, basename="account")
router.register(r"destination", DestinationViewSet, basename="destination")

urlpatterns = router.urls
urlpatterns += [
    path("server/incoming_data/", TriggerView.as_view(), name="trigger_webhook")
]

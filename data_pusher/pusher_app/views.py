# Standard imports here:
from json import dumps

# Third party imports here:
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

# Local imports here:
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from .utility import hit_destination_url_with_data


# Create your views here.
class AccountViewSet(ModelViewSet):
    """
    ViewSet to create Account related APIs:
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DestinationViewSet(ModelViewSet):
    """
    ViewSet to create Destination related APIs:
    """

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    # If Account id is passed in get method in only
    def get_queryset(self):
        account_id = self.request.GET.get("account_id")
        if account_id:
            self.queryset = self.queryset.filter(account__account_id=account_id)
        return super().get_queryset()


class TriggerView(APIView):
    def post(self, request, *args, **kwargs):
        # Checking the weather the secret_token is provided and valid.
        secret_token = request.headers.get("Cl-X-TOKEN")
        if not secret_token or not Account.objects.filter(secret_token=secret_token):
            return Response(status=HTTP_401_UNAUTHORIZED, data="Un Authenticated")

        # Hit all the url of the account:
        destination_response_counts: dict = hit_destination_url_with_data(
            secret_token, {"data": request.data}
        )
        # If everything works fine return 201 status:
        return Response(status=HTTP_201_CREATED, data=destination_response_counts)

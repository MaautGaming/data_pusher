# Standard imports here:

# Third party imports here:
from rest_framework.serializers import ModelSerializer, ValidationError

# Local imports here:
from .models import Account, Destination


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["secret_token", "account_id"]


# To make sure that headers is not null as that is also a valid JSON:
class NotNullValidator:
    require_context = True

    def __call__(self, value):
        if not value.get("headers"):
            raise ValidationError("Header can't be null!!!")


class DestinationSerializer(ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"
        validators = [NotNullValidator()]

# Standard imports here:
from uuid import uuid4
from urllib.parse import quote
from secrets import token_urlsafe

# Third party imports here:
from django.db.models import (
    Model,
    EmailField,
    UUIDField,
    CharField,
    URLField,
    ForeignKey,
    TextChoices,
    JSONField,
    DateTimeField,
    CASCADE,
)

# Local imports here:


# Defined funtion to create strong secret key for the api accounts:
# Defined here to avoid circular import error
def generate_api_key(account_name: str) -> str:
    """
    generating a 64 character long urlsafe token
    """
    account_name = quote(account_name)
    return account_name + "." + token_urlsafe(64)


class HTTPMethodChoice(TextChoices):
    """
    To define the choice of the method that can be accepted with destination.
    """

    get: str = "GET"
    post: str = "POST"
    put: str = "PUT"


class Account(Model):
    account_id = UUIDField(default=uuid4, unique=True, blank=True)
    email_id = EmailField(unique=True)
    account_name = CharField(max_length=100)
    secret_token = CharField(max_length=200, unique=True, blank=True)
    website_link = URLField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.account_name} <{self.email_id}>"

    def save(self, *args, **kwargs) -> None:
        """
        overriding the save method to create a secret_token before saving
        the model. The secret_token consist of the account_name ten chars as
        prefix and rest is 64 bits
        """
        if not self.secret_token:
            secret_token = generate_api_key(self.account_name[:10])
            # Iterating over to make sure the secret token is unique
            while Account.objects.filter(secret_token=secret_token):
                secret_token = generate_api_key(self.account_name[:10])
            self.secret_token = secret_token

        return super().save(*args, **kwargs)


class Destination(Model):
    account = ForeignKey(Account, on_delete=CASCADE)
    destination_url = URLField()
    http_method = CharField(max_length=10, choices=HTTPMethodChoice)
    headers = JSONField(help_text="")

    def __str__(self) -> str:
        return f"{self.http_method} <{self.destination_url}>"

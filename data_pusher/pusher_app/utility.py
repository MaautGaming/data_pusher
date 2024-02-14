r"""pusher_app.utility
    This app has the utility functions that are needed in the pusher app.
"""

from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from .models import Destination


def hit_destination_url_with_data(secret_token: str, request_data: Any) -> dict:
    destination_response_counts = {
        "successful": {"count": 0},
        "unsuccessful": {"count": 0, "details": []},
    }
    destinations_to_send_info = Destination.objects.filter(
        account__secret_token=secret_token
    )
    for destination in destinations_to_send_info:
        success, error = fire_webhook(request_data, destination)
        if success:
            destination_response_counts["successful"]["count"] += 1
        else:
            destination_response_counts["unsuccessful"]["count"] += 1
            destination_response_counts["unsuccessful"]["details"].append(
                {str(destination): str(error)}
            )

    return destination_response_counts


def fire_webhook(request_data: Any, destination: Destination) -> (bool, str):
    success, error = False, ""
    request_method = destination.http_method
    headers = destination.headers
    destination_url = destination.destination_url
    data = urlencode(request_data)
    if request_method == "GET":
        destination_url = destination_url + "?" + data
        request = Request(
            url=destination_url,
            headers=headers,
            method=request_method,
        )
    else:
        request = Request(
            url=destination_url,
            data=data.encode("ascii"),
            headers=headers,
            method=request_method,
        )
    try:
        with urlopen(request) as res:
            print(res.status)
            if res.status // 100 == 2:
                success = True
    except HTTPError as http_error:
        error = http_error
        print(http_error)
    except URLError as url_error:
        error = url_error
        print(url_error)
    return success, error

r"""pusher_app.utility
    This app has the utility functions that are needed in the pusher app.
"""

# Standard imports here:
from typing import Tuple
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Third party imports here:

# Local imports here:
from .models import Destination


def create_http_method_based_request(
    request_method: str, headers: dict, destination_url: str, encoded_request_data: str
) -> Request:
    """
    Method to create http request based Request object
    """
    if request_method == "GET":
        destination_url = destination_url + "?" + encoded_request_data
        request = Request(
            url=destination_url,
            headers=headers,
            method=request_method,
        )
    else:
        request = Request(
            url=destination_url,
            data=encoded_request_data.encode("ascii"),
            headers=headers,
            method=request_method,
        )

    return request


def fire_webhook(request_data: Any, destination: Destination) -> Tuple[bool, str]:
    """
    Funtion to hit urls with urllib request package
    """
    success, info = False, ""
    request_method = destination.http_method
    headers = destination.headers
    destination_url = destination.destination_url
    encoded_request_data = urlencode(request_data)
    # Create http method based on request type
    request = create_http_method_based_request(
        request_method, headers, destination_url, encoded_request_data
    )
    try:
        with urlopen(request) as res:
            success = True
            info = str(res)
    except HTTPError as http_error:
        info = str(http_error)
    except URLError as url_error:
        info = str(url_error)
    except Exception as error:
        info = str(error)
    return success, info


def hit_destination_url_with_data(secret_token: str, request_data: Any) -> dict:
    # Structure to send response
    destination_response_counts = {
        "successful": {"count": 0, "details": []},
        "unsuccessful": {"count": 0, "details": []},
    }
    # Get all the destination for that secret_token:
    destinations_to_send_info = Destination.objects.filter(
        account__secret_token=secret_token
    )
    # Fire webhooks for  all the destination:
    for destination in destinations_to_send_info:
        success, info = fire_webhook(request_data, destination)
        # Based on response set details and count for successfula and
        # unsuccessful requests.
        if success:
            destination_response_counts["successful"]["count"] += 1
            destination_response_counts["successful"]["details"].append(
                {str(destination): info}
            )
        else:
            destination_response_counts["unsuccessful"]["count"] += 1
            destination_response_counts["unsuccessful"]["details"].append(
                {str(destination): info}
            )

    return destination_response_counts

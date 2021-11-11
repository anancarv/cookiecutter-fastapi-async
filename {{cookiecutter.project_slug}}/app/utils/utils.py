from fastapi import Response


def format_response_headers(response: Response, total_count: int) -> Response:
    # This is necessary for pagination
    response.headers["Access-Control-Expose-Headers"] = "X-Total-Count"
    response.headers["X-Total-Count"] = f"{total_count}"
    return response

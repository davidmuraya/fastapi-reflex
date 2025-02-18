import time

from fastapi import Request


async def calculate_process_time(start: float) -> float:
    """
    Utility function to calculate processing time
    """
    return round(time.perf_counter() - start, 3)


async def log_and_track_request_process_time(request: Request, call_next):
    """
    Asynchronous middleware function that:

    1. Calculates the process time for handling a request.
    2. Adds the process time as an "X-Process-Time" header to the response.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The function to call to proceed with the request handling.

    Returns:
        Response: The response object with added process time header.
    """

    # Record start time of request processing
    start = time.perf_counter()

    # Proceed with request handling
    response = await call_next(request)

    # Add process time as header to the response
    response.headers["X-Process-Time"] = (
        f"{str(await calculate_process_time(start=start))} s."
    )

    return response

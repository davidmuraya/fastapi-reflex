from fastapi import Request


async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    response.headers["Permissions-Policy"] = (
        "geolocation=(),midi=(),sync-xhr=(),microphone=(),camera=()," "magnetometer=(),gyroscope=(),fullscreen=(self),payment=()"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' data: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.google.com https://www.gstatic.com https://z.clarity.ms https://*.clarity.ms; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https://lh3.googleusercontent.com image/; "
        "font-src 'self' data: https://fonts.gstatic.com; "
        "object-src 'none'; "
        "form-action 'self'; "
        "frame-src 'self' https://www.google.com https://www.gstatic.com; "
        "connect-src 'self' https://*.clarity.ms https://z.clarity.ms; "  # Added connect-src
        "upgrade-insecure-requests"
    )

    return response

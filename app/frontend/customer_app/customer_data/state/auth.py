"""The authentication state."""

import re

import httpx
import reflex as rx
from sqlmodel import select

from ..config import settings
from .base import State
from .models import User

BASE_URL = f"{settings.fastapi_host}/api/v1"


class AuthState(State):
    """The authentication state for sign up and login page."""

    email: str
    password: str
    confirm_password: str
    otp: str

    # Cookie to store authentication status
    access_token: str = rx.Cookie(name="access_token", same_site="strict")

    @rx.var(cache=True)
    def invalid_email(self) -> bool:
        email = self.email.strip()
        if email:
            return not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        return False

    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match.")
            if session.exec(select(User).where(User.email == self.email)).first():
                return rx.window_alert("Username already exists.")
            self.user = User(email=self.email, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""

        # If email is empty, return an error toast.
        if not self.email.strip():
            return rx.toast.error("Email cannot be empty", close_button=True)

        # If password is empty, return an error toast.
        if not self.password.strip():
            return rx.toast.error("Password cannot be empty", close_button=True)

        # If OTP is empty, return an error toast.
        if not self.otp.strip():
            return rx.toast.error("OTP cannot be empty", close_button=True)

        # Make the API request
        data = {"email": self.email, "password": self.password}
        try:
            response = httpx.post(
                f"{BASE_URL}/auth/login",
                json=data,
            )

        except Exception as e:
            return rx.toast.error(f"Error: {e}", position="bottom-right")

        # check if the response is a 200 OK
        if response.status_code == 200:
            user_data = response.json()

            # Create the user object:
            user = User(
                id=user_data.get("id"),
                email=user_data.get("email"),
                name=user_data.get("name"),
            )
            self.user = user

            # Get the access token:
            access_token = user_data.get("access_token")

            # Set the auth cookie - this will automatically handle browser storage
            self.access_token = f"Bearer {access_token}"

            return rx.redirect("/dashboard")
        else:
            print(f"Error occured {response.text=}")
            error_message = response.json().get(
                "detail", "Unknown error occurred. Please try again."
            )
            return rx.toast.error(error_message, close_button=True)

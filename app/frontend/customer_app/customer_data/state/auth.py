"""The authentication state."""

import re

import httpx
import reflex as rx

from ..config import settings
from .base import State
from .models import User

BASE_URL = f"{settings.fastapi_host}/api/v1"


class AuthState(State):
    """The authentication state for sign up and login page."""

    name: str
    email: str
    password: str
    confirm_password: str
    account_created: bool = False

    @rx.var(cache=True)
    def invalid_email(self) -> bool:
        email = self.email.strip()
        if email:
            return not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        return False

    @rx.var(cache=True)
    def invalid_password(self) -> bool:
        password = self.password.strip()

        if password:
            # Check if the password is non-empty and has the minimum length
            if not password or len(password) < 8:
                return True

            # Check for at least one uppercase letter
            if not re.search(r"[A-Z]", password):
                return True

            # Check for at least one lowercase letter
            if not re.search(r"[a-z]", password):
                return True

            # Check for at least one digit
            if not re.search(r"\d", password):
                return True

        return False

    def signup(self):
        """Sign up a user."""

        # If name is empty, return an error toast.
        if not self.name.strip():
            return rx.toast.error("Name cannot be empty", close_button=True)

        # If email is empty, return an error toast.
        if not self.email.strip():
            return rx.toast.error("Email cannot be empty", close_button=True)

        # If password is empty, return an error toast.
        if not self.password.strip():
            return rx.toast.error("Password cannot be empty", close_button=True)

        # If confirm password is empty, return an error toast.
        if not self.confirm_password.strip():
            return rx.toast.error("Confirm password cannot be empty", close_button=True)

        # If passwords do not match, return an error toast.
        if self.password != self.confirm_password:
            return rx.toast.error("Passwords do not match", close_button=True)

        # Show a toast in the UI the account is being created:
        rx.toast.info("Creating your account..", close_button=True)

        # Create the data obj
        data = [
            {
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "active": True,
            }
        ]

        try:
            response = httpx.post(
                f"{BASE_URL}/users",
                json=data,
            )

        except Exception as e:
            return rx.toast.error(f"Error: {e}", position="bottom-right")

        # check if the response is a 200 OK
        if response.status_code == 200:
            self.account_created = True
            return rx.toast.success(
                "Your account has been created successfully. Please sign in.",
                position="bottom-right",
            )

        else:
            print(f"Error occured {response.text=}")
            error_message = response.json().get(
                "detail", "Unknown error occurred. Please try again."
            )
            return rx.toast.error(error_message, close_button=True)

    def login(self):
        """Log in a user."""

        # If email is empty, return an error toast.
        if not self.email.strip():
            return rx.toast.error("Email cannot be empty", close_button=True)

        # If password is empty, return an error toast.
        if not self.password.strip():
            return rx.toast.error("Password cannot be empty", close_button=True)

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

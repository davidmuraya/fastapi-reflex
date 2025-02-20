"""Base state for example."""

from typing import Optional

import reflex as rx

from .models import User


class State(rx.State):
    """The base state for the app."""

    user: Optional[User] = None

    # Cookie to store authentication status
    access_token: str = rx.Cookie(name="access_token", same_site="strict")

    def logout(self):
        """Log out a user."""
        self.reset()
        rx.remove_cookie("access_token")
        return rx.redirect("/")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/")

    @rx.var
    def logged_in(self) -> bool:
        """Check if a user is logged in."""
        return self.user is not None

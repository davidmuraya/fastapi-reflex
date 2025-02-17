import re

import reflex as rx

from ..components.form_field import form_field
from ..views.navbar import navbar


def is_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


class LoginPageState(rx.State):
    """State for the login page."""

    form_data: dict = {}
    email: str
    password: str
    otp: str

    @rx.var(cache=True)
    def invalid_email(self) -> bool:
        email = self.email.strip()
        if email:
            return not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        return False

    @rx.event
    def submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

        # If email is empty, return an error toast.
        if not self.email.strip():
            return rx.toast.error("Email cannot be empty", close_button=True)

        # If password is empty, return an error toast.
        if not self.password.strip():
            return rx.toast.error("Password cannot be empty", close_button=True)

        # If OTP is empty, return an error toast.
        if not self.otp.strip():
            return rx.toast.error("OTP cannot be empty", close_button=True)

        return rx.toast.success(
            f"Login successful!, {self.email=}, {self.password=}", close_button=True
        )


def login_form() -> rx.Component:
    return (
        rx.form.root(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.badge(
                            rx.icon(tag="user", size=52),
                            color_scheme="blue",
                            radius="full",
                            padding="0.65rem",
                        ),
                        rx.vstack(
                            rx.heading(
                                "Login",
                                size="7",
                                weight="bold",
                            ),
                            rx.text(
                                "Fill the form to login to Bima-MO",
                                size="2",
                            ),
                            spacing="1",
                            height="100%",
                        ),
                        height="100%",
                        spacing="4",
                        align_items="center",
                        width="100%",
                    ),
                    form_field(
                        label="Email address",
                        icon="user",
                        placeholder="Email address",
                        type="email",
                        name="email",
                    ),
                    # Conditionally render the error message if the email is invalid.
                    rx.cond(
                        LoginPageState.invalid_email,
                        rx.text(
                            "Invalid email address!",
                            size="2",
                            color="red",
                        ),
                    ),
                    form_field(
                        label="Password",
                        icon="lock",
                        placeholder="Password",
                        type="password",
                        name="password",
                    ),
                    form_field(
                        label="OTP",
                        icon="key-round",
                        placeholder="OTP",
                        type="text",
                        name="otp",
                    ),
                    rx.button("Sign in", size="3", width="100%", type="submit"),
                    rx.center(
                        rx.text("New here?", size="3"),
                        rx.link("Sign up", href="#", size="3"),
                        opacity="0.8",
                        spacing="2",
                        direction="row",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                size="4",
                width="100%",
                min_width=[
                    "20em",
                    "35em",
                ],  # Mobile first: 20em, 35em on medium+ screens
                max_width="40em",
                margin_x="1em",
            ),
            on_submit=LoginPageState.submit,
            reset_on_submit=False,
        ),
    )


@rx.page(route="/login", title="Login", description="Login page")
def login_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(login_form()),
            width="100%",
            height="80vh",
        ),
    )

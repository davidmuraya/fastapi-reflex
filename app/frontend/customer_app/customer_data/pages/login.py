"""
Login Page
"""

import reflex as rx

from ..components.input import input
from ..state.auth import AuthState
from ..views.navbar import navbar

BASE_URL = "http://localhost:5000/api"


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
                    input(
                        label="Email address",
                        icon="user",
                        placeholder="Email address",
                        type="email",
                        name="email",
                        on_blur=AuthState.set_email,
                    ),
                    input(
                        label="Password",
                        icon="lock",
                        placeholder="Password",
                        type="password",
                        name="password",
                        on_blur=AuthState.set_password,
                    ),
                    input(
                        label="OTP",
                        icon="key-round",
                        placeholder="OTP",
                        type="text",
                        name="otp",
                        on_blur=AuthState.set_otp,
                    ),
                    rx.button("Sign in", size="3", width="100%", type="submit"),
                    # Conditionally render the error messages if the email is invalid.
                    rx.cond(
                        AuthState.invalid_email,
                        rx.callout(
                            "Invalid email address!",
                            icon="info",
                            color_scheme="red",
                            width="100%",
                        ),
                    ),
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
            on_submit=AuthState.login,
            reset_on_submit=False,
        ),
    )


@rx.page(route="/", title="Login", description="Login page")
def login_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(login_form()),
            width="100%",
            height="80vh",
        ),
    )

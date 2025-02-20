"""
Login Page
"""

import reflex as rx

from ..components.input import input
from ..state.auth import AuthState
from ..views.navbar import navbar


def sign_up_form() -> rx.Component:
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
                                "Sign Up",
                                size="7",
                                weight="bold",
                            ),
                            rx.text(
                                "Fill the form to Sign up",
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
                        label="Name",
                        icon="user",
                        placeholder="Name",
                        type="text",
                        name="name",
                        on_blur=AuthState.set_name,
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
                        label="Confirm Password",
                        icon="lock",
                        placeholder="Password",
                        type="password",
                        name="password",
                        on_blur=AuthState.set_confirm_password,
                    ),
                    rx.button("Sign up", size="3", width="100%", type="submit"),
                    # Conditionally render the callout if the account was created.
                    rx.cond(
                        AuthState.account_created,
                        rx.callout(
                            f"Your account has been created successfully. Please sign in with your email {AuthState.email} and password.",
                            icon="check",
                            color_scheme="green",
                            width="100%",
                        ),
                    ),
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
                    # Conditionally render the error messages if the password is invalid.
                    rx.cond(
                        AuthState.invalid_password,
                        rx.callout(
                            "Password must be 8 characters, Must contain a number and a letter.",
                            icon="info",
                            color_scheme="red",
                            width="100%",
                        ),
                    ),
                    rx.center(
                        rx.text("Already have an account?", size="3"),
                        rx.link("Sign in", href="/", size="3"),
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
            on_submit=AuthState.signup,
            reset_on_submit=False,
        ),
    )


@rx.page(route="/sign-up", title="Sign Up", description="Sign up page")
def sign_up_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(sign_up_form()),
            width="100%",
            height="80vh",
        ),
    )

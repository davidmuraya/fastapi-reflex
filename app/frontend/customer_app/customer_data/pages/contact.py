import re

import reflex as rx

from ..components.form_field import form_field
from ..views.navbar import navbar


def is_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


class ContactPageState(rx.State):
    """State for the contact page."""

    form_data: dict = {}
    email_error: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    message: str = ""

    @rx.var(cache=False)
    def invalid_email(self) -> bool:
        email = self.email.strip()
        if email:
            return not re.match(r"[^@]+@[^@]+\.[^@]+", email)
        return False

    def validate_email(self):
        """Validate email format on blur"""
        if not is_email(self.email):
            self.email_error = "Invalid email format"
        else:
            self.email_error = ""

    @rx.event
    def submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data

        # If first_name is empty, return an error toast.
        if not self.first_name.strip():
            return rx.toast.error("First name cannot be empty", close_button=True)

        # If last_name is empty, return an error toast.
        if not self.last_name.strip():
            return rx.toast.error("Last name cannot be empty", close_button=True)

        # If email is empty, return an error toast.
        if not self.email.strip():
            return rx.toast.error("Email cannot be empty", close_button=True)

        # If message is empty, return an error toast.
        if not self.message.strip():
            return rx.toast.error("Message cannot be empty", close_button=True)

        return rx.toast.success(
            f"Contact form submitted!, {self.first_name=}, {self.last_name=}, {self.email=}, {self.phone=}, {self.message=}",
            close_button=True,
        )


def contact_form() -> rx.Component:
    return rx.card(
        rx.flex(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="mail-plus", size=32),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading(
                        "Send us a message",
                        size="4",
                        weight="bold",
                    ),
                    rx.text(
                        "Fill the form to contact us",
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
            rx.form.root(
                rx.flex(
                    rx.flex(
                        form_field(
                            "First Name",
                            "First Name",
                            "text",
                            "first_name",
                            icon="user",
                        ),
                        form_field(
                            "Last Name",
                            "Last Name",
                            "text",
                            "last_name",
                            icon="user",
                        ),
                        spacing="3",
                        flex_direction=[
                            "column",
                            "row",
                            "row",
                        ],
                    ),
                    rx.flex(
                        form_field(
                            "Email",
                            "user@reflex.dev",
                            "email",
                            "email",
                            icon="mail",
                        ),
                        form_field("Phone", "Phone", "tel", "phone", icon="phone"),
                        spacing="3",
                        flex_direction=[
                            "column",
                            "row",
                            "row",
                        ],
                    ),
                    rx.flex(
                        rx.text(
                            "Message",
                            style={
                                "font-size": "15px",
                                "font-weight": "500",
                                "line-height": "35px",
                            },
                        ),
                        rx.text_area(
                            placeholder="Message",
                            name="message",
                            resize="vertical",
                        ),
                        direction="column",
                        spacing="1",
                    ),
                    rx.form.submit(
                        rx.button("Submit"),
                        as_child=True,
                    ),
                    # Conditionally render the error messages if the email is invalid.
                    rx.cond(
                        ContactPageState.invalid_email,
                        rx.callout(
                            "Invalid email address!",
                            icon="info",
                            color_scheme="red",
                        ),
                    ),
                    direction="column",
                    spacing="3",
                    width="100%",
                ),
                on_submit=ContactPageState.submit,
                reset_on_submit=False,
            ),
            width="100%",
            direction="column",
            spacing="4",
        ),
        size="4",
        width="100%",
        min_width=[
            "20em",
            "35em",
        ],  # Mobile first: 20em, 35em on medium+ screens
        max_width="40em",
        margin_x="1em",
    )


@rx.page(route="/contact", title="Contact", description="Contact page")
def contact_page() -> rx.Component:
    return (
        rx.box(
            navbar(),
            rx.center(contact_form(), width="100%", height="80vh"),
        ),
    )

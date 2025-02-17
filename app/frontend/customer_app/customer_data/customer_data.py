"""
Customer data app.
"""

import reflex as rx

from .components.stats_cards import stats_cards_group
from .pages.contact import contact_page
from .pages.login import login_page
from .views.navbar import navbar
from .views.sidebar import sidebar
from .views.table import main_table


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            navbar(),
            stats_cards_group(),
            rx.spacer(),
            rx.box(
                main_table(),
                width="100%",
                overflow_x="auto",  # Allow horizontal scrolling
            ),
            width="100%",
            spacing="4",
            padding_x=["1.5em", "1.5em", "3em"],
            margin_left=["0", "0", "16em"],  # Responsive margin
        ),
        width="100%",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="grass"
    ),
)

app.add_page(
    index,
    title="Customer Data App",
    description="A simple app to manage customer data.",
)

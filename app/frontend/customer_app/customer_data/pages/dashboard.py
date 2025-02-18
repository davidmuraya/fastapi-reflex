"""
Customer data Dashboard.

User must be logged in to view
"""

import reflex as rx

from ..components.stats_cards import stats_cards_group
from ..state.base import State
from ..views.navbar import navbar
from ..views.sidebar import sidebar
from ..views.table import main_table


@rx.page(
    route="/dashboard",
    title="Dashboard",
    description="Dashboard page",
    on_load=State.check_login(),
)
def dashboard_page() -> rx.Component:
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

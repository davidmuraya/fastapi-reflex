"""
Navbar view for the customer data app.
"""

import reflex as rx

from ..components.dark_light_mode_toggle import toggle_switch


def navbar():
    return rx.hstack(
        toggle_switch(),
        justify="end",
        width="100%",
        padding="2em",
    )

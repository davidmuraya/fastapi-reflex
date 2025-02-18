"""
Input component.
"""

import reflex as rx


def input(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    on_change: rx.EventHandler = None,
    on_blur: rx.EventHandler = None,
) -> rx.Component:
    """
    Input with Icon box inside the input field
    """
    return (
        rx.vstack(
            rx.text(
                label,
                size="3",
                weight="medium",
                text_align="left",
                width="100%",
            ),
            rx.input(
                rx.input.slot(rx.icon(icon)),
                placeholder=placeholder,
                type=type,
                size="3",
                width="100%",
                name=name,
                on_change=on_change,  # Add handler
                on_blur=on_blur,  # Add handler
            ),
            spacing="1",
            width="100%",
        ),
    )

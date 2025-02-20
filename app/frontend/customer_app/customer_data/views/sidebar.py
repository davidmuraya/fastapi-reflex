"""
Sidebar view for the customer data app.
"""

import reflex as rx

from ..state.base import State


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    """Navigation Links"""
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="3"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_button(text: str, icon: str, on_click=rx.EventHandler) -> rx.Component:
    """Navigation buttons that look like links"""
    return rx.button(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="3", weight="medium"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        on_click=on_click,
        underline="none",
        weight="medium",
        width="100%",
        variant="ghost",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/contact"),
        sidebar_item("API Documentation", "book-open", "/api/docs"),
        sidebar_item("About", "info", "/about"),
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.badge(
                        rx.icon(tag="monitor-cog", size=30),
                        color_scheme="blue",
                        radius="full",
                        padding="0.65rem",
                    ),
                    rx.text(
                        "Customer App",
                        size="4",
                        weight="bold",
                    ),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        sidebar_item("Settings", "settings", "/#"),
                        sidebar_button("Logout", "log-out", on_click=State.logout),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.icon_button(
                            rx.icon("user"),
                            size="3",
                            radius="full",
                        ),
                        rx.vstack(
                            rx.box(
                                rx.text(
                                    State.user.name,
                                    size="3",
                                    weight="bold",
                                ),
                                rx.text(
                                    State.user.email,
                                    size="2",
                                    weight="medium",
                                ),
                                width="100%",
                            ),
                            spacing="0",
                            align="start",
                            justify="start",
                            width="100%",
                        ),
                        padding_x="0.5rem",
                        align="center",
                        justify="start",
                        width="100%",
                    ),
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                position="fixed",
                left="0px",
                top="0px",
                z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    sidebar_item(
                                        "Settings",
                                        "settings",
                                        "/#",
                                    ),
                                    sidebar_item(
                                        "Log out",
                                        "log-out",
                                        "/#",
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                rx.hstack(
                                    rx.icon_button(
                                        rx.icon("user"),
                                        size="3",
                                        radius="full",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.text(
                                                State.user.name,
                                                size="3",
                                                weight="bold",
                                            ),
                                            rx.text(
                                                State.user.email,
                                                size="2",
                                                weight="medium",
                                            ),
                                            width="100%",
                                        ),
                                        spacing="0",
                                        justify="start",
                                        width="100%",
                                    ),
                                    padding_x="0.5rem",
                                    align="center",
                                    justify="start",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )

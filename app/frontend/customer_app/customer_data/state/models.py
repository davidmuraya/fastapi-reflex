import reflex as rx


class User(rx.Base):
    """Users Model."""

    id: int
    email: str
    name: str

from datetime import datetime, timedelta
from typing import Optional, Union

import httpx
import reflex as rx

from ..config import settings

# Base URL for the FastAPI backend.
BASE_URL = f"{settings.fastapi_host}/api"


def _get_percentage_change(
    value: Union[int, float], prev_value: Union[int, float]
) -> float:
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0.0
        if value == 0
        else float("inf")
    )
    return percentage_change


class Customer(rx.Base):
    """Frontend customer model."""

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    date: str = ""
    payments: float = 0.0
    status: str = ""


class MonthValues(rx.Base):
    """Values for a month."""

    num_customers: int = 0
    total_payments: float = 0.0
    num_delivers: int = 0


class State(rx.State):
    """The app state."""

    users: list[Customer] = []
    sort_value: str = ""
    sort_reverse: bool = False
    search_value: str = ""
    current_user: Customer = Customer()
    current_month_values: MonthValues = MonthValues()
    previous_month_values: MonthValues = MonthValues()

    def load_entries(self):
        """Load customers from FastAPI backend."""

        params = {}

        # Add search and sort parameters to the request
        if self.search_value:
            params["search"] = self.search_value
        if self.sort_value:
            params["sort_by"] = self.sort_value
            params["sort_order"] = "desc" if self.sort_reverse else "asc"

        # Make the API request
        try:
            response = httpx.get(
                f"{BASE_URL}/customers",
                params=params,
            )

        except Exception as e:
            return rx.toast.error(f"Error: {e}", position="bottom-right")

        if response.status_code == 200:
            self.users = [Customer(**customer) for customer in response.json()]

        self.get_current_month_values()
        self.get_previous_month_values()

    def add_customer_to_db(self, form_data: dict):
        """Add customer to the database."""
        new_customer = Customer(date=datetime.now().strftime("%Y-%m-%d"), **form_data)

        try:
            # Add new customer
            response = httpx.post(
                f"{BASE_URL}/customers",
                json=[new_customer.dict()],
            )
            if response.status_code == 200:
                self.load_entries()
                return rx.toast.info(
                    "Customer added successfully", position="bottom-right"
                )
        except Exception as e:
            return rx.toast.error(f"Error {e}", position="bottom-right")

    def update_customer_to_db(self, form_data: dict):
        """Update customer through FastAPI."""
        customer_id = self.current_user.id

        yield rx.toast.info("Updating customer...", position="bottom-right")

        # Update the customer in the database
        try:
            response = httpx.put(
                f"{BASE_URL}/customers/{customer_id}",
                json=form_data,
            )
            if response.status_code == 200:
                self.load_entries()
                yield rx.toast.info(
                    "Customer updated successfully", position="bottom-right"
                )
        except Exception as e:
            yield rx.toast.error(f"Error: {e}", position="bottom-right")

    def delete_customer(self, customer_id: int):
        """Delete customer through FastAPI."""

        try:
            response = httpx.delete(
                f"{BASE_URL}/customers/{customer_id}",
            )
            if response.status_code == 200:
                self.load_entries()
                return rx.toast.info(
                    "Customer deleted successfully", position="bottom-right"
                )
        except Exception as e:
            yield rx.toast.error(f"Connection error {e}", position="bottom-right")

    # Keep the following methods unchanged as they process local data
    def get_current_month_values(self):
        """Calculate current month's values."""

        now = datetime.now()
        start_of_month = datetime(now.year, 1, 1)

        current_month_users = [
            user
            for user in self.users
            if datetime.strptime(user.date, "%Y-%m-%d") >= start_of_month
        ]
        num_customers = len(current_month_users)
        total_payments = sum(user.payments for user in current_month_users)
        num_delivers = len(
            [user for user in current_month_users if user.status == "Delivered"]
        )
        self.current_month_values = MonthValues(
            num_customers=num_customers,
            total_payments=total_payments,
            num_delivers=num_delivers,
        )

    def get_previous_month_values(self):
        """Calculate previous month's values."""
        now = datetime.now()
        first_day_of_current_month = datetime(now.year, 1, 1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        start_of_last_month = datetime(
            last_day_of_last_month.year, last_day_of_last_month.month, 1
        )

        previous_month_users = [
            user
            for user in self.users
            if start_of_last_month
            <= datetime.strptime(user.date, "%Y-%m-%d")
            <= last_day_of_last_month
        ]
        # We add some dummy values to simulate growth/decline. Remove them in production.
        num_customers = len(previous_month_users) + 3
        total_payments = sum(user.payments for user in previous_month_users) + 240
        num_delivers = (
            len([user for user in previous_month_users if user.status == "Delivered"])
            + 5
        )

        self.previous_month_values = MonthValues(
            num_customers=num_customers,
            total_payments=total_payments,
            num_delivers=num_delivers,
        )

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        return self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        return self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        return self.load_entries()

    def get_user(self, user: Customer):
        self.current_user = user

    @rx.var(cache=True)
    def payments_change(self) -> float:
        return _get_percentage_change(
            self.current_month_values.total_payments,
            self.previous_month_values.total_payments,
        )

    @rx.var(cache=True)
    def customers_change(self) -> float:
        return _get_percentage_change(
            self.current_month_values.num_customers,
            self.previous_month_values.num_customers,
        )

    @rx.var(cache=True)
    def delivers_change(self) -> float:
        return _get_percentage_change(
            self.current_month_values.num_delivers,
            self.previous_month_values.num_delivers,
        )

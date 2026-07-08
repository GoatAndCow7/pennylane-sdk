"""Billing subscriptions resource (Company API v2).

Reference: https://pennylane.readme.io/reference/getbillingsubscriptions
"""

from __future__ import annotations

from typing import Any

from ..._models import drop_none
from ..._pagination import AsyncCursorPage, SyncCursorPage
from ..._resource import AsyncAPIResource, SyncAPIResource
from ...filters import FiltersInput
from ...types.company.billing_subscriptions import (
    BillingSubscription,
    BillingSubscriptionInvoiceLine,
    BillingSubscriptionInvoiceLineSection,
)

__all__ = ["AsyncBillingSubscriptions", "BillingSubscriptions"]


class BillingSubscriptions(SyncAPIResource):
    """Manage recurring customer invoice subscriptions."""

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[BillingSubscription]:
        """List billing subscriptions.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptions

        Args:
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            filter: Conditions built with :mod:`pennylane_sdk.filters`. Supported
                fields: ``id``, ``start``, ``customer_id`` (``lt``, ``lteq``,
                ``gt``, ``gteq``, ``eq``, ``not_eq``, ``in``, ``not_in``) and
                ``status`` (``eq``, ``not_eq``, ``in``, ``not_in``).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            "/billing_subscriptions",
            item_type=BillingSubscription,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    def get(self, billing_subscription_id: int) -> BillingSubscription:
        """Retrieve a billing subscription by its Pennylane identifier.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscription
        """
        return self._get(
            f"/billing_subscriptions/{billing_subscription_id}", cast_to=BillingSubscription
        )

    def create(
        self,
        *,
        start: str,
        mode: dict[str, Any],
        payment_conditions: str,
        payment_method: str,
        recurring_rule: dict[str, Any],
        customer_id: int,
        customer_invoice_data: dict[str, Any],
        label: str | None = None,
    ) -> BillingSubscription:
        """Create a billing subscription.

        Pennylane generates a customer invoice at each occurrence of the
        subscription. It can also be linked to a GoCardless mandate.

        Scope: ``billing_subscriptions:all``.
        Reference: https://pennylane.readme.io/reference/postbillingsubscriptions

        Args:
            start: Subscription start date (``YYYY-MM-DD``).
            mode: Invoice generation mode, ``{"type": "awaiting_validation" | "finalized"}``
                or ``{"type": "email", "email_settings": {"recipients": [...]}}``.
            payment_conditions: One of ``upon_receipt``, ``7_days``, ``15_days``,
                ``30_days``, ``30_days_end_of_month``, ``45_days``,
                ``45_days_end_of_month``, ``60_days``.
            payment_method: One of ``offline``, ``gocardless_direct_debit``,
                ``pro_account_sepa_core``.
            recurring_rule: Recurrence rule, e.g.
                ``{"type": "monthly", "interval": 1, "day_of_month": 1}``
                (``type`` is one of ``yearly``, ``monthly``, ``weekly``, each
                with its own optional ``interval``/``count`` and, respectively,
                ``day_of_month`` or ``day_of_week``).
            customer_id: Customer identifier.
            customer_invoice_data: Data used to generate each invoice, with keys
                such as ``currency``, ``customer_invoice_template_id``,
                ``pdf_invoice_free_text``, ``pdf_invoice_subject``,
                ``pdf_description``, ``special_mention``, ``language``,
                ``discount``, ``invoice_line_sections`` and the required
                ``invoice_lines`` (list of line dicts with ``label``,
                ``quantity``, ``unit``, ``raw_currency_unit_price``, ``vat_rate``).
            label: Subscription label.
        """
        body = drop_none(
            {
                "start": start,
                "mode": mode,
                "payment_conditions": payment_conditions,
                "payment_method": payment_method,
                "recurring_rule": recurring_rule,
                "customer_id": customer_id,
                "customer_invoice_data": customer_invoice_data,
                "label": label,
            }
        )
        return self._post("/billing_subscriptions", cast_to=BillingSubscription, body=body)

    def update(
        self,
        billing_subscription_id: int,
        *,
        stop: bool | None = None,
        mode: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        payment_method: str | None = None,
        recurring_rule: dict[str, Any] | None = None,
        customer_id: int | None = None,
        customer_invoice_data: dict[str, Any] | None = None,
        label: str | None = None,
    ) -> BillingSubscription:
        """Update a billing subscription. Only the provided fields are modified.

        Scope: ``billing_subscriptions:all``.
        Reference: https://pennylane.readme.io/reference/putbillingsubscriptions

        Args:
            stop: Use ``True`` to stop an ``in_progress`` subscription, ``False``
                to resume a ``stopped`` one.
            mode: See :meth:`create`.
            payment_conditions: See :meth:`create`.
            payment_method: See :meth:`create`.
            recurring_rule: See :meth:`create`.
            customer_id: Customer identifier.
            customer_invoice_data: See :meth:`create`.
            label: Subscription label.
        """
        body = drop_none(
            {
                "stop": stop,
                "mode": mode,
                "payment_conditions": payment_conditions,
                "payment_method": payment_method,
                "recurring_rule": recurring_rule,
                "customer_id": customer_id,
                "customer_invoice_data": customer_invoice_data,
                "label": label,
            }
        )
        return self._put(
            f"/billing_subscriptions/{billing_subscription_id}",
            cast_to=BillingSubscription,
            body=body,
        )

    def list_invoice_lines(
        self,
        billing_subscription_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[BillingSubscriptionInvoiceLine]:
        """List the invoice lines generated by a billing subscription.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptioninvoicelines

        Args:
            billing_subscription_id: Parent billing subscription identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/billing_subscriptions/{billing_subscription_id}/invoice_lines",
            item_type=BillingSubscriptionInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    def list_invoice_line_sections(
        self,
        billing_subscription_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> SyncCursorPage[BillingSubscriptionInvoiceLineSection]:
        """List the invoice line sections generated by a billing subscription.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptioninvoicelinesections

        Args:
            billing_subscription_id: Parent billing subscription identifier.
            cursor: Pagination cursor from a previous page.
            limit: Results per page (1-100, API default 20).
            sort: Sort field, prefixed with ``-`` for descending (default ``-id``).
        """
        return self._get_page(
            f"/billing_subscriptions/{billing_subscription_id}/invoice_line_sections",
            item_type=BillingSubscriptionInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )


class AsyncBillingSubscriptions(AsyncAPIResource):
    """Manage recurring customer invoice subscriptions (async)."""

    async def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        filter: FiltersInput | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[BillingSubscription]:
        """List billing subscriptions.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptions
        """
        return await self._get_page(
            "/billing_subscriptions",
            item_type=BillingSubscription,
            params={"cursor": cursor, "limit": limit, "filter": filter, "sort": sort},
        )

    async def get(self, billing_subscription_id: int) -> BillingSubscription:
        """Retrieve a billing subscription by its Pennylane identifier.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscription
        """
        return await self._get(
            f"/billing_subscriptions/{billing_subscription_id}", cast_to=BillingSubscription
        )

    async def create(
        self,
        *,
        start: str,
        mode: dict[str, Any],
        payment_conditions: str,
        payment_method: str,
        recurring_rule: dict[str, Any],
        customer_id: int,
        customer_invoice_data: dict[str, Any],
        label: str | None = None,
    ) -> BillingSubscription:
        """Create a billing subscription.

        Scope: ``billing_subscriptions:all``.
        Reference: https://pennylane.readme.io/reference/postbillingsubscriptions
        """
        body = drop_none(
            {
                "start": start,
                "mode": mode,
                "payment_conditions": payment_conditions,
                "payment_method": payment_method,
                "recurring_rule": recurring_rule,
                "customer_id": customer_id,
                "customer_invoice_data": customer_invoice_data,
                "label": label,
            }
        )
        return await self._post("/billing_subscriptions", cast_to=BillingSubscription, body=body)

    async def update(
        self,
        billing_subscription_id: int,
        *,
        stop: bool | None = None,
        mode: dict[str, Any] | None = None,
        payment_conditions: str | None = None,
        payment_method: str | None = None,
        recurring_rule: dict[str, Any] | None = None,
        customer_id: int | None = None,
        customer_invoice_data: dict[str, Any] | None = None,
        label: str | None = None,
    ) -> BillingSubscription:
        """Update a billing subscription. Only the provided fields are modified.

        Scope: ``billing_subscriptions:all``.
        Reference: https://pennylane.readme.io/reference/putbillingsubscriptions
        """
        body = drop_none(
            {
                "stop": stop,
                "mode": mode,
                "payment_conditions": payment_conditions,
                "payment_method": payment_method,
                "recurring_rule": recurring_rule,
                "customer_id": customer_id,
                "customer_invoice_data": customer_invoice_data,
                "label": label,
            }
        )
        return await self._put(
            f"/billing_subscriptions/{billing_subscription_id}",
            cast_to=BillingSubscription,
            body=body,
        )

    async def list_invoice_lines(
        self,
        billing_subscription_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[BillingSubscriptionInvoiceLine]:
        """List the invoice lines generated by a billing subscription.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptioninvoicelines
        """
        return await self._get_page(
            f"/billing_subscriptions/{billing_subscription_id}/invoice_lines",
            item_type=BillingSubscriptionInvoiceLine,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

    async def list_invoice_line_sections(
        self,
        billing_subscription_id: int,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        sort: str | None = None,
    ) -> AsyncCursorPage[BillingSubscriptionInvoiceLineSection]:
        """List the invoice line sections generated by a billing subscription.

        Scope: ``billing_subscriptions:readonly``.
        Reference: https://pennylane.readme.io/reference/getbillingsubscriptioninvoicelinesections
        """
        return await self._get_page(
            f"/billing_subscriptions/{billing_subscription_id}/invoice_line_sections",
            item_type=BillingSubscriptionInvoiceLineSection,
            params={"cursor": cursor, "limit": limit, "sort": sort},
        )

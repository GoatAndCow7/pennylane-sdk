"""The four public Pennylane clients.

- :class:`Pennylane` / :class:`AsyncPennylane`: Company API v2, for a single
  company managing its own accounting and invoicing.
- :class:`PennylaneFirm` / :class:`AsyncPennylaneFirm`: Firm API v1, for
  accounting firms operating on their client portfolio.
"""

from __future__ import annotations

import os

import httpx

from ._base_client import (
    DEFAULT_MAX_RETRIES,
    AsyncAPIClient,
    RateLimitInfo,
    SyncAPIClient,
)
from ._exceptions import PennylaneError
from ._throttle import AsyncRateThrottle, RateThrottle
from .resources import company

__all__ = ["AsyncPennylane", "AsyncPennylaneFirm", "Pennylane", "PennylaneFirm"]

DEFAULT_COMPANY_BASE_URL = "https://app.pennylane.com/api/external/v2"
DEFAULT_FIRM_BASE_URL = "https://app.pennylane.com/api/external/firm/v1"

# Official API rate limits (requests, window seconds), applied per token.
COMPANY_RATE_LIMIT = (25, 5.0)
FIRM_RATE_LIMIT = (5, 1.0)

_COMPANY_TOKEN_ENV = "PENNYLANE_API_TOKEN"
_FIRM_TOKEN_ENV = "PENNYLANE_FIRM_API_TOKEN"


def _resolve_token(explicit: str | None, env_var: str, client_name: str) -> str:
    token = explicit if explicit is not None else os.environ.get(env_var)
    if not token:
        raise PennylaneError(
            f"The api_token client option must be set: pass api_token to {client_name}() "
            f"or set the {env_var} environment variable. Generate a token in Pennylane "
            "under Settings > Connectivity > Developers."
        )
    return token


class Pennylane:
    """Synchronous client for the Pennylane Company API (v2).

    Args:
        api_token: Company API token. Falls back to the ``PENNYLANE_API_TOKEN``
            environment variable.
        base_url: Override the API base URL (e.g. for a proxy).
        timeout: Request timeout in seconds or an ``httpx.Timeout`` (default 60s).
        max_retries: Automatic retry budget (default 3). See the retry policy
            in :mod:`pennylane_sdk._base_client`.
        auto_throttle: When ``True`` (default), outgoing requests are paced
            client-side to the official limit of 25 requests per 5 seconds so
            bulk operations never hit HTTP 429.
        http_client: Custom ``httpx.Client`` (advanced: proxies, transports...).

    Usage::

        from pennylane_sdk import Pennylane

        client = Pennylane()
        for invoice in client.customer_invoices.list():
            print(invoice.invoice_number)
    """

    # Invoicing (sales)
    customer_invoices: company.CustomerInvoices
    customer_invoice_templates: company.CustomerInvoiceTemplates
    quotes: company.Quotes
    commercial_documents: company.CommercialDocuments
    billing_subscriptions: company.BillingSubscriptions
    customers: company.Customers
    products: company.Products
    # Purchases
    suppliers: company.Suppliers
    supplier_invoices: company.SupplierInvoices
    purchase_requests: company.PurchaseRequests
    # Banking
    transactions: company.Transactions
    bank_accounts: company.BankAccounts
    bank_establishments: company.BankEstablishments
    # Accounting
    journals: company.Journals
    ledger_accounts: company.LedgerAccounts
    ledger_entries: company.LedgerEntries
    ledger_attachments: company.LedgerAttachments
    ledger_entry_lines: company.LedgerEntryLines
    trial_balance: company.TrialBalance
    fiscal_years: company.FiscalYears
    # Analytics
    categories: company.Categories
    category_groups: company.CategoryGroups
    # Exports
    exports: company.Exports
    # Payment mandates
    sepa_mandates: company.SepaMandates
    gocardless_mandates: company.GocardlessMandates
    pro_account: company.ProAccount
    # French e-invoicing
    e_invoices: company.EInvoices
    pa_registrations: company.PaRegistrations
    # Misc
    file_attachments: company.FileAttachments
    changelogs: company.Changelogs
    webhook_subscriptions: company.WebhookSubscriptions
    me: company.Me

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        token = _resolve_token(api_token, _COMPANY_TOKEN_ENV, "Pennylane")
        throttle = RateThrottle(*COMPANY_RATE_LIMIT) if auto_throttle else None
        self._client = SyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_COMPANY_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        client = self._client
        self.customer_invoices = company.CustomerInvoices(client)
        self.customer_invoice_templates = company.CustomerInvoiceTemplates(client)
        self.quotes = company.Quotes(client)
        self.commercial_documents = company.CommercialDocuments(client)
        self.billing_subscriptions = company.BillingSubscriptions(client)
        self.customers = company.Customers(client)
        self.products = company.Products(client)
        self.suppliers = company.Suppliers(client)
        self.supplier_invoices = company.SupplierInvoices(client)
        self.purchase_requests = company.PurchaseRequests(client)
        self.transactions = company.Transactions(client)
        self.bank_accounts = company.BankAccounts(client)
        self.bank_establishments = company.BankEstablishments(client)
        self.journals = company.Journals(client)
        self.ledger_accounts = company.LedgerAccounts(client)
        self.ledger_entries = company.LedgerEntries(client)
        self.ledger_attachments = company.LedgerAttachments(client)
        self.ledger_entry_lines = company.LedgerEntryLines(client)
        self.trial_balance = company.TrialBalance(client)
        self.fiscal_years = company.FiscalYears(client)
        self.categories = company.Categories(client)
        self.category_groups = company.CategoryGroups(client)
        self.exports = company.Exports(client)
        self.sepa_mandates = company.SepaMandates(client)
        self.gocardless_mandates = company.GocardlessMandates(client)
        self.pro_account = company.ProAccount(client)
        self.e_invoices = company.EInvoices(client)
        self.pa_registrations = company.PaRegistrations(client)
        self.file_attachments = company.FileAttachments(client)
        self.changelogs = company.Changelogs(client)
        self.webhook_subscriptions = company.WebhookSubscriptions(client)
        self.me = company.Me(client)

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> Pennylane:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncPennylane:
    """Asynchronous client for the Pennylane Company API (v2).

    Same options as :class:`Pennylane`. Usage::

        from pennylane_sdk import AsyncPennylane

        async with AsyncPennylane() as client:
            page = await client.customer_invoices.list()
            async for invoice in page:
                print(invoice.invoice_number)
    """

    # Invoicing (sales)
    customer_invoices: company.AsyncCustomerInvoices
    customer_invoice_templates: company.AsyncCustomerInvoiceTemplates
    quotes: company.AsyncQuotes
    commercial_documents: company.AsyncCommercialDocuments
    billing_subscriptions: company.AsyncBillingSubscriptions
    customers: company.AsyncCustomers
    products: company.AsyncProducts
    # Purchases
    suppliers: company.AsyncSuppliers
    supplier_invoices: company.AsyncSupplierInvoices
    purchase_requests: company.AsyncPurchaseRequests
    # Banking
    transactions: company.AsyncTransactions
    bank_accounts: company.AsyncBankAccounts
    bank_establishments: company.AsyncBankEstablishments
    # Accounting
    journals: company.AsyncJournals
    ledger_accounts: company.AsyncLedgerAccounts
    ledger_entries: company.AsyncLedgerEntries
    ledger_attachments: company.AsyncLedgerAttachments
    ledger_entry_lines: company.AsyncLedgerEntryLines
    trial_balance: company.AsyncTrialBalance
    fiscal_years: company.AsyncFiscalYears
    # Analytics
    categories: company.AsyncCategories
    category_groups: company.AsyncCategoryGroups
    # Exports
    exports: company.AsyncExports
    # Payment mandates
    sepa_mandates: company.AsyncSepaMandates
    gocardless_mandates: company.AsyncGocardlessMandates
    pro_account: company.AsyncProAccount
    # French e-invoicing
    e_invoices: company.AsyncEInvoices
    pa_registrations: company.AsyncPaRegistrations
    # Misc
    file_attachments: company.AsyncFileAttachments
    changelogs: company.AsyncChangelogs
    webhook_subscriptions: company.AsyncWebhookSubscriptions
    me: company.AsyncMe

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        token = _resolve_token(api_token, _COMPANY_TOKEN_ENV, "AsyncPennylane")
        throttle = AsyncRateThrottle(*COMPANY_RATE_LIMIT) if auto_throttle else None
        self._client = AsyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_COMPANY_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        client = self._client
        self.customer_invoices = company.AsyncCustomerInvoices(client)
        self.customer_invoice_templates = company.AsyncCustomerInvoiceTemplates(client)
        self.quotes = company.AsyncQuotes(client)
        self.commercial_documents = company.AsyncCommercialDocuments(client)
        self.billing_subscriptions = company.AsyncBillingSubscriptions(client)
        self.customers = company.AsyncCustomers(client)
        self.products = company.AsyncProducts(client)
        self.suppliers = company.AsyncSuppliers(client)
        self.supplier_invoices = company.AsyncSupplierInvoices(client)
        self.purchase_requests = company.AsyncPurchaseRequests(client)
        self.transactions = company.AsyncTransactions(client)
        self.bank_accounts = company.AsyncBankAccounts(client)
        self.bank_establishments = company.AsyncBankEstablishments(client)
        self.journals = company.AsyncJournals(client)
        self.ledger_accounts = company.AsyncLedgerAccounts(client)
        self.ledger_entries = company.AsyncLedgerEntries(client)
        self.ledger_attachments = company.AsyncLedgerAttachments(client)
        self.ledger_entry_lines = company.AsyncLedgerEntryLines(client)
        self.trial_balance = company.AsyncTrialBalance(client)
        self.fiscal_years = company.AsyncFiscalYears(client)
        self.categories = company.AsyncCategories(client)
        self.category_groups = company.AsyncCategoryGroups(client)
        self.exports = company.AsyncExports(client)
        self.sepa_mandates = company.AsyncSepaMandates(client)
        self.gocardless_mandates = company.AsyncGocardlessMandates(client)
        self.pro_account = company.AsyncProAccount(client)
        self.e_invoices = company.AsyncEInvoices(client)
        self.pa_registrations = company.AsyncPaRegistrations(client)
        self.file_attachments = company.AsyncFileAttachments(client)
        self.changelogs = company.AsyncChangelogs(client)
        self.webhook_subscriptions = company.AsyncWebhookSubscriptions(client)
        self.me = company.AsyncMe(client)

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    async def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> AsyncPennylane:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()


class PennylaneFirm:
    """Synchronous client for the Pennylane Firm API (v1), for accounting firms.

    Args:
        api_token: Firm API token. Falls back to the
            ``PENNYLANE_FIRM_API_TOKEN`` environment variable.
        auto_throttle: When ``True`` (default), paces requests to the official
            Firm API limit of 5 requests per second.

    Other options are identical to :class:`Pennylane`. Usage::

        from pennylane_sdk import PennylaneFirm

        firm = PennylaneFirm()
        for company in firm.companies.list():
            print(company.name)
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        token = _resolve_token(api_token, _FIRM_TOKEN_ENV, "PennylaneFirm")
        throttle = RateThrottle(*FIRM_RATE_LIMIT) if auto_throttle else None
        self._client = SyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_FIRM_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        # Firm resources are attached once resources/firm is implemented.
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> PennylaneFirm:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncPennylaneFirm:
    """Asynchronous client for the Pennylane Firm API (v1), for accounting firms.

    Same options as :class:`PennylaneFirm`.
    """

    def __init__(
        self,
        api_token: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | httpx.Timeout | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        auto_throttle: bool = True,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        token = _resolve_token(api_token, _FIRM_TOKEN_ENV, "AsyncPennylaneFirm")
        throttle = AsyncRateThrottle(*FIRM_RATE_LIMIT) if auto_throttle else None
        self._client = AsyncAPIClient(
            api_token=token,
            base_url=base_url or DEFAULT_FIRM_BASE_URL,
            timeout=timeout,
            max_retries=max_retries,
            throttle=throttle,
            http_client=http_client,
        )
        self._attach_resources()

    def _attach_resources(self) -> None:
        # Firm resources are attached once resources/firm is implemented.
        pass

    @property
    def last_rate_limit(self) -> RateLimitInfo | None:
        """Rate-limit state from the most recent API response."""
        return self._client.last_rate_limit

    async def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> AsyncPennylaneFirm:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()

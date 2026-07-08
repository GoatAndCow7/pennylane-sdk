from __future__ import annotations

import datetime as dt
from decimal import Decimal

from pennylane_sdk._models import Money, PennylaneModel, jsonable


class Invoice(PennylaneModel):
    id: int
    amount: Money | None = None
    date: dt.date | None = None


class TestPennylaneModel:
    def test_parses_money_string_to_decimal(self) -> None:
        invoice = Invoice.model_validate({"id": 1, "amount": "1234.56"})
        assert invoice.amount == Decimal("1234.56")

    def test_serializes_money_back_to_string(self) -> None:
        invoice = Invoice(id=1, amount=Decimal("0.10"))
        assert invoice.model_dump()["amount"] == "0.10"

    def test_money_never_uses_scientific_notation(self) -> None:
        invoice = Invoice(id=1, amount=Decimal("1E+4"))
        assert invoice.model_dump()["amount"] == "10000"

    def test_unknown_fields_are_preserved(self) -> None:
        invoice = Invoice.model_validate({"id": 1, "brand_new_field": "kept"})
        assert invoice.brand_new_field == "kept"  # type: ignore[attr-defined]

    def test_missing_optional_fields_default_to_none(self) -> None:
        invoice = Invoice.model_validate({"id": 1})
        assert invoice.amount is None
        assert invoice.date is None


class TestJsonable:
    def test_decimal_becomes_plain_string(self) -> None:
        assert jsonable(Decimal("19.60")) == "19.60"
        assert jsonable(Decimal("1E+2")) == "100"

    def test_dates_become_iso_strings(self) -> None:
        assert jsonable(dt.date(2026, 1, 31)) == "2026-01-31"
        assert jsonable(dt.datetime(2026, 1, 31, 12, 30)) == "2026-01-31T12:30:00"

    def test_nested_structures(self) -> None:
        payload = {
            "customer_id": 42,
            "invoice_lines": [
                {"quantity": Decimal("2"), "raw_currency_unit_price": Decimal("10.50")},
            ],
            "date": dt.date(2026, 7, 8),
        }
        assert jsonable(payload) == {
            "customer_id": 42,
            "invoice_lines": [{"quantity": "2", "raw_currency_unit_price": "10.50"}],
            "date": "2026-07-08",
        }

    def test_models_dump_only_set_fields(self) -> None:
        invoice = Invoice(id=1)
        assert jsonable(invoice) == {"id": 1}

    def test_plain_values_pass_through(self) -> None:
        assert jsonable("text") == "text"
        assert jsonable(3) == 3
        assert jsonable(None) is None
        assert jsonable(True) is True

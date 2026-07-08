"""Helpers to build Pennylane list filters.

The Pennylane API filters list endpoints through a ``filter`` query parameter
containing a JSON array of conditions::

    [{"field": "date", "operator": "gteq", "value": "2026-01-01"}]

This module provides typed helpers so you never have to hand-write that JSON:

    from pennylane_sdk import filters

    client.customer_invoices.list(
        filter=[filters.gte("date", "2026-01-01"), filters.eq("status", "upcoming")],
    )

Supported operators (availability varies by field, see the endpoint docs):
``eq``, ``not_eq``, ``lt``, ``lteq``, ``gt``, ``gteq``, ``in``, ``not_in``.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

__all__ = [
    "Filter",
    "encode_filters",
    "eq",
    "gt",
    "gte",
    "in_",
    "lt",
    "lte",
    "not_eq",
    "not_in",
    "where",
]

FilterValue = str | int | float | bool | Decimal | _dt.date | _dt.datetime | None


@dataclass(frozen=True)
class Filter:
    """A single filter condition (field, operator, value)."""

    field: str
    operator: str
    value: FilterValue | list[FilterValue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "operator": self.operator,
            "value": _encode_value(self.value),
        }


def _encode_value(value: FilterValue | list[FilterValue]) -> Any:
    if isinstance(value, list):
        return [_encode_value(item) for item in value]
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (_dt.datetime, _dt.date)):
        return value.isoformat()
    return value


def where(field: str, operator: str, value: FilterValue | list[FilterValue]) -> Filter:
    """Build a filter with an arbitrary operator."""
    return Filter(field, operator, value)


def eq(field: str, value: FilterValue) -> Filter:
    """``field == value``"""
    return Filter(field, "eq", value)


def not_eq(field: str, value: FilterValue) -> Filter:
    """``field != value``"""
    return Filter(field, "not_eq", value)


def lt(field: str, value: FilterValue) -> Filter:
    """``field < value``"""
    return Filter(field, "lt", value)


def lte(field: str, value: FilterValue) -> Filter:
    """``field <= value`` (Pennylane operator ``lteq``)"""
    return Filter(field, "lteq", value)


def gt(field: str, value: FilterValue) -> Filter:
    """``field > value``"""
    return Filter(field, "gt", value)


def gte(field: str, value: FilterValue) -> Filter:
    """``field >= value`` (Pennylane operator ``gteq``)"""
    return Filter(field, "gteq", value)


def in_(field: str, values: list[FilterValue]) -> Filter:
    """``field IN values``"""
    return Filter(field, "in", values)


def not_in(field: str, values: list[FilterValue]) -> Filter:
    """``field NOT IN values``"""
    return Filter(field, "not_in", values)


FiltersInput = str | Filter | dict[str, Any] | list[Filter | dict[str, Any]]


def encode_filters(filters: FiltersInput) -> str:
    """Encode filters into the JSON string the API expects.

    Accepts a single :class:`Filter`, a raw dict, a list mixing both, or an
    already-encoded JSON string (returned unchanged).
    """
    if isinstance(filters, str):
        return filters
    if isinstance(filters, (Filter, dict)):
        filters = [filters]
    encoded: list[dict[str, Any]] = []
    for item in filters:
        if isinstance(item, Filter):
            encoded.append(item.to_dict())
        elif isinstance(item, dict):
            encoded.append({key: _encode_value(value) for key, value in item.items()})
        else:
            raise TypeError(f"Unsupported filter type: {type(item).__name__}")
    return json.dumps(encoded, ensure_ascii=False)

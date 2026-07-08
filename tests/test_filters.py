from __future__ import annotations

import datetime as dt
import json
from decimal import Decimal

import pytest

from pennylane_sdk import filters


class TestFilterHelpers:
    @pytest.mark.parametrize(
        ("helper", "operator"),
        [
            (filters.eq, "eq"),
            (filters.not_eq, "not_eq"),
            (filters.lt, "lt"),
            (filters.lte, "lteq"),
            (filters.gt, "gt"),
            (filters.gte, "gteq"),
        ],
    )
    def test_scalar_helpers(self, helper, operator: str) -> None:
        condition = helper("date", "2026-01-01")
        assert condition.to_dict() == {
            "field": "date",
            "operator": operator,
            "value": "2026-01-01",
        }

    def test_membership_helpers(self) -> None:
        assert filters.in_("status", ["draft", "upcoming"]).to_dict() == {
            "field": "status",
            "operator": "in",
            "value": ["draft", "upcoming"],
        }
        assert filters.not_in("id", [1, 2]).operator == "not_in"

    def test_where_arbitrary_operator(self) -> None:
        assert filters.where("amount", "gteq", 100).operator == "gteq"

    def test_date_and_decimal_values_are_encoded(self) -> None:
        assert filters.gte("date", dt.date(2026, 1, 1)).to_dict()["value"] == "2026-01-01"
        assert filters.eq("amount", Decimal("10.50")).to_dict()["value"] == "10.50"


class TestEncodeFilters:
    def test_encodes_filter_list_to_json(self) -> None:
        encoded = filters.encode_filters(
            [filters.gte("date", "2026-01-01"), filters.eq("status", "upcoming")]
        )
        assert json.loads(encoded) == [
            {"field": "date", "operator": "gteq", "value": "2026-01-01"},
            {"field": "status", "operator": "eq", "value": "upcoming"},
        ]

    def test_accepts_single_filter(self) -> None:
        encoded = filters.encode_filters(filters.eq("status", "draft"))
        assert json.loads(encoded) == [{"field": "status", "operator": "eq", "value": "draft"}]

    def test_accepts_raw_dicts(self) -> None:
        encoded = filters.encode_filters([{"field": "id", "operator": "eq", "value": 1}])
        assert json.loads(encoded) == [{"field": "id", "operator": "eq", "value": 1}]

    def test_passes_through_pre_encoded_json(self) -> None:
        raw = '[{"field":"id","operator":"eq","value":1}]'
        assert filters.encode_filters(raw) == raw

    def test_rejects_unsupported_types(self) -> None:
        with pytest.raises(TypeError, match="Unsupported filter type"):
            filters.encode_filters([42])  # type: ignore[list-item]

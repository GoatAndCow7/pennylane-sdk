"""Models for the Categories and Category Groups resources (Firm API v1)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = [
    "FirmCategory",
    "FirmCategoryGroup",
    "FirmCategoryGroupCategoriesLink",
    "FirmCategoryGroupRef",
]


class FirmCategoryGroupRef(PennylaneModel):
    """Minimal reference to the category group a category belongs to."""

    id: int | None = None


class FirmCategoryGroupCategoriesLink(PennylaneModel):
    """Link to the categories of a category group."""

    url: str | None = None


class FirmCategory(PennylaneModel):
    """A category used to classify transactions and invoice lines.

    Reference: https://firm-pennylane.readme.io/reference/getcategory
    """

    id: int
    label: str | None = None
    direction: str | None = None
    analytical_code: str | None = None
    category_group: FirmCategoryGroupRef | None = None
    archived_at: dt.datetime | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class FirmCategoryGroup(PennylaneModel):
    """A group of categories.

    Reference: https://firm-pennylane.readme.io/reference/getcategorygroup
    """

    id: int
    label: str | None = None
    categories: FirmCategoryGroupCategoriesLink | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None

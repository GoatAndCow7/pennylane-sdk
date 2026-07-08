"""Models for the Categories and Category Groups resources (Company API v2)."""

from __future__ import annotations

import datetime as dt

from ..._models import PennylaneModel

__all__ = ["Category", "CategoryGroup", "CategoryGroupCategoriesLink", "CategoryGroupRef"]


class CategoryGroupRef(PennylaneModel):
    """Minimal reference to the category group a category belongs to."""

    id: int | None = None


class CategoryGroupCategoriesLink(PennylaneModel):
    """Link to the categories of a category group."""

    url: str | None = None


class Category(PennylaneModel):
    """A category used to classify transactions and invoice lines.

    Reference: https://pennylane.readme.io/reference/getcategory
    """

    id: int
    label: str | None = None
    direction: str | None = None
    analytical_code: str | None = None
    category_group: CategoryGroupRef | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None


class CategoryGroup(PennylaneModel):
    """A group of categories.

    Reference: https://pennylane.readme.io/reference/getcategorygroup
    """

    id: int
    label: str | None = None
    categories: CategoryGroupCategoriesLink | None = None
    created_at: dt.datetime | None = None
    updated_at: dt.datetime | None = None

"""Base Pydantic model and serialization helpers.

The Pennylane API v2 transmits monetary values as strings (to avoid float
rounding), and expects the same on input. :data:`Money` is an annotated
``Decimal`` that serializes back to a plain string, and :func:`jsonable`
recursively prepares arbitrary user input (dicts, models, Decimals, dates)
for JSON encoding.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, PlainSerializer

__all__ = ["Money", "PennylaneModel", "jsonable"]


def _decimal_to_string(value: Decimal) -> str:
    """Render a Decimal as a plain decimal string (never scientific notation)."""
    return format(value, "f")


# Monetary amount: parsed from the API's string representation into a Decimal,
# serialized back to a plain string as the API requires.
Money = Annotated[Decimal, PlainSerializer(_decimal_to_string, return_type=str)]


class PennylaneModel(BaseModel):
    """Base class for every API object returned by the SDK.

    Unknown fields returned by the API are preserved (``extra="allow"``)
    instead of raising, so a Pennylane-side addition never breaks the SDK.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)


def jsonable(value: Any) -> Any:
    """Recursively convert a request payload into JSON-encodable data.

    Handles the Pennylane-specific conventions:

    - ``Decimal`` → plain string (the API requires monetary values as strings)
    - ``date`` / ``datetime`` → ISO 8601 string
    - ``PennylaneModel`` / any Pydantic model → dict of its set fields
    """
    if isinstance(value, BaseModel):
        return jsonable(value.model_dump(exclude_unset=True))
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, Decimal):
        return _decimal_to_string(value)
    if isinstance(value, _dt.datetime):
        return value.isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    return value

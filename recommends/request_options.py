import typing as t
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class GetBookOptions:
    sku: str
    min: t.Optional[float]
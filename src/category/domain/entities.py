from dataclasses import dataclass, field
import datetime as dt
import typing as t
import uuid

# O frozen evita o comportamento anêmico com as entidades
@dataclass(kw_only=True, frozen=True)
class Category:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str
    description: t.Optional[str] = None
    is_active: bool = True
    created_at: dt.datetime = field(default_factory=dt.datetime.now)

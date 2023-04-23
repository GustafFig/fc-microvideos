from dataclasses import dataclass, field
import datetime as dt
import typing as t

from __seedwork.domain.entities import Entity, ToggleIsActive

# O frozen evita o comportamento anêmico com as entidades


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity, ToggleIsActive):

    name: str
    description: t.Optional[str] = None
    is_active: bool = True
    created_at: dt.datetime = field(default_factory=dt.datetime.now)

    def update(self, *, name: str, description: t.Optional[str]) -> None:
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)

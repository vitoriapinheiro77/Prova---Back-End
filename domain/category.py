import uuid
from dataclasses import dataclass, field
from typing import Optional, List, Any
from events.category_events import (
    CategoryCreated, CategoryUpdated, CategoryActivated, CategoryDeactivated
)

MAX_NAME = 255

@dataclass(eq=True)
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: Optional[str] = field(default=None)
    
    events: List[Any] = field(default_factory=list, init=False, repr=False, compare=False)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
            
        self.name = self._validate_name(self.name)
        self.description = self.description or ""
        self.is_active = bool(self.is_active)
        
        self._add_domain_event(CategoryCreated(
            category_id=self.id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        ))
    
    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        data['class_name'] = self.__class__.__name__ 
        data.pop('events', None) 
        return data

    @classmethod
    def from_dict(cls, data: dict):
        data.pop('class_name', None) 
        return cls(
            name=data['name'],
            description=data.get('description', ''),
            is_active=data.get('is_active', True),
            id=data.get('id')
        )
    

    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        old_name = self.name
        old_description = self.description
        updated = False
        
        if name is not None and name != self.name:
            self.name = self._validate_name(name)
            updated = True
        
        if description is not None and description != self.description:
            self.description = description
            updated = True

        if updated:
            self._add_domain_event(CategoryUpdated(
                category_id=self.id,
                old_name=old_name,
                new_name=self.name,
                old_description=old_description,
                new_description=self.description
            ))

    def activate(self) -> None:
        if not self.is_active: 
            self.is_active = True
            self._add_domain_event(CategoryActivated(category_id=self.id))

    def deactivate(self) -> None:
        if self.is_active: 
            self.is_active = False
            self._add_domain_event(CategoryDeactivated(category_id=self.id))

    
    def _add_domain_event(self, event) -> None:
        self.events.append(event)
        
    def clear_domain_events(self) -> List[Any]:
        events = self.events[:]
        self.events.clear()
        return events
    
    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("name deve ser string")
        n = name.strip()
        if not n:
            raise ValueError("name é obrigatório")
        if len(n) > MAX_NAME:
            raise ValueError(f"name deve ter no máximo {MAX_NAME} caracteres")
        return n
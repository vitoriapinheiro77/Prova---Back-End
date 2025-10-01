import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass(frozen=True) 
class DomainEvent:
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    
    occurred_on: datetime = field(default_factory=datetime.now, init=False)
    
    class_name: ClassVar[str] = 'DomainEvent'
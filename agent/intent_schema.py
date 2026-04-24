from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DeclaredIntent:
    task: str
    allowed_tools: List[str]
    allowed_recipients: List[str] = field(default_factory=list)
    allowed_queries: List[str] = field(default_factory=list)
    max_emails: Optional[int] = None
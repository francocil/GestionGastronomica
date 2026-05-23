from typing import Optional

class AuthenticatedState:
    user_id: Optional[int] = None
    tenant_id: Optional[int] = None
    role: Optional[str] = None

from dataclasses import dataclass
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from settings import Settings


@dataclass(frozen=True)
class SupabaseTokenPayload:
    sub: str       # Supabase user UUID
    email: str     # rider email — used as identity key in snaap_riders
    exp: int


class SupabaseTokenHandler:
    """
    Verifies Supabase-issued JWTs offline using the project JWT secret.

    The secret is found in:
      Supabase Dashboard → Project Settings → API → JWT Settings → JWT Secret
    """

    _AUDIENCE = "authenticated"

    def __init__(self, settings: Settings) -> None:
        self.secret = settings.supabase_jwt_secret
        self.algorithm = "HS256"

    def decode(self, token: str) -> SupabaseTokenPayload:
        """
        Decode and verify a Supabase Bearer token.
        Raises ValueError on any validation failure (expired, bad sig, missing claims).
        """
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self._AUDIENCE,
            )
        except InvalidTokenError as exc:
            raise ValueError("Could not validate Supabase token") from exc

        sub: Optional[str] = payload.get("sub")
        email: Optional[str] = payload.get("email")
        exp: Optional[int] = payload.get("exp")

        if not sub or not email or exp is None:
            raise ValueError("Supabase token is missing required claims (sub, email, exp)")

        return SupabaseTokenPayload(sub=sub, email=email, exp=exp)

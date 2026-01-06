# backend/auth.py
"""
FASE 0: JWT Authentication and RBAC Utilities

This module provides JWT token generation, validation, and role-based access control.
"""

import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class JWTConfig(BaseModel):
    """JWT Configuration"""
    secret_key: str
    algorithm: str
    audience: str
    expiration_hours: int

    @classmethod
    def from_env(cls):
        """Load JWT configuration from environment variables"""
        return cls(
            secret_key=os.getenv("JWT_SECRET_KEY", "your-256-bit-secret-key-change-in-production"),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            audience=os.getenv("JWT_AUDIENCE", "maas-v4-0"),
            expiration_hours=int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
        )


class JWTPayload(BaseModel):
    """JWT Token Payload"""
    sub: str  # Subject (user_id)
    aud: str  # Audience
    iat: int  # Issued at
    exp: int  # Expiration time
    scopes: List[str]  # User scopes/roles
    session_id: Optional[str] = None
    project_id: Optional[int] = None


class JWTManager:
    """Manages JWT token generation and validation"""
    
    def __init__(self, config: JWTConfig):
        self.config = config
    
    def generate_token(
        self,
        user_id: str,
        scopes: List[str],
        session_id: Optional[str] = None,
        project_id: Optional[int] = None
    ) -> str:
        """
        Generate a JWT token.
        
        Args:
            user_id: User identifier
            scopes: List of allowed scopes (e.g., ["workflows:DocumentCreationWorkflow:run"])
            session_id: Optional session identifier
            project_id: Optional project identifier
            
        Returns:
            Encoded JWT token
        """
        import time
        now_ts = int(time.time())
        iat = now_ts - 60  # 1 minute leeway for clock skew
        expiration = now_ts + (self.config.expiration_hours * 3600)
        
        payload = {
            "sub": user_id,
            "aud": self.config.audience,
            "iat": iat,
            "exp": expiration,
            "scopes": scopes,
            "session_id": session_id,
            "project_id": project_id
        }
        
        token = jwt.encode(
            payload,
            self.config.secret_key,
            algorithm=self.config.algorithm
        )
        
        logger.info(f"✅ Token generated for user {user_id} with scopes {scopes}")
        return token
    
    def validate_token(self, token: str) -> Optional[JWTPayload]:
        """
        Validate a JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            JWTPayload if valid, None otherwise
        """
        try:
            decoded = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                audience=self.config.audience,
                options={"verify_exp": True},
                leeway=10
            )
            
            payload = JWTPayload(**decoded)
            logger.info(f"✅ Token validated for user {payload.sub}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ Token has expired")
            return None
        except jwt.InvalidAudienceError:
            logger.warning("⚠️ Invalid audience in token")
            return None
        except jwt.InvalidSignatureError:
            logger.warning("⚠️ Invalid token signature")
            return None
        except Exception as e:
            logger.error(f"❌ Error validating token: {str(e)}")
            return None
    
    def verify_scope(self, token_payload: JWTPayload, required_scope: str) -> bool:
        """
        Verify if token has required scope.
        
        Args:
            token_payload: Decoded JWT payload
            required_scope: Required scope (e.g., "workflows:DocumentCreationWorkflow:run")
            
        Returns:
            True if token has the scope, False otherwise
        """
        has_scope = required_scope in token_payload.scopes or "*:*" in token_payload.scopes
        
        if not has_scope:
            logger.warning(f"⚠️ User {token_payload.sub} lacks scope {required_scope}")
        
        return has_scope


# RBAC Roles
RBAC_ROLES = {
    "VIEWER": {
        "scopes": ["agents:read", "sessions:read"],
        "description": "Read-only access to agents and sessions"
    },
    "OPERATOR": {
        "scopes": ["workflows:DocumentCreationWorkflow:run", "sessions:write", "agents:read"],
        "description": "Can run workflows and write sessions"
    },
    "ADMIN": {
        "scopes": ["*:*"],
        "description": "Full access to all resources"
    }
}


def get_scopes_for_role(role: str) -> List[str]:
    """Get scopes for a given role"""
    return RBAC_ROLES.get(role, {}).get("scopes", [])


# Singleton JWT Manager (initialized at startup)
jwt_config = JWTConfig.from_env()
jwt_manager = JWTManager(jwt_config)


# Test helper function
def create_test_token(
    user_id: str = "test-user",
    role: str = "OPERATOR"
) -> str:
    """Create a test JWT token for development"""
    scopes = get_scopes_for_role(role)
    return jwt_manager.generate_token(
        user_id=user_id,
        scopes=scopes,
        session_id="test-session-001"
    )


if __name__ == "__main__":
    # Test token generation
    print("🧪 Testing JWT Token Generation")
    token = create_test_token()
    print(f"Token: {token[:50]}...")
    
    # Test token validation
    payload = jwt_manager.validate_token(token)
    if payload:
        print(f"✅ Token valid for user: {payload.sub}")
        print(f"   Scopes: {payload.scopes}")
    else:
        print("❌ Token validation failed")

# Auth Manager Service
# Handles authentication and authorization

import jwt
import datetime
from typing import Optional, Dict, Any

class AuthManager:
    def __init__(self, secret_key: str = "your-secret-key"):
        self.secret_key = secret_key

    def generate_token(self, user_id: int, username: str, role: str) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Extract user info from token"""
        payload = self.verify_token(token)
        if payload:
            return {
                'user_id': payload['user_id'],
                'username': payload['username'],
                'role': payload['role']
            }
        return None

    def check_permission(self, user_role: str, required_role: str) -> bool:
        """Check if user has required permission"""
        role_hierarchy = {
            'user': 1,
            'analyst': 2,
            'admin': 3
        }

        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)

        return user_level >= required_level

# Global instance
auth_manager = AuthManager()

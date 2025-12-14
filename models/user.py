"""User model implemented as a class.

Private attributes, getters, `to_dict` and `__str__`.
"""

from typing import Optional, Dict, Any


class User:
	"""Represents a user in the system."""

	def __init__(self, user_id: str, username: str, email: Optional[str] = None,
				 role: str = "user", active: bool = True, extra: Optional[Dict[str, Any]] = None):
		self.__user_id = user_id
		self.__username = username
		self.__email = email
		self.__role = role
		self.__active = active
		self.__extra = extra or {}

	# Accessors
	def get_id(self) -> str:
		return self.__user_id

	def get_username(self) -> str:
		return self.__username

	def get_email(self) -> Optional[str]:
		return self.__email

	def get_role(self) -> str:
		return self.__role

	def is_active(self) -> bool:
		return self.__active

	def get_extra(self) -> Dict[str, Any]:
		return self.__extra

	# Small helpers
	def deactivate(self):
		self.__active = False

	def activate(self):
		self.__active = True

	def to_dict(self) -> Dict[str, Any]:
		return {
			"user_id": self.__user_id,
			"username": self.__username,
			"email": self.__email,
			"role": self.__role,
			"active": self.__active,
			"extra": self.__extra,
		}

	def __str__(self) -> str:
		return f"User(id={self.__user_id}, username={self.__username}, role={self.__role})"


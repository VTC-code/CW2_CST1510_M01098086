"""IT ticket model implemented as a class.

Provides private attributes, getters, `to_dict`, and `__str__`.
"""

from typing import Optional, Dict, Any
from datetime import datetime


class ITTicket:
	"""Represents an IT support ticket."""

	def __init__(self, ticket_id: str, title: str, description: str,
				 status: str = "open", created_at: Optional[datetime] = None,
				 reporter: Optional[str] = None, assigned_to: Optional[str] = None):
		self.__ticket_id = ticket_id
		self.__title = title
		self.__description = description
		self.__status = status
		self.__created_at = created_at or datetime.utcnow()
		self.__reporter = reporter
		self.__assigned_to = assigned_to

	# Accessors
	def get_id(self) -> str:
		return self.__ticket_id

	def get_title(self) -> str:
		return self.__title

	def get_description(self) -> str:
		return self.__description

	def get_status(self) -> str:
		return self.__status

	def get_created_at(self) -> datetime:
		return self.__created_at

	def get_reporter(self) -> Optional[str]:
		return self.__reporter

	def get_assigned_to(self) -> Optional[str]:
		return self.__assigned_to

	# Mutators (small, controlled setters)
	def set_status(self, new_status: str):
		self.__status = new_status

	def assign_to(self, assignee: str):
		self.__assigned_to = assignee

	# Serialization
	def to_dict(self) -> Dict[str, Any]:
		return {
			"ticket_id": self.__ticket_id,
			"title": self.__title,
			"description": self.__description,
			"status": self.__status,
			"created_at": self.__created_at.isoformat(),
			"reporter": self.__reporter,
			"assigned_to": self.__assigned_to,
		}

	def __str__(self) -> str:
		return f"ITTicket(id={self.__ticket_id}, title={self.__title}, status={self.__status})"


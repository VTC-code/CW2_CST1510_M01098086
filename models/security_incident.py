"""Security incident model implemented as a class.

Includes private attributes, getters, a `to_dict` method and `__str__`.
"""

from typing import Optional, Dict, Any
from datetime import datetime


class SecurityIncident:
	"""Represents a security/cyber incident."""

	def __init__(self, incident_id: str, incident_type: str, severity: str,
				 description: Optional[str] = None, reported_at: Optional[datetime] = None):
		self.__incident_id = incident_id
		self.__incident_type = incident_type
		self.__severity = severity
		self.__description = description
		self.__reported_at = reported_at or datetime.utcnow()

	# Accessors
	def get_id(self) -> str:
		return self.__incident_id

	def get_type(self) -> str:
		return self.__incident_type

	def get_severity(self) -> str:
		return self.__severity

	def get_description(self) -> Optional[str]:
		return self.__description

	def get_reported_at(self) -> datetime:
		return self.__reported_at

	def to_dict(self) -> Dict[str, Any]:
		return {
			"incident_id": self.__incident_id,
			"incident_type": self.__incident_type,
			"severity": self.__severity,
			"description": self.__description,
			"reported_at": self.__reported_at.isoformat(),
		}

	def __str__(self) -> str:
		return f"SecurityIncident(id={self.__incident_id}, type={self.__incident_type}, severity={self.__severity})"


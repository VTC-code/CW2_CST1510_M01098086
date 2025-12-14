"""Dataset model implemented as a class with private attributes.

The class follows the pattern used in the Car/Vehicle example: private
attributes, accessor methods (getters), a `to_dict` serializer and a
user-friendly `__str__`.
"""

from typing import Optional, Dict, Any


class Dataset:
	"""Represents a dataset in the system.

	Attributes (private):
		__dataset_id: unique identifier for the dataset
		__name: human readable name
		__description: optional description
		__source: optional source (file, url, owner)
		__metadata: optional metadata dictionary
	"""

	def __init__(self, dataset_id: str, name: str, description: Optional[str] = None,
				 source: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
		self.__dataset_id = dataset_id
		self.__name = name
		self.__description = description
		self.__source = source
		self.__metadata = metadata or {}

	# Accessors
	def get_id(self) -> str:
		return self.__dataset_id

	def get_name(self) -> str:
		return self.__name

	def get_description(self) -> Optional[str]:
		return self.__description

	def get_source(self) -> Optional[str]:
		return self.__source

	def get_metadata(self) -> Dict[str, Any]:
		return self.__metadata

	# Utility
	def to_dict(self) -> Dict[str, Any]:
		return {
			"dataset_id": self.__dataset_id,
			"name": self.__name,
			"description": self.__description,
			"source": self.__source,
			"metadata": self.__metadata,
		}

	def __str__(self) -> str:
		return f"Dataset(id={self.__dataset_id}, name={self.__name})"

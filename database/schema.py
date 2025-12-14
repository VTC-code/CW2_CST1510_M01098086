"""Database schema helper that can generate or apply simple table definitions.

This module intentionally keeps SQL simple and optional: calling
`create_tables(execute=True)` will attempt to open the sqlite database at
`platform.db` (or a custom path) and create four tables that mirror the
models. By default it only returns the SQL statements so it's safe to run
without side effects.
"""

import sqlite3
from typing import List


class DatabaseSchema:
	def __init__(self, db_path: str = "platform.db"):
		self.__db_path = db_path

	def get_create_statements(self) -> List[str]:
		"""Return SQL statements (strings) for creating the tables."""
		return [
			# datasets
			"""
			CREATE TABLE IF NOT EXISTS datasets (
				dataset_id TEXT PRIMARY KEY,
				name TEXT NOT NULL,
				description TEXT,
				source TEXT
			);
			""",
			# it_tickets
			"""
			CREATE TABLE IF NOT EXISTS it_tickets (
				ticket_id TEXT PRIMARY KEY,
				title TEXT NOT NULL,
				description TEXT,
				status TEXT,
				created_at TEXT,
				reporter TEXT,
				assigned_to TEXT
			);
			""",
			# security_incidents
			"""
			CREATE TABLE IF NOT EXISTS security_incidents (
				incident_id TEXT PRIMARY KEY,
				incident_type TEXT,
				severity TEXT,
				description TEXT,
				reported_at TEXT
			);
			""",
			# users
			"""
			CREATE TABLE IF NOT EXISTS users (
				user_id TEXT PRIMARY KEY,
				username TEXT NOT NULL,
				email TEXT,
				role TEXT,
				active INTEGER
			);
			""",
		]

	def create_tables(self, execute: bool = False) -> List[str]:
		"""Return the CREATE statements and optionally execute them.

		If `execute` is True the SQL will be executed against the sqlite
		database at `self.__db_path`. Default is False to avoid accidental
		writes.
		"""
		stmts = self.get_create_statements()
		if not execute:
			return stmts

		conn = sqlite3.connect(self.__db_path)
		try:
			cur = conn.cursor()
			for s in stmts:
				cur.executescript(s)
			conn.commit()
		finally:
			conn.close()

		return stmts


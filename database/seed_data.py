"""Small seed-data helper that demonstrates creating model instances.

This module constructs a few model objects (using the new classes in
`models/`) and provides an optional `apply_to_db` helper which can insert
the seed rows into the sqlite database created by `DatabaseSchema`.

By default this module only constructs Python objects and prints them so
it's safe to run during development.
"""

from datetime import datetime
from typing import List

from models.dataset import Dataset
from models.it_ticket import ITTicket
from models.security_incident import SecurityIncident
from models.user import User
from .schema import DatabaseSchema


def build_seed_objects():
	datasets = [
		Dataset("ds1", "Cyber Incidents", description="Historic cyber incident log", source="DATA/cyber_incidents.csv"),
		Dataset("ds2", "IT Tickets", description="Support ticket export", source="DATA/it_tickets.csv"),
	]

	users = [
		User("u1", "alice", email="alice@example.com", role="admin"),
		User("u2", "bob", email="bob@example.com", role="user"),
	]

	tickets = [
		ITTicket("t1", "Cannot login", "User cannot login to VPN", status="open", reporter="alice"),
		ITTicket("t2", "Email issue", "Delayed mail delivery", status="resolved", reporter="bob"),
	]

	incidents = [
		SecurityIncident("inc1", "phishing", "low", description="Phishing email reported by user"),
		SecurityIncident("inc2", "malware", "high", description="Detected malware on endpoint"),
	]

	return {
		"datasets": datasets,
		"users": users,
		"tickets": tickets,
		"incidents": incidents,
	}


def apply_to_db(db_path: str = "platform.db") -> None:
	"""Create tables (if needed) and insert seed rows.

	NOTE: this will modify the sqlite database at `db_path`. It's a
	convenience helper for local development only.
	"""
	schema = DatabaseSchema(db_path)
	schema.create_tables(execute=True)

	import sqlite3

	seeds = build_seed_objects()

	conn = sqlite3.connect(db_path)
	try:
		cur = conn.cursor()

		# users
		for u in seeds["users"]:
			cur.execute(
				"INSERT OR REPLACE INTO users (user_id, username, email, role, active) VALUES (?, ?, ?, ?, ?)",
				(u.get_id(), u.get_username(), u.get_email(), u.get_role(), 1 if u.is_active() else 0),
			)

		# datasets
		for d in seeds["datasets"]:
			cur.execute(
				"INSERT OR REPLACE INTO datasets (dataset_id, name, description, source) VALUES (?, ?, ?, ?)",
				(d.get_id(), d.get_name(), d.get_description(), d.get_source()),
			)

		# it_tickets
		for t in seeds["tickets"]:
			cur.execute(
				"INSERT OR REPLACE INTO it_tickets (ticket_id, title, description, status, created_at, reporter, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
				(t.get_id(), t.get_title(), t.get_description(), t.get_status(), t.get_created_at().isoformat(), t.get_reporter(), t.get_assigned_to()),
			)

		# incidents
		for i in seeds["incidents"]:
			cur.execute(
				"INSERT OR REPLACE INTO security_incidents (incident_id, incident_type, severity, description, reported_at) VALUES (?, ?, ?, ?, ?)",
				(i.get_id(), i.get_type(), i.get_severity(), i.get_description(), i.get_reported_at().isoformat()),
			)

		conn.commit()
	finally:
		conn.close()


if __name__ == "__main__":
	# Demonstration run: build and print seed objects (safe) but do not write by default.
	seeds = build_seed_objects()
	for k, lst in seeds.items():
		print(f"\n=== {k.upper()} ===")
		for obj in lst:
			print(obj)


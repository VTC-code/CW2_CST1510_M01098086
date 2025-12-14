"""Quick smoke script to exercise the model classes.

Constructs one instance of each model, calls key methods, and prints results.
Run with the project venv to validate imports and basic behavior.
"""
from models.dataset import Dataset
from models.it_ticket import ITTicket
from models.security_incident import SecurityIncident
from models.user import User
from database import seed_data


def main():
    print("Running quick model smoke test...\n")

    d = Dataset("ds_quick", "Quick Dataset", description="Smoke test dataset", source="DATA/cyber_incidents.csv")
    print(d)
    print('to_dict:', d.to_dict())

    t = ITTicket("t_quick", "Quick Title", "Quick desc", reporter="tester")
    print(t)
    print('status before:', t.get_status())
    t.set_status('in_progress')
    print('status after:', t.get_status())
    print('ticket to_dict:', t.to_dict())

    s = SecurityIncident("inc_quick", "phishing", "low", description="Quick incident")
    print(s)
    print('incident to_dict:', s.to_dict())

    u = User("u_quick", "quickuser", email="q@example.com", role="tester")
    print(u)
    print('user active?', u.is_active())
    u.deactivate()
    print('user active after deactivate?', u.is_active())
    print('user to_dict:', u.to_dict())

    seeds = seed_data.build_seed_objects()
    print('\nSeed groups:', list(seeds.keys()))


if __name__ == '__main__':
    main()

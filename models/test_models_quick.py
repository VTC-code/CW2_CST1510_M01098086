# test_models_quick.py
from models.dataset import Dataset
from models.it_ticket import ITTicket
from models.security_incident import SecurityIncident
from models.user import User
from database import seed_data

def main():
    d = Dataset("ds1", "Sample", description="desc")
    t = ITTicket("t1", "Title", "desc")
    s = SecurityIncident("i1", "phishing", "low")
    u = User("u1", "alice", email="a@example.com")
    print(d)
    print(t)
    print(s)
    print(u)
    seeds = seed_data.build_seed_objects()
    print('Seed groups:', list(seeds.keys()))

if __name__ == '__main__':
    main()
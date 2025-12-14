import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="CRUD", layout="wide")

# --- AUTH ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Access denied. Please sign in.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("CRUD Operations")

base_dir = Path(__file__).parents[1]
data_dir = base_dir / "DATA"
data_dir.mkdir(exist_ok=True)

# defaults
incidents_db = data_dir / "incidents.db"
cyber_db = data_dir / "cyber_incidents.db"
tickets_csv = data_dir / "it_tickets.csv"

# try to import helpers (fall back to raw operations)
try:
    from app.data.incidents import add_incident_db, delete_incident_db, get_all_incidents
except Exception:
    add_incident_db = None
    delete_incident_db = None
    get_all_incidents = None

try:
    from app.data.tickets import add_ticket_csv, delete_ticket_csv
except Exception:
    add_ticket_csv = None
    delete_ticket_csv = None

st.divider()
st.subheader("Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Incidents")
    with st.form("add_inc"):
        title = st.text_input("Title", key="inc_add_title")
        severity = st.selectbox("Severity", ["low", "medium", "high"], index=1, key="inc_add_sev")
        status = st.selectbox("Status", ["open", "resolved", "closed"], index=0, key="inc_add_stat")
        if st.form_submit_button("Add"):
            try:
                if add_incident_db:
                    add_incident_db(incidents_db, title, severity, status)
                else:
                    conn = sqlite3.connect(str(incidents_db))
                    cur = conn.cursor()
                    cur.execute("CREATE TABLE IF NOT EXISTS cyber_incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, severity TEXT, status TEXT, date TEXT)")
                    cur.execute("INSERT INTO cyber_incidents (title,severity,status) VALUES (?,?,?)", (title, severity, status))
                    conn.commit()
                    conn.close()
                st.success("Incident added")
            except Exception as e:
                st.error(f"Add failed: {e}")

    with st.form("del_inc"):
        del_id = st.number_input("ID to delete", min_value=1, step=1, key="inc_del_id")
        if st.form_submit_button("Delete"):
            try:
                if delete_incident_db:
                    removed = delete_incident_db(incidents_db, int(del_id))
                else:
                    conn = sqlite3.connect(str(incidents_db))
                    cur = conn.cursor()
                    cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (int(del_id),))
                    conn.commit()
                    removed = cur.rowcount
                    conn.close()
                st.info(f"Removed: {removed}")
            except Exception as e:
                st.error(f"Delete failed: {e}")

with col2:
    st.markdown("### Tickets (CSV)")
    with st.form("add_ticket"):
        t_title = st.text_input("Title", key="tic_add_title")
        t_sev = st.selectbox("Severity", ["low", "medium", "high"], index=1, key="tic_add_sev")
        t_status = st.selectbox("Status", ["open", "closed"], index=0, key="tic_add_stat")
        if st.form_submit_button("Add Ticket"):
            try:
                ticket = {"title": t_title, "severity": t_sev, "status": t_status}
                if add_ticket_csv:
                    add_ticket_csv(tickets_csv, ticket)
                else:
                    # simple CSV append
                    df = pd.read_csv(tickets_csv) if tickets_csv.exists() else pd.DataFrame(columns=["id", "title", "severity", "status"])
                    if "id" in df.columns:
                        next_id = int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
                        ticket["id"] = next_id
                    df = pd.concat([df, pd.DataFrame([ticket])], ignore_index=True, sort=False)
                    df.to_csv(tickets_csv, index=False)
                st.success("Ticket added")
            except Exception as e:
                st.error(f"Add failed: {e}")

    with st.form("del_ticket"):
        tid = st.text_input("Ticket id to delete", key="tic_del_id")
        if st.form_submit_button("Delete Ticket"):
            try:
                removed = 0
                if delete_ticket_csv:
                    removed = delete_ticket_csv(tickets_csv, int(tid))
                else:
                    if tickets_csv.exists():
                        df = pd.read_csv(tickets_csv)
                        before = len(df)
                        df = df[df.get("id", pd.Series(range(len(df)))) != int(tid)]
                        df.to_csv(tickets_csv, index=False)
                        removed = before - len(df)
                st.info(f"Removed: {removed}")
            except Exception as e:
                st.error(f"Delete failed: {e}")

with col3:
    st.markdown("### Cyber_Incidents")
    with st.form("add_cy"):
        title = st.text_input("Title", key="cy_add_title")
        severity = st.selectbox("Severity", ["low", "medium", "high"], index=1, key="cy_add_sev")
        status = st.selectbox("Status", ["open", "resolved", "closed"], index=0, key="cy_add_stat")
        if st.form_submit_button("Add Cyber"):
            try:
                if add_incident_db:
                    add_incident_db(cyber_db, title, severity, status)
                else:
                    conn = sqlite3.connect(str(cyber_db))
                    cur = conn.cursor()
                    cur.execute("CREATE TABLE IF NOT EXISTS cyber_incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, severity TEXT, status TEXT, date TEXT)")
                    cur.execute("INSERT INTO cyber_incidents (title,severity,status) VALUES (?,?,?)", (title, severity, status))
                    conn.commit()
                    conn.close()
                st.success("Cyber incident added")
            except Exception as e:
                st.error(f"Add failed: {e}")

    with st.form("del_cy"):
        did = st.number_input("ID to delete", min_value=1, step=1, key="cy_del_id")
        if st.form_submit_button("Delete Cyber"):
            try:
                if delete_incident_db:
                    removed = delete_incident_db(cyber_db, int(did))
                else:
                    conn = sqlite3.connect(str(cyber_db))
                    cur = conn.cursor()
                    cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (int(did),))
                    conn.commit()
                    removed = cur.rowcount
                    conn.close()
                st.info(f"Removed: {removed}")
            except Exception as e:
                st.error(f"Delete failed: {e}")

st.divider()
st.subheader("Preview (short: Title / Severity / Status)")

def show_incident_table(db_path):
    try:
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query("SELECT id, title, severity, status FROM cyber_incidents ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        if not df.empty:
            st.table(df[["id","title","severity","status"]])
        else:
            st.write("No rows")
    except Exception:
        st.write("No DB or table")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("**Incidents (latest 10)**")
    show_incident_table(incidents_db)
with col_b:
    st.markdown("**Tickets (latest 10)**")
    try:
        if tickets_csv.exists():
            df = pd.read_csv(tickets_csv)
            short = pd.DataFrame({
                "id": df.get("id", pd.Series(range(1, len(df)+1))).astype(object),
                "title": df.get("title", ""),
                "severity": df.get("severity", ""),
                "status": df.get("status", "")
            })
            st.table(short.head(10))
        else:
            st.write("No tickets CSV")
    except Exception:
        st.write("Failed to read tickets")
with col_c:
    st.markdown("**Cyber_Incidents (latest 10)**")
    show_incident_table(cyber_db)
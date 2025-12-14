import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Dashboard", layout="wide")

# --- PAGE ACCESS CONTROL ---
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("Access denied. Please log in first.")
    if st.button("Return to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("📊 Dashboard")
st.success(f"Hello, {st.session_state.username}! You are now logged in.")

st.write("Welcome to your Week 09 dashboard area.")

st.divider()

if st.button("Sign Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been signed out.")
    st.switch_page("Home.py")

# --- Show tables for all CSVs found in project root and DATA/ folder ---
base_dir = Path(__file__).parents[1]  # week9 folder
csv_files = []
# project root CSVs
csv_files += sorted(base_dir.glob("*.csv"))
# DATA folder CSVs
data_dir = base_dir / "DATA"
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))
# unique, preserve order
seen = set()
csv_files = [p for p in csv_files if not (p in seen or seen.add(p))]

st.divider()
st.subheader("CSV Tables")

if not csv_files:
    st.info("No CSV files found in project root or DATA/ folder.")
else:
    for fp in csv_files:
        st.markdown(f"**{fp.name}** — {fp}")
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            st.error(f"Failed to read {fp.name}: {e}")
            continue
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"Showing first 10 rows of {fp.name} — {len(df)} rows × {len(df.columns)} columns.")
        try:
            summary = df.describe(include="all").transpose().fillna("")
            st.table(summary)
        except Exception:
            pass
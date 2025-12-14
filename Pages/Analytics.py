import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Analytics", layout="wide")

# --- PAGE AUTHENTICATION ---
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("You need to sign in to continue.")
    st.stop()

st.title("📈 Analytics Overview")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Threats", 14, "+2")
with col2:
    st.metric("Incidents Closed", 32, "+5")
with col3:
    st.metric("Pending Tickets", 6, "-1")

# quick sample chart
data = pd.DataFrame({"Time": ["Mon", "Tue", "Wed", "Thu", "Fri"], "CPU Usage": [45, 55, 70, 60, 50]})
st.line_chart(data, x="Time", y="CPU Usage")

# --- Load up to 3 CSVs and show visualizations (choose graph or pie) ---
base_dir = Path(__file__).parents[1]
csv_files = sorted(base_dir.glob("*.csv"))
data_dir = base_dir / "DATA"
if data_dir.exists():
    csv_files += sorted(data_dir.glob("*.csv"))
# keep unique, stable
csv_files = list(dict.fromkeys(csv_files))[:3]

if not csv_files:
    st.warning("No CSV files found in project root or DATA/ folder.")
else:
    st.divider()
    st.subheader("CSV Visualizations (pick type per file)")
    for fp in csv_files:
        st.markdown(f"### {fp.name}")
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            st.error(f"Failed to read {fp.name}: {e}")
            continue

        # determine column candidates
        num_cols = list(df.select_dtypes(include="number").columns)
        cat_cols = list(df.select_dtypes(include="object").columns)
        dt_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
        # try parsing common date-like columns
        if not dt_cols:
            for c in df.columns:
                if "date" in c.lower() or "time" in c.lower():
                    try:
                        df[c] = pd.to_datetime(df[c], errors="coerce")
                        if df[c].notna().any():
                            dt_cols.append(c)
                            break
                    except Exception:
                        continue

        viz = st.selectbox(f"Visualization for {fp.name}", ["Table", "Line", "Bar", "Area", "Scatter", "Pie/Donut"], key=str(fp))
        if viz == "Table":
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"First 10 rows — {len(df)} rows × {len(df.columns)} columns.")
            continue

        # Pie / Donut: prefer categorical column with <= 15 uniques
        if viz == "Pie/Donut":
            pie_col = None
            for c in cat_cols + num_cols:
                try:
                    if df[c].nunique(dropna=True) <= 15:
                        pie_col = c
                        break
                except Exception:
                    continue
            if pie_col is None:
                st.info("No suitable column for pie (need ≤15 unique values). Showing table instead.")
                st.dataframe(df.head(10), use_container_width=True)
                continue
            counts = df[pie_col].fillna("N/A").value_counts().reset_index()
            counts.columns = [pie_col, "count"]
            hole = st.checkbox("Donut style", value=False, key=f"donut_{fp.name}")
            fig = px.pie(counts, names=pie_col, values="count", title=f"{pie_col} distribution", hole=0.4 if hole else 0.0)
            st.plotly_chart(fig, use_container_width=True)
            continue

        # For other charts, pick x and y
        x_choice = None
        y_choice = None
        if viz == "Line":
            # prefer datetime x and numeric y
            x_choice = dt_cols[0] if dt_cols else (cat_cols[0] if cat_cols else None)
            y_choice = num_cols[0] if num_cols else (df.columns[0] if df.columns.any() else None)
            if x_choice is None or y_choice is None:
                st.info("Not enough columns for line chart — showing table.")
                st.dataframe(df.head(10), use_container_width=True)
                continue
            fig = px.line(df, x=x_choice, y=y_choice, title=f"Line: {y_choice} over {x_choice}")
            st.plotly_chart(fig, use_container_width=True)
            continue

        if viz == "Bar" or viz == "Area":
            # bar: categorical x and numeric aggregation
            if cat_cols and num_cols:
                x_choice = st.selectbox("Categorical (x)", cat_cols, key=f"bar_x_{fp.name}")
                y_choice = st.selectbox("Numeric (y)", num_cols, key=f"bar_y_{fp.name}")
                agg = df.groupby(x_choice)[y_choice].sum().reset_index()
                if viz == "Bar":
                    fig = px.bar(agg, x=x_choice, y=y_choice, title=f"{y_choice} by {x_choice}")
                else:
                    fig = px.area(agg, x=x_choice, y=y_choice, title=f"{y_choice} by {x_choice}")
                st.plotly_chart(fig, use_container_width=True)
            elif num_cols:
                y_choice = num_cols[0]
                fig = px.bar(df, y=y_choice, title=f"Bar: {y_choice}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric data for Bar/Area — showing table.")
                st.dataframe(df.head(10), use_container_width=True)
            continue

        if viz == "Scatter":
            if len(num_cols) >= 2:
                x_choice = st.selectbox("X (numeric)", num_cols, index=0, key=f"sc_x_{fp.name}")
                y_choice = st.selectbox("Y (numeric)", num_cols, index=1, key=f"sc_y_{fp.name}")
                fig = px.scatter(df, x=x_choice, y=y_choice, title=f"Scatter: {y_choice} vs {x_choice}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least two numeric columns for scatter — showing table.")
                st.dataframe(df.head(10), use_container_width=True)
            continue

    # --- Additional graphs (use DATA/it_tickets.csv when present) ---
    tickets_path = base_dir / "DATA" / "it_tickets.csv"
    if tickets_path.exists():
        try:
            tickets = pd.read_csv(tickets_path, parse_dates=["created_date", "resolved_date"], infer_datetime_format=True)
            st.divider()
            st.subheader("Additional Visualizations (from it_tickets.csv)")

            # 1) Tickets by priority (bar)
            if "priority" in tickets.columns:
                prio = tickets["priority"].fillna("N/A").value_counts().reset_index()
                prio.columns = ["priority", "count"]
                fig_prio = px.bar(prio, x="priority", y="count", color="priority", title="Tickets by Priority")
                st.plotly_chart(fig_prio, use_container_width=True)

            # 2) Status by priority (grouped bar)
            if {"status", "priority"}.issubset(tickets.columns):
                fig_status = px.histogram(
                    tickets.fillna("N/A"),
                    x="status",
                    color="priority",
                    barmode="group",
                    title="Ticket Status grouped by Priority"
                )
                st.plotly_chart(fig_status, use_container_width=True)

            # 3) Tickets created per month (time series)
            if "created_date" in tickets.columns:
                tickets["created_date"] = pd.to_datetime(tickets["created_date"], errors="coerce", infer_datetime_format=True)
                ts = tickets.dropna(subset=["created_date"]).copy()
                if not ts.empty:
                    ts["month"] = ts["created_date"].dt.to_period("M").astype(str)
                    monthly = ts.groupby("month").size().reset_index(name="count")
                    fig_ts = px.line(monthly, x="month", y="count", title="Tickets Created per Month")
                    fig_ts.update_xaxes(type="category")
                    st.plotly_chart(fig_ts, use_container_width=True)

            # 4) Assigned-to distribution (donut)
            if "assigned_to" in tickets.columns:
                assigned = tickets["assigned_to"].fillna("Unassigned").value_counts().reset_index()
                assigned.columns = ["assigned_to", "count"]
                fig_assign = px.pie(assigned, names="assigned_to", values="count", title="Assigned To (Donut)", hole=0.4)
                st.plotly_chart(fig_assign, use_container_width=True)

        except Exception as e:
            st.error(f"Failed to build additional visuals from {tickets_path.name}: {e}")
    else:
        st.info("Additional graphs skipped: DATA/it_tickets.csv not found.")
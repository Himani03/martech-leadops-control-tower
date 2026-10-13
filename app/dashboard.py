import pandas as pd
import streamlit as st
from app.db import connect, DB_PATH
from app.pipeline import process_file

st.set_page_config(page_title="MarTech LeadOps Control Tower", layout="wide")
st.title("MarTech LeadOps Control Tower")
st.caption("Synthetic B2B lead operations demo | validation, enrichment, scoring, routing")

if st.button("Run / refresh lead processing"):
    process_file()
    st.success("Processing complete. Metrics refreshed.")

try:
    with connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM lead_processing", conn)
except Exception:
    df = pd.DataFrame()

if df.empty:
    st.info("No processed leads found. Click 'Run / refresh lead processing' or run `python -m app.pipeline` first.")
    st.stop()

total = len(df)
valid = int(df["is_valid"].sum())
invalid = total - valid
duplicates = int(df["is_duplicate"].sum())
routed = int((df["processing_status"] == "routed").sum())
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total leads", total)
c2.metric("Valid leads", valid, f"{valid/total:.0%} valid" if total else "0%")
c3.metric("Invalid records", invalid)
c4.metric("Duplicates", duplicates)
c5.metric("Routed leads", routed)

left, right = st.columns(2)
with left:
    st.subheader("Lead routing distribution")
    st.bar_chart(df["route_queue"].value_counts())
with right:
    st.subheader("Processing status")
    st.bar_chart(df["processing_status"].value_counts())

st.subheader("Lead quality exceptions")
exceptions = df[(df["is_valid"] == 0) | (df["is_duplicate"] == 1)].copy()
if not exceptions.empty:
    st.dataframe(exceptions[["record_id","email","company","country","validation_errors","is_duplicate","route_queue"]], use_container_width=True)
else:
    st.success("No exceptions detected.")

st.subheader("Lead records")
queue_options = ["All"] + sorted(df["route_queue"].dropna().unique().tolist())
selected_queue = st.selectbox("Filter by routing queue", queue_options)
view = df if selected_queue == "All" else df[df["route_queue"] == selected_queue]
st.dataframe(view[["record_id","email","company","country","industry","company_size","lead_score","route_queue","processing_status"]], use_container_width=True)

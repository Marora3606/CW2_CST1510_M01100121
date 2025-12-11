import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_all_tables

st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="shield",
    layout="wide"
)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")

st.title("Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Dashboard", use_container_width=True):
        st.session_state.dashboard_view = "cybersecurity"
with col2:
    if st.button("IT Tickets", use_container_width=True):
        st.session_state.dashboard_view = "tickets"
with col3:
    if st.button("Data Science", use_container_width=True):
        st.session_state.dashboard_view = "datascience"

# Initialize dashboard view
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "cybersecurity"

st.divider()

def load_csv_to_database():
    conn = connect_database()
    cursor = conn.cursor()
    tables = {
        'cyber_incidents': 'cyber_incidents.csv',
        'it_tickets': 'it_tickets.csv',
        'datasets_metadata': 'datasets_metadata.csv'
    }
    for table, csv_file in tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        if cursor.fetchone()[0] == 0:
            csv_path = Path("DATA") / csv_file
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                if 'id' in df.columns:
                    df = df.drop('id', axis=1)
                df.to_sql(table, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

try:
    from app.data.incidents import get_all_incidents
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    load_csv_to_database()
    
    if st.session_state.dashboard_view == "cybersecurity":
        st.header("Cybersecurity Dashboard")
        incidents_df = get_all_incidents()
        
        if incidents_df.empty:
            st.warning("No incidents data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Incidents", len(incidents_df))
            col2.metric("Critical", len(incidents_df[incidents_df['severity'] == 'critical']))
            col3.metric("High", len(incidents_df[incidents_df['severity'] == 'high']))
            col4.metric("Resolved", len(incidents_df[incidents_df['status'] == 'resolved']))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Incidents by Severity")
                fig = px.bar(x=incidents_df['severity'].value_counts().index, 
                           y=incidents_df['severity'].value_counts().values)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Incidents by Status")
                status_counts = incidents_df['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.dataframe(incidents_df, use_container_width=True)
    
    elif st.session_state.dashboard_view == "tickets":
        st.header("IT Tickets Dashboard")
        conn = connect_database()
        tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
        conn.close()
        
        if tickets_df.empty:
            st.warning("No IT tickets data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Tickets", len(tickets_df))
            col2.metric("Open", len(tickets_df[tickets_df['status'] == 'open']))
            col3.metric("In Progress", len(tickets_df[tickets_df['status'] == 'in_progress']))
            col4.metric("Closed", len(tickets_df[tickets_df['status'] == 'closed']))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Tickets by Priority")
                priority_counts = tickets_df['priority'].value_counts()
                fig = px.bar(x=priority_counts.index, y=priority_counts.values)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Tickets by Status")
                status_counts = tickets_df['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.dataframe(tickets_df, use_container_width=True)
    
    elif st.session_state.dashboard_view == "datascience":
        st.header("Data Science Dashboard")
        conn = connect_database()
        datasets_df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
        conn.close()
        
        if datasets_df.empty:
            st.warning("No datasets data available")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Datasets", len(datasets_df))
            col2.metric("Security", len(datasets_df[datasets_df['category'] == 'Security']))
            col3.metric("Analytics", len(datasets_df[datasets_df['category'] == 'Analytics']))
            col4.metric("Avg Size (KB)", f"{datasets_df['size'].mean():.1f}")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Datasets by Source")
                source_counts = datasets_df['source'].value_counts()
                fig = px.bar(x=source_counts.index, y=source_counts.values)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Datasets by Category")
                category_counts = datasets_df['category'].value_counts()
                fig = px.pie(values=category_counts.values, names=category_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.dataframe(datasets_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
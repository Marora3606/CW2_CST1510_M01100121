import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from app.data.db import connect_database

st.set_page_config(page_title="Analytics & Reporting", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.info("Go to Home page to login")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")

st.title("Analytics & Reporting")

def load_csv_data():
    conn = connect_database()
    tables = {
        'users_data': 'users.csv',
        'cyber_incidents': 'cyber_incidents.csv',
        'it_tickets': 'it_tickets.csv',
        'datasets_metadata': 'datasets_metadata.csv'
    }
    for table_name, csv_file in tables.items():
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not cursor.fetchone():
            csv_path = Path("DATA") / csv_file
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

load_csv_data()

try:
    conn = connect_database()
    users_df = pd.read_sql_query("SELECT * FROM users_data", conn)
    incidents_df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    tickets_df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    datasets_df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", len(users_df))
    col2.metric("Total Incidents", len(incidents_df))
    col3.metric("Total Tickets", len(tickets_df))
    col4.metric("Total Datasets", len(datasets_df))
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["Users", "Incidents", "Tickets"])
    
    with tab1:
        st.header("User Analysis")
        role_counts = users_df['role'].value_counts().reset_index()
        role_counts.columns = ['role', 'count']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Role Distribution")
            fig1 = px.pie(role_counts, values='count', names='role')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("Role Statistics")
            st.dataframe(role_counts, use_container_width=True, hide_index=True)
    
    with tab2:
        st.header("Incident Analysis")
        type_counts = incidents_df['incident_type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']
        severity_counts = incidents_df['severity'].value_counts().reset_index()
        severity_counts.columns = ['severity', 'count']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Incidents by Type")
            fig3 = px.bar(type_counts, x='type', y='count')
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.markdown("Severity Breakdown")
            fig4 = px.bar(severity_counts, x='severity', y='count', color='severity')
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        st.header("Ticket Analysis")
        priority_counts = tickets_df['priority'].value_counts().reset_index()
        priority_counts.columns = ['priority', 'count']
        ticket_status_counts = tickets_df['status'].value_counts().reset_index()
        ticket_status_counts.columns = ['status', 'count']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Tickets by Priority")
            fig5 = px.bar(priority_counts, x='priority', y='count', color='priority')
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            st.markdown("Tickets by Status")
            fig6 = px.pie(ticket_status_counts, values='count', names='status')
            st.plotly_chart(fig6, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please ensure the database is properly initialized and contains data.")

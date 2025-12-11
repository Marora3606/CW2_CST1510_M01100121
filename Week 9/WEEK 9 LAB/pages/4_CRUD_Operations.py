import streamlit as st
import pandas as pd

st.set_page_config(page_title="CRUD", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

with st.sidebar:
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role.upper()}")
    st.divider()
    st.metric("Total Records", len(st.session_state.get("records", [])))
    if st.button("Clear All"):
        st.session_state.records = []
        st.rerun()

st.title("CRUD Operations")

if "records" not in st.session_state:
    st.session_state.records = []

st.subheader("CREATE")
with st.form("add"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["User", "Admin"])
    if st.form_submit_button("Add"):
        if name and email:
            st.session_state.records.append({"name": name, "email": email, "role": role})
            st.success("Added!")
            st.rerun()
        else:
            st.error("Fill all fields!")

st.divider()

st.subheader("READ")
if st.session_state.records:
    st.dataframe(pd.DataFrame(st.session_state.records), use_container_width=True)
else:
    st.info("No records")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("UPDATE")
    if st.session_state.records:
        names = [r['name'] for r in st.session_state.records]
        selected = st.selectbox("Select record", names)
        idx = names.index(selected)
        record = st.session_state.records[idx]
        
        with st.form("update"):
            new_email = st.text_input("Email", record["email"])
            new_role = st.selectbox("Role", ["User", "Admin"], index=0 if record["role"] == "User" else 1)
            if st.form_submit_button("Update"):
                if new_email:
                    st.session_state.records[idx]["email"] = new_email
                    st.session_state.records[idx]["role"] = new_role
                    st.success("Updated!")
                    st.rerun()
    else:
        st.info("No records")

with col2:
    st.subheader("DELETE")
    if st.session_state.records:
        names = [r['name'] for r in st.session_state.records]
        to_delete = st.selectbox("Select to delete", names, key="del")
        if st.button("Delete", type="primary"):
            st.session_state.records.pop(names.index(to_delete))
            st.success("Deleted!")
            st.rerun()
    else:
        st.info("No records")

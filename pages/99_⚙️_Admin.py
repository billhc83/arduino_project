import streamlit as st

# Immediately stop unauthorized users
if not st.session_state.get("is_admin", False):
    st.error("Unauthorized Access")
    st.stop()

st.title("Admin Management")

import streamlit as st
from data_base import conn

# Security Guard
if not st.session_state.get("is_admin"):
    st.error("🔒 Restricted Access")
    st.stop()

st.title("⚙️ Admin Dashboard")

# Tabbed interface to keep things organized
tab1, tab2, tab3, tab4 = st.tabs(["User Approvals", "User Feedback", "Usage Stats", "User Table"])

with tab1:
    st.subheader("Pending Requests")
    
    # Fetch unapproved users
    pending_users = conn.query("SELECT username FROM users WHERE is_approved = FALSE", ttl=0)

    if not pending_users.empty:
        for index, row in pending_users.iterrows():
            user = row['username']
            # Creating 3 columns: Name, Approve Button, Reject Button
            col1, col2, col3 = st.columns([2, 1, 1])
            
            col1.write(f"👤 **{user}**")
            
            # --- APPROVE BUTTON ---
            if col2.button("Approve", key=f"app_{user}"):
                from sqlalchemy import text
                with conn.session as s:
                    s.execute(
                        text("UPDATE users SET is_approved = TRUE WHERE username = :u"),
                        {"u": user}
                    )
                    s.commit()
                st.success(f"Approved {user}!")
                st.rerun()

            # --- REJECT/DELETE BUTTON ---
            if col3.button("Reject", key=f"rej_{user}", type="secondary", help="Delete this request"):
                from sqlalchemy import text
                with conn.session as s:
                    s.execute(
                        text("DELETE FROM users WHERE username = :u AND is_approved = FALSE"),
                        {"u": user}
                    )
                    s.commit()
                st.warning(f"Request for {user} deleted.")
                st.rerun()
    else:
        st.info("No pending requests.")
with tab2:
    st.subheader("📬 Manage Feedback")
    
    # 1. Fetch feedback
    feedback_df = conn.query(
        "SELECT id, username, category, message, created_at FROM feedback ORDER BY created_at DESC", 
        ttl=0
    )
    print(feedback_df)
    if not feedback_df.empty:
        # Add a 'Select' column for the user to check off rows
        feedback_df.insert(0, "Select", False)
        
        # 2. Use data_editor to allow selection
        edited_df = st.data_editor(
            feedback_df,
            hide_index=True,
            width= "stretch",
            column_config={
                "id": None, # Hide the ID from the user
                "Select": st.column_config.CheckboxColumn("Delete?", default=False),
                "created_at": st.column_config.DatetimeColumn("Date", format="D MMM, h:mm a"),
            },
            disabled=["username", "category", "message", "created_at"] # Only 'Select' is editable
        )
        
        # 3. Filter for rows where 'Select' is True
        to_delete = edited_df[edited_df["Select"] == True]
        
        if not to_delete.empty:
            if st.button(f"Delete {len(to_delete)} Selected Entries", type="primary"):
                from sqlalchemy import text
                ids_to_del = to_delete["id"].tolist()
                
                with conn.session as s:
                    # Using WHERE id IN (...) to delete multiple at once
                    s.execute(
                        text("DELETE FROM feedback WHERE id IN :ids"),
                        {"ids": tuple(ids_to_del)}
                    )
                    s.commit()
                st.success(f"Successfully deleted {len(to_delete)} entries.")
                st.rerun()
    else:
        st.info("No feedback submitted yet.")


with tab3:
    st.subheader("User Activity Logs")
    # Fetch logs and calculate total time per user
    logs_df = conn.query("SELECT username, page_name, stay_duration_seconds, timestamp FROM activity_logs ORDER BY timestamp DESC", ttl=0)
    
    if not logs_df.empty:
        # Show a summary: Total time spent by each user
        summary = logs_df.groupby("username")["stay_duration_seconds"].sum().reset_index()
        summary["stay_duration_minutes"] = (summary["stay_duration_seconds"] / 60).round(2)
        st.write("### Total Time per User (Minutes)")
        st.bar_chart(summary.set_index("username")["stay_duration_minutes"])
        
        st.write("### Raw Logs")
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No activity recorded yet.")

with tab4:
    st.title("User Management")
    st.subheader("👥 Edit App Users")
    
    # 1. Fetch current user data
    user_df = conn.query("SELECT username, password, is_admin, is_approved FROM users", ttl=0)
    
    # 2. Display editable table
    edited_data = st.data_editor(
        user_df,
        key="user_editor",
        width="stretch",
        num_rows="dynamic", # Allows adding/deleting rows manually
        column_config={
            "password": st.column_config.TextColumn("Hashed Password (Read-Only)", disabled=True),
            "is_admin": st.column_config.CheckboxColumn("Admin Status"),
            "is_approved": st.column_config.CheckboxColumn("Approved")
        }
    )
    
    # 1. Define your master username
if st.button("Save User Changes"):
    # 1. Count how many admins are in your EDITED data
    # edited_data is what you see on the screen right now
    current_admin_count = edited_data['is_admin'].sum()
    MAX_ALLOWED = 1 

    # 2. Check for the ceiling
    if current_admin_count > MAX_ALLOWED:
        st.error(f"🛑 Over Limit: You can only have {MAX_ALLOWED} admin. Please uncheck others before saving.")
    
    # 3. Check for the floor (Don't lock yourself out!)
    elif current_admin_count < 1:
        st.error("🛑 Safety Error: You must have at least 1 admin. Don't lock yourself out!")
    
    else:
        # 4. If count is exactly 1, proceed with the database update
        try:
            from sqlalchemy import text
            with conn.session as s:
                for index, row in edited_data.iterrows():
                    s.execute(
                        text("""
                            UPDATE users 
                            SET is_admin = :a, is_approved = :ap, username = :un 
                            WHERE username = :old_un
                        """),
                        {
                            "a": row['is_admin'], 
                            "ap": row['is_approved'], 
                            "un": row['username'], 
                            "old_un": user_df.iloc[index]['username']
                        }
                    )
                s.commit()
            st.success("User table updated successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to update users: {e}")


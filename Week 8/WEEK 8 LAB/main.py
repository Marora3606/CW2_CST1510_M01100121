from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.tickets import insert_ticket, get_all_tickets
from app.data.datasets import insert_dataset, get_all_datasets
from app.data.users import insert_user, get_all_users
import pandas as pd


def load_csv_data():
    """Load CSV data into the database"""
    from pathlib import Path
    data_dir = Path(__file__).resolve().parent / 'DATA'
    conn = connect_database()
    cursor = conn.cursor()

    # Helper to clear and load a CSV into an existing table without replacing schema
    def _clear_and_load(table_name, csv_path):
        try:
            if not csv_path.exists():
                print(f"  {table_name}: file not found: {csv_path}")
                return

            # Clear existing rows so repeated runs don't duplicate data
            try:
                cursor.execute(f"DELETE FROM {table_name}")
                conn.commit()
            except Exception:
                # If deletion fails (table might not exist), ignore and let to_sql create/insert
                pass

            df = pd.read_csv(csv_path)
            # Append to the existing table (do not replace schema)
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f" Loaded {len(df)} {table_name}")
        except Exception as e:
            print(f"  {table_name}: {e}")

    _clear_and_load('users', data_dir / 'users.csv')
    _clear_and_load('cyber_incidents', data_dir / 'cyber_incidents.csv')
    _clear_and_load('it_tickets', data_dir / 'it_tickets.csv')
    _clear_and_load('datasets_metadata', data_dir / 'datasets_metadata.csv')

    conn.close()


def test_authentication():
    """Test user registration and login"""
    success, msg = register_user("bob", "SecurePass123!", "analyst")
    print(f"Register: {msg}")
    
    success, msg = login_user("bob", "SecurePass123!")
    print(f"Login: {msg}")


def test_crud():
    """Test CRUD operations"""
    # Test incidents
    incident_id = insert_incident(
        date="2024-11-05",
        incident_type="Phishing",
        severity="High",
        status="Open",
        description="Suspicious email detected",
        reported_by="bob"
    )
    print(f"Created incident #{incident_id}")
    df = get_all_incidents()
    print(f"Total incidents after insertion: {len(df)}")
    
    # Test tickets
    ticket_id = insert_ticket(
        id=None,
        title="Cannot access VPN",
        priority="High",
        status="Open",
        created_date="2024-11-05"
    )   
    print(f"Created ticket #{ticket_id}")
    df_tickets = get_all_tickets()
    print(f"Total tickets after insertion: {len(df_tickets)}")
    
    # Test datasets
    dataset_id = insert_dataset(
        id=None,
        name="Employee Data",
        source="HR System",
        category="Internal",
        size=2048
    )
    print(f"Created dataset #{dataset_id}")
    df_datasets = get_all_datasets()
    print(f"Total datasets after insertion: {len(df_datasets)}")
    
    # Test users
    insert_user(
        id=None,
        username="alice",
        password_hash="hashed_password_123",
        role="admin"
    )
    users = get_all_users()
    print(f"Total users after insertion: {len(users)}")
    # Note: the users table is displayed later in `query_data()`; avoid
    # printing it twice here to reduce duplicate output.
    

 


def query_data():
    """Query and display all data"""
    # Query incidents
    df_incidents = get_all_incidents()
    print(f"Total incidents: {len(df_incidents)}")
    print("\nFirst 5 incidents:")
    print(df_incidents.head(5))
    
    # Query tickets
    df_tickets = get_all_tickets()
    print(f"\nTotal tickets: {len(df_tickets)}")
    print("\nFirst 5 tickets:")
    print(df_tickets.head(5))
    
    # Query datasets
    df_datasets = get_all_datasets()
    print(f"\nTotal datasets: {len(df_datasets)}")
    print("\nFirst 5 datasets:")
    print(df_datasets.head(5))
    
    # Query users
    users = get_all_users()
    df_users = pd.DataFrame(users)
    print(f"\nTotal users: {len(users)}")
    print("\nFirst 5 users:")
    print(df_users.head(5))



def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    
    print("\n[1/6] Setting up database...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    
    print("\n[2/6] Loading CSV data...")
    load_csv_data()
    
    print("\n[3/6] Testing authentication...")
    test_authentication()
    
    print("\n[4/6] Testing CRUD operations...")
    test_crud()
    
    print("\n[5/6] Querying data...")
    query_data()
    
    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

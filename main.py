from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

# Connect to Cassandra
def connect_to_cassandra():
    """
    Establish connection to Cassandra cluster
    """
    try:
        # For local Cassandra instance
        cluster = Cluster(['127.0.0.1'])
        
        # For cloud-based Cassandra (e.g., DataStax Astra)
        # auth_provider = PlainTextAuthProvider(username='your_username', password='your_password')
        # cluster = Cluster(['your_cassandra_host'], auth_provider=auth_provider)
        
        session = cluster.connect()
        print("Successfully connected to Cassandra!")
        return session, cluster
    except Exception as e:
        print(f"Error connecting to Cassandra: {e}")
        return None, None

# Create keyspace
def create_keyspace(session, keyspace_name='data_management'):
    """
    Create a keyspace for data management
    """
    try:
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {keyspace_name}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
        """)
        print(f"Keyspace '{keyspace_name}' created successfully!")
        session.set_keyspace(keyspace_name)
    except Exception as e:
        print(f"Error creating keyspace: {e}")

# Create table
def create_table(session):
    """
    Create a table for storing user data
    """
    try:
        session.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY,
                username TEXT,
                email TEXT,
                created_at TIMESTAMP
            )
        """)
        print("Table 'users' created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

# Insert data
def insert_user(session, username, email):
    """
    Insert a new user into the users table
    """
    try:
        user_id = uuid.uuid4()
        query = "INSERT INTO users (user_id, username, email, created_at) VALUES (%s, %s, %s, toTimestamp(now()))"
        session.execute(query, (user_id, username, email))
        print(f"User '{username}' inserted successfully!")
        return user_id
    except Exception as e:
        print(f"Error inserting user: {e}")
        return None

# Query data
def query_users(session):
    """
    Query all users from the users table
    """
    try:
        rows = session.execute("SELECT * FROM users")
        print("\nUsers in database:")
        print("-" * 80)
        for row in rows:
            print(f"ID: {row.user_id} | Username: {row.username} | Email: {row.email} | Created: {row.created_at}")
        print("-" * 80)
    except Exception as e:
        print(f"Error querying users: {e}")

# Query specific user
def query_user_by_id(session, user_id):
    """
    Query a specific user by ID
    """
    try:
        query = "SELECT * FROM users WHERE user_id = %s"
        rows = session.execute(query, (user_id,))
        for row in rows:
            print(f"\nFound user: {row.username} ({row.email})")
            return row
        print(f"No user found with ID: {user_id}")
        return None
    except Exception as e:
        print(f"Error querying user: {e}")
        return None

# Main execution
def main():
    print("=" * 80)
    print("Cassandra Data Management System")
    print("=" * 80)
    
    # Connect to Cassandra
    session, cluster = connect_to_cassandra()
    
    if session is None:
        print("Failed to connect to Cassandra. Exiting...")
        return
    
    try:
        # Create keyspace
        create_keyspace(session)
        
        # Create table
        create_table(session)
        
        # Insert sample users
        print("\nInserting sample users...")
        user_id_1 = insert_user(session, "john_doe", "john@example.com")
        user_id_2 = insert_user(session, "jane_smith", "jane@example.com")
        user_id_3 = insert_user(session, "bob_wilson", "bob@example.com")
        
        # Query all users
        query_users(session)
        
        # Query specific user
        if user_id_1:
            query_user_by_id(session, user_id_1)
        
        print("\n" + "=" * 80)
        print("Data management operations completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close connection
        if cluster:
            cluster.shutdown()
            print("\nConnection closed.")

if __name__ == "__main__":
    main()

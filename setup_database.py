# Test PostgreSQL connection and create database if needed
import psycopg2
from psycopg2 import sql

def setup_database():
    try:
        # Connect to PostgreSQL server (default postgres database)
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'todo_db'")
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('todo_db')
            ))
            print("✅ Database 'todo_db' created successfully!")
        else:
            print("✅ Database 'todo_db' already exists!")
        
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is running")
        print("2. Username: postgres, Password: 123456")
        print("3. PostgreSQL is listening on localhost:5432")
        return False

if __name__ == "__main__":
    setup_database()

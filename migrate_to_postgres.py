#!/usr/bin/env python3
"""
Sina Database Migration Script
Migrates from SQLite to PostgreSQL for production deployment
"""

import sqlite3
import psycopg2
import os
from datetime import datetime

def migrate_sqlite_to_postgres():
    """
    Migrate Sina database from SQLite to PostgreSQL
    """
    
    # Database connection strings
    SQLITE_DB = 'instance/sina.db'
    POSTGRES_URL = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/sina_db')
    
    print("🚀 Starting Sina database migration...")
    
    # Connect to databases
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    postgres_conn = psycopg2.connect(POSTGRES_URL)
    
    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = postgres_conn.cursor()
    
    # Create PostgreSQL schema
    create_postgres_schema(postgres_cursor)
    
    # Migrate each table
    tables = [
        'users', 'tasks', 'focus_sessions', 
        'journal_entries', 'habits', 'habit_tracking', 'user_settings'
    ]
    
    for table in tables:
        print(f"📊 Migrating {table}...")
        migrate_table(sqlite_cursor, postgres_cursor, table)
    
    # Commit and close
    postgres_conn.commit()
    sqlite_conn.close()
    postgres_conn.close()
    
    print("✅ Migration completed successfully!")

def create_postgres_schema(cursor):
    """Create PostgreSQL schema matching SQLite structure"""
    
    schema_sql = """
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        secure_mode BOOLEAN DEFAULT FALSE,
        pin VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tasks table
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        title VARCHAR(255) NOT NULL,
        description TEXT,
        priority VARCHAR(10) DEFAULT 'medium',
        category VARCHAR(50) DEFAULT 'personal',
        deadline TIMESTAMP,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    );
    
    -- Focus sessions table
    CREATE TABLE IF NOT EXISTS focus_sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        task_id INTEGER REFERENCES tasks(id),
        duration INTEGER NOT NULL,
        notes TEXT,
        session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Journal entries table
    CREATE TABLE IF NOT EXISTS journal_entries (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        content TEXT NOT NULL,
        mood INTEGER DEFAULT 5,
        entry_date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Habits table
    CREATE TABLE IF NOT EXISTS habits (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        name VARCHAR(255) NOT NULL,
        description TEXT,
        frequency VARCHAR(20) DEFAULT 'daily',
        target_count INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Habit tracking table
    CREATE TABLE IF NOT EXISTS habit_tracking (
        id SERIAL PRIMARY KEY,
        habit_id INTEGER NOT NULL REFERENCES habits(id),
        completion_date DATE DEFAULT CURRENT_DATE,
        completed BOOLEAN DEFAULT TRUE,
        notes TEXT
    );
    
    -- User settings table
    CREATE TABLE IF NOT EXISTS user_settings (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        persona_tone VARCHAR(20) DEFAULT 'balanced',
        timer_work_duration INTEGER DEFAULT 25,
        timer_break_duration INTEGER DEFAULT 5,
        dark_mode BOOLEAN DEFAULT FALSE,
        notifications BOOLEAN DEFAULT TRUE
    );
    
    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
    CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
    CREATE INDEX IF NOT EXISTS idx_focus_sessions_user_id ON focus_sessions(user_id);
    CREATE INDEX IF NOT EXISTS idx_journal_entries_user_id ON journal_entries(user_id);
    CREATE INDEX IF NOT EXISTS idx_journal_entries_date ON journal_entries(entry_date);
    """
    
    cursor.execute(schema_sql)

def migrate_table(sqlite_cursor, postgres_cursor, table_name):
    """Migrate a specific table from SQLite to PostgreSQL"""
    
    # Get all data from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    if not rows:
        print(f"  ⚠️  No data found in {table_name}")
        return
    
    # Get column names
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in sqlite_cursor.fetchall()]
    
    # Prepare INSERT statement
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join(columns)
    insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    # Insert data into PostgreSQL
    postgres_cursor.executemany(insert_sql, rows)
    print(f"  ✅ Migrated {len(rows)} rows to {table_name}")

if __name__ == "__main__":
    migrate_sqlite_to_postgres() 
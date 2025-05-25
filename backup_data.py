#!/usr/bin/env python3
"""
Sina Data Backup & Export Script
Creates backups and exports user data in multiple formats
"""

import sqlite3
import json
import csv
import os
from datetime import datetime
import zipfile

def backup_user_data(user_id=None, export_format='json'):
    """
    Backup user data from Sina database
    
    Args:
        user_id: Specific user ID to backup (None for all users)
        export_format: 'json', 'csv', or 'sql'
    """
    
    db_path = 'instance/sina.db'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    # Create backup directory
    backup_dir = f'backups/sina_backup_{timestamp}'
    os.makedirs(backup_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    
    if export_format == 'json':
        export_to_json(conn, backup_dir, user_id)
    elif export_format == 'csv':
        export_to_csv(conn, backup_dir, user_id)
    elif export_format == 'sql':
        export_to_sql(conn, backup_dir, user_id)
    
    conn.close()
    
    # Create zip archive
    create_backup_archive(backup_dir, timestamp)
    
    print(f"✅ Backup completed: {backup_dir}.zip")

def export_to_json(conn, backup_dir, user_id=None):
    """Export data to JSON format"""
    
    cursor = conn.cursor()
    
    # Define tables and their relationships
    tables = {
        'users': 'SELECT * FROM users' + (f' WHERE id = {user_id}' if user_id else ''),
        'tasks': 'SELECT * FROM tasks' + (f' WHERE user_id = {user_id}' if user_id else ''),
        'focus_sessions': 'SELECT * FROM focus_sessions' + (f' WHERE user_id = {user_id}' if user_id else ''),
        'journal_entries': 'SELECT * FROM journal_entries' + (f' WHERE user_id = {user_id}' if user_id else ''),
        'user_settings': 'SELECT * FROM user_settings' + (f' WHERE user_id = {user_id}' if user_id else ''),
    }
    
    backup_data = {
        'export_info': {
            'timestamp': datetime.now().isoformat(),
            'format': 'json',
            'user_id': user_id,
            'sina_version': '0.2.0'
        },
        'data': {}
    }
    
    for table_name, query in tables.items():
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        backup_data['data'][table_name] = [dict(row) for row in rows]
        print(f"📊 Exported {len(rows)} records from {table_name}")
    
    # Save to JSON file
    json_file = os.path.join(backup_dir, 'sina_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, default=str)

def export_to_csv(conn, backup_dir, user_id=None):
    """Export data to CSV format"""
    
    cursor = conn.cursor()
    
    tables = ['users', 'tasks', 'focus_sessions', 'journal_entries', 'user_settings']
    
    for table in tables:
        query = f'SELECT * FROM {table}'
        if user_id and table != 'users':
            query += f' WHERE user_id = {user_id}'
        elif user_id and table == 'users':
            query += f' WHERE id = {user_id}'
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if rows:
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            # Write CSV file
            csv_file = os.path.join(backup_dir, f'{table}.csv')
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(column_names)
                writer.writerows(rows)
            
            print(f"📊 Exported {len(rows)} records to {table}.csv")

def export_to_sql(conn, backup_dir, user_id=None):
    """Export data to SQL format"""
    
    sql_file = os.path.join(backup_dir, 'sina_backup.sql')
    
    with open(sql_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"-- Sina Database Backup\n")
        f.write(f"-- Generated: {datetime.now().isoformat()}\n")
        f.write(f"-- User ID: {user_id if user_id else 'ALL'}\n\n")
        
        # Export schema
        f.write("-- Database Schema\n")
        for line in conn.iterdump():
            if 'CREATE TABLE' in line:
                f.write(line + '\n')
        
        f.write("\n-- Data Export\n")
        
        # Export data
        cursor = conn.cursor()
        tables = ['users', 'tasks', 'focus_sessions', 'journal_entries', 'user_settings']
        
        for table in tables:
            query = f'SELECT * FROM {table}'
            if user_id and table != 'users':
                query += f' WHERE user_id = {user_id}'
            elif user_id and table == 'users':
                query += f' WHERE id = {user_id}'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                f.write(f"\n-- {table} data\n")
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                
                for row in rows:
                    values = []
                    for value in row:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, str):
                            values.append(f"'{value.replace(\"'\", \"''\")}'")
                        else:
                            values.append(str(value))
                    
                    f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});\n")
                
                print(f"📊 Exported {len(rows)} records to SQL for {table}")

def create_backup_archive(backup_dir, timestamp):
    """Create a zip archive of the backup"""
    
    zip_filename = f"{backup_dir}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_dir)
                zipf.write(file_path, arcname)
    
    # Remove the temporary directory
    import shutil
    shutil.rmtree(backup_dir)

def restore_from_backup(backup_file, target_db='instance/sina_restored.db'):
    """Restore data from a backup file"""
    
    print(f"🔄 Restoring from {backup_file}...")
    
    if backup_file.endswith('.zip'):
        # Extract zip file
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Find JSON file
            json_file = os.path.join(temp_dir, 'sina_data.json')
            if os.path.exists(json_file):
                restore_from_json(json_file, target_db)
            else:
                print("❌ No JSON data file found in backup")
    
    elif backup_file.endswith('.json'):
        restore_from_json(backup_file, target_db)
    
    else:
        print("❌ Unsupported backup format")

def restore_from_json(json_file, target_db):
    """Restore data from JSON backup"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # Create new database
    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()
    
    # Create tables (you would need to import the schema creation function)
    # For now, assume tables exist
    
    # Restore data
    for table_name, records in backup_data['data'].items():
        if records:
            # Get column names from first record
            columns = list(records[0].keys())
            placeholders = ', '.join(['?' for _ in columns])
            
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            for record in records:
                values = [record[col] for col in columns]
                cursor.execute(insert_sql, values)
            
            print(f"✅ Restored {len(records)} records to {table_name}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database restored to {target_db}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'backup':
            user_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
            format_type = sys.argv[3] if len(sys.argv) > 3 else 'json'
            backup_user_data(user_id, format_type)
        
        elif command == 'restore':
            backup_file = sys.argv[2] if len(sys.argv) > 2 else None
            if backup_file:
                restore_from_backup(backup_file)
            else:
                print("❌ Please provide backup file path")
        
        else:
            print("Usage: python backup_data.py [backup|restore] [user_id] [format]")
    
    else:
        # Default: backup all data as JSON
        backup_user_data() 
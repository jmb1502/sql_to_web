#!/usr/bin/env python3
#!C:\Dev\Projects\learning\sql_to_web\.env

"""
SQL Server to Web Page dataset

This script connects to SQL Server, queries a table, and generates
an HTML web page populated with the data.

Requirements:
- pyodbc (for SQL Server connection)
- python-decouple (for environment variables)

Installation:
pip install pyodbc python-decouple

Usage:
python sql_to_web.py
"""

import pyodbc
import json
import os
from datetime import datetime
from decouple import config, Csv
from typing import List, Dict, Any, Optional

import sys
sys.path.append('C:\Dev\Projects\learning\sql_to_web')
sys.path.append('C:\Dev\Projects\learning\sql_to_web\database')
sys.path.append('C:\Dev\Projects\learning\sql_to_web\models')

import SQLClass as SQC
import WEBClass as WBC


def main():
    """Main function to demonstrate usage"""
    
    # Load configuration from environment variables or .env file
    # Create a .env file with your database credentials
    try:
        SERVER = config('SQL_SERVER', default='localhost')
        DATABASE = config('SQL_DATABASE', default='TestDB')
        USERNAME = config('SQL_USERNAME', default='')
        PASSWORD = config('SQL_PASSWORD', default='')
        USE_WINDOWS_AUTH = config('USE_WINDOWS_AUTH', default=True, cast=bool)
        
        # SQL Query - modify this to match your table
        QUERY = config('SQL_QUERY', default="""
            SELECT TOP 100 
                *
            FROM YourTableName
            ORDER BY 1
        """)
        
        TABLE_TITLE = config('TABLE_TITLE', default='Database Table')
        PAGE_TITLE = config('PAGE_TITLE', default='Database Report')
        OUTPUT_FILE = config('OUTPUT_FILE', default='')
        
    except Exception as e:
        print(f"❌ Error loading configuration: {str(e)}")
        print("Using default values...")
        
        # Default configuration
        SERVER = 'localhost'
        DATABASE = 'TestDB'
        USERNAME = ''
        PASSWORD = ''
        USE_WINDOWS_AUTH = True
        
        QUERY = """
            SELECT TOP 100 
                *
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """
        
        TABLE_TITLE = 'Database Tables'
        PAGE_TITLE = 'Database Report'
        OUTPUT_FILE = ''
    
    # Create SQl Class instance
    dataset = SQC.SQLClass(
        server=SERVER,
        database=DATABASE,
        username=USERNAME,
        password=PASSWORD,
        use_windows_auth=USE_WINDOWS_AUTH
    )
    
        # Create WEB Class instance
    webset = WBC.WEBClass(
    )


    try:
        # Connect to database
        if not dataset.connect():
            return
        
        # Execute query
        print(f"🔍 Executing query...")
        data = dataset.execute_query(QUERY)
        
        if not data:
            print("❌ No data retrieved from query")
            return
        
        # Generate HTML
        print(f"🌐 Generating HTML webpage...")
        html_content = webset.generate_complete_webpage(
            data=data,
            title=PAGE_TITLE,
            table_title=TABLE_TITLE
        )
        
        # Save to file
        output_filename = OUTPUT_FILE if OUTPUT_FILE else None
        saved_file = webset.save_to_file(html_content, output_filename)
        
        if saved_file:
            print(f"🎉 Success! Open {saved_file} in your web browser to view the report.")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    
    finally:
        # Clean up
        dataset.close_connection()

if __name__ == "__main__":
    main()
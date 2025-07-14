#!/usr/bin/env python3
#!C:\Dev\Projects\learning\sql_to_web\.env
# 

import pyodbc
import json
import os
from datetime import datetime
from decouple import config, Csv
from typing import List, Dict, Any, Optional

class SQLClass:
    def __init__(self, 
                 server: str, 
                 database: str, 
                 username: str = None, 
                 password: str = None,
                 use_windows_auth: bool = False):
        """
        Initialize the SQL Server connection
        
        Args:
            server: SQL Server instance name
            database: Database name
            username: SQL Server username (if not using Windows auth)
            password: SQL Server password (if not using Windows auth)
            use_windows_auth: Use Windows authentication
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.use_windows_auth = use_windows_auth
        self.connection = None
        
    # SC.SQLConnect(server, database, username, password)

    def connect(self) -> bool:
        """
        Establish connection to SQL Server
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.use_windows_auth:
                # Windows Authentication
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                # SQL Server Authentication
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password};"
                )
            
            self.connection = pyodbc.connect(connection_string)
            print(f"✅ Connected to SQL Server: {self.server}/{self.database}")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to SQL Server: {str(e)}")
            return False
    
    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """
        Execute SQL query and return results
        
        Args:
            query: SQL query string
            
        Returns:
            List of dictionaries containing query results
        """
        if not self.connection:
            print("❌ No database connection established")
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Fetch all rows and convert to list of dictionaries
            rows = cursor.fetchall()
            results = []
            
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    # Handle different data types
                    if isinstance(value, datetime):
                        row_dict[columns[i]] = value.strftime('%Y-%m-%d %H:%M:%S')
                    elif value is None:
                        row_dict[columns[i]] = ''
                    else:
                        row_dict[columns[i]] = str(value)
                results.append(row_dict)
            
            print(f"✅ Query executed successfully. Retrieved {len(results)} rows.")
            return results
            
        except Exception as e:
            print(f"❌ Error executing query: {str(e)}")
            return None
    
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("🔌 Database connection closed")

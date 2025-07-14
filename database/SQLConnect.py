def SQLConnect(server, database, username, pasword) -> bool:
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
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                # SQL Server Authentication
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                )
            
            self.connection = pyodbc.connect(connection_string)
            print(f"✅ Connected to SQL Server: {server}/{database}")
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to SQL Server: ", server)
            return False
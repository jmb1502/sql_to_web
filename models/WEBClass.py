#!/usr/bin/env python3
#!C:\Dev\Projects\learning\sql_to_web\.env
# 

import pyodbc
import json
import os
from datetime import datetime
from decouple import config, Csv
from typing import List, Dict, Any, Optional


class WEBClass:
    def __init__(self):

        """

        Format the data into a web page
        
        """
    
    def generate_html_table(self, data: List[Dict[str, Any]], 
                          table_title: str = "Database Table") -> str:
        """
        Generate HTML table from data
        
        Args:
            data: List of dictionaries containing table data
            table_title: Title for the table
            
        Returns:
            HTML string containing the table
        """
        if not data:
            return "<p>No data available</p>"
        
        # Get column names from first row
        columns = list(data[0].keys())
        
        # Start building HTML table
        html = f"""
        <div class="table-container">
            <h2>{table_title}</h2>
            <div class="table-info">
                <p>Total Records: <strong>{len(data)}</strong></p>
                <p>Generated: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
            </div>
            <table class="data-table">
                <thead>
                    <tr>
        """
        
        # Add column headers
        for column in columns:
            html += f"                        <th>{column}</th>\n"
        
        html += """                    </tr>
                </thead>
                <tbody>
        """
        
        # Add data rows
        for i, row in enumerate(data):
            css_class = "even" if i % 2 == 0 else "odd"
            html += f'                    <tr class="{css_class}">\n'
            
            for column in columns:
                value = row.get(column, '')
                html += f"                        <td>{value}</td>\n"
            
            html += "                    </tr>\n"
        
        html += """                </tbody>
            </table>
        </div>
        """
        
        return html
    
    def generate_complete_webpage(self, data: List[Dict[str, Any]], 
                                title: str = "Database Report",
                                table_title: str = "Database Table") -> str:
        """
        Generate complete HTML webpage
        
        Args:
            data: List of dictionaries containing table data
            title: Page title
            table_title: Table title
            
        Returns:
            Complete HTML webpage as string
        """
        table_html = self.generate_html_table(data, table_title)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            text-align: center;
            margin-bottom: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .table-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-bottom: 2rem;
        }}
        
        .table-container h2 {{
            background: #f8f9fa;
            padding: 1rem;
            margin: 0;
            border-bottom: 2px solid #e9ecef;
            color: #495057;
        }}
        
        .table-info {{
            padding: 1rem;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .table-info p {{
            display: inline-block;
            margin-right: 2rem;
            color: #6c757d;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .data-table th {{
            background: #495057;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #343a40;
        }}
        
        .data-table td {{
            padding: 10px 8px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .data-table tr:hover {{
            background-color: #e3f2fd;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem 0;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        
        .search-container {{
            margin-bottom: 1rem;
            padding: 1rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .search-input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            font-size: 16px;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .data-table {{
                font-size: 0.8rem;
            }}
            
            .data-table th,
            .data-table td {{
                padding: 8px 4px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Data retrieved from SQL Server database</p>
        </div>
        
        <div class="search-container">
            <input type="text" id="searchInput" class="search-input" 
                   placeholder="Search table data...">
        </div>
        
        {table_html}
        
        <div class="footer">
            <p>Generated by SQL Server to Web Page Script</p>
            <p>© {datetime.now().year} - Data Report</p>
        </div>
    </div>
    
    <script>
        // Simple search functionality
        document.getElementById('searchInput').addEventListener('keyup', function() {{
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.data-table tbody tr');
            
            tableRows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }});
        
        // Add click-to-sort functionality
        document.querySelectorAll('.data-table th').forEach((header, index) => {{
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {{
                sortTable(index);
            }});
        }});
        
        function sortTable(columnIndex) {{
            const table = document.querySelector('.data-table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            rows.sort((a, b) => {{
                const aText = a.cells[columnIndex].textContent.trim();
                const bText = b.cells[columnIndex].textContent.trim();
                
                // Try to parse as numbers first
                const aNum = parseFloat(aText);
                const bNum = parseFloat(bText);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {{
                    return aNum - bNum;
                }}
                
                return aText.localeCompare(bText);
            }});
            
            // Re-add sorted rows
            rows.forEach(row => tbody.appendChild(row));
        }}
    </script>
</body>
</html>"""
        
        return html
    
    def save_to_file(self, content: str, filename: str = None) -> str:
        """
        Save content to HTML file
        
        Args:
            content: HTML content to save
            filename: Output filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"database_report_{timestamp}.html"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ HTML file saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")
            return None

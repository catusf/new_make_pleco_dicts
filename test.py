import sqlite3
import csv

def export_table_to_csv(db_path, table_name, output_csv_path):
    """
    Exports a table from a SQLite database to a CSV file.

    Args:
        db_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to export.
        output_csv_path (str): Path to the output CSV file.
    """
    conn = None  # Initialize conn to ensure it's accessible in finally block
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to fetch all data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Write data to CSV
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)        # Write data rows

        print(f"Table '{table_name}' exported successfully to '{output_csv_path}'")

    except sqlite3.Error as e:
        print(f"Error exporting table: {e}")

    finally:
        # Close the connection only if it was successfully opened
        if conn:
            conn.close()

# Usage example
if __name__ == "__main__":
    database_path = "data/hanlearn.db"  # Path to your SQLite database file
    table_name = "words"  # Name of the table to export
    csv_output_path =f"data/hanlearn-{table_name}.csv"  # Path to save the CSV file

    export_table_to_csv(database_path, table_name, csv_output_path)


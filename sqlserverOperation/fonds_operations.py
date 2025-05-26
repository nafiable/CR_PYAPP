# sqlserverOperation/fonds_operations.py

import pyodbc # Assuming you are using pyodbc for SQL Server connection

def create_fonds(conn: pyodbc.Connection, fonds_data: dict):
    """
    Creates a new record in the 'fonds' table in SQL Server.

    Args:
        conn: The pyodbc database connection object.
        fonds_data: A dictionary containing the data for the new fonds record.
                    Example: {'nom': 'Fonds A', 'symbole': 'FA'}
    """
    try:
        cursor = conn.cursor()
        # TODO: Implement the SQL INSERT statement for the 'fonds' table.
        # Use parameterized queries to prevent SQL injection.
        # Example (replace with actual column names and data placeholders):
        # sql = "INSERT INTO fonds (column1, column2) VALUES (?, ?)"
        # cursor.execute(sql, (fonds_data['key1'], fonds_data['key2']))
        conn.commit()
        print("Fonds record created successfully.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error creating fonds record: {ex}")
        conn.rollback() # Rollback changes if an error occurs

def get_fonds(conn: pyodbc.Connection, fonds_id: int = None, symbole: str = None):
    """
    Retrieves records from the 'fonds' table in SQL Server.

    Args:
        conn: The pyodbc database connection object.
        fonds_id: The ID of the fonds to retrieve (optional).
        symbole: The symbol of the fonds to retrieve (optional).

    Returns:
        A list of dictionaries, where each dictionary represents a fonds record,
        or None if no records are found or an error occurs.
    """
    try:
        cursor = conn.cursor()
        # TODO: Implement the SQL SELECT statement for the 'fonds' table.
        # Add WHERE clauses based on fonds_id or symbole if provided.
        # Use parameterized queries.
        sql = "SELECT * FROM fonds"
        params = []
        if fonds_id is not None:
            sql += " WHERE id = ?"
            params.append(fonds_id)
        elif symbole is not None:
            sql += " WHERE symbole = ?"
            params.append(symbole)

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        # TODO: Convert the fetched rows to a list of dictionaries.
        # This depends on how you want to structure the output.
        # Example:
        # columns = [column[0] for column in cursor.description]
        # fonds_list = [dict(zip(columns, row)) for row in rows]
        fonds_list = rows # Placeholder

        return fonds_list if fonds_list else None
    except pyodbc.Error as ex:
        print(f"Error retrieving fonds record(s): {ex}")
        return None

def update_fonds(conn: pyodbc.Connection, fonds_id: int, updated_data: dict):
    """
    Updates a record in the 'fonds' table in SQL Server.

    Args:
        conn: The pyodbc database connection object.
        fonds_id: The ID of the fonds record to update.
        updated_data: A dictionary containing the data to update.
                      Example: {'nom': 'Nouveau Nom', 'symbole': 'NN'}
    """
    try:
        cursor = conn.cursor()
        # TODO: Implement the SQL UPDATE statement for the 'fonds' table.
        # Use parameterized queries. Construct the SET clause dynamically
        # from the updated_data dictionary.
        # Example:
        # sql = "UPDATE fonds SET column1 = ?, column2 = ? WHERE id = ?"
        # params = [updated_data['key1'], updated_data['key2'], fonds_id]
        # cursor.execute(sql, params)
        conn.commit()
        print(f"Fonds record with ID {fonds_id} updated successfully.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error updating fonds record with ID {fonds_id}: {ex}")
        conn.rollback()

def delete_fonds(conn: pyodbc.Connection, fonds_id: int):
    """
    Deletes a record from the 'fonds' table in SQL Server.

    Args:
        conn: The pyodbc database connection object.
        fonds_id: The ID of the fonds record to delete.
    """
    try:
        cursor = conn.cursor()
        # TODO: Implement the SQL DELETE statement for the 'fonds' table.
        # Use parameterized queries.
        # Example:
        # sql = "DELETE FROM fonds WHERE id = ?"
        # cursor.execute(sql, (fonds_id,))
        conn.commit()
        print(f"Fonds record with ID {fonds_id} deleted successfully.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error deleting fonds record with ID {fonds_id}: {ex}")
        conn.rollback()

# Example usage (assuming you have a connection object 'conn'):
if __name__ == '__main__':
    # This is a placeholder and won't work without a real connection
    # from database.connexionsqlServer import create_sqlserver_connection
    # conn = create_sqlserver_connection()
    #
    # if conn:
    #     # Example create
    #     # new_fonds = {'nom': 'Test Fonds', 'symbole': 'TF'}
    #     # create_fonds(conn, new_fonds)
    #
    #     # Example read
    #     # fonds_records = get_fonds(conn, symbole='TF')
    #     # print(fonds_records)
    #
    #     # Example update
    #     # update_data = {'nom': 'Updated Test Fonds'}
    #     # update_fonds(conn, fonds_id=1, updated_data=update_data) # Replace 1 with an actual ID
    #
    #     # Example delete
    #     # delete_fonds(conn, fonds_id=1) # Replace 1 with an actual ID
    #
    #     conn.close()
    pass
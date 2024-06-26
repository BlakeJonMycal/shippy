import sqlite3
import json

def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data['name'], ship_data['hauler_id'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False

def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Ship WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "query_params" in url and "_expand" in url["query_params"] and "hauler" in url["query_params"]["_expand"]:
            db_cursor.execute("""
             SELECT                                                                                                                                      
                s.id,
                s.name,
                s.hauler_id,
                h.id AS haulerId,
                h.name AS haulerName,
                h.dock_id AS haulerDockId
            FROM Ship s
            JOIN Hauler h ON s.hauler_id = h.id
            """)
        else:
            db_cursor.execute("""
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        ships = []
        for row in query_results:
            ship = {
                "id": row['id'],
                "name": row['name'],
                "hauler_id": row["hauler_id"]
            }
            if "query_params" in url and "_expand" in url["query_params"] and "hauler" in url["query_params"]["_expand"]:
                hauler = {
                    "id": row['haulerId'],
                    "name": row['haulerName'],
                    "dock_id": row["haulerDockId"]
                }
                ship["hauler"] = hauler

            ships.append(ship)

        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships

def retrieve_ship(pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.hauler_id
        FROM Ship s
        WHERE s.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        dictionary_version_of_object = dict(query_results)
        serialized_ship = json.dumps(dictionary_version_of_object)

    return serialized_ship

def make_ship(ship_data):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        # Write the SQL query to insert ship data into the Ship table
        db_cursor.execute(
            """
            INSERT INTO Ship (name, hauler_id)
            VALUES (?, ?)
            """,
            (ship_data['name'], ship_data['hauler_id'])
        )

        # Get the ID of the newly inserted ship
        new_ship_id = db_cursor.lastrowid

    # Return the ID of the newly created ship
    return new_ship_id

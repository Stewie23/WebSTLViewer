import argparse
import sqlite3

def check_tags(name_part, tag):
    # Connect to the SQLite database
    conn = sqlite3.connect('stlDatabase.db')
    cursor = conn.cursor()

    # Retrieve item IDs from the Items table based on the name part
    cursor.execute("SELECT itemID FROM Items WHERE name COLLATE BINARY LIKE ?", ('%' + name_part + '%',))
    item_ids = cursor.fetchall()

    for item_id in item_ids:
        # Check if itemID exists in the Taggings table for the given tag
        cursor.execute("SELECT * FROM Taggins WHERE itemID=? AND tag=?", (item_id[0], tag))
        result = cursor.fetchone()

        if result is None:
            # Add the tag for the itemID
            cursor.execute("INSERT INTO Taggins (itemID, tag) VALUES (?, ?)", (item_id[0], tag))
            print(f"Added tag: {tag} for itemID: {item_id[0]}")
        else:
            print(f"Tag: {tag} already exists for itemID: {item_id[0]}")



    

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for adding additional tags.")
    parser.add_argument("-n", "--name", type=str, help="part of the item name")
    parser.add_argument("-t", "--tag", type=str, help="Tag to be added")
    args = parser.parse_args()

    check_tags(args.name, args.tag)


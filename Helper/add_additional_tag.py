import argparse
import sqlite3

def check_tags(existing_tag, new_tag):
    # Connect to the SQLite database
    conn = sqlite3.connect('stlDatabase.db')
    cursor = conn.cursor()

    # Check if existing_tag exists in Taggings table
    cursor.execute("SELECT * FROM Taggins WHERE tag=?", (existing_tag,))
    existing_result = cursor.fetchone()

    if existing_result is None:
        print(f"The existing_tag: {existing_tag} is not present in the Taggings table. Something is wrong!")
        conn.close()
        return

    # Retrieve itemIDs from the Items table
    cursor.execute("SELECT itemID FROM Items")
    item_ids = cursor.fetchall()
    for item_id in item_ids:
        # Check if itemID exists in the Taggings table for the existing_tag
        cursor.execute("SELECT * FROM Taggins WHERE itemID=? AND tag=?", (item_id[0], existing_tag))
        existing_result = cursor.fetchone()

        #item does not have tag do nothing
        if existing_result is None:
            continue

        # Check if itemID exists in the Taggings table for the new_tag
        cursor.execute("SELECT * FROM Taggins WHERE itemID=? AND tag=?", (item_id[0], new_tag))
        new_result = cursor.fetchone()

        if new_result is None:
            # Add the new_tag for the itemID
            cursor.execute("INSERT INTO Taggins (itemID, tag) VALUES (?, ?)", (item_id[0], new_tag))
            print(f"Added new_tag: {new_tag} for itemID: {item_id[0]}")
        else:
            print(f"new_tag: {new_tag} already exists for itemID: {item_id[0]}")

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for adding additional tags.")
    parser.add_argument("-e", "--existing_tag", type=str, help="Existing tag in the database")
    parser.add_argument("-n", "--new_tag", type=str, help="Tag to be added")
    args = parser.parse_args()

    check_tags(args.existing_tag, args.new_tag)


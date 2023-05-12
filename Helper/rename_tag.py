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
    
    # Update the existing_tag with the new_tag name
    cursor.execute("UPDATE Taggins SET tag=? WHERE tag=?", (new_tag, existing_tag))
    print(f"Tag: {existing_tag} has been renamed to: {new_tag}")

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for adding additional tags.")
    parser.add_argument("-e", "--existing_tag", type=str, help="Existing tag in the database")
    parser.add_argument("-n", "--new_tag", type=str, help="Renamed tag")
    args = parser.parse_args()

    check_tags(args.existing_tag, args.new_tag)


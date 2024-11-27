import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, "locations.txt") # Path to the locations file

def change_data():
    position = load_data()
    
    # Display the current locations
    print("This is the current data:")
    for i, row in enumerate(position, start=1):
        print(f"{i}: {row}") 

    choice = input("\nDo you want to add or remove data? (A to add, R to remove): ").strip().upper()

        # Add new data
    if choice == "A":
        name = input("Enter name (e.g., Relative_11): ")
        street = input("Enter street name: ")
        district = input("Enter district name: ")
        latitude = float(input("Enter latitude (e.g., 37.1234): "))
        longitude = float(input("Enter longitude (e.g., 127.5678): "))
        print("Invalid latitude or longitude. Please enter valid numbers.")

            # Append new data to the locations file
        position.append([name, street, district, latitude, longitude])
        print("\nNew data added successfully!")

        # Remove data
    elif choice == "R":
        try:
            # Ask user which location to remove
            index = int(input(f"Enter the row number to remove (1-{len(position)}): ")) - 1
            if 0 <= index < len(position):
                removed = position.pop(index)  # Remove the selected entry
                print(f"\nRemoved the following entry: {removed}")
            else:
                print("Invalid row number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    else:
        print("\nInvalid choice. Please enter 'A' to add or 'R' to remove.")

        # Show updated data and save the updated locations
    if (choice == "A" or choice == "R"):
        print("\nUpdated data:")
        for row in position:
            print(row)
        save_data(position)
    
def save_data(position):
        # Open the locations file and write to it
    with open(FILE_PATH, "w") as file:
        for row in position:
            file.write(",".join(map(str, row)) + "\n")

def load_data():
        # Finds the absolute path to the current file's directory
    position = []
        # Open the locations file and read it's content
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()
    
        # Process each line
    for line in lines:
        line = line.strip()
        parts = line.split(",")  # Split the line by commas
        entry = [parts[0], parts[1], parts[2], float(parts[3]), float(parts[4])]
        position.append(entry)

        # Return all the locations
    return position

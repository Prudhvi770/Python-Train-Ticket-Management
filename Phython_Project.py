import pandas as pd
import os
import json
from datetime import datetime

# Storing data to file paths
TRAIN_DATA_FILE = "trains.csv"
BOOKING_DATA_FILE = "bookings.json"

def initializing_files():
    # Initializing train data
    if not os.path.exists(TRAIN_DATA_FILE):
        train_data = {
            'Train No': [101, 102, 103],
            'Train Name': ['Express A1', 'Express A2', 'Express A3'],
            'From': ['City B1 ', 'City B2 ', 'City B3 '],
            'To': ['City C1', 'City C2', 'City C3'],
            'Seats Available': [100, 50, 75]
        }
        df = pd.DataFrame(train_data)
        df.to_csv(TRAIN_DATA_FILE, index=False)

    # Initializing booking data
    if not os.path.exists(BOOKING_DATA_FILE):
        with open(BOOKING_DATA_FILE, 'w') as file:
            json.dump([], file)

# Taking data from CSV
def Load_train_data():
    return pd.read_csv(TRAIN_DATA_FILE)

# Taking bookings from JSON
def Load_bookings():
    with open(BOOKING_DATA_FILE, 'r') as file:
        return json.load(file)
    
# Save bookings data to JSON
def Save_bookings(bookings):
    with open(BOOKING_DATA_FILE, 'w') as file:
        json.dump(bookings, file)
        
# Display all available trains details
def Available_trains():
    trains = Load_train_data()
    print("\n Available Trains:")
    print(trains.to_string(index=False))

# Booking a ticket
def booking_ticket():
    trains = Load_train_data()
    bookings = Load_bookings()

    try:
        train_no = int(input("\n Enter Train Number to Book: "))
    except ValueError:
        print("Incorrect input...! Please enter a correct train number.")
        return

    train_row = trains[trains['Train No'] == train_no]
    if train_row.empty:
        print("Train was not found...!")
        return

    available_seats = train_row['Seats Available'].values[0]
    if available_seats == 0:
        print("No seats are available...!")
        return

    name = input("Enter Passenger Name: ").strip()
    if not name:
        print("Passenger name can not be empty.")
        return

    try:
        age = int(input("Enter Passenger Age: "))
        if age <= 0:
            print("Age cannot be a negative number.")
            return
    except ValueError:
        print("Incorrect age...! Please enter a number.")
        return

    try:
        seat_count = int(input("Number of Seats: "))
        if seat_count <= 0:
            print("Seat count cannot be negative.")
            return
    except ValueError:
        print("Invalid seat count! Please enter a number.")
        return

    if seat_count > available_seats:
        print("Only ",available_seats," seats available. Cannot book ",seat_count ," seats.")
        return

    booking_ref = f"{train_no}_{len(bookings) + 1}"
    booking_details = {
        'Booking Ref': booking_ref,
        'Train No': train_no,
        'Name': name,
        'Age': age,
        'Seats': seat_count,
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    bookings.append(booking_details)
    Save_bookings(bookings)

    trains.loc[trains['Train No'] == train_no, 'Seats Available'] -= seat_count
    trains.to_csv(TRAIN_DATA_FILE, index=False)

    print("Booking Successful...! Reference No: ",booking_ref)


# Cancel a ticket Bookings
def Cancel_booking():
    bookings = Load_bookings()
    
    booking_ref = input("Enter the specific Booking Reference to Cancel: ")
    for booking in bookings:
        if booking['Booking Ref'] == booking_ref:
            bookings.remove(booking)
            Save_bookings(bookings)
            
            # Updating train seat 
            trains = Load_train_data()
            trains.loc[trains['Train No'] == booking['Train No'], 'Seats Available'] += booking['Seats']
            trains.to_csv(TRAIN_DATA_FILE, index=False)

            print("Booking ",booking_ref," canceled successfully.")
            return
    print("Booking cannot found...!")

# View all bookings
def See_bookings():
    bookings = Load_bookings()
    if not bookings:
        print("No bookings are available.")
        return

    print("\nAll Bookings:")
    df = pd.DataFrame(bookings)
    print(df.to_string(index=False))

# Main menu of the Train Ticket Booking System
def main_display():
    while True:
        print("\nTrain Ticket Booking System")
        print("1. View Available Trains")
        print("2. Book a Ticket")
        print("3. Cancel a Ticket")
        print("4. View Bookings")
        print("5. Exit")

        choice = input("Choose an respective option: ")
        
        if choice == '1':
            Available_trains()
        elif choice == '2':
            booking_ticket()
        elif choice == '3':
            Cancel_booking()
        elif choice == '4':
            See_bookings()
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Incorrect choice...! Please try again.")

if __name__ == "__main__":
    initializing_files()
    main_display()
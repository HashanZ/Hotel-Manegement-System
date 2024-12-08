from datetime import date

# Room Class
class Room:
    def __init__(self, number, room_type, price):
        self.number = number
        self.room_type = room_type
        self.price = price
        self.available = True

    def __str__(self):
        return f"Room {self.number} ({self.room_type}) - ${self.price} per night"

    def mark_unavailable(self):
        self.available = False

    def mark_available(self):
        self.available = True


# Guest Class
class Guest:
    def __init__(self, guest_id, name, email):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.reservations = []

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def view_reservations(self):
        print(f"Reservations for {self.name}:")
        for res in self.reservations:
            print(res)

    def __str__(self):
        return f"{self.name} ({self.email})"


# Reservation Class
class Reservation:
    def __init__(self, reservation_id, guest, room, check_in_date, check_out_date):
        if check_in_date >= check_out_date:
            raise ValueError("Check-out date must be after check-in date")
        
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = self.calculate_price()

    def calculate_price(self):
        stay_duration = (self.check_out_date - self.check_in_date).days
        return stay_duration * self.room.price

    def confirm_reservation(self):
        self.room.mark_unavailable()
        self.guest.make_reservation(self)

    def cancel_reservation(self):
        self.room.mark_available()

    def __str__(self):
        return f"Reservation ID {self.reservation_id}: {self.room} from {self.check_in_date} to {self.check_out_date} - ${self.total_price}"


# Employee Class
class Employee:
    def __init__(self, employee_id, name, position):
        self.employee_id = employee_id
        self.name = name
        self.position = position

    def assign_room(self, room):
        if room.available:
            print(f"Room {room.number} has been assigned.")
        else:
            raise ValueError(f"Room {room.number} is already booked.")

    def __str__(self):
        return f"{self.name} - {self.position}"


# Admin Class (inherits from Employee)
class Admin(Employee):
    def __init__(self, employee_id, name):
        super().__init__(employee_id, name, position="Admin")

    def add_new_room(self, hotel, room):
        if room not in hotel.rooms:
            hotel.add_room(room)
            print(f"Room {room.number} has been added.")
        else:
            raise ValueError(f"Room {room.number} already exists in the hotel.")

    def remove_room(self, hotel, room_number):
        room = hotel.get_room_by_number(room_number)
        if room:
            hotel.remove_room(room)
            print(f"Room {room.number} has been removed.")
        else:
            raise ValueError(f"Room {room_number} does not exist in the hotel.")

    def view_all_reservations(self, hotel):
        print("All reservations in the hotel:")
        for reservation in hotel.reservations:
            print(reservation)


# Hotel Class
class Hotel:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.rooms = []
        self.reservations = []

    def add_room(self, room):
        self.rooms.append(room)

    def remove_room(self, room):
        self.rooms.remove(room)

    def book_room(self, reservation):
        if reservation.room.available:
            reservation.confirm_reservation()
            self.reservations.append(reservation)
            print(f"Reservation for room {reservation.room.number} has been confirmed.")
        else:
            raise ValueError(f"Room {reservation.room.number} is not available for the selected dates.")

    def check_availability(self):
        available_rooms = [room for room in self.rooms if room.available]
        return available_rooms

    def get_room_by_number(self, room_number):
        for room in self.rooms:
            if room.number == room_number:
                return room
        return None

    def __str__(self):
        return f"{self.name} - {self.address}"


# Main Execution
def main():
    # Create a hotel
    hotel = Hotel("Grand Plaza", "1234 Sunset Blvd")

    # Add rooms to the hotel
    room1 = Room(101, "Single", 100.0)
    room2 = Room(102, "Double", 150.0)
    room3 = Room(103, "Suite", 200.0)

    hotel.add_room(room1)
    hotel.add_room(room2)
    hotel.add_room(room3)

    # Create a guest
    guest1 = Guest(1, "John Doe", "john@example.com")

    # Create a reservation with incorrect dates (check-out before check-in)
    try:
        check_in_date = date(2024, 12, 5)
        check_out_date = date(2024, 12, 1)
        reservation1 = Reservation(1, guest1, room1, check_in_date, check_out_date)
    except Exception as e:
        print(f"Error in reservation creation: {e}")

    # Try to book a room that is already booked
    try:
        check_in_date = date(2024, 12, 1)
        check_out_date = date(2024, 12, 5)
        reservation1 = Reservation(1, guest1, room1, check_in_date, check_out_date)
        hotel.book_room(reservation1)  # First booking
        reservation2 = Reservation(2, guest1, room1, date(2024, 12, 2), date(2024, 12, 4))  # Same room
        hotel.book_room(reservation2)  # Second booking for the same room (should fail)
    except Exception as e:
        print(f"Error during booking: {e}")

    # View guest's reservations
    guest1.view_reservations()

    # Create an employee
    employee1 = Employee(1, "Alice", "Front Desk")

    # Employee trying to assign an unavailable room
    try:
        employee1.assign_room(room1)  # Room 1 is already booked, should fail
    except Exception as e:
        print(f"Error while assigning room: {e}")

    # Create an admin
    admin1 = Admin(1, "Bob")

    # Admin adding a room that already exists (duplicate)
    try:
        admin1.add_new_room(hotel, room1)  # Room 1 already exists in hotel
    except Exception as e:
        print(f"Error while adding room: {e}")

    # Admin removing a non-existing room (room 999 doesn't exist)
    try:
        admin1.remove_room(hotel, 999)  # Room 999 does not exist
    except Exception as e:
        print(f"Error while removing room: {e}")

    # Admin viewing all reservations
    admin1.view_all_reservations(hotel)

    # Check available rooms after booking
    available_rooms = hotel.check_availability()
    print("\nAvailable rooms after booking:")
    for room in available_rooms:
        print(room)

    # Cancel a reservation and check room availability
    try:
        reservation1.cancel_reservation()
    except Exception as e:
        print(f"Error during cancellation: {e}")

    # Available rooms after canceling reservation
    available_rooms = hotel.check_availability()
    print("\nAvailable rooms after canceling reservation:")
    for room in available_rooms:
        print(room)


if __name__ == "__main__":
    main()
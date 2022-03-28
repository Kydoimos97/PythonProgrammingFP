# Created by Willem van der Schans

import FPCore
import datetime

# This file will create some mock data to work with while testing the database.
# Here you add some data manually but in the user_ui data is pulled automatically

# Create Classes
Airport = FPCore.Airport()
Airplane = FPCore.Airplane()
Flight = FPCore.Flight()
Customer = FPCore.Customer()
Reservation = FPCore.Reservation()
Seatmap = FPCore.Seatmap()
Costs = FPCore.Costs()

# Reset_Database
Airport.connect()
Airport.reset_database()

Airplane.connect()
Airplane.reset_database()

Flight.connect()
Flight.reset_database()

Customer.connect()
Customer.reset_database()

Reservation.connect()
Reservation.reset_database()

Seatmap.connect()
Seatmap.reset_database()

Costs.connect()
Costs.reset_database()


# Add Data to test with
Airport.add("United States", "New York", 1.5)
Airport.add("Netherlands", "Amsterdam", 2)
Airport.add("United States", "Los Angeles", 1)
Airport.add("United States", "Salt Lake City", 1.5)
Airport.add("United Kingdom", "London", 1.5)

Customer.add("Willem", "P", "van der Schans", "The Netherlands", "23423F", 2331)
Customer.add("Ali", None, "Scotty", "United Kingdom", "156ASD", 3245325)
Customer.add("Johan", "Z", "Jodocus", "United States", "21321ASD", 764185615)
Customer.add("Will", "G", "Smith", "United States", "23423DS", 15616)

Airplane.add("Boeing", "Airbus 373", 1500, 9, 10, 1, 6, 5, 2, 2, 2, 10)
Airplane.add("Boeing", "Airbus 747", 2500, 9, 25, 1, 6, 15, 2, 4, 10, 5)

Flight.add(1, 2, 1, datetime.datetime(2020, 3, 26, 15, 20), 7)
Flight.add(1, 1, 2, datetime.datetime(2022, 3, 27, 10, 0), 8)
Flight.add(2, 1, 3, datetime.datetime(2022, 3, 26, 8, 45), 6)
Flight.add(2, 3, 4, datetime.datetime(2022, 3, 27, 19, 22), 2)
Flight.add(2, 4, 5, datetime.datetime(2022, 3, 28, 8, 00), 10)

Seatmap.add(1)
Seatmap.add(2)
Seatmap.add(3)
Seatmap.add(4)
Seatmap.add(5)

Costs.refresh()


Reservation.add(1, 1, 180, "01A", datetime.datetime.now())
Reservation.add(2, 1, 180, "10A", datetime.datetime.now())
Reservation.add(3, 2, 180, "10A", datetime.datetime.now())

Airport.close_db()



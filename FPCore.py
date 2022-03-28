# Created by Willem van der Schans

import FPBase as db
import string
import datetime



# Note if a function has not been commented on they are extremely simple and should be easy to understand.

class Airport(db.Dbase):
    # This class holds airport data including the location of the airport and a cost multiplier based on airport fees.

    def __init__(self):
        super().__init__("airdb.sqlite")

    def update(self, dest_id, country, city, price_mult):
        try:
            super().connect()
            super().get_cursor.execute("""UPDATE Airport SET country = ?, city = ?, price_mult = ? 
            WHERE dest_id = ?;""", (country, city, price_mult, dest_id))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add(self, country, city, price_mult):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT OR IGNORE INTO Airport(country, city, price_mult) VALUES (?,?,?);""",
                (country, city, price_mult))
            super().get_connection.commit()
            super().close_db()
            print("Added Destination to Database")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, dest_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Airport WHERE dest_id = ?;""", (dest_id,))
            super().get_connection.commit()
            super().close_db()
            print("Airport Deleted")
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, dest_id=None, country=None, city=None):
        try:
            super().connect()
            if dest_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Airport WHERE dest_id = ?;""", (dest_id,)).fetchone()
            elif country is not None and city is not None:
                return super().get_cursor.execute("""SELECT * FROM Airport WHERE country = ? AND city = ?;""",
                                                  (country, city)).fetchall()
            else:
                return super().get_cursor.execute("""SELECT * FROM Airport;""").fetchall()
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Airport;
            
            CREATE TABLE Airport (
                dest_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                country TEXT NOT NULL, 
                city TEXT NOT NULL, 
                price_mult NUMERIC NOT NULL
            );
            """

        super().execute(sql)
        super().close_db()

    def table_information(self):
        try:
            super().connect()
            return super().get_cursor.execute("SELECT * FROM pragma_table_info(?);",
                                              (self.__class__.__name__,)).fetchall()

        except Exception as e:
            print("An error occurred.", e)


class Customer(Airport):

    def update(self, customer_id, first_name, middle_name, last_name, country, document_number, loyalty_number=None):
        super().connect()
        super().get_cursor.execute("""UPDATE Customer SET first_name = ?, middle_name = ?, last_name = ?, 
        country = ?, document_number = ?, loyalty_number = ? WHERE customer_id = ?;""",
                                   (first_name, middle_name, last_name, country, document_number, loyalty_number,
                                    customer_id))
        super().get_connection.commit()
        super().close_db()

    def add(self, first_name, middle_name, last_name, country, document_number, loyalty_number=None):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT OR IGNORE INTO Customer(first_name, middle_name, last_name, 
                country, document_number, loyalty_number) VALUES (?,?,?,?,?,?);""",
                (first_name, middle_name, last_name, country, document_number, loyalty_number))
            super().get_connection.commit()
            super().close_db()
            print("Added Customer to Database")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, customer_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Customer WHERE customer_id = ?;""", (customer_id,))
            super().get_connection.commit()
            super().close_db()
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, customer_id=None, first_name=None, middle_name=None, last_name=None, document_number=None):
        try:
            super().connect()

            if customer_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Customer WHERE customer_id = ?;""",
                                                  (customer_id,)).fetchall()

            # with some customers not having a middle name logic needed to be included for the code to work for these cases.
            # First a name check is done after which a middle_name check is done, which then directs the loop to the right point.
            elif first_name is not None and last_name is not None:
                if middle_name is not None:
                    return super().get_cursor.execute(
                        """SELECT * FROM Customer WHERE first_name = ? AND middle_name = ? AND last_name = ?;""",
                        (first_name, middle_name, last_name)).fetchone()
                else:
                    return super().get_cursor.execute(
                        """SELECT * FROM Customer WHERE first_name = ? AND last_name = ?;""",
                        (first_name, last_name)).fetchone()
            elif document_number is not None:
                return super().get_cursor.execute("""SELECT * FROM Customer WHERE document_number = ?;""",
                                                  (document_number,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Customer;""").fetchall()

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Customer;

            CREATE TABLE Customer (
                customer_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                first_name TEXT NOT NULL, 
                middle_name TEXT, 
                last_name TEXT NOT NULL, 
                country TEXT NOT NULL, 
                document_number TEXT NOT NULL, 
                loyalty_number INTEGER
            );
            """

        super().execute(sql)
        super().close_db()


class Airplane(Airport):
    # This class has a lot of arguments due to the array generation of the seatmap.

    def update(self, airplane_id, manufacturer, airplane_type, cost_flighthour,
               rowsize_econ, colsize_econ, pricemult_econ,
               rowsize_mid, colsize_mid, pricemult_mid,
               rowsize_first, colsize_first, pricemult_first):
        super().connect()
        super().get_cursor.execute(
            """UPDATE Airplane SET manufacturer = ?,  airplane_type = ?, cost_flighthour = ?,
             rowsize_econ = ? , colsize_econ = ?, pricemult_econ = ?, 
             rowsize_mid = ? , colsize_mid = ?, pricemult_mid = ?, 
             rowsize_first = ? , colsize_first = ?, pricemult_first = ? WHERE airplane_id = ?;""",
            (manufacturer, airplane_type, cost_flighthour,
             rowsize_econ, colsize_econ, pricemult_econ,
             rowsize_mid, colsize_mid, pricemult_mid, rowsize_first,
             colsize_first, pricemult_first, airplane_id))
        super().get_connection.commit()
        super().close_db()

    def add(self, manufacturer, airplane_type, cost_flighthour,
            rowsize_econ, colsize_econ, pricemult_econ,
            rowsize_mid, colsize_mid, pricemult_mid,
            rowsize_first, colsize_first, pricemult_first):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT OR IGNORE INTO Airplane(
                manufacturer, airplane_type, cost_flighthour, 
                rowsize_econ, colsize_econ, pricemult_econ, 
                rowsize_mid, colsize_mid, pricemult_mid, 
                rowsize_first, colsize_first, pricemult_first) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);""",
                (manufacturer, airplane_type, cost_flighthour,
                 rowsize_econ, colsize_econ, pricemult_econ,
                 rowsize_mid, colsize_mid, pricemult_mid,
                 rowsize_first, colsize_first, pricemult_first))
            super().get_connection.commit()
            super().close_db()
            print("Added Airplane to Database")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, airplane_id):
        try:
            super().connect()
            flight_id = super().get_cursor.execute("""SELECT flight_id FROM flight where airplane_id = ?;""",
                                                   (airplane_id,)).fetchall()
            # Due to a number of interdependencies it is vital that if an airplane gets removed this change is continued on depended tables.
            for i in flight_id:
                super().get_cursor.execute("""DELETE FROM Seatmap WHERE Seatmap.flight_id = ?;""", (int(i),))
                super().get_cursor.execute("""DELETE FROM Reservation WHERE flight_id = ?;""", (int(i),))
                super().get_cursor.execute("""DELETE FROM Flight WHERE flight_id = ?;""", (int(i),))
            super().get_cursor.execute("""DELETE FROM Airplane WHERE airplane_id = ?;""", (airplane_id,))
            super().get_connection.commit()
            super().close_db()
            print("Airplane Deleted")
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, airplane_id=None, manufacturer=None, airplane_type=None):
        try:
            super().connect()
            if airplane_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Airplane WHERE airplane_id = ?;""",
                                                  (airplane_id,)).fetchall()
            elif manufacturer is not None and airplane_type is not None:
                return super().get_cursor.execute(
                    """SELECT * FROM Airplane WHERE manufacturer = ? AND airplane_type = ?;""",
                    (manufacturer, airplane_type))
            else:
                return super().get_cursor.execute("""SELECT * FROM Airplane;""").fetchall()

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Airplane;

            CREATE TABLE Airplane (
            airplane_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
            manufacturer TEXT NOT NULL , 
            airplane_type TEXT NOT NULL, 
            cost_flighthour NUMERIC NOT NULL, 
            rowsize_econ INTEGER NOT NULL, 
            colsize_econ INTEGER NOT NULL,  
            pricemult_econ NUMERIC NOT NULL, 
            rowsize_mid INTEGER, 
            colsize_mid INTEGER, 
            pricemult_mid NUMERIC, 
            rowsize_first INTEGER, 
            colsize_first INTEGER, 
            pricemult_first NUMERIC
            );
            """

        super().execute(sql)
        super().close_db()


class Flight(Airplane):

    def update(self, airplane_id, origin_id, dest_id, dept_date, flight_hours):
        super().connect()
        super().get_cursor.execute(
            """UPDATE Flight SET dept_date = ?, flight_hours = ? 
            WHERE airplane_id = ? AND origin_id = ? AND dest_id = ?;""",
            (dept_date, flight_hours, airplane_id, origin_id, dest_id))
        super().get_connection.commit()
        super().close_db()

    def add(self, airplane_id, origin_id, dest_id, dept_date, flight_hours):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT OR IGNORE INTO Flight(airplane_id, origin_id, dest_id, dept_date, flight_hours) VALUES (?,?,?,?,?);""",
                (airplane_id, origin_id, dest_id, dept_date, flight_hours))
            super().get_connection.commit()
            super().close_db()
            print("Added Flight to Database")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, flight_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Flight WHERE flight_id = ?;""", (flight_id,))
            super().get_connection.commit()
            super().close_db()
            print("Flight Deleted")
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, flight_id=None, airplane_id=None, origin_id=None, dest_id=None, query=None, query_country=None,
              query_city=None, start_date=None, end_date=None, seat_class=None):
        try:
            super().connect()
            # I needed a number of different fetch options here to be able to retrieve the right data from different inputs coming from the user_ui
            if query == "Country":
                return super().get_cursor.execute(
                    """SELECT DISTINCT Airport.country FROM Flight JOIN Airport on Flight.origin_id = Airport.dest_id""").fetchall()
            elif query_country is not None and query_city is None:
                return super().get_cursor.execute(
                    """SELECT DISTINCT Airport.city FROM Flight JOIN Airport on Flight.origin_id = Airport.dest_id WHERE Airport.country = ?;""",
                    (query_country,)).fetchall()
            elif query_country is not None and query_city is not None:
                return super().get_cursor.execute(
                    """SELECT DISTINCT Airport.dest_id FROM Flight JOIN Airport on Flight.origin_id = Airport.dest_id WHERE Airport.country = ? AND Airport.city = ?;""",
                    (query_country, query_city)).fetchone()
            elif start_date is not None and end_date is not None and origin_id is not None and dest_id is not None and seat_class is not None:
                return super().get_cursor.execute(
                    """SELECT DISTINCT Flight.flight_id, Flight.dept_date, COUNT(Seatmap.seat_id) From Flight Join Seatmap on Flight.flight_id=Seatmap.flight_id WHERE Flight.origin_id = ? AND Flight.dest_id = ? AND Seatmap.seat_class = ? AND Flight.dept_date BETWEEN ? AND ?;""",
                    (origin_id, dest_id, seat_class, start_date, end_date)).fetchall()
            elif flight_id is not None:
                return super().get_cursor.execute("""SELECT * FROM FLight WHERE flight_id = ?;""",
                                                  (flight_id,)).fetchone()
            elif airplane_id is not None:
                return super().get_cursor.execute("""SELECT flight_id FROM Flight WHERE airplane_id = ?;""",
                                                  (airplane_id,)).fetchall()
        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Flight;

            CREATE TABLE Flight (
                flight_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                airplane_id INTEGER NOT NULL, 
                origin_id INTEGER NOT NULL,
                dest_id INTEGER NOT NULL, 
                dept_date TIMESTAMP NOT NULL,
                flight_hours NUMERIC NOT NULL, 
                FOREIGN KEY (airplane_id) REFERENCES Airplane(airplane_id), 
                FOREIGN KEY (dest_id) REFERENCES Airport(dest_id),
                FOREIGN KEY (origin_id) REFERENCES AIRPORT(dest_id)
            );
            """

        super().execute(sql)
        super().close_db()


class Seatmap(Airplane):
    # The seatmap is the hardest class especially the add class is quite large.
    # What happens in the add class is that the seatmap is automatically generated for each flight based on airplane data.

    def add(self, flight_id):

        try:
            input_list = list()
            super().connect()
            airplane_id = super().get_cursor.execute(
                """SELECT airplane_id FROM Flight WHERE flight_id = ?;""", (flight_id,)).fetchone()[0]

            rowsize_econ = super().get_cursor.execute(
                """SELECT rowsize_econ FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            colsize_econ = super().get_cursor.execute(
                """SELECT colsize_econ FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            pricemult_econ = super().get_cursor.execute(
                """SELECT pricemult_econ FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            rowsize_mid = super().get_cursor.execute(
                """SELECT rowsize_mid FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            colsize_mid = super().get_cursor.execute(
                """SELECT colsize_mid FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            pricemult_mid = super().get_cursor.execute(
                """SELECT pricemult_mid FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            rowsize_first = super().get_cursor.execute(
                """SELECT rowsize_first FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            colsize_first = super().get_cursor.execute(
                """SELECT colsize_first FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

            pricemult_first = super().get_cursor.execute(
                """SELECT pricemult_first FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()[0]

        # Here the classes within the airplane are assigned and all seats are set to "Available"
            for i in range(0, int(colsize_first)):
                if i < 9:
                    for x in range(0, int(rowsize_first)):
                        inp = (f"0{i + 1}{list(string.ascii_uppercase)[x]}", "F", "A", float(pricemult_first))
                        input_list.append(inp)
                else:
                    for x in range(0, int(rowsize_first)):
                        inp = (f"{i + 1}{list(string.ascii_uppercase)[x]}", "F", "A", float(pricemult_first))
                        input_list.append(inp)
            if colsize_mid is None:
                pass
            else:
                for i in range(int(colsize_first), int(colsize_first) + int(colsize_mid)):
                    for x in range(0, int(rowsize_mid)):
                        inp = (f"{i + 1}{list(string.ascii_uppercase)[x]}", "M", "A", float(pricemult_mid))
                        input_list.append(inp)
            for i in range(int(colsize_first) + int(colsize_mid),
                           int(colsize_first) + int(colsize_mid) + int(colsize_econ)):
                for x in range(0, int(rowsize_econ)):
                    inp = (f"{i + 1}{list(string.ascii_uppercase)[x]}", "E", "A", float(pricemult_econ))
                    input_list.append(inp)

            # Then a looping insert statement to create multiple rows.
            for item in input_list:
                super().get_cursor.execute(
                    """INSERT OR IGNORE INTO Seatmap(flight_id, seat_id, seat_class, seat_availability, class_mult) 
                    VALUES (?,?,?,?,?);""",
                    (flight_id, item[0], item[1], item[2], item[3]))
            super().get_connection.commit()
            super().close_db()
            print("Seatmap Updated")

        except Exception as e:
            print("An error occurred.", e)

    def delete(self, flight_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE FROM Seatmap WHERE flight_id = ?;""", (flight_id,))
            super().get_connection.commit()
            super().close_db()
            print("Seatmap Deleted")
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, flight_id=None, seat_id=None, seat_availability=None):
        try:
            super().connect()
            if flight_id is not None:
                super().get_cursor.execute("""SELECT seat_id FROM Seatmap WHERE flight_id = ?;""",
                                           (flight_id,)).fetchall()
            elif flight_id is not None and seat_id is not None:
                super().get_cursor.execute("""SELECT * FROM Seatmap WHERE flight_id = ? AND seat_id = ?;""",
                                           (flight_id, seat_id)).fetchall()
            elif flight_id is not None and seat_availability is not None:
                super().get_cursor.execute(
                    """SELECT seat_id FROM Seatmap WHERE flight_id = ? AND seat_availability = ?;""",
                    (flight_id, seat_availability)).fetchall()
            else:
                super().get_cursor.execute("""SELECT * FROM Flight;""").fetchall()

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def update(self, flight_id, seat_id, seat_availability):
        try:
            if seat_availability == "A" or seat_availability == "O":
                super().get_cursor.execute(
                    """UPDATE Seatmap SET seat_availability = ? WHERE flight_id = ? AND seat_id = ?;""",
                    (seat_availability, flight_id, seat_id))
                super().get_connection.commit()
                super().close_db()
        except Exception as e:
            print("An error occurred.", e)

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Seatmap;

            CREATE TABLE Seatmap (
                flight_id INTEGER NOT NULL, 
                seat_id TEXT NOT NULL, 
                seat_class TEXT NOT NULL, 
                seat_availability TEXT NOT NULL, 
                class_mult NUMERIC NOT NULL,
                PRIMARY KEY (flight_id, seat_id),
                FOREIGN KEY (flight_id) REFERENCES Flight(flight_id)
            );
            """

        super().execute(sql)
        super().close_db()


class Costs(Flight):
# The costs class is also quite complex and has no add or delete functions since no interaction should be albe to be had with the table directly.
# The table is refreshed and cleaned automatically at all times.
    def refresh(self, flight_id = None, base_price= 1):
        input_list = list()


        try:
            # First a refresh for when flight_id is not none allowing for price updates on specific flights.
            if flight_id is not None:
                super().connect()
                airplane_id = super().get_cursor.execute(
                    """SELECT airplane_id FROM Flight WHERE flight_id = ?;""", (flight_id,)).fetchone()[0]

                pricemult_econ = super().get_cursor.execute(
                    """SELECT pricemult_econ FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()

                pricemult_mid = super().get_cursor.execute(
                    """SELECT pricemult_mid FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()

                pricemult_first = super().get_cursor.execute(
                    """SELECT pricemult_first FROM Airplane WHERE airplane_id = ?;""", (airplane_id,)).fetchone()

                seat_list = super().get_cursor.execute(
                    """SELECT Seatmap.seat_id, Seatmap.seat_class, Seatmap.seat_availability From Seatmap WHERE flight_id = ?;""",
                    (flight_id,)).fetchall()

                flight_data = super().get_cursor.execute(
                    """SELECT Airport.price_mult, Flight.flight_hours From Flight JOIN Airport ON Flight.dest_id = Airport.dest_id WHERE Flight.flight_id = ?;""",
                    (flight_id,)).fetchone()

                for seat in seat_list:
                    seat_cost = 0
                    if seat[2] == "A":
                        if seat[1] == "F":
                            # The check here is nessecary to allow for over time price changes where
                            # reserved seats do not get assigned a new cost since they have already been sold.
                            seat_cost = base_price * float(flight_data[0]) * float(flight_data[1]) * float(
                                pricemult_first[0]) * float(flight_data[1])
                            input_list.append([flight_id, str(seat[0]), float(seat_cost)])
                        elif seat[1] == "M":
                            seat_cost = base_price * float(flight_data[0]) * float(flight_data[1]) * float(
                                pricemult_mid[0]) * float(flight_data[1])
                            input_list.append([flight_id, str(seat[0]), float(seat_cost)])
                        elif seat[1] == "E":
                            seat_cost = base_price * float(flight_data[0]) * float(flight_data[1]) * float(
                                pricemult_first[0]) * float(flight_data[1])
                            input_list.append([flight_id, str(seat[0]), float(seat_cost)])
                        else:
                            print("An error occurred seat_cost is 0")
                            input_list.append(seat_cost)
                    else:
                        pass  # seat is already occupied and paid for

                for item in input_list:
                    super().get_cursor.execute(
                        """INSERT OR REPLACE INTO Costs(flight_id, seat_id, seat_cost) VALUES (?,?,?);""",
                        (flight_id, item[1], item[2]))
                super().get_connection.commit()
                print("Seat Cost Updated")

            else:
                # Here all flights will get updated allowing for pricehikes to be added to the system.
                super().connect()
                airplane_id = super().get_cursor.execute(
                    """SELECT DISTINCT airplane_id, flight_id FROM Flight;""").fetchall()

                pricemult= super().get_cursor.execute(
                    """SELECT airplane_id, pricemult_econ, pricemult_mid, pricemult_econ FROM Airplane;""").fetchall()

                seat_list = super().get_cursor.execute(
                    """SELECT Seatmap.flight_id, Seatmap.seat_id, Seatmap.seat_class, Seatmap.seat_availability From Seatmap;""").fetchall()

                flight_data = super().get_cursor.execute(
                    """SELECT Airport.price_mult, Flight.flight_hours, Flight.flight_id From Flight JOIN Airport ON Flight.dest_id = Airport.dest_id;""").fetchall()

                for seat in seat_list:
                    for flight in airplane_id:
                        for price in pricemult:
                            if price[0] == flight[0] and flight[1] == seat[0]:

                                if seat[3] == "A":
                                    for data in flight_data:
                                        if data[2] == flight[1]:
                                            # The check here is nessecary to allow for over time price changes where
                                            # reserved seats do not get assigned a new cost since they have already been sold.
                                            if seat[2] == "F":
                                                seat_cost = base_price * float(data[0]) * float(
                                                    data[1]) * float(
                                                    price[3]) * float(data[1])
                                                input_list.append([flight[1], str(seat[1]), float(seat_cost)])
                                            elif seat[2] == "M":
                                                seat_cost = base_price * float(data[0]) * float(
                                                    data[1]) * float(
                                                    price[2]) * float(data[1])
                                                input_list.append([flight[1], str(seat[1]), float(seat_cost)])
                                            elif seat[2] == "E":
                                                seat_cost = base_price * float(data[0]) * float(
                                                    data[1]) * float(
                                                    price[1]) * float(data[1])
                                                input_list.append([flight[1], str(seat[1]), float(seat_cost)])
                                            else:
                                                print("An error occurred seat_cost is 0")
                                                input_list.append(seat_cost)
                                        else:
                                            pass  # seat is already occupied and paid for
                                else:
                                    pass
                            else:
                                pass

                for item in input_list:
                    super().get_cursor.execute(
                        """INSERT OR REPLACE INTO Costs(flight_id, seat_id, seat_cost) VALUES (?,?,?);""",
                        (item[0], item[1], item[2]))

                super().get_connection.commit()
                print("Seat Cost Updated")

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def clean(self):
        # This function checks for missing flights (removed from the system) and removes all cost data from deleted flights automatically.
        try:
            super().connect()
            id_list = []
            flight_id = super().get_cursor.execute("""SELECT DISTINCT flight_id FROM Flight;""").fetchall()
            for i in flight_id:
                id_list.append(i[0])
            flight_id_cost = super().get_cursor.execute("""SELECT DISTINCT flight_id FROM Costs;""").fetchall()
            remove_list = list()

            for i in flight_id_cost:
                if i[0] not in id_list:
                    print()
                    remove_list.append(i[0])

            for i in remove_list:
                super().get_cursor.execute("""DELETE FROM Costs WHERE flight_id = ?;""", (int(i),))

            super().get_connection.commit()
            print("Cost table cleaned")

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def fetch(self, flight_id, seat_class):
        try:
            super().connect()
            if flight_id is not None:
                return super().get_cursor.execute(
                    """SELECT Costs.seat_id, Costs.seat_cost FROM Seatmap JOIN Costs ON Costs.seat_id = Seatmap.seat_id AND Costs.flight_id = Seatmap.flight_id WHERE Seatmap.flight_id = ? AND Seatmap.seat_class = ? AND Seatmap.seat_availability = ?;""",
                    (flight_id, seat_class, "A")).fetchall()


        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Costs;

            CREATE TABLE Costs (
                flight_id INTEGER NOT NULL, 
                seat_id TEXT NOT NULL,
                seat_cost NUMERIC NOT NULL,
                PRIMARY KEY (flight_id, seat_id), 
                FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
                FOREIGN KEY (seat_id) REFERENCES Seatmap(seat_id)
            );
            """

        super().execute(sql)
        super().close_db()


class Reservation(Flight):
    # The reservation table interacts heavily with the seatmap table as the seatmap holds seat specific reservations.

    def update(self, flight_id, customer_id, cost, seat_id, reservation_date):
        # This formula should actually also update the seatmap table however I do not have time to implement this
        # Since i wouldn't want this table to be updated and i rather have reservations deleted and readded this isn't too much of a problem however.
        super().connect()
        super().get_cursor.execute(
            """UPDATE Reservation SET cost = ?,  seat_id = ?, reservation_date = ?  WHERE flight_id = ? AND customer_id = ?;""",
            (cost, seat_id, reservation_date, flight_id, customer_id))

        super().get_connection.commit()
        super().close_db()

    def add(self, flight_id, customer_id, cost, seat_id, reservation_date):
        # Here when an entry gets added the seatmap gets updated accordingly.
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT OR IGNORE INTO Reservation(flight_id, customer_id, cost, seat_id,reservation_date) VALUES (?,?,?,?,?);""",
                (flight_id, customer_id, cost, seat_id, reservation_date))
            super().get_cursor.execute(
                """UPDATE Seatmap SET seat_availability = ? WHERE Seatmap.flight_id = ? AND Seatmap.seat_id = ?;""",
                ("R", flight_id, seat_id))
            super().get_connection.commit()
            super().close_db()
            print("Added Reservation to Database and database updated")
        except Exception as e:
            print("An error occurred.", e)

    def delete(self, reservation_id=None, flight_id=None):
        # And here the same happens as the add table where the seatmap is updated alongside the reservation table.
        try:
            super().connect()
            res_data = super().get_cursor.execute("""SELECT * FROM Reservation WHERE reservation_id = ?;""",
                                                  (reservation_id,)).fetchone()
            if reservation_id is not None:
                super().get_cursor.execute(
                    """UPDATE Seatmap SET seat_availability = ? WHERE Seatmap.flight_id = ? AND Seatmap.seat_id = ?;""",
                    ("A", res_data[1], res_data[4]))
                super().get_cursor.execute("""DELETE FROM Reservation WHERE reservation_id = ?;""", (reservation_id,))

            super().get_connection.commit()
            super().close_db()
            print("Removed Reservation from Database and database updated")
        except Exception as e:
            print("An error occurred.", e)

    def fetch(self, reservation_id=None, customer_id=None):
        try:
            super().connect()
            if reservation_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Reservation WHERE reservation_id = ?;""",
                                                  (reservation_id,)).fetchall()
            if customer_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Reservation WHERE customer_id = ?;""",
                                                  (customer_id,)).fetchall()
            else:
                super().get_cursor.execute("""SELECT * FROM Reservation;""").fetchall()

        except Exception as e:
            print("An error occurred.", e)

        finally:
            super().close_db()

    def reset_database(self):
        sql = """
            DROP TABLE IF EXISTS Reservation;

            CREATE TABLE Reservation (
                reservation_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                flight_id INTEGER NOT NULL, 
                customer_id INTEGER NOT NULL, 
                cost NUMERIC NOT NULL, 
                seat_id TEXT NOT NULL, 
                reservation_date TIMESTAMP NOT NULL,
                FOREIGN KEY (flight_id) REFERENCES Flight(flight_id), 
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
            );
            """

        super().execute(sql)
        super().close_db()

# Created by Willem van der Schans

import datetime
import FPCore as classes
import time
import inspect


# The user_ui is extremely large and nested but holds a lot of functionality.
# It was hard to debug everything but I think I did get most of the bugs out.

# A function to extract values from nested lists
def Extract(lst):
    return list(list(zip(*lst))[0])


# A function to automatically generate inputs based on arguments and datatypes to circumvent code duplication
def arg_func(arg_list, data_type_list):
    input_list = []
    for p in range(2, len(arg_list)):
        user_arg_str = input(
            f"Value for argument {arg_list[p]} with datatype {data_type_list[p - 1][2]} : ")
        if user_arg_str == "":
            user_arg_str = "None"
        else:
            pass

        if data_type_list[p - 1][2] == "NUMERIC":
            input_list.append(float(user_arg_str))
        elif data_type_list[p - 1][2] == "INTEGER":
            input_list.append(int(user_arg_str))
        else:
            input_list.append(user_arg_str)

    return input_list


# Start of the User_UI
def user_ui():
    user_options = {"Airline": "For Airline airline employees",
                    "Customer": "For Airline Customers"}

    customer_options = {"Register": "Register a new account.",
                        "Book": "Make a new reservation in the system",
                        "Modify Booking": "View or Modify Booking"}

    airline_options = {"Add": "Add data to the database",
                       "View": "View data within the database",
                       "Modify": "Modify or delete data within the database",
                       "Refresh": "Refresh Cost table",
                       "Clean": "Clean Cost table"}

    user_options_sel = ""
    print("""
                                 |
                       - -= == = |= == =--
                                 |
                             .-\"\"\"\"\"-.                            
                           .'_________'.                          
                          /_/_|__|__|_\_\ 
                         ;'-._       _.-';
    ,--------------------|    `-. .-'    |--------------------,
     ``""--..__    ___   ;       '       ;   ___    __..--""``
               `"-// \\.._\             /_..// \\-"`
                  \\_//    '._       _.'    \\_//
                   `"`        ``---``        `"`                  
            Welcome to the AA airlines Management Program!""")


    print("\n")
    # Here you pick if you are an employee or customer, which of course is a major security risk
    # A login system or different system for employees would be best here.
    print("First let us know what kind of user you are. \n")

    type_user_flag = False
    while not type_user_flag:
        print("---OPTION LIST---")
        for option in user_options.items():
            print(option)
        print("---END OF OPTION LIST---\n")

        user_options_sel = str(input("Select a user type: ")).title()

        if user_options_sel not in ["Airline", "Customer"]:
            print("Please provide a valid input.")
            continue

        # The customer side of the user_UI
        elif user_options_sel == "Customer":

            type_user_flag = True
            cust_system_flag = True
            while cust_system_flag:
                print("---OPTION LIST---")
                for option in customer_options.items():
                    print(option)
                print("---END OF OPTION LIST---\n")

                customer_options_sel = str(input("Select an option: ")).title()

                if customer_options_sel not in ["Register", "Book", "Modify Booking"]:
                    print("Please provide a valid input.")
                    continue

                # Here customers can registered so they can be put into the system.
                elif customer_options_sel == "Register":
                    db_class = classes.Customer()
                    table_list = db_class.table_information()
                    f_name = input("What is your first name?: ")
                    m_name = input("What is your middle name?: ")
                    l_name = input("What is your last name?: ")
                    country = input("Which country's citizenship do you hold?: ")
                    document_number = input(
                        f"Please provide your travel document number (Datatype = {table_list[4][2]}): ")
                    loyalty_number = input(
                        f"Please provide your airline loyalty number (Datatype = {table_list[5][2]}): ")

                    if loyalty_number == "":
                        loyalty_number = None

                    try:
                        db_class.add(first_name=f_name, middle_name=m_name, last_name=l_name,
                                     country=country, document_number=document_number, loyalty_number=loyalty_number)
                        print("You have successfully registered")

                    except Exception as e:
                        print(f"An error occurred please check all your inputs")

                    finally:
                        db_class.close_db()

                # After registering customer can book a flight
                elif customer_options_sel == "Book":
                    book_flag = True

                    print("Welcome to the Airlines booking service.")
                    inp_choice = input("Would you like to input your [name] or [document number]?")

                    # Customers can identify themselves with either their name or their travel document number.
                    if inp_choice.lower() == "name":
                        f_name = input("Please input your first name: ")
                        m_name = input("Please input your middle name, leave blank if you have no middle name: ")
                        l_name = input("Please input your last name: ")
                    elif inp_choice.lower() == "document number":
                        d_num = input("Please input your document number: ")

                    # Book loop starts here
                    while book_flag is True:
                        db_class = classes.Flight()
                        table_list = db_class.table_information()

                        # Here we Get the origin_id data
                        #  First the Country someone flies from
                        origin_options = db_class.fetch(query="Country")
                        for i in range(0, len(origin_options)): origin_options[i] = origin_options[i][0]

                        print("---OPTION LIST---")
                        for option in origin_options:
                            print(f"Country: {option}")
                        print("---END OF OPTION LIST---\n")

                        origin_country = input("What country are you traveling from?: ")

                        if origin_country not in origin_options:
                            print("Please provide a valid input")
                            continue
                        else:
                            # Then the city someone flies from within the previously selected country.
                            origin_options = db_class.fetch(query_country=str(origin_country))
                            for i in range(0, len(origin_options)): origin_options[i] = origin_options[i][0]

                            print("---OPTION LIST---")
                            for option in origin_options:
                                print(f"Country: {option}")
                            print("---END OF OPTION LIST---\n")

                            origin_city = input("What city are you traveling from?: ")

                            if origin_city not in origin_options:
                                print("Please provide a valid input")
                                continue

                            origin_id = db_class.fetch(query_country=origin_country, query_city=origin_city)[0]

                        # Here the designation is selected by the customer.
                        #  First the Country
                        dest_options = db_class.fetch(query="Country")
                        for i in range(0, len(dest_options)): dest_options[i] = dest_options[i][0]

                        print("---OPTION LIST---")
                        for option in dest_options:
                            print(f"Country: {option}")
                        print("---END OF OPTION LIST---\n")

                        dest_country = input("What country are you traveling to?: ")

                        if dest_country not in dest_options:
                            print("Please provide a valid input")
                            continue
                        else:
                            # Then the city
                            dest_options = db_class.fetch(query_country=str(dest_country))
                            for i in range(0, len(dest_options)): dest_options[i] = dest_options[i][0]

                            print("---OPTION LIST---")
                            for option in dest_options:
                                print(f"Country: {option}")
                            print("---END OF OPTION LIST---\n")

                            dest_city = input("What city are you traveling to?: ")

                            if dest_city not in dest_options:
                                print("Please provide a valid input")
                                continue

                            dest_id = db_class.fetch(query_country=dest_country, query_city=dest_city)[0]

                        # Get Date Range: This gives a starting  and end date for searching for flights.
                        confirm_flag = False
                        while confirm_flag is not True:
                            start_date_str = input("Start search date range, format(yyyy,m,d): ")
                            end_date_str = input("End search date range, format(yyyy,m,d): ")

                            seat_class = input("What class do you want to fly? F(irst), M(iddle), E(conomy)?")

                            start_date = datetime.datetime(int(start_date_str.split(",")[0]),
                                                           int(start_date_str.split(",")[1]),
                                                           int(start_date_str.split(",")[2]))
                            end_date = datetime.datetime(int(end_date_str.split(",")[0]),
                                                         int(end_date_str.split(",")[1]),
                                                         int(end_date_str.split(",")[2]))

                            found_flights = db_class.fetch(origin_id=origin_id, dest_id=dest_id, start_date=start_date,
                                                           end_date=end_date, seat_class=seat_class)

                            # Here a customer selects their flight.
                            print("---FLIGHT LIST---")
                            for flight in found_flights:
                                print(
                                    f"Flight ID: {flight[0]}, departing on {flight[1]}, seats available in selected class {flight[2]}")
                            print("---END OF FLIGHT LIST---\n")

                            selected_flight = input("Select flight with flight id: ")

                            for flight in found_flights:
                                if str(flight[0]) == str(selected_flight):
                                    selected_flight_data = flight

                            if selected_flight not in str(Extract(found_flights)):
                                print("Please provide valid input, restarting search.")
                                continue
                            else:
                                print(f"Flight {selected_flight} departing on {selected_flight_data[1]}")
                                confirm_flag = True

                            # A customer select their seat based on what flight they selected
                            db_class = classes.Costs()
                            found_seats = db_class.fetch(selected_flight, seat_class)

                            print("---SEAT LIST---")
                            for seat in found_seats:
                                print(
                                    f"Seat ID: {seat[0]} | Cost ${seat[1]}")
                            print("---END OF SEAT LIST---\n")

                            selected_seat = input("Select seat with seat id: ")

                            for seat in found_seats:
                                if str(seat[0]) == str(selected_seat):
                                    selected_seat_data = seat

                            print(f"Seat selected {selected_seat}, payment due: {selected_seat_data[1]}")

                            # Here a fake payment process.
                            credit_card_number = input("Input credit card number: ")
                            credit_card_cvc = input("Input credit card cvc: ")
                            credit_card_expiration = ("Input credit card expiration: ")

                            print("Data Received Payment Authorizing")
                            time.sleep(1)
                            print("...Payment Authorizing...")
                            time.sleep(1)
                            print("Payment authorization successful.")
                            time.sleep(5)

                            db_class = classes.Reservation()
                            db_class2 = classes.Customer()

                            # a commit of the reservation to the database
                            if inp_choice.lower() == "booking_number":
                                customer_data = db_class2.fetch(document_number=d_num)
                            else:
                                if m_name == "":
                                    customer_data = db_class2.fetch(first_name=f_name, last_name=l_name)
                                else:
                                    customer_data = db_class2.fetch(first_name=f_name, middle_name=m_name,
                                                                    last_name=l_name)

                            db_class.add(selected_flight, customer_id=customer_data[0], cost=selected_seat_data[1],
                                         seat_id=selected_seat, reservation_date=datetime.datetime.now())
                            book_flag = False

                # Here customers can see and cancel their booking
                elif customer_options_sel == "Modify Booking":

                    modify_flag = False
                    while not modify_flag:
                        print("Welcome to the Airlines booking service.")
                        inp_choice = input("Would you like to input your [name] or [document number]?")

                        m_name = None
                        f_name = None
                        l_name = None
                        d_num = None
                        customer_data = None

                        # A choice again of identification method
                        if inp_choice.lower() == "name":
                            f_name = input("Please input your first name: ")
                            m_name = input("Please input your middle name, leave blank if you have no middle name: ")
                            l_name = input("Please input your last name: ")
                            if m_name == "":
                                customer_data = classes.Customer().fetch(first_name=f_name, last_name=l_name)
                            else:
                                customer_data = classes.Customer().fetch(first_name=f_name, middle_name=m_name,
                                                                         last_name=l_name)
                        elif inp_choice.lower() == "document number":
                            customer_data = classes.Customer().fetch(
                                document_number=input("Please input your document number: "))

                        reservation_data = classes.Reservation().fetch(customer_id=customer_data[0])

                        # The booking are printed
                        print("---RESERVATION LIST---")
                        for reservation in reservation_data:
                            flight_data = classes.Flight().fetch(flight_id=reservation[1])
                            airport_data = classes.Airport().fetch(dest_id=int(flight_data[3]))
                            print(
                                f"Reservation_id: {reservation[0]}, departing on {flight_data[4]} to {airport_data[2]} in {airport_data[1]} | Booked seat: {reservation[4]}")
                        print("---END OF RESERVATION LIST---\n")

                        cust_inp = input("Do you want to [exit], or [modify] your booking?: ")

                        if cust_inp.lower() == "exit":
                            break

                        # Here the booking can be cancelled
                        elif cust_inp.lower() == "modify":
                            selected_reservation = input("Select reservation to modify by reservation id: ")
                            if selected_reservation not in str(Extract(reservation_data)):
                                print("Please provide valid input, restarting search.")
                                continue
                            else:
                                res_options = input(f"Do you want to cancel booking {selected_reservation}? Y or N : ")
                                if res_options.lower() == "n":
                                    continue
                                elif res_options.lower() == "y":
                                    classes.Reservation().delete(selected_reservation)
                                    modify_flag = True
                                    continue

        # The airline side of the system
        elif user_options_sel == "Airline":
            airline_system_flag = True
            while airline_system_flag:
                print("---OPTION LIST---")
                for option in airline_options.items():
                    print(option)
                print("---END OF OPTION LIST---\n")

                airline_options_sel = str(input("Select an option: ")).title()

                if airline_options_sel not in ["Add", "View", "Modify", "Refresh", "Clean"]:
                    print("Please provide a valid input.")
                    continue
                else:
                    pass

                option_flag = True
                while option_flag:
                    # Add functionality loop starts
                    if airline_options_sel == "Add":
                        add_options = {"Airplane": "Add data to Airplane table",
                                       "Airport": "Add data to Airport table",
                                       "Flight": "Add data to Flight table"}

                        print("---OPTION LIST---")
                        for option in add_options.items():
                            print(option)
                        print("---END OF OPTION LIST---\n")

                        airline_add_sel = str(input("Select an option: ")).title()

                        if airline_add_sel not in ["Airplane", "Airport", "Flight"]:
                            print("Please provide a valid input.")
                            continue
                        else:
                            pass

                        # This section is verbose and could be done with eval() however with only three classes covered it isn't too bad.
                        # Below argument lists and table information is generated to allow users to see what they are doing when adding data.
                        if airline_add_sel == "Airplane":
                            arg_list = inspect.getfullargspec(classes.Airplane().update).args
                            data_type_list = classes.Airplane().table_information()

                            input_list = arg_func(arg_list=arg_list, data_type_list=data_type_list)

                            classes.Airplane().add(*input_list)

                        elif airline_add_sel == "Airport":
                            arg_list = inspect.getfullargspec(classes.Airport().update).args
                            data_type_list = classes.Airport().table_information()

                            input_list = arg_func(arg_list=arg_list, data_type_list=data_type_list)

                            classes.Airport().add(*input_list)

                        elif airline_add_sel == "Flight":
                            arg_list = inspect.getfullargspec(classes.Flight().update).args
                            data_type_list = classes.Flight().table_information()

                            input_list = arg_func(arg_list=arg_list, data_type_list=data_type_list)

                            classes.Flight().add(*input_list)

                        option_flag = False

                    # View loop starts here.
                    elif airline_options_sel == "View":
                        view_options = {"Airplane": "View Airplane data",
                                        "Airport": "View Airport data",
                                        "Costs": "View Costs data",
                                        "Customer": "View Customer data",
                                        "Flight": "View Flight data",
                                        "Reservation": "View Reservation data",
                                        "Seatmap": "View Seatmap data"}

                        view_settings = {"All": "View all data",
                                         "Unique": "View unique instance"}

                        option_list = ["Airplane", "Airport", "Costs", "Customer", "Flight", "Reservation", "Seatmap"]
                        settings_list = ["All", "Unique"]

                        print("---OPTION LIST---")
                        for option in view_options.items():
                            print(option)
                        print("---END OF OPTION LIST---\n")

                        airline_view_sel = str(input("Select an option: ")).title()

                        if airline_view_sel not in option_list:
                            print("Please provide a valid input.")
                            continue

                        print("---OPTION LIST---")
                        for option in view_settings.items():
                            print(option)
                        print("---END OF OPTION LIST---\n")

                        airline_view_set = str(input("Select an option: ")).title()

                        if airline_view_set not in settings_list:
                            print("Please provide a valid input.")
                            continue
                        # Here a unique data entry is viewed based on extraction of primary key information this section automatically changes based on different tables.
                        if airline_view_set == "Unique":

                            for i in option_list:
                                if i == airline_view_sel:
                                    table_information = eval(f"classes.{airline_view_sel}().table_information()")
                                    arg_list = eval(f"inspect.getfullargspec(classes.{airline_view_sel}().fetch).args")
                                    input_list = []

                                    for arg in arg_list[1:]:
                                        for info in table_information:
                                            if info[1] == arg:
                                                if info[5] == 1:
                                                    if info[2] == "NUMERIC":
                                                        x = float(input(
                                                            f"Input the value for primary key {info[1]} with data type {info[2].title()}: "))
                                                    elif info[2] == "INTEGER":
                                                        x = int(float(input(
                                                            f"Input the value for primary key {info[1]} with data type {info[2].title()}: ")))
                                                    else:
                                                        x = input(
                                                            f"Input the value for primary key {info[1]} with data type {info[2].title()}: ")
                                                else:
                                                    x = None
                                            else:
                                                pass

                                        input_list.append(x)

                            output_list = eval(f"classes.{airline_view_sel}().fetch(*input_list)")

                            print("---OUTPUT START---")
                            for output in output_list:
                                print(output_list)
                            print("---OUTPUT END---\n")

                        # Here the view all starts
                        elif airline_view_set == "All":
                            output_list = eval(f"classes.{airline_view_sel}().fetch()")

                            print(f"{len(output_list)} rows of data found.")

                            output_size = int(input("How many rows would you like to view: "))
                            start_row = int(input("What row would you like to start viewing: "))

                            print("---OUTPUT START---")
                            for output in output_list[start_row:start_row + output_size]:
                                print(output)
                            print("---OUTPUT END---\n")
                            print("\n")

                            option_flag = False

                    # Here the modify loop starts
                    elif airline_options_sel == "Modify":

                        modify_options = {"Airplane": "modify Airplane data",
                                          "Airport": "modify Airport data",
                                          "Customer": "modify Customer data",
                                          "Flight": "modify Flight data"}

                        modify_settings = {"Update": "Update data",
                                           "Delete": "Delete data"}

                        settings_list = ["Update", "Delete"]
                        option_list = ["Airplane", "Airport", "Customer", "Flight", "Reservation"]

                        print("---OPTION LIST---")
                        for option in modify_options.items():
                            print(option)
                        print("---END OF OPTION LIST---\n")

                        airline_modify_sel = str(input("Select an option: ")).title()

                        if airline_modify_sel not in option_list:
                            print("Please provide a valid input.")
                            continue

                        print("---OPTION LIST---")
                        for option in modify_settings.items():
                            print(option)
                        print("---END OF OPTION LIST---\n")

                        airline_modify_set = str(input("Select an option: ")).title()

                        if airline_modify_set not in settings_list:
                            print("Please provide a valid input.")
                            continue

                        # an employee can delete based on the primary key of a table.
                        if airline_modify_set == "Delete":

                            arg_list = eval(f"inspect.getfullargspec(classes.{airline_modify_sel}().delete).args")
                            table_information = eval(f"classes.{airline_modify_sel}().table_information()")
                            input_list = []

                            # Here the right input list is generated for delete functions.
                            for arg in arg_list[1:]:
                                for info in table_information:
                                    if info[1] == arg:
                                        if info[5] == 1:
                                            if info[2] == "NUMERIC":
                                                x = float(input(
                                                    f"Input the value for primary key {info[1]} with data type {info[2].title()}: "))
                                            elif info[2] == "INTEGER":
                                                x = int(float(input(
                                                    f"Input the value for primary key {info[1]} with data type {info[2].title()}: ")))
                                            else:
                                                x = input(
                                                    f"Input the value for primary key {info[1]} with data type {info[2].title()}: ")
                                        else:
                                            x = None
                                    else:
                                        pass

                                input_list.append(x)

                            eval(f"classes.{airline_modify_sel}().delete(*input_list)")

                            option_flag = False

                        # A user can also update based on primary keys of tables which are all ID based.
                        elif airline_modify_set == "Update":
                            update_flag = True
                            while update_flag:
                                try:
                                    arg_list = eval(
                                        f"inspect.getfullargspec(classes.{airline_modify_sel}().update).args")
                                    table_information = eval(f"classes.{airline_modify_sel}().table_information()")
                                    input_list = []

                                    # Here an option list should be added, but again I had not time to do so.
                                    id_input = int(input("What Id would you like to update? : "))

                                    input_list.append(id_input)

                                    current_data = eval(f"classes.{airline_modify_sel}().fetch({id_input})")

                                    # Here the right inputs are requests and the current data type and data in the row are shown.
                                    counter = 0
                                    for arg in arg_list[2:]:
                                        counter += 1
                                        for info in table_information:
                                            if info[1] == arg:
                                                if info[2] == "NUMERIC":
                                                    print(1)
                                                    x = input(
                                                        f"Input the value for primary key {info[1]} with data type {info[2].title()}, current data = {current_data[0][counter]} : ")
                                                    if x == "":
                                                        x = int(float(current_data[0][counter]))
                                                elif info[2] == "INTEGER":
                                                    print(2)
                                                    x = input(
                                                        f"Input the value for primary key {info[1]} with data type {info[2].title()}, current data = {current_data[0][counter]} : ")
                                                    if x == "":
                                                        x = int(float(current_data[0][counter]))
                                                else:
                                                    print(3)
                                                    x = input(
                                                        f"Input the value for primary key {info[1]} with data type {info[2].title()}, current data = {current_data[0][counter]} : ")
                                            else:
                                                pass

                                        # Here we circumvent overwriting data when an entry is skipped
                                        if x == "":
                                            x = current_data[0][counter]
                                        input_list.append(x)

                                    eval(f"classes.{airline_modify_sel}().update(*input_list)")

                                    update_flag = False
                                    continue

                                except Exception as e:
                                    print(f"An error occurred {e}, make sure you are selecting a valid id.")
                                    continue

                    # This will refresh the Costs table to allow for price changes.
                    elif airline_options_sel == "Refresh":

                        setting_refresh = input("Do you want to updated [unique] or [all]?: ")

                        if setting_refresh.title() == "Unique":
                            flight_id_inp = input("What flight_id do you want to update?: ")
                            base_price = float(input("Please input the new cost base:"))
                            classes.Costs().refresh(flight_id=flight_id_inp, base_price=base_price)

                        elif setting_refresh == "All":
                            base_price = float(input("Please input the new cost base: "))

                            classes.Costs().refresh(base_price=base_price)

                    # Here an employee can clean the costs table by removing old flight_id's
                    elif airline_options_sel == "Clean":
                        classes.Costs().clean()

                    option_flag = False
                    continue



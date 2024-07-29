import read
import write
import datetime

MAX_RENTAL_DAYS = 365
LATE_FEE_THRESHOLD_DAYS = 5


def display_equipment(equipment_list):
    print("Available Equipment:")
    # Iterate through the equipment_list using enumerate to get both the index and the equipment details
    for idx, equip in enumerate(equipment_list, start=1):
        print(f"{idx}. {equip['name']} ({equip['brand']}), Price: ${equip['price']:.2f}, Stock: {equip['quantity']}")
    print()


def get_integer_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def generate_invoice(customer_name, equipment_rented, rental_days, late_days=0):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        invoice_name = f"Invoice_{customer_name}_{timestamp}.txt"  # Create invoice file name
        rental_datetime = datetime.datetime.now()

        total_amount = sum(equip['price'] * equip['quantity'] * (rental_days + late_days) for equip in equipment_rented)

        with open(invoice_name, "w") as invoice_file:
            invoice_file.write("Invoice\n")
            invoice_file.write("----------------------------\n")
            invoice_file.write(f"Customer: {customer_name}\n")
            invoice_file.write(f"Date and Time of Rental: {rental_datetime}\n")
            invoice_file.write("Equipment rented:\n")
            for equip in equipment_rented:
                invoice_file.write(f"- {equip['name']} ({equip['brand']}), Quantity: {equip['quantity']}\n")
            invoice_file.write("----------------------------\n")
            invoice_file.write(f"Total Amount: ${total_amount:.2f}\n")

        return invoice_name
    except FileNotFoundError as e:
        raise Exception(f"Error generating invoice: {e}")


def rent_equipment(equipment_list, customer_name):
    try:
        customer_equipment = []  # Initializing an empty list to store rented equipment

        while True:
            available_equipment = [equip for equip in equipment_list if equip['quantity'] > 0]

            if not available_equipment:
                print("All equipment is currently out of stock.")
                return False

            display_equipment(available_equipment)

            equip_idx = get_integer_input("Enter the equipment number to rent (0 to exit): ",
                                          min_value=0, max_value=len(available_equipment))
            if equip_idx == 0:
                break

            equip = available_equipment[equip_idx - 1]
            max_quantity = equip['quantity']
            quantity = get_integer_input(f"Enter quantity to rent (max {max_quantity}): ",
                                         min_value=1, max_value=max_quantity)
            equip['quantity'] -= quantity

            print(f"Equipment rented: {equip['name']}")

            # Record rented equipment details
            customer_equipment.append({
                "name": equip['name'],
                "brand": equip['brand'],
                "price": equip['price'],
                "quantity": quantity
            })

            continue_renting = input("Do you want to continue renting? (yes/no): ").strip().lower()
            if continue_renting != "yes":
                address = input("Address: ")
                while not address.strip():  # Validation for non-empty address
                    print("Address should not be empty.")
                    address = input("Address: ")

                phone_number = input("Phone number: ")
                while not (phone_number.strip() and phone_number.isdigit() and len(phone_number) <= 10):
                    if not phone_number.strip():
                        print("Phone number should not be empty.")
                    elif not phone_number.isdigit():
                        print("Phone number should contain only digits.")
                    else:
                        print("Phone number should not be more than 10 digits.")
                    phone_number = input("Phone number: ")

                rental_days = get_integer_input("Enter the rental duration (days, max 365): ",
                                                min_value=1, max_value=MAX_RENTAL_DAYS)

                late_days = max(rental_days - LATE_FEE_THRESHOLD_DAYS, 0)
                invoice_name = generate_invoice(customer_name, customer_equipment, rental_days, late_days)
                write.update_equipment_data(equipment_list)

                # Display invoice and rental details
                print("Invoice generated:")
                print(f"Customer: {customer_name}")
                print(f"Address: {address}")
                print(f"Phone number: {phone_number}")
                print(f"Invoice: {invoice_name}")
                print("Thank you for renting.")
                return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def return_equipment(equipment_list, customer_name):
    try:
        customer_returned = []  # Initialize an empty list to store returned equipment

        while True:
            display_equipment(equipment_list)

            equip_idx = get_integer_input("Enter the equipment number to return (0 to exit): ",
                                          min_value=0, max_value=len(equipment_list))
            if equip_idx == 0:
                break
            equip = equipment_list[equip_idx - 1]
            max_quantity = equip['quantity']
            quantity = get_integer_input(f"Enter quantity to return (max {max_quantity}): ",
                                         min_value=1, max_value=max_quantity)
            equip['quantity'] += quantity

            print(f"Equipment returned: {equip['name']}")

            # Append returned equipment details to the customer_returned list
            customer_returned.append({
                "name": equip['name'],
                "brand": equip['brand'],
                "quantity": quantity,
                "price": equip['price']
            })

            continue_returning = input("Do you want to continue returning? (yes/no): ").strip().lower()
            if continue_returning != "yes":
                address = input("Address: ")
                while not address.strip():
                    print("Address should not be empty.")
                    address = input("Address: ")

                phone_number = input("Phone number: ")
                while not (phone_number.strip() and phone_number.isdigit() and len(phone_number) <= 10):
                    if not phone_number.strip():
                        print("Phone number should not be empty.")
                    elif not phone_number.isdigit():
                        print("Phone number should contain only digits.")
                    else:
                        print("Phone number should not be more than 10 digits.")
                    phone_number = input("Phone number: ")

                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                invoice_name = generate_return_invoice(customer_name, customer_returned, current_datetime)
                write.update_equipment_data(equipment_list)

                print("Return Invoice generated:")
                print(f"Customer: {customer_name}")
                print(f"Address: {address}")
                print(f"Phone number: {phone_number}")
                print(f"Invoice: {invoice_name}")
                print("Return successful.")
                return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def generate_return_invoice(customer_name, equipment_returned, rental_datetime):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        invoice_name = f"Return_Invoice_{customer_name}_{timestamp}.txt"

        with open(invoice_name, "w") as invoice_file:
            invoice_file.write("Return Invoice\n")
            invoice_file.write("----------------------------\n")
            invoice_file.write(f"Customer: {customer_name}\n")
            invoice_file.write(f"Date and Time of Return: {datetime.datetime.now()}\n")
            invoice_file.write(f"Date and Time of Rental: {rental_datetime}\n")
            invoice_file.write("Equipment returned:\n")

            total_return_amount = 0
            for equip in equipment_returned:
                invoice_file.write(f"- {equip['name']} ({equip['brand']}), Quantity: {equip['quantity']}\n")
                total_return_amount += equip['price'] * equip['quantity']

            invoice_file.write("----------------------------\n")
            invoice_file.write(f"Total Return Amount: ${total_return_amount:.2f}\n")

        return invoice_name
    except FileNotFoundError as e:
        raise Exception(f"Error generating return invoice: {e}")


def run_program(customer_name):
    try:
        equipment_list = read.read_equipment_data()

        while True:
            print("\nDo you want to:")
            print("(R)ent")
            print("(Return) equipment")
            print("(Q)uit")

            choice = input("Enter your choice: ").strip().lower()

            if choice == "q":
                print("Exiting the program.")
                break
            elif choice == "r":
                rent_equipment(equipment_list, customer_name)  # Call rent_equipment function
            elif choice == "return":
                return_equipment(equipment_list, customer_name)  # Call return_equipment function
            else:
                print("Invalid choice. Please select a valid option.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_program("Default Customer")

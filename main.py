import operations


def main():
    while True:
        customer_name = input("Enter your name: ").strip()
        if customer_name.isalpha():
            print(f"Welcome to the Rental Shop, {customer_name}!")
            operations.run_program(customer_name)
            break
        else:
            print("Please enter a valid name containing only letters.")


if __name__ == "__main__":
    main()

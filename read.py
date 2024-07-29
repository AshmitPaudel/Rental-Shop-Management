def read_equipment_data():
    equipment_list = []  # Initialize an empty list to store equipment data
    try:
        with open("information.txt", "r") as file:
            for line in file:
                name, brand, price, quantity = line.strip().split(", ")
                equipment_list.append({
                    "name": name,
                    "brand": brand,
                    "price": float(price.strip("$")),
                    "quantity": int(quantity)
                })
        return equipment_list
    except FileNotFoundError:
        print("Equipment data file not found.")
        return []

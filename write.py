def update_equipment_data(equipment_list):
    with open("information.txt", "w") as file:  # Open equipment data file for writing
        for equip in equipment_list:
            file.write(f"{equip['name']}, {equip['brand']}, ${equip['price']:.2f}, {equip['quantity']}\n")

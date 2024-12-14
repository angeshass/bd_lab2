import dearpygui.dearpygui as dpg
import json
import os
import pandas
import openpyxl as pxl


#удаление базы данных
def delete_db():
    file_path = os.path.join("C:\+учеба\питон\db_lab2", "database.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        dpg.configure_item("status", default_value="Database deleted")
    else:
        dpg.configure_item("status", default_value="Database not found")


#импорт в  эксель таблицу
def save_to_xlsx():
    pandas.read_json("database.json").to_excel("library.xlsx")
    dpg.configure_item("status", default_value="Saved to library.xlsx")

# чтение данных из файла
def load_database(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file) # десериализация
    return []

# красивое сохранение данных в файл
def save_database(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2) # сериализация

# проверка уникальности ID для добавления
def not_unique_id(data, new_id):
    return any(item['ID'] == new_id for item in data)

# добавление новой записи
def add_record():
    ID = dpg.get_value("input_id")
    name = dpg.get_value("input_name")
    availability = dpg.get_value("input_availability")
    owner = dpg.get_value("input_owner")

    if not ID or not name or not availability or not owner: # если ввели не все данные
        dpg.configure_item("status", default_value="Enter every field")
        return

    if not_unique_id(database, ID) is True: # если ввели неуникальный ID
        dpg.configure_item("status", default_value="ID must be unique")
        return

    new_record = {
        "ID": ID,
        "Name": name,
        "Availability": availability,
        "Owner": owner
    }

    database.append(new_record)
    save_database(db_file_path, database)
    dpg.configure_item("status", default_value="Added")

# удаление записи по ID (создание новой без ненужного)
def delete_record():
    delete_value = dpg.get_value("delete_value")
    delete_field = dpg.get_value("delete_field")

    if not delete_value:
        dpg.configure_item("status", default_value="Enter value for delete")
        return

    global database
    database = [item for item in database if item[delete_field] != delete_value]
    save_database(db_file_path, database)
    dpg.configure_item("status", default_value="Deleted")

# функция для поиска записи
def search_record():
    search_value = dpg.get_value("search_value")
    search_field = dpg.get_value("search_field")

    if not search_value:
        dpg.configure_item("status", default_value="Enter value for search")
        return

    results = [item for item in database if item[search_field] == search_value]
    if results:
        dpg.configure_item("status", default_value=f"Founded: {results}")
    else:
        dpg.configure_item("status", default_value="Not founded")

# редактирование записи
def edit_record():
    edit_id = dpg.get_value("edit_id")
    new_name = dpg.get_value("edit_name")
    new_availability = dpg.get_value("edit_availability")
    new_owner = dpg.get_value("edit_owner")

    if not edit_id or not new_name or not new_availability or not new_owner:
        dpg.configure_item("status", default_value="Enter every field")
        return

    for item in database:
        if item["ID"] == edit_id:
            item["Name"] = new_name
            item["Availability"] = new_availability
            item["Owner"] = new_owner
            save_database(db_file_path, database)
            dpg.configure_item("status", default_value="Edited")
            return

    dpg.configure_item("status", default_value="ID does not exists")


# создание резервной копии
def create_backup():
    backup_path = db_file_path + ".bak"
    save_database(backup_path, database)
    dpg.configure_item("status", default_value="Backup is made")

# восстановления из резервной копии
def restore_backup():
    backup_path = db_file_path + ".bak"
    if os.path.exists(backup_path):
        database = load_database(backup_path)
        save_database(db_file_path, database)
        dpg.configure_item("status", default_value="Data base is restored")
    else:
        dpg.configure_item("status", default_value="Backup not founded")

# Инициализация базы данных
db_file_path = "database.json"
database = load_database(db_file_path)

# Настройка GUI
dpg.create_context()
dpg.create_viewport(title='DATABASE', width=700, height=750)

with dpg.window(label="library", width=700, height=750, tag="Primary Window"):
    dpg.add_text("Add a record:")
    dpg.add_input_text(label="ID", tag="input_id")
    dpg.add_input_text(label="Name", tag="input_name")
    dpg.add_combo(label="Availability", items=("Available", "Not available"),  tag="input_availability")
    dpg.add_input_text(label="Owner", tag="input_owner")
    dpg.add_button(label="Add", callback=add_record)

    dpg.add_text("Delete a record:")
    dpg.add_input_text(label="Value", tag="delete_value")
    dpg.add_combo(("ID", "Name", "Availability", "Owner"), default_value="ID", tag="delete_field")
    dpg.add_button(label="Delete", callback=delete_record)

    dpg.add_text("Record search:")
    dpg.add_input_text(label="Value", tag="search_value")
    dpg.add_combo(("ID", "Name", "Availability", "Owner"), default_value="ID", tag="search_field")
    dpg.add_button(label="Search", callback=search_record)

    dpg.add_text("Edit a record:")
    dpg.add_input_text(label="ID", tag="edit_id")
    dpg.add_input_text(label="Name", tag="edit_name")
    dpg.add_combo(label="Availability", items=("Available", "Not available"),  tag="edit_availability")
    dpg.add_input_text(label="Owner", tag="edit_owner")
    dpg.add_button(label="Edit", callback=edit_record)

    dpg.add_text("Backuping:")
    dpg.add_button(label="Make a backup", callback=create_backup)
    dpg.add_button(label="Restore from backup", callback=restore_backup)

    dpg.add_text("Save to:")
    dpg.add_button(label=".xlsx", callback=save_to_xlsx)

    dpg.add_text("DataBase:")
    dpg.add_button(label="Delete database", callback=delete_db)

    dpg.add_text("Status:", tag="status")



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
from nicegui import ui
import sqlite3

# Define choices
choix = ['hh', 'jj', 'gg']

# Initialize the database
def initialize_database():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hh TEXT,
            jj TEXT,
            gg TEXT
        )
    ''')
    connect.commit()
    connect.close()

# Create database and insert data
def create_database(column, value):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO my_data ({column}) VALUES (?)", (value,))
    connect.commit()
    connect.close()

# Display data from the database
def display_data(column, card, card_label):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT {column} FROM my_data WHERE {column} IS NOT NULL")
    rows = cursor.fetchall()
    connect.close()

    # Clear existing content in the card
    card.clear()

    # Add labels for each row dynamically
    with card:
        ui.label(card_label).classes('text-red')  # Add card title
        for row in rows:
            with ui.row():
                ui.label(row[0])
                ui.button('clear',on_click=on_press_delete)

# Function to handle the "OK" button press
def on_press_ok():
    if ref.value.strip():  # Ensure input is not empty
        create_database(selecte.value, ref.value)
        if selecte.value == 'hh':
            display_data('hh', in_card, 'IN')
        elif selecte.value == 'jj':
            display_data('jj', out_card, 'OUT')
        elif selecte.value == 'gg':
            display_data('gg', use_card, 'IN USE')

# Initialize cards with labels
def initialize_cards():
    display_data('hh', in_card, 'IN')
    display_data('jj', out_card, 'OUT')
    display_data('gg', use_card, 'IN USE')
###fonction for dealet 

def on_press_delete():
    print('deleat')
    
# UI
with ui.header():
    ui.space()
    ui.label('IIM APP').classes('text-h4')
    ui.space()

with ui.row():
    ui.label('Enter Reference')
    ref = ui.input('Enter your reference').props('rounded outlined dense')

with ui.row().classes('w-full'):
    ui.label('TYPE').classes('text-h6')
    ui.space()
    selecte = ui.select(choix, value=choix[0], with_input=True)
    ui.button('OK', on_click=on_press_ok)

with ui.row().classes('w-full'):
    in_card = ui.card().style("width:32%;height:full;align-items:center")
    with in_card:
        ui.label('IN').classes('text-red')

    out_card = ui.card().style("width:32%;height:full;align-items:center")
    with out_card:
        ui.label('OUT').classes('text-red')

    use_card = ui.card().style("width:32%;height:full;align-items:center")
    with use_card:
        ui.label('IN USE').classes('text-red')

# Initialize database and cards
initialize_database()
initialize_cards()
ui.run()

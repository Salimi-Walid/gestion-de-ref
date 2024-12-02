from nicegui import ui,app
import sqlite3
from functools import partial
from datetime import datetime

# Define choices
choix = ['in', 'out', 'use']
icon = 'data:$.png'
# Initialize the database
def initialize_database():
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "in" TEXT,
                "out" TEXT,
                "use" TEXT,
                timestamp TEXT
            )
        ''')
        connect.commit()

# Create database and insert data
def create_database(column, value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')  # Current timestamp
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute(f'INSERT INTO my_data ("{column}", timestamp) VALUES (?, ?)', (value, timestamp))
        connect.commit()

# Display data from the database
def display_data(column, card, card_label):
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute(f'SELECT id, "{column}", timestamp FROM my_data WHERE "{column}" IS NOT NULL')
        rows = cursor.fetchall()

    # Clear existing content in the card
    card.clear()

    # Add labels for each row dynamically
    with card:
        ui.label(card_label).classes('text-red')  # Add card title
        for row_id, row_value, row_time in rows:
            with ui.row().classes('w-full'):
                ui.label(f'{row_value}')
                ui.space() 
                ui.label(f'{row_time}').classes('text-green')
                ui.space() 
                ui.button('Clear', on_click=partial(on_press_delete, row_id=row_id, column=column))

# Function to handle the "OK" button press
def on_press_ok():
    if ref.value.strip():  # Ensure input is not empty
        create_database(selecte.value, ref.value)
        if selecte.value == 'in':
            display_data('in', in_card, 'IN')
        elif selecte.value == 'out':
            display_data('out', out_card, 'OUT')
        elif selecte.value == 'use':
            display_data('use', use_card, 'IN USE')
        ref.value = ""  # Clear the input field

# Initialize cards with labels
def initialize_cards():
    display_data('in', in_card, 'IN')
    display_data('out', out_card, 'OUT')
    display_data('use', use_card, 'IN USE')
# Function to confirm deletion
def on_press_delete(row_id, column):
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM my_data WHERE id = ?", (row_id,))
        connect.commit()
    # Refresh the UI for the relevant column
    if column == 'in':
        display_data('in', in_card, 'IN')
    elif column == 'out':
        display_data('out', out_card, 'OUT')
    elif column == 'use':
        display_data('use', use_card, 'IN USE')
##### and sheft emploi
def handle_click():
    ui.timer(1.0, lambda: ui.notify('end sheft emploi Tanx for your job'), once=True)
# UI
with ui.header():
    ui.space()
    ui.label('IIM APP').classes('text-h4')
    ui.space()

with ui.row().classes('w-full'):
    ui.label('Enter Reference').classes('text-h6')
    ref = ui.input('Enter your reference').props('rounded outlined dense')
    ui.space()
    with ui.card():
        label = ui.label()
        ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}')) .classes('text-h6')
    ui.button('Notify after 1h', on_click=handle_click).classes('heigh:150px')
with ui.row().classes('w-full'):
    ui.label('TYPE').classes('text-h6')
    selecte = ui.select(choix, value=choix[0], with_input=True).props('rounded outlined ')
    ui.button('SAVE', on_click=on_press_ok)

with ui.row().classes('w-full'):
    in_card = ui.card().style("width:32%;height:full;align-items:center")
    with in_card:
        ui.label('IN').classes('text-red')
        ui.separator()

    out_card = ui.card().style("width:32%;height:full;align-items:center")
    with out_card:
        ui.label('OUT').classes('text-red')
        ui.separator()
    use_card = ui.card().style("width:32%;height:full;align-items:center")
    with use_card:
        ui.label('IN USE').classes('text-red')
        ui.separator()
ui.link('My gethub','https://github.com/Salimi-Walid')
# Initialize database and cards
initialize_database()
initialize_cards()
ui.run(native=True,window_size=[1500,500],title='walid app',favicon='🚀')

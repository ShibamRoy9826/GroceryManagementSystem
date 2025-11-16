import sqlite3
import os
import sys
import datetime
from rich.console import Console
from rich.table import Table

db_was_missing = not os.path.exists("./grocery.db")

con = sqlite3.connect("grocery.db")
cur = con.cursor()
c=Console()

# Functions
def create_table():
    """
    Creates the items table.
    """
    cur.execute("""
        create table if not exists
            items(
                item_id integer primary key autoincrement,
                name text,
                price float,
                stocks integer
            )
    """)


def print_table(data:list,cols=[]):
    new_data=[]
    for row in data:
        new_data.append(list(map(str,row)))

    table=Table(title="Items",style="cyan")

    if(len(cols)==0):
        for col in cur.description:
            table.add_column(col[0])
    else:
        for col in cols:
            table.add_column(col)

    for point in new_data:
        table.add_row(*point)
    c.print(table)


def add_item(name:str,price:str,stocks:str): 
    cur.execute("""
        insert into items(name,price,stocks)
        values
        (?,?,?)
    """,(name,price,stocks))

    c.print(f"[green] New item successfully added [white]({name})[/white] [/green]")
    con.commit()

def remove_item(item_id:str):
    cur.execute("""
    delete from items
    where item_id=?
    """,(item_id,))
    con.commit()

def search_by_name(name:str):
    output = cur.execute("select * from items where name like ?", (f"%{name}%",))
    if not output:
        c.print("[red]No item with the provided name found![/red]")
    print_table(output)

def search_by_price(minima:str,maxima:str):
    output=cur.execute("""
    select * from items
    where price >= ? and price <= ?
    """,(minima,maxima))
    if not output:
        c.print("[red]No item with the provided value found![/red]")
    print_table(output)

def print_all():
    output = cur.execute("select * from items")
    if not output:
        c.print("[red]No items present!![/red]")
    print_table(output)

def update_stock(ID:str,new_stock:str):
    cur.execute("""
    update items
    set stocks=?
    where item_id=?
    """,(new_stock,ID))

    con.commit()

def update_price(ID:str,new_price:str):
    cur.execute("""
    update items
    set price=?
    where item_id=?
    """,(new_price,ID))
    con.commit()

def increment_stock(ID:str):
    cur.execute("""
    update items
    set stocks=stocks+1
    where item_id=?
    """,(ID))
    con.commit()

def decrement_stock(ID:str):
    cur.execute("""
    update items
    set stocks=stocks-1
    where item_id=?
    """,(ID))
    con.commit()

def int_input(text:str):
    data=input(text)
    if not data.isdigit():
        c.print("[red]Given data is invalid! Please enter an integral value[/red]")
        return None
    else:
        return data

def ui_add_item():
    c.print("[yellow]Please enter the item details[/yellow]")
    name=input("Item name:")
    price=input("Item price (in INR):")
    stocks=input("Initial stocks (in INR):")
    add_item(name,price,stocks)


def ui_remove_item():
    ID = input("Item ID to delete: ")
    cur.execute("select name from items where item_id=?", (ID,))
    row = cur.fetchone()
    if not row:
        c.print("[red]No such item.[/red]")
        return
    confirm = input(f"Delete '{row[0]}' (id {ID})? [y/n]: ").strip().lower()
    if confirm == 'y':
        remove_item(ID)
        c.print("[green]Deleted.[/green]")
    else:
        c.print("[yellow]Aborted.[/yellow]")

def ui_increment():
    ID = input("Item ID to increment stocks: ")
    exists= cur.execute("select name from items where item_id=?",(ID,)).fetchone()
    if not exists:
        c.print("[red]No such item[/red]")
        return
    else:
        increment_stock(ID)
        c.print(f"[green]Increment stock of ({exists[0]})[/green]")


def ui_decrement():
    ID = input("Item ID to decrement stocks: ")
    exists= cur.execute("select name from items where item_id=?",(ID,)).fetchone()
    if not exists:
        c.print("[red]No such item[/red]")
        return
    else:
        decrement_stock(ID)
        c.print(f"[green]Decrement stock of ({exists[0]})[/green]")

def ui_update_stock():
    ID = input("Item ID to update stocks: ")
    exists= cur.execute("select stocks,name from items where item_id=?",(ID,)).fetchone()
    if not exists:
        c.print("[red]No such item[/red]")
        return
    else:
        c.print(f"[yellow]Current stock is {exists[0]}[/yellow]")
        new_stock=int_input("New stocks:")
        if new_stock:
            update_stock(ID,new_stock)
            c.print(f"[green]Updated stock of ({exists[1]})[/green]")

def ui_update_price():
    ID = input("Item ID to update price: ")
    exists= cur.execute("select price,name from items where item_id=?",(ID,)).fetchone()
    if not exists:
        c.print("[red]No such item[/red]")
        return
    else:
        c.print(f"[yellow]Current price is {exists[0]}[/yellow]")
        new_price=int_input("New price(in INR):")
        if new_price:
            update_price(ID,new_price)
            c.print(f"[green]Updated price of ({exists[1]})[/green]")

def ui_search_by_price():
    c.print("[yellow]Search By Price[/yellow]")
    minima=int_input("Minimum price:")
    maxima=int_input("Maximum price:")
    if minima and maxima:
        search_by_price(minima,maxima)

def ui_search_by_price():
    c.print("[yellow]Search By Price[/yellow]")
    minima=input("Minimum value:")
    maxima=input("Maximum value:")
    search_by_price(minima,maxima)

def ui_search_by_name():
    c.print("[yellow]Search By Name[/yellow]")
    name = input("Search item name: ").strip()
    search_by_name(name)

create_table()
if db_was_missing:
    add_item("Biscuits","10","30")
    add_item("Cakes","15","45")
    add_item("Chocolates","5","10")
    add_item("Candies","1","30")

def title(s): 
    c.print(f"[bold underline cyan] {s} [/bold underline cyan]")

def pause(msg="[gray]\nPress Enter to continue...[/gray]"):
    c.input(msg)

def main_menu():
    while True:
        c.clear()
        title("Grocery Management System")
        print("""
        1) Display all items
        2) Add a new item
        3) Remove an existing item
        4) Increment stock
        5) Decrement stock
        6) Set stock of an item
        7) Update price of an item
        8) Filter items by price
        9) Filter items by name
        0) Quit
        """)

        choice = input("Choose an option: ").strip()
        c.clear()
        match choice:
            case '1':
                print_all()
            case '2':
                ui_add_item()
            case '3':
                ui_remove_item()
            case '4':
                ui_increment()
            case '5':
                ui_decrement()
            case '6':
                ui_update_stock()
            case '7':
                ui_update_price()
            case '8':
                ui_search_by_price()
            case '9':
                ui_search_by_name()
            case '0':
                c.print("[yellow]Bye![/yellow]")
                break
            case _:
                c.print("[red]Invalid choice.[/red]")
        if choice=='0':
            break
        else:
            pause()

create_table()
main_menu()


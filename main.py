import sqlite3
import os
import sys
import datetime
from rich.console import Console
from rich.table import Table

db_was_missing = not os.path.exists("./data.db")

con = sqlite3.connect("data.db")
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
    delete items
    where item_id=?
    """,(item_id,))
    con.commit()

def search_by_name(name:str):
    q = input("Search item name: ").strip()
    output = cur.execute("select * from items where name like ?", (f"%{q}%",))
    if not output:
        c.print("[red]No item with the provided name found![/red]")
    print_table(output)

def search_by_val(minima:str,maxima:str):
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

create_table()
if db_was_missing:
    add_item("Biscuits","10","30")
    add_item("Cakes","15","45")
    add_item("Chocolates","5","10")
    add_item("Candies","1","30")


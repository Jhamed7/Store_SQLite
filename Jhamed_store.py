import colorama
from colorama import Fore
from sqlite3 import connect
from os import name, system
from PySide6 import QtGui


# ----------init---------------

colorama.init()
cart = []

# --------------- Load Database

con = connect('database.db')
my_cursor = con.cursor()


# -----------------------------


def db_status():
    print(Fore.LIGHTBLUE_EX, "Our store contains below Items: ")
    print('-----------------------------------------')
    my_cursor.execute('SELECT * FROM products')
    show(my_cursor)
    menu()


# ------------- database Insert new product


def db_insert():
    p_name = input("Product Name: ")
    if check_availability(p_name):
        print(Fore.CYAN, 'already available in store, please use edit option')
        menu()
    p_count = input("Product Count: ")
    p_price = input("Product Price: ")

    my_cursor.execute(f"INSERT INTO products(name, count, price) VALUES('{p_name}', {p_count}, {p_price})")
    con.commit()
    menu()


# -----------------------------------------

def check_availability(p_name):
    # ------ check for repeated name
    my_cursor.execute(f"SELECT * FROM products WHERE name='{p_name}'")
    if my_cursor.fetchall():
        return True
    else:
        return False


# ------------------------------
def db_remove():
    p_name = input("Please insert Product Name: ")
    if not check_availability(p_name):
        print(Fore.RED, 'there is no such product in store')
        menu()
    else:
        my_cursor.execute(f"DELETE FROM products WHERE name='{p_name}'")
        print(Fore.GREEN, 'successfully deleted')
        con.commit()
        menu()


# ------------------------------

def db_edit():
    quit_ = False
    p_name = input("Please insert Product Name: ")
    if not check_availability(p_name):
        print(Fore.RED, 'there is no such product in store')
        menu()
    else:
        while True:
            if quit_:
                break
            parameter = input('what do you want to edit: 1-name , 2-count , 3-price : ')
            if parameter == '1':
                new_name = input('new name: ')
                my_cursor.execute(f"UPDATE products SET name = '{new_name}' WHERE name='{p_name}'")
                print('successfully updated')
                con.commit()
                menu()
            elif parameter == '2':
                new_count = input('new count: ')
                my_cursor.execute(f"UPDATE products SET count = '{new_count}' WHERE name='{p_name}'")
                print('successfully updated')
                con.commit()
                menu()
            elif parameter == '3':
                new_price = input('new price: ')
                my_cursor.execute(f"UPDATE products SET price = '{new_price}' WHERE name='{p_name}'")
                print('successfully updated')
                con.commit()
                menu()
            elif input('please select a correct number. (0 to quit)') == '0':
                quit_ = True
    menu()


def db_search():
    while True:

        print('please choose search parameter(number): 1-id, 2-name')
        parameter = int(input('Parameter: '))
        if parameter == 1:
            try:
                id_ = int(input('enter product id: '))
                my_cursor.execute(f"SELECT * FROM products WHERE id={id_}")
                show(my_cursor)
                break
            except:
                print('there is no product whit this id')
                break
        elif parameter == 2:
            try:
                name_ = input('enter product name: ')
                my_cursor.execute(f"SELECT * FROM products WHERE name='{name_}'")
                show(my_cursor)
                break
            except:
                print('there is no product whit this name')
                break
        else:
            print('please choose 1 or 2')
    menu()


def show(cursor):
    result = cursor.fetchall()
    if not result:
        print(Fore.RED, 'there is no data available')
    else:
        print('\tid\t\tname\t\tcount\tprice')
        print('----------------------------------------')
        for item in result:
            print(f"\t{item[0]}\t\t{item[1]}\t\t{item[2]}\t\t{item[3]}")


# -----------------------------------------------
def check_enough(name_, count_):
    my_cursor.execute(f"SELECT count FROM products WHERE name='{name_}'")
    res = my_cursor.fetchall()
    if count_ <= int(res[0][0]):
        return True
    else:
        return False


# -----------------------------------------------
def price_calculation(name_, count_):
    my_cursor.execute(f"SELECT price FROM products WHERE name='{name_}'")
    price_unit = my_cursor.fetchall()
    return int(price_unit[0][0]) * int(count_)


# -----------------------------------------------
def update_database(card_info):
    for item in card_info:
        my_cursor.execute(f"UPDATE products SET count = count - '{item[1]}' WHERE name='{item[0]}'")
        con.commit()


# -----------------------------------------------


def buy_product():
    print(Fore.MAGENTA, '------Below items are available to Buy------')
    print('--------Please choose your products---------')
    my_cursor.execute(f"SELECT name FROM products")
    product_list = my_cursor.fetchall()
    print([item[0] for item in product_list])
    global cart
    while True:
        name_p = input('product name : ')
        if not check_availability(name_p):
            print('please insert correct name!')
        else:
            count_p = input(f'how many {name_p} do you want? : ')

            if not check_enough(name_p, int(count_p)):
                print(f'there is not enough {name_p} in store!')

            else:
                if name_p in [item[0] for item in cart]:  # check if there is tha same item in cart or not?
                    current_value = int([item[1] for item in cart if item[0] == name_p][0])
                    #cart = [list(item) for item in cart]
                    for counter, item in enumerate(cart):
                        if item[0] == name_p:
                            cart[counter][1] = str(int(count_p) + current_value)

                else:  # add new item to cart
                    price = price_calculation(name_p, count_p)
                    cart.append([name_p, count_p, price])

                if input('Do you want to buy more? (y /n):') == 'n':
                    break

    update_database(cart)
    print(Fore.GREEN, 'Tanks for your shopping!')
    menu()


def card_status(cart_):
    if not cart_:
        print(Fore.BLUE, 'Your cart is empty now, please buy some products')
    else:
        print(Fore.GREEN, '---------------------------------------')
        print('Your cart information is as below: ')
        print('---------------------------------------')
        # for item in cart_:
        #     print(item)
        total_price = 0
        print('\tname\t\tcount\t\tprice')
        print('----------------------------------------')
        for item in cart_:
            print(f"\t{item[0]}\t\t{item[1]}\t\t{item[2]}")
            total_price += item[2]
        print('----------------------------------------')
        print(f"Total price : {total_price}")

    menu()


def saveAndExit():
    con.close()
    print(Fore.LIGHTGREEN_EX + 'Thanx! Goodbye')
    exit()


def menu():
    print(Fore.LIGHTYELLOW_EX +
          '\n 1- add new product \n 2- search \n 3- edit \n 4- remove \n 5- buy \n 6- show all \n 7- show cart\
           \n 8- save changes and exit')

    user_select = input('please enter the option you want: ')

    if user_select == '1':
        # addNewProduct()
        db_insert()
    elif user_select == '2':
        # search()
        db_search()
    elif user_select == '3':
        # edit()
        db_edit()
    elif user_select == '4':
        # remove()
        db_remove()
    elif user_select == '5':
        # buy()
        buy_product()
    elif user_select == '6':
        # showAll()
        db_status()
    elif user_select == '7':
        # showCart()
        card_status(cart)
    else:
        saveAndExit()
        con.close()


if __name__ == '__main__':
    menu()

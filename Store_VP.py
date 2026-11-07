# -*- coding: utf-8 -*-
"""
STORE INVENTORY MANAGER
A command-line application to manage a small store's inventory and sales.
Data is persisted in a JSON file; no external dependencies are required.
"""

import json
import os

class Inventory:
    """
    Data layer: stores products and sales, and persists them to a JSON file.
    Attributes:
    file (str): path of the JSON file used for persistence
    data (dict): inventory data (products and sales)
    """

    def __init__(self, file='inventory.json'):
        """
        Initializes the inventory object and loads data from the specified file
        Args:
        file (str): path to the file from which to load the data (default: inventory.json)
        """
        self.file = file
        self.data = self.load_data()


    def load_data(self):
        """
        Loads inventory data from the JSON file
        Returns:
            dict: The data stored in the file, or an empty inventory
                if the file does not exist yet.
        """
        if os.path.exists(self.file):
            with open(self.file) as f:
                return json.load(f)
        return {'PRODUCTS':[], 'SALES':[]}


    def save_data(self):
        """
        Saves the inventory data to the JSON file
        """
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=4)


    def add_product(self, name, quantity, purchase_price, selling_price):
        """
        Adds a product to the inventory.
        Args:
            name (str): product name
            quantity (int): quantity in stock
            purchase_price (float): purchase price per unit
            selling_price (float): selling price per unit
        """
        new_product={
            'NAME': name.strip(),
            'QUANTITY': quantity,
            'PURCHASE PRICE': purchase_price,
            'SELLING PRICE': selling_price
        }
        self.data['PRODUCTS'].append(new_product)
        self.save_data()


    def list_products(self):
        """
        Returns:
            list[dict]: all products in the inventory
        """
        return self.data['PRODUCTS']


    def remove_product(self, name, quantity):
        """
        Removes a quantity of a product from the inventory.
        The product record is deleted when its remaining quantity reaches zero.

        Args:
            name (str): name of the product to remove
            quantity (int): quantity to remove
        """
        for product in self.data['PRODUCTS']:
            if product['NAME']==name:
                product['QUANTITY']-=quantity
                if product['QUANTITY']<=0:
                    self.data['PRODUCTS'].remove(product)
            self.save_data()


    def selling(self, name, quantity):
        """
        Records new sales or calls the function to update them
        Args:
            name (str): name of the product sold
            quantity (int): quantity sold
        """
        for product in self.data['PRODUCTS']:
            if product['NAME']==name:
                sale_check = any(sale['NAME']==name for sale in self.data['SALES'])
                if sale_check:
                    self.update_selling(name,quantity)
                else:
                    new_sale = {
                    'NAME': name,
                    'QUANTITY': quantity,
                    'PURCHASE PRICE': product['PURCHASE PRICE'],
                    'SELLING PRICE': product['SELLING PRICE']
                    }
                    self.data['SALES'].append(new_sale)
                    self.save_data()


    def update_selling(self, name, quantity):
        """
        Updates the quantities of products that are sold multiple times
        Args:
            name (str): name of the product sold
            quantity (int): additional quantity sold
        """
        for sale in self.data['SALES']:
            if sale['NAME']==name:
                sale['QUANTITY']+=quantity
                self.save_data()


    def get_price(self, name):
        """
        Returns the selling price of a product
        Args:
            name (str): name of the product for which you want to know the price
        Returns:
            float: selling price of the product
        """
        for product in self.data['PRODUCTS']:
            if product['NAME']==name:
                price = product['SELLING PRICE']
                return price


    def profits(self):
        """
        Calculates total revenue and profit
        Returns:
            str: total revenue and profit
        """
        gross_profit, diff = 0,0
        for sale in self.data['SALES']:
            gross_profit+= sale['QUANTITY']*sale['SELLING PRICE']
            diff+= sale['QUANTITY']*sale['PURCHASE PRICE']
        net_profit = gross_profit-diff
        return f'Profit: gross=€{round(gross_profit,2)} net=€{round(net_profit,2)}'



class Store:
    """
    User Interface layer: handles commands and input validation
    """

    def __init__(self):
        """
        Initializes the store object with the inventory
        """
        self.inventory = Inventory()


    def help(self):
        """
        Shows the available command options
        """
        print('Available commands:\n'+'add: add a product to the inventory\n'
             +'list: list the products in the inventory\n'+'sales: records new sales\n'
             +'profits: shows total profits\n'+'help: shows available commands\n'
             +'close: exit')


    def start(self):
        """
        Starts the main loop of the user interface
        """
        while True:
            query = input('Insert a command ("help" to show available commands): ')
            query = query.strip().lower()
            if query=='help':
                self.help()
            elif query=='add':
                self.add_product()
            elif query=='list':
                self.list_products()
            elif query=='sales':
                self.selling()
            elif query=='profits':
                self.profits()
            elif query=='close':
                print('Bye!')
                break
            else:
                print('Command not valid')
                self.help()


    def add_product(self):
        """
        Adds a new product to the inventory or updates the stock.
        Prices are only requested for new products.
        Handles cases of invalid input.
        """
        products = self.inventory.data['PRODUCTS']
        name = input('Product name: ')
        quantity = None
        while type(quantity)!=int:
            try:
                quantity = int(input('Quantity: '))
            except:
                print('Error: not a valid quantity')

        for product in products:
            if product['NAME']==name:
                product['QUANTITY']+= quantity
                self.inventory.save_data()
                print('UPDATED: ',product['QUANTITY'],' X ',name)
                break
        else:
            purchase_price, selling_price = None, None
            while type(purchase_price)!=float:
                try:
                    purchase_price = float(input('Purchase price: '))
                except:
                    print('Error: not a valid price')
            while type(selling_price)!=float:
                try:
                    selling_price = float(input('Selling price: '))
                except:
                    print('Error: not a valid price')

            self.inventory.add_product(name,quantity,purchase_price,selling_price)
            print(f'ADDED: {quantity} X {name}')


    def list_products(self):
        """
        Lists all products in the inventory in a table-like format
        """
        products = self.inventory.list_products()
        name_max_length = max(len(product['NAME']) for product in products + [{'NAME':'PRODUCT'}]) +1
        print('{:<{name_width}} {:<{quantity_width}} {:<{price_width}}'.format(
            'PRODUCT', 'QUANTITY', 'PRICE',
            name_width=name_max_length,
            quantity_width=10,
            price_width=10
        ))
        for product in products:
            print('{:<{name_width}} {:<{quantity_width}} €{:<{price_width}.2f}'.format(
                product['NAME'],
                product['QUANTITY'],
                product['SELLING PRICE'],
                name_width=name_max_length,
                quantity_width=10,
                price_width=10
                ))


    def selling(self):
        """
        Records the sale of one or more products from the inventory.
        Available products are displayed to facilitate the entry of completed sales.
        Handles cases of invalid input
        """
        print(f'Products in stock: ')
        self.list_products()
        names_cart = []
        quantities_cart = []
        prices_cart = []
        tot = 0
        add = True
        products = self.inventory.data['PRODUCTS']

        while add:
            try:
                name = input('Product name: ')
                assert any(product['NAME']==name for product in products), 'Product not found'
                try:
                    quantity = int(input('Quantity: '))
                except ValueError:
                    print('Error: not a valid quantity')
                    break
                product = next(product for product in products if product['NAME']==name)
                if product['QUANTITY']<quantity:
                    raise Exception('Insufficient quantity. Availability: '+str(product['QUANTITY']))

                prod_price = self.inventory.get_price(name)
                prices_cart.append(prod_price)
                self.inventory.selling(name,quantity)
                names_cart.append(name)
                quantities_cart.append(quantity)
                print(f'NEW SALE RECORDED')
                for name,quantity,prod_price in zip(names_cart,quantities_cart,prices_cart):
                    print(quantity,' X ',name,': €',prod_price)
                tot+=(quantity*prod_price)
                self.inventory.remove_product(name,quantity)

            except AssertionError as e:
                print(e)
            except Exception as e:
                print(e)

            if input('Do you want to add another product? [y/n] ')=='y':
                add = True
            else:
                add = False
        print('Total: €',round(tot,2))


    def profits(self):
        """
        Prints total profit
        """
        print(self.inventory.profits())



if __name__ == '__main__':
    store = Store()
    store.start()

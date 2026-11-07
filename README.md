# Store Inventory Manager
A command-line application for managing a small store's inventory and sales,
built in pure Python with no external dependencies. Data is persisted in a JSON file.

**Context:** Project developed as part of the Data Science Master Course by ProAI SRL. The brief was provided by the course; the code and documentation are my own work.

## Features

- **Inventory management**: add products, or increase stock of existing ones
- **Sales registration**: multi-item sales with stock validation
- **Profit reporting**: total revenue and profit across all recorded sales
- **Input validation**: invalid quantities, prices and unknown products are handled gracefully
- **Persistent storage**: all changes are saved automatically to `inventory.json`

## Quick start

    git clone https://github.com/<VittyP>/<Store_inventory_manager_VP>.git
    cd <Store_inventory_manager_VP>
    python Store_VP.py

## Commands

| Command   | Description                          |
|-----------|--------------------------------------|
| `add`     | Add a product or update its quantity |
| `list`    | Show products, quantities and prices |
| `sales`   | Record a sale (one or more items)    |
| `profits` | Show total revenue and profit        |
| `help`    | Show available commands              |
| `close`   | Exit the program                     |

## Example session

    Insert a command ("help" to show available commands): add
    Product name: Coffee beans
    Quantity: 20
    Purchase price: 4.50
    Selling price: 7.90
    ADDED: 20 X Coffee beans

## Design

The code is split into two classes with distinct responsibilities:

- `Inventory`: data layer (load/save JSON, products, sales, profit calculation)
- `Store`: user interface layer (command loop, input validation, formatted output)

Data model (`inventory.json`):

    {
      "PRODUCTS": [{"NAME": "...", "QUANTITY": 0, "PURCHASE PRICE": 0.0, "SELLING PRICE": 0.0}],
      "SALES":    [{"NAME": "...", "QUANTITY": 0, "PURCHASE PRICE": 0.0, "SELLING PRICE": 0.0}]
    }

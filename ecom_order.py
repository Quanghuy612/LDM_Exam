from pymongo import MongoClient

def connect_to_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["eShop"]
    collection = db["OrderCollection"]
    print("✅ Connected to MongoDB | Database: eShop | Collection: OrderCollection\n")
    return collection

def insert_orders(collection):
    orders = [
        {
            "orderid": 1,
            "products": [
                {"product_id": "quanau", "product_name": "quan au", "size": "XL", "price": 10, "quantity": 1},
                {"product_id": "somi", "product_name": "ao so mi", "size": "XL", "price": 10.5, "quantity": 2}
            ],
            "total_amount": 31,
            "delivery_address": "Hanoi"
        },
        {
            "orderid": 2,
            "products": [
                {"product_id": "somi", "product_name": "ao so mi", "size": "M", "price": 10.5, "quantity": 3},
                {"product_id": "giay", "product_name": "giay the thao", "size": "42", "price": 50, "quantity": 1}
            ],
            "total_amount": 81.5,
            "delivery_address": "Ho Chi Minh"
        },
        {
            "orderid": 3,
            "products": [
                {"product_id": "quanau", "product_name": "quan au", "size": "L", "price": 10, "quantity": 2},
                {"product_id": "somi", "product_name": "ao so mi", "size": "L", "price": 10.5, "quantity": 1}
            ],
            "total_amount": 30.5,
            "delivery_address": "Da Nang"
        }
    ]
    collection.delete_many({})
    result = collection.insert_many(orders)
    print(f"✅ Inserted {len(result.inserted_ids)} orders into OrderCollection\n")

def edit_delivery_address(collection):
    orderid = int(input("   Enter Order ID to edit: "))
    new_address = input("   Enter new delivery address: ")
    result = collection.update_one(
        {"orderid": orderid},
        {"$set": {"delivery_address": new_address}}
    )
    if result.matched_count:
        print(f"✅ Updated order {orderid}: delivery_address → '{new_address}'\n")
    else:
        print(f"⚠️  Order {orderid} not found.\n")

def remove_order(collection):
    orderid = int(input("   Enter Order ID to remove: "))
    result = collection.delete_one({"orderid": orderid})
    if result.deleted_count:
        print(f"✅ Removed order with orderid = {orderid}\n")
    else:
        print(f"⚠️  Order {orderid} not found.\n")

def read_all_orders(collection):
    orders = list(collection.find({}, {"_id": 0}))
    print("=" * 58)
    print(f"{'No':<5} {'Product Name':<20} {'Price':<10} {'Quantity':<10} {'Total'}")
    print("-" * 58)
    row_no = 1
    for order in orders:
        for product in order.get("products", []):
            name     = product["product_name"]
            price    = product["price"]
            quantity = product["quantity"]
            total    = price * quantity
            print(f"{row_no:<5} {name:<20} {price:<10} {quantity:<10} {total}")
            row_no += 1
    print("=" * 58)
    print()

def calculate_total_amount(collection):
    pipeline = [
        {"$group": {"_id": None, "grand_total": {"$sum": "$total_amount"}}}
    ]
    result = list(collection.aggregate(pipeline))
    grand_total = result[0]["grand_total"] if result else 0
    print(f"✅ Total Amount of all orders: {grand_total}\n")

def count_somi_products(collection):
    pipeline = [
        {"$unwind": "$products"},
        {"$match": {"products.product_id": "somi"}},
        {"$count": "total_somi"}
    ]
    result = list(collection.aggregate(pipeline))
    count = result[0]["total_somi"] if result else 0
    print(f"✅ Total product entries with product_id = 'somi': {count}\n")

def show_menu():
    print("=" * 40)
    print("  eShop Order Manager — LDM SET01")
    print("=" * 40)
    print("  1. Insert sample orders")
    print("  2. Edit delivery address")
    print("  3. Remove an order")
    print("  4. Read all orders")
    print("  5. Calculate total amount")
    print("  6. Count product_id = 'somi'")
    print("  0. Exit")
    print("=" * 40)

if __name__ == "__main__":
    col = connect_to_mongodb()

    while True:
        show_menu()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            print("\n--- Task 2: Insert Orders ---")
            insert_orders(col)
        elif choice == "2":
            print("\n--- Task 3: Edit Delivery Address ---")
            edit_delivery_address(col)
        elif choice == "3":
            print("\n--- Task 4: Remove Order ---")
            remove_order(col)
        elif choice == "4":
            print("\n--- Task 5: Read All Orders ---")
            read_all_orders(col)
        elif choice == "5":
            print("\n--- Task 6: Calculate Total Amount ---")
            calculate_total_amount(col)
        elif choice == "6":
            print("\n--- Task 7: Count product_id = 'somi' ---")
            count_somi_products(col)
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️  Invalid option. Try again.\n")
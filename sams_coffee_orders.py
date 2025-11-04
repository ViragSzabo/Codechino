import csv, json
from collections import Counter, defaultdict
from datetime import datetime

# 🧁 Menu with categories
menu = {
"Coffee": {
    "Cappuccino": 3.95,
    "Long black": 3.95,
    "Espresso Tonic": 5.00,
    "Caramel Latte": 6.00,
    "Flatwhite": 4.50,
    "Americano": 3.50,
    "Cortado": 4.20,
    "Doppio": 3.50,
    "Caffe latte": 3.95,
    "Caffe latte strong": 4.50,
    "Latte Machiatto": 4.50,
    "V60 Slow coffee": 6.00,
    },
"Tea & Hot Chocolate": {
    "Hot chocolate": 3.95,
    "Caffe mocha": 4.95,
    "Earl grey": 3.95,
    "Jasmine tea": 3.95,
    "Green tea lemongrass": 3.95,
    "White tea": 3.95,
    },
"Iced Drinks" : {
    "Iced latte": 4.50,
    "Iced caramel coffee": 5.00,
    "Iced vanilla coffee": 5.00,
    "Iced black coffee": 5.00,
    "Iced strawberry matcha": 6.00,
    "Iced matcha blueberry": 7.00,
    "Iced mango matcha": 6.00,
    "Iced matcha yuzu": 7.00,
    "Iced matcha passion fruit": 7.00,
    "Iced Chai latte": 4.80,
    "Iced Matcha latte": 5.00,
    },
"Chai & Special Lattes" : {
    "Baby chino": 1.50,
    "Ceremonial matcha": 30.00,
    "Cinnamon Chai latte": 4.80,
    "Dirty Chai": 4.95,
    "Golden Turmeric latte": 4.50,
    "Matcha latte": 4.50,
    "Spicy Oolong Chai latte": 4.50,
    "Vanilla Honey Chai latte": 4.50,
    "Pumpkin Spice Latte": 5.00,
    },
"Cold Drinks" : {
    "Fuze tea Peach": 3.95,
    "Naturfrisk ginger ale": 4.50,
    "Appelsap": 3.80,
    "Fritz Fanta": 4.50,
    "Fritz Kola": 4.50,
    "Fritz Melone": 4.50,
    "Fritz Rabarber": 4.50,
    "Jus de orange": 3.95,
    "Water": 3.50,
    "Water klein": 0.50,
    },
"Beans" : {
    "Italian business 250 gram": 9.95,
    "Italian business 1 kilo": 30.00,
    "Italian supreme 250 gram": 30.00,
    "Colombia 250gr": 9.95,
    "Colombia 1kg": 29.95,
    "Costa Rica 250gr": 9.95,
    "Costa Rica 1kg": 29.95,
    "Ethiopie 250gr": 9.95,
    "Ethiopie 1kg": 29.95,
    "Guatemala 250gr": 9.95,
    "Guatemala 1kg": 29.95,
    "India 250gr": 9.95,
    "India 1kg": 29.95,
    "Kenya 250gr": 12.00,
    "Rwanda 250gr": 12.00,
    "Rwanda 1kg": 29.95,
    "Specialty Coffee 250 gram": 15.00,
    },
"Workshops" : {
    "Barista masterclass workshop 1 persoon": 85.00,
    "Barista basis workshop 1 persoon": 75.00,
    },
"Giftcards" : {
    "Giftcard": 10.00,
    "Giftcard": 20.00,
    "Giftcard": 30.00,
    "Giftcard": 50.00,
    },
"Cakes" : {
    "Lime cheesecake": 4.50,
    "Pistachio cheesecake": 6.00,
    "Hazelnoot caramel cake": 5.00,
    "Stroopwafel cake": 5.00,
    "Banana cake": 4.80,
    "Carrot cake": 4.80,
    "Appeltaart": 4.80,
    "Red velvet": 4.80,
    "Cheesecake red fruit": 4.80,
    "Pistachio cookie": 5.00,
    "Chocolate brownie cake": 4.80,
    "Matcha roll": 6.00,
    },
},

# Flatten menu for price lookup
prices = {item: price for category in menu.values() for item, price in category.items()}

# 🧾 Order data: (order_items, date, table_number)
order_data = [
    (["Cinnamon Chai latte", "Water klein"], "2024.10.25.", 15),
    (["Pumpkin Spice Latte", "Caramel Latte"], "2024.11.10.", 14),
    (["Caffe mocha", "Water klein", "Cappuccino"], "2024.11.28.", 14),
    (["Golden Turmeric latte", "Appeltaart", "Cappuccino"], "2024.11.28.", 6),
    (["White tea", "Chocolate brownie cake", "Cinnamon Chai latte"], "2024.12.03.", 6),
    (["Cappuccino"], "2024.12.11.", 3),
    (["Cappuccino", "Pistachio cheesecake", "White tea"], "2025.02.19.", 4),
    (["White tea", "Matcha latte"], "2025.02.26.", 7),
    (["Cappuccino", "Carrot cake", "Vanilla Honey Chai latte"], "2025.03.19.", 8),
    (["White tea", "Matcha roll"], "2025.03.23.", 9),
    (["Iced strawberry matcha", "White tea", "Pistachio cookie"], "2025.03.27.", 14),
    (["Cinnamon Chai latte", "Cruffin deluxe"], "2025.04.13", 7),
    (["Iced Matcha Latte", "Golden Turmeric Latte"], "2025.05.20", 32),
    (["Caramel latte", "Pistachio cookie"], "2025.05.25", 7),
    (["Cappuccino", "Lime cheesecake"], "2025.05.28", 14),
    (["White tea"], "2025.06.05", 13),
    (["Iced vanilla coffee", "Iced Latte", "Water klein"], "2025.06.13", 2),
    (["Iced caramel coffee", "Iced Matcha Latte", "Jus de orange"], "2025.06.18", 3),
    (["Cappuccino", "Water klein", "Matcha cookie", "Arizona honey"], "2025.06.24", 2),
    (["Cappuccino", "White tea"], "2025.06.26", 3),
    (["Cheesecake red fruit", "Iced Latte"], "2025.06.27", 12),
    (["Cappuccino", "Water klein", "Iced Matcha Latte"], "2025.07.05", 3),
    (["Cappuccino", "Pistachio cookie"], "2025.07.18", 4),
    (["Iced Latte"], "2025.07.19", 14),
    (["Cappuccino", "Water klein"], "2025.07.22", 4),
    (["Matcha Latte", "Green tea", "Matcha cookie"], "2025.07.25", 1),
    (["Lime cheesecake", "Cappuccino"], "2025.08.01", 17),
    (["Cappuccino", "Water klein"], "2025.08.07", 14),
    (["Cappuccino", "Cheesecake red fruit", "Iced latte"], "2025.08.11", 5),
    (["Cappuccino", "Water klein"], "2025.08.13", 5),
    (["Carrot cake", "Cinnamon Chai latte"], "2025.08.19", 5),
    (["Cappuccino", "Water klein"], "2025.08.23", 14),
    (["Latte Machiatto", "Banana cake", "Cinnamon Chai latte"], "2025.08.26", 5),
    (["Cappuccino"], "2025.09.04", 32),
    (["Cappuccino", "Matcha latte"], "2025.09.05", 3),
    (["Golden Turmeric latte", "Water klein"], "2025.09.11", 13),
    (["Iced Matcha latte"], "2025.09.15", 14),
    (["Cappuccino", "Water klein", "Cinnamon Chai latte"], "2025.09.17", 2),
    (["Iced latte"], "2025.09.19", 3),
    (["Iced latte", "Cinnamon Chai latte"], "2025.09.22", 10),
    (["Cappuccino"], "2025.09.26", 10),
    (["Cinnamon Chai latte"], "2025.09.27", 16),
    (["Caffe latte"], "2025.09.29", 4),
    (["Cappuccino", "Stroopwafel cake", "Caffe latte"], "2025.10.01", 2),
    (["Cappuccino", "Appeltaart", "Caffe latte"], "2025.10.04", 8),
    (["Caffe mocha"], "2025.10.07", 10),
    (["Naturfrisk ginger ale", "Cappuccino"], "2025.10.08", 3),
    (["Cinnamon Chai latte", "Naturfrisk ginger ale"], "2025.10.13", 12),
    (["Caffe latte", "Pistachio cookie"], "2025.10.14", 8),
    (["Latte Machiatto", "Cinnamon bun"], "2025.10.25", 16),
    (["Cappuccino", "Hazelnoot caramel cake", "Water klein"], "2025.10.29", 4),
    (["Latte Machiatto", "Cappuccino"], "2025.10.31", 3),
    (["Cappuccino", "Water klein"], "2025.11.04", 3)
]

# 🆔 Add order IDs and convert dates
orders = []
for i, (items, date, table) in enumerate(order_data, start=1):
    orders.append({
        "Order ID": i,
        "Items": items,
        "Date": datetime.strptime(date, "%Y.%m.%d."),
        "Table": table
    })

# 💰 Calculate totals and analytics
spending_per_year = defaultdict(float)
spending_per_month = defaultdict(float)
spending_per_category = defaultdict(float)
order_totals = []

for order in orders:
    total = sum(prices.get(item, 0) for item in order["Items"])
    order["Total (€)"] = round(total, 2)
    order_totals.append(total)

    # Year/month stats
    y, m = order["Date"].year, order["Date"].month
    spending_per_year[y] += total
    spending_per_month[(y, m)] += total

    # Category stats
    for category, items in menu.items():
        for item in order["Items"]:
            if item in items:
                spending_per_category[category] += prices.get(item, 0)

# 🧮 Summary
summary = {
    "Total Spending Per Year": dict(spending_per_year),
    "Total Spending Per Month": {f"{y}-{m:02d}": v for (y, m), v in spending_per_month.items()},
    "Top 5 Most Ordered Items": Counter(
        item for o in orders for item in o["Items"]
    ).most_common(5),
    "Average Order Spend (€)": round(sum(order_totals) / len(order_totals), 2),
    "Most Expensive Order (€)": max(order_totals),
    "Least Expensive Order (€)": min(order_totals),
    "Spending by Category (€)": dict(spending_per_category)
}

# 💾 Export
with open("sam_orders.json", "w", encoding="utf-8") as f:
    json.dump([dict(o, Date=o["Date"].strftime("%Y-%m-%d")) for o in orders], f, indent=4)

with open("sam_summary.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Spending (€)"])
    for cat, val in spending_per_category.items():
        writer.writerow([cat, round(val, 2)])

# 🪞 Display summary
for key, value in summary.items():
    print(f"{key}:")
    if isinstance(value, dict):
        for k, v in value.items():
            print(f"    {k}: {v}")
    else:
        print(f"    {value}")
    print()
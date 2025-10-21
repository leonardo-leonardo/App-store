import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛒 Common Store", layout="wide")

# --- TITLE ---
st.title("🏪 Common Store - All Common Items")

# --- GENERATE 100 UNIQUE COMMON ITEMS ---
categories = ["Electronics", "Stationery", "Accessories", "Clothing", "Kitchen", "Sports", "Toys"]

adjectives = ["Ultra", "Pro", "Eco", "Smart", "Classic", "Deluxe", "Compact", "Premium", "Mega", "Super"]
nouns = ["Laptop", "Notebook", "Backpack", "Water Bottle", "Headphones", "Sneakers", "Jacket", "Camera", "Watch", "Tablet", 
         "Pen", "Keyboard", "Mouse", "Chair", "Ball", "Gloves", "Mixer", "Drone", "Puzzle", "Toy Car"]

common_items = []
used_names = set()

while len(common_items) < 100:
    category = random.choice(categories)
    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    # Ensure uniqueness
    if name in used_names:
        continue
    used_names.add(name)
    price = round(random.uniform(5, 500), 2)
    description = f"The {name} is a high-quality {category.lower()} item. Perfect for everyday use."
    common_items.append({
        "name": name,
        "category": category,
        "price": price,
        "description": description
    })

# --- CART SETUP ---
if "cart" not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item):
    st.session_state.cart.append(item)
    st.success(f"🛒 Added '{item['name']}' to cart!")

def checkout():
    if not st.session_state.cart:
        st.warning("Your cart is empty.")
    else:
        st.success("✅ Checkout complete!")
        st.session_state.cart.clear()

# --- FILTERS ---
categories_display = ["All"] + sorted({item["category"] for item in common_items})
category_filter = st.selectbox("Filter by category", categories_display)
search = st.text_input("Search items")

# Filter items
filtered_items = common_items
if category_filter != "All":
    filtered_items = [i for i in filtered_items if i["category"] == category_filter]
if search:
    filtered_items = [i for i in filtered_items if search.lower() in i["name"].lower()]

# --- DISPLAY ITEMS ---
if not filtered_items:
    st.info("No items found.")
else:
    for item in filtered_items:
        st.markdown(f"### {item['name']}")
        st.write(f"**Category:** {item['category']}")
        st.write(f"**Price:** ${item['price']}")
        st.write(f"**Description:** {item['description']}")
        if st.button(f"Add to Cart: {item['name']}", key=item['name']):
            add_to_cart(item)
        st.write("---")

# --- CART DISPLAY ---
st.subheader("🛒 Your Cart")
if st.session_state.cart:
    total = sum(i["price"] for i in st.session_state.cart)
    for i in st.session_state.cart:
        st.write(f"- {i['name']} (${i['price']})")
    st.write(f"**Total: ${total}**")
    if st.button("Checkout"):
        checkout()
else:
    st.info("Cart is empty.")


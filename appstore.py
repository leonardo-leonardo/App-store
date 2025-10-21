import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛒 Common Store", layout="wide")
st.title("🏪 Common Store - Browse Items")

# --- DATA SETUP ---
categories = ["Electronics", "Stationery", "Accessories", "Clothing", "Kitchen", "Sports", "Toys"]
adjectives = ["Ultra", "Pro", "Eco", "Smart", "Classic", "Deluxe", "Compact", "Premium", "Mega", "Super"]
nouns = ["Laptop", "Notebook", "Backpack", "Water Bottle", "Headphones", "Sneakers", "Jacket", "Camera", "Watch", "Tablet", 
         "Pen", "Keyboard", "Mouse", "Chair", "Ball", "Gloves", "Mixer", "Drone", "Puzzle", "Toy Car"]

description_templates = {
    "Electronics": [
        "High-performance {name} suitable for work, gaming, and daily use. Comes with a sleek design and optimized features to enhance your productivity and entertainment.",
        "Innovative {name} equipped with cutting-edge technology, providing seamless experience and maximum efficiency.",
        "Reliable {name} designed to enhance your productivity and entertainment, ensuring durability, speed, and modern design."
    ],
    "Stationery": [
        "Perfect for school, office, or creative projects, the {name} ensures smooth writing and long-lasting use.",
        "Durable {name} that supports your academic and professional tasks. A must-have for students, teachers, and office workers.",
        "Essential {name} for all your writing, drawing, and planning needs. Combines practicality with style."
    ],
    "Accessories": [
        "Stylish and functional {name} that complements your daily life. Designed with comfort, convenience, and durability in mind.",
        "High-quality {name} made to last while providing practicality and style.",
        "Durable {name} designed to offer both fashion and utility, adding elegance to your everyday routine."
    ],
    "Clothing": [
        "Comfortable and trendy {name} ideal for daily wear. Crafted from premium fabrics to ensure durability, style, and comfort.",
        "Premium fabric {name} that combines fashion with practicality, perfect for casual or professional environments.",
        "Perfect {name} to enhance your wardrobe with style and comfort. Designed to last while keeping you fashionable."
    ],
    "Kitchen": [
        "Essential {name} for a seamless cooking experience. Crafted with quality materials, it makes everyday kitchen tasks efficient and enjoyable.",
        "Durable {name} suitable for home chefs and culinary enthusiasts. Enhances your cooking experience with functionality and style.",
        "Premium quality {name} designed to simplify kitchen tasks, combining durability, practicality, and ease of use."
    ],
    "Sports": [
        "Designed for performance, the {name} helps improve your game and keeps you active. Built to withstand rigorous training and outdoor activities.",
        "Durable {name} perfect for sports enthusiasts. Enhances performance while ensuring safety and comfort.",
        "High-quality {name} crafted to support your fitness journey, providing reliability, durability, and style."
    ],
    "Toys": [
        "Fun and safe {name} suitable for children of all ages. Promotes creativity, imagination, and endless hours of play.",
        "Engaging {name} designed to stimulate learning and enjoyment. Perfect for gifting or personal collection.",
        "Durable {name} that encourages interactive and imaginative play, ensuring children stay entertained safely."
    ]
}

# --- GENERATE ITEMS ---
common_items = []
used_names = set()

while len(common_items) < 100:
    category = random.choice(categories)
    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    if name in used_names:
        continue
    used_names.add(name)
    price = round(random.uniform(5, 500), 2)
    description = random.choice(description_templates[category]).format(name=name)
    
    common_items.append({
        "name": name,
        "category": category,
        "price": price,
        "description": description
    })

# --- INITIALIZE CART ---
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- CART FUNCTIONS ---
def add_to_cart(item_name):
    if item_name in st.session_state.cart:
        st.session_state.cart[item_name]["qty"] += 1
    else:
        item = next((i for i in common_items if i["name"] == item_name), None)
        if item:
            st.session_state.cart[item_name] = {"item": item, "qty": 1}

def remove_from_cart(item_name):
    if item_name in st.session_state.cart:
        del st.session_state.cart[item_name]

def checkout():
    if st.session_state.cart:
        st.success("✅ Checkout complete!")
        st.session_state.cart.clear()
    else:
        st.warning("Cart is empty!")

# --- SEARCH & CATEGORY FILTER ---
search = st.text_input("🔍 Search items", "")
selected_category = st.radio("Select category", ["All"] + categories, horizontal=True)

filtered_items = common_items
if selected_category != "All":
    filtered_items = [i for i in filtered_items if i["category"] == selected_category]
if search:
    filtered_items = [i for i in filtered_items if search.lower() in i["name"].lower()]

# --- TOP CART SUMMARY ---
st.subheader("🛒 Cart Summary")
if st.session_state.cart:
    total_qty = sum(v["qty"] for v in st.session_state.cart.values())
    total_price = sum(v["item"]["price"] * v["qty"] for v in st.session_state.cart.values())
    st.write(f"Items in cart: **{total_qty}**  |  Total: **${total_price:.2f}**")
    with st.expander("View / Edit Cart"):
        for name, v in list(st.session_state.cart.items()):
            st.write(f"- {name} x {v['qty']} (${v['item']['price']} each)")
            col1, col2 = st.columns([1,3])
            with col1:
                if st.button("➖", key=f"minus_{name}"):
                    if v["qty"] > 1:
                        st.session_state.cart[name]["qty"] -= 1
                    else:
                        remove_from_cart(name)
            with col2:
                if st.button("❌ Remove", key=f"remove_{name}"):
                    remove_from_cart(name)
        if st.button("Checkout"):
            checkout()
else:
    st.info("Cart is empty.")

st.markdown("---")

# --- DISPLAY ITEMS AS LIST ---
st.subheader("🛍️ Browse Items")
for item in filtered_items:
    st.markdown(f"### {item['name']}")
    st.write(f"**Category:** {item['category']}  |  **Price:** ${item['price']}")
    st.write(f"{item['description']}")
    if st.button("Add to Cart", key=f"add_{item['name']}"):
        add_to_cart(item["name"])
        st.experimental_rerun()  # forces page to refresh and show updated cart
    st.markdown("---")

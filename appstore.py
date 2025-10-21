import streamlit as st
import uuid
import datetime

st.set_page_config(page_title="App Store Online", layout="wide")

# --- INITIAL STATE ---
if "users" not in st.session_state:
    st.session_state.users = {}
if "apps" not in st.session_state:
    st.session_state.apps = []
if "reviews" not in st.session_state:
    st.session_state.reviews = []
if "cart" not in st.session_state:
    st.session_state.cart = []
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# --- FUNCTIONS ---
def register_user(username, password, email):
    if username in st.session_state.users:
        st.warning("⚠️ Username already exists.")
    else:
        st.session_state.users[username] = {
            "password": password,
            "email": email,
            "is_admin": False,
        }
        st.success("✅ Registered successfully!")

def login_user(username, password):
    user = st.session_state.users.get(username)
    if not user or user["password"] != password:
        st.error("❌ Invalid username or password.")
    else:
        st.session_state.logged_in_user = username
        st.success(f"✅ Welcome back, {username}!")

def logout_user():
    st.session_state.logged_in_user = None
    st.success("👋 Logged out successfully.")

def add_app(name, description, category, price, uploaded_by):
    app_id = str(uuid.uuid4())
    st.session_state.apps.append({
        "id": app_id,
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "uploaded_by": uploaded_by,
        "uploaded_on": datetime.datetime.now(),
    })
    st.success(f"✅ App '{name}' added successfully!")

def add_review(app_id, username, rating, comment):
    st.session_state.reviews.append({
        "app_id": app_id,
        "username": username,
        "rating": rating,
        "comment": comment,
        "date": datetime.datetime.now(),
    })

def get_reviews(app_id):
    return [r for r in st.session_state.reviews if r["app_id"] == app_id]

def add_to_cart(app):
    st.session_state.cart.append(app)
    st.info(f"🛒 Added {app['name']} to cart.")

def checkout():
    if not st.session_state.cart:
        st.warning("🛍️ Your cart is empty.")
        return
    st.success("✅ Purchase successful! (Simulated checkout)")
    st.session_state.cart.clear()

# --- SIDEBAR AUTH ---
st.sidebar.title("👤 User")
if st.session_state.logged_in_user:
    st.sidebar.write(f"Hello, **{st.session_state.logged_in_user}**")
    if st.sidebar.button("Logout"):
        logout_user()
else:
    auth_action = st.sidebar.radio("Login / Register", ["Login", "Register"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    email = ""
    if auth_action == "Register":
        email = st.sidebar.text_input("Email")
    if st.sidebar.button(auth_action):
        if auth_action == "Login":
            login_user(username, password)
        else:
            register_user(username, password, email)

# --- MAIN CONTENT ---
st.title("🛍️ Streamlit App Store Online")

tabs = st.tabs(["🏠 Home", "🆕 Upload App", "📦 My Cart", "⭐ Reviews", "🧑‍💻 Admin"])

# --- TAB 1: HOME ---
with tabs[0]:
    st.subheader("Browse Apps")
    search = st.text_input("🔍 Search apps")
    if st.session_state.apps:
        category_filter = st.selectbox(
            "Filter by category",
            ["All"] + sorted({a.get("category", "Other") for a in st.session_state.apps if isinstance(a, dict)})
        )
    else:
        category_filter = "All"

    apps = [a for a in st.session_state.apps if isinstance(a, dict) and "name" in a]

    if search:
        apps = [a for a in apps if search.lower() in a["name"].lower()]
    if category_filter != "All":
        apps = [a for a in apps if a.get("category") == category_filter]

    if not apps:
        st.info("No apps found yet.")
    else:
        for app in apps:
            name = app.get("name", "Unnamed App")
            cat = app.get("category", "Unknown")
            price = app.get("price", 0.0)
            uploader = app.get("uploaded_by", "Anonymous")
            desc = app.get("description", "")

            with st.container(border=True):
                st.write(f"### {name}")
                st.caption(f"🗂 {cat} | 💰 ${price} | 👨‍💻 {uploader}")
                st.write(desc)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"Add to Cart: {app['id']}", key=f"cart_{app['id']}"):
                        add_to_cart(app)
                with col2:
                    if st.button(f"Rate/Review: {app['id']}", key=f"rev_{app['id']}"):
                        st.session_state["review_target"] = app["id"]

# --- TAB 2: UPLOAD APP ---
with tabs[1]:
    if not st.session_state.logged_in_user:
        st.warning("Please log in to upload.")
    else:
        st.subheader("Upload a New App")
        name = st.text_input("App Name")
        desc = st.text_area("Description")
        cat = st.selectbox("Category", ["Games", "Productivity", "Education", "Tools", "Other"])
        price = st.number_input("Price ($)", min_value=0.0, value=0.0)
        if st.button("Submit App"):
            if name and desc:
                add_app(name, desc, cat, price, st.session_state.logged_in_user)
            else:
                st.warning("Please fill in all fields.")

# --- TAB 3: CART ---
with tabs[2]:
    st.subheader("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = sum(app["price"] for app in st.session_state.cart)
        for app in st.session_state.cart:
            st.write(f"- {app['name']} (${app['price']})")
        st.write(f"### Total: ${total}")
        if st.button("Checkout"):
            checkout()

# --- TAB 4: REVIEWS ---
with tabs[3]:
    st.subheader("⭐ App Reviews")
    for app in st.session_state.apps:
        app_reviews = get_reviews(app["id"])
        st.write(f"#### {app.get('name','Unnamed App')} ({len(app_reviews)} reviews)")
        for r in app_reviews:
            st.write(f"- {r['username']} ({r['rating']}/5): {r['comment']}")

    if "review_target" in st.session_state:
        target_id = st.session_state["review_target"]
        app = next((a for a in st.session_state.apps if a["id"] == target_id), None)
        if app and st.session_state.logged_in_user:
            st.write(f"### Add Review for {app['name']}")
            rating = st.slider("Rating", 1, 5, 5)
            comment = st.text_area("Comment")
            if st.button("Submit Review"):
                add_review(app["id"], st.session_state.logged_in_user, rating, comment)
                st.success("✅ Review added!")
                del st.session_state["review_target"]

# --- TAB 5: ADMIN ---
with tabs[4]:
    if not st.session_state.logged_in_user:
        st.warning("Log in as admin to access this page.")
    else:
        user = st.session_state.users.get(st.session_state.logged_in_user)
        if not user.get("is_admin", False):
            st.info("You are not an admin.")
        else:
            st.subheader("🧑‍💻 Admin Dashboard")
            st.write("All registered users:")
            st.json(st.session_state.users)
            st.write("All apps:")
            st.json(st.session_state.apps)

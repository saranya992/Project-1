import streamlit as st
import pandas as pd
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",   # Update with your MySQL username
    password="",  # Update with your MySQL password
    database="redbus_project"
)
cursor = conn.cursor()

# Function to retrieve data from the MySQL database
def fetch_bus_routes():
    query = "SELECT * FROM bus_routes"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    return pd.DataFrame(rows, columns=columns)

# Fetch data
bus_data = fetch_bus_routes()

# Streamlit UI
st.set_page_config(page_title="REDBUS_APP", page_icon="🚌")
st.title("🚌 Welcome to the Bus Booking App!")
st.markdown("**Book your bus tickets easily and quickly!**")

# Filters
st.sidebar.subheader("Filter Buses")
route_name = st.sidebar.text_input("Route Name")
bus_name = st.sidebar.text_input("Bus Name")
bus_type = st.sidebar.selectbox("Bus Type", options=["Any"] + list(bus_data['Bus_Type'].unique()))
min_price, max_price = st.sidebar.slider("Price Range (₹)", 0, 5000, (0, 5000))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0)

# Filter the data
if route_name:
    bus_data = bus_data[bus_data['Route_Name'].str.contains(route_name, case=False)]
if bus_name:
    bus_data = bus_data[bus_data['Bus_Name'].str.contains(bus_name, case=False)]
if bus_type != "Any":
    bus_data = bus_data[bus_data['Bus_Type'] == bus_type]
bus_data = bus_data[(bus_data['Price'] >= min_price) & (bus_data['Price'] <= max_price)]
bus_data = bus_data[bus_data['Star_Rating'] >= min_rating]

if not bus_data.empty:
    bus_data['Price'] = '₹' + bus_data['Price'].astype(str)

# Display the filtered data
st.subheader("Available Buses")
if not bus_data.empty:
    st.dataframe(bus_data)
else:
    st.warning("No buses found for the given criteria.")

# Promotional Banners
st.markdown("### 🏷️ Special Offers!")
st.image("https://via.placeholder.com/800x200?text=Flat+20%25+OFF+on+First+Ride!", use_column_width=True)

# Footer - support and legal info
st.markdown("---")
st.write("📞 **Customer Support**: Call us at +91 123-456-7890 or email support@redbus.com")
st.write("📄 [Terms and Conditions](#) | [Privacy Policy](#) | [Refund Policy](#)")

# Close the MySQL connection
cursor.close()
conn.close()

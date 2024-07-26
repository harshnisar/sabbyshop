import streamlit as st
import json
import qrcode
from PIL import Image
from io import BytesIO
import base64

# Poster details
poster_details = {
    "Autorides": "1.png",
    "Metro blues": "2.png",
    "Somewhere in Humayunpur": "3.png",
    "Waiting": "4.png",
    "In the crowd": "5.png",
    "Caretaker": "6.png"
}

# Poster descriptions
poster_descriptions = {
    "Autorides": "Daily ritual to start and end the day.",
    "Metro blues": "Sometimes mindless scrolling is an act of self-preservation.",
    "Somewhere in Humayunpur": "Warmth of their hand and soft lights.",
    "Waiting": "As the day ends the sky welcomes you home.",
    "In the crowd": "When life get too much, just look up.",
    "Caretaker": "An act of unconditional love."
}

# Poster prices
prices = {
    "A3": 600,
    "A4": 400
}

# Function to generate QR code
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=5, border=5)  # Reduced size
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

# Function to calculate total price
def calculate_total(selected_posters):
    total = 0
    for poster, quantities in selected_posters.items():
        total += quantities["A3"] * prices["A3"]
        total += quantities["A4"] * prices["A4"]
    return total

# Function to load and encode images
def load_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# CSS for improved aesthetics with dark background and contrasting colors
st.markdown("""
    <style>
    body {
        background-color: #2c3e50 !important;
        color: #ecf0f1 !important;
    }
    .stApp {
        background-color: #2c3e50 !important;
        color: #ecf0f1;
        }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #ecf0f1;
    }
    .horizontal-center {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .quantity-input {
        width: 100px !important;
        margin: 10px;
    }
    .title {
        font-size: 4.5em;
        color: #ecf0f1;
        margin-bottom: 0;
        margin-top: 0;
    }
    .header {
        font-size: 1.5em;
        color: #ecf0f1;
        margin-bottom: 10px;
        margin-top: 10px; /
    }
    .poster-title {
        font-size: 1.2em;
        color: #ecf0f1;
        margin-top: 0px;
    }
    .poster-description {
        font-size: 1em;
        color: #bdc3c7;
        margin-bottom: 20px;
    }
    .total-amount {
        font-size: 1.5em;
        color: #e74c3c;
    }
    .qr-button {
        background-color: #2ecc71;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .qr-button:hover {
        background-color: #27ae60;
    }
    .submit-button {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .submit-button:hover {
        background-color: #2980b9;
    }
    .input-field {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        background-color: #34495e;
        color: #ecf0f1;
    }
            
    hr {
    margin: 10px 0; /* Adjust as needed */
    border: 0;
    border-top: 1px solid #ecf0f1;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app
st.markdown("<h1 class='title'>Sabhyata Design</h1>", unsafe_allow_html=True)
st.markdown("<div class='header'><i>An Ode to Bade Shehr Ki Ladkiyaan</i></div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal rule


selected_posters = {}
qr_code_generated = False
qr_img_str = None
pay_link = None

def reset_qr_code():
    global qr_code_generated, qr_img_str, pay_link
    qr_code_generated = False
    qr_img_str = None
    pay_link = None

for poster, file in poster_details.items():
    image_data = load_image(file)
    st.markdown(f"""<div class='center'>
                <h3 class='poster-title'>{poster}</h3>
                <p class='poster-description'>{poster_descriptions[poster]}</p>
                <img src='data:image/png;base64,{image_data}' width='250'>
                </div>""", unsafe_allow_html=True)
    st.markdown("<div class='horizontal-center'>", unsafe_allow_html=True)
    a3_qty = st.number_input(f"A3 Quantity", min_value=0, value=0, key=f"{poster}_A3", format="%d", on_change=reset_qr_code)
    a4_qty = st.number_input(f"A4 Quantity", min_value=0, value=0, key=f"{poster}_A4", format="%d", on_change=reset_qr_code)
    st.markdown("</div>", unsafe_allow_html=True)
    selected_posters[poster] = {"A3": a3_qty, "A4": a4_qty}
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal rule

total_amount = calculate_total(selected_posters)
st.markdown(f"<div class='total-amount'>Total Amount: Rs {total_amount}</div>", unsafe_allow_html=True)

# Additional fields
name = st.text_input("Name", key="name", help="Please enter your full name.")
email = st.text_input("Email Address", key="email", help="Please enter your email address.")
address = st.text_area("Shipping Address", key="address", help="Please enter your shipping address.")
mobile = st.text_input("Mobile Number", key="mobile", help="Please enter your mobile number.")

if st.button("Generate QR Code", key="generate_qr"):
    if total_amount > 0:
        qr_url = f"upi://pay?pa=sabhyatajain3997@okhdfcbank&pn=Sabhyata&cu=INR&am={total_amount}&tn={email}"
        qr_img_str = generate_qr_code(qr_url)
        pay_link = qr_url
        qr_code_generated = True
    else:
        st.error("Total amount must be greater than 0 to generate QR code.")

if qr_code_generated and qr_img_str:
    st.image(qr_img_str, caption="Scan to Pay", use_column_width=True)
    st.markdown(f"<div style='text-align: center;'><a href='{pay_link}'>Click This to Pay by UPI (Mobile)</a></div>", unsafe_allow_html=True)

# Upload button should only appear once
payment_screenshot = st.file_uploader("Upload Payment Screenshot", type=["jpg", "jpeg", "png"])

if st.button("Submit", key="submit"):
    if payment_screenshot is None:
        st.error("Please upload a payment screenshot.")
    else:
        # Save data to a local JSON file
        data = {
            "name": name,
            "email": email,
            "address": address,
            "mobile": mobile,
            "selected_posters": selected_posters,
            "total_amount": total_amount,
            "payment_screenshot": payment_screenshot.name
        }
        with open("orders.json", "a") as f:
            json.dump(data, f)
            f.write("\n")
        st.success("Order submitted successfully!")

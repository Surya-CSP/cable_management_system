from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import qrcode
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dummy credentials for login
VALID_USERNAME = "surya"
VALID_PASSWORD = "surya"

# Ensure a storage directory for QR codes
if not os.path.exists("qrcodes"):
    os.makedirs("qrcodes")

# Serve the HTML file directly from the project root
@app.route('/')
def home():
    return send_from_directory('.', 'av.html')

# Serve the CSS file directly from the project root
@app.route('/style.css')
def serve_css():
    return send_from_directory('.', 'style.css')

# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"})

# Route to generate QR code and save data
@app.route("/generate_qrcode", methods=["POST"])
def generate_qrcode():
    data = request.get_json()
    print("Received data:", data)
    try:
        # Extract data from the POST request
        name = data["name"]
        box_number = data["boxNumber"]
        amount = data["amount"]

        # Save data to Excel
        df = pd.DataFrame([[name, box_number, amount]], columns=["Customer Name", "Box Number", "Amount"])
        excel_file = "payments.xlsx"

        if os.path.exists(excel_file):
            existing_df = pd.read_excel(excel_file)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(excel_file, index=False)

        # Generate QR code text
        qr_text = f"Name: {name}, Box Number: {box_number}, Amount: {amount}"
        qr_code = qrcode.make(qr_text)
        qr_code_file = os.path.join("qrcodes", f"{box_number}.png")
        qr_code.save(qr_code_file)

        # Return the result in JSON format
        return jsonify({
            "success": True,
            "qrData": qr_text,
            "qrImage": f"/qrcodes/{box_number}.png"
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "error": str(e)})

# Route to serve QR code images
@app.route("/qrcodes/<filename>")
def serve_qrcode(filename):
    print(f"Serving file: {filename}")
    return send_from_directory("qrcodes", filename)

# Function to process Excel files and find unmatched box numbers
def process_files():
    customer_file = "customer.xlsx"  # First Excel file
    payments_file = "payments.xlsx"  # Second Excel file

    # Read the Excel files
    if not os.path.exists(customer_file) or not os.path.exists(payments_file):
        return []

    customer_data = pd.read_excel(customer_file)
    payments_data = pd.read_excel(payments_file)

    # Sort by 'Box number' and find mismatched box numbers
    unmatched_boxes = set(customer_data['Box number']) - set(payments_data['Box number'])
    return list(unmatched_boxes)

# Route for sending alerts
@app.route('/send-alert', methods=['POST'])
def send_alert():
    unmatched_boxes = process_files()
    # Simulate sending an alert (you can integrate with an SMS or email service here)
    return jsonify({"status": "success", "message": "Alert sent successfully", "unmatched_boxes": unmatched_boxes})

# Route for viewing box numbers
@app.route('/view-box-numbers', methods=['GET'])
def view_box_numbers():
    unmatched_boxes = process_files()
    return jsonify({"status": "success", "message": "Those who haven't paid yet", "unmatched_boxes": unmatched_boxes})

if __name__ == "__main__":
    app.run(debug=True)

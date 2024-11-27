from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Twilio credentials and endpoints (replace with your actual credentials)
TWILIO_ACCOUNT_SID = "AC1f42d2ab5fb3f955895a340386741d32"
TWILIO_AUTH_TOKEN = "d31ab9d8ec9335d25466d05d14cf64c4"
TWILIO_PHONE_NUMBER = "+15076970451"  # Your Twilio number
OWNER_PHONE_NUMBER = "+919059723299"  # Owner's phone number

TWILIO_SMS_URL = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

@app.route('/')
def index():
    return render_template("report.html")

@app.route('/send-report', methods=["POST"])
def send_report():
    customer_address = request.form.get("customer_address")
    customer_number = request.form.get("customer_number")
    complaint = request.form.get("complaint")

    # Combine fields into a single message
    message_body = f"""
    Customer Details:
    Address: {customer_address}
    Phone: {customer_number}

    Complaint:
    {complaint}
    """

    # Prepare data for Twilio API
    data = {
        "To": OWNER_PHONE_NUMBER,
        "From": TWILIO_PHONE_NUMBER,
        "Body": message_body
    }

    # Send SMS using Twilio API via HTTP POST
    try:
        response = requests.post(
            TWILIO_SMS_URL,
            data=data,
            auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        )

        if response.status_code == 201:  # HTTP 201 Created indicates success
            return "Report sent successfully!"
        else:
            # Log the response for debugging
            print(f"Twilio Response: {response.text}")
            return f"Failed to send report: {response.json().get('message', 'Unknown error')}"
    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return f"Failed to send report: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

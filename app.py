# app.py
import requests
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, render_template, request

# -------------------------------
# Function to get public IPs (fallback using ipify)
# -------------------------------
def get_public_ip():
    ipv4, ipv6 = None, None
    try:
        ipv4 = requests.get("https://api.ipify.org?format=json", timeout=5).json().get("ip")
    except:
        pass
    try:
        ipv6 = requests.get("https://api64.ipify.org?format=json", timeout=5).json().get("ip")
    except:
        pass
    return ipv4, ipv6

# -------------------------------
# Function to get local/private IP
# -------------------------------
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return None

# -------------------------------
# Function to get IP details (ipinfo.io)
# -------------------------------
def get_ip_details(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=5).json()
        return response
    except:
        return {}

# -------------------------------
# Function to get mobile details
# -------------------------------
def get_mobile_details(number, default_region=None):
    try:
        phone_number = phonenumbers.parse(number, default_region)
        details = {
            "International format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "National format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
            "E.164 format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164),
            "Location": geocoder.description_for_number(phone_number, "en"),
            "Carrier": carrier.name_for_number(phone_number, "en"),
            "Time Zones": ", ".join(timezone.time_zones_for_number(phone_number)),
            "Valid Number": "Yes" if phonenumbers.is_valid_number(phone_number) else "No",
            "Possible Number": "Yes" if phonenumbers.is_possible_number(phone_number) else "No"
        }
        return details
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return {"Error": f"Error parsing number: {e}"}

# -------------------------------
# Label map for pretty results
# -------------------------------
label_map = {
    "local_ip": "💻 Local IP",
    "public_ipv4": "🌐 Public IPv4",
    "public_ipv6": "🌐 Public IPv6",
    "ip": "🌍 IP Address",
    "hostname": "🖥 Hostname",
    "city": "🏙 City",
    "region": "📍 Region",
    "country": "🚩 Country",
    "loc": "📌 Coordinates",
    "org": "📡 ISP/Organization",
    "timezone": "🕒 Timezone",
    "postal": "📮 Postal Code",
    "readme": "ℹ️ Readme",
    "International format": "☎ International Format",
    "National format": "☎ National Format",
    "E.164 format": "☎ E.164 Format",
    "Location": "📍 Location",
    "Carrier": "📡 Carrier",
    "Time Zones": "🕒 Time Zones",
    "Valid Number": "✅ Valid Number",
    "Possible Number": "❓ Possible Number",
    "Error": "⚠️ Error"
}

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def show_results():
    lookup_type = request.form.get('type')
    input_value = request.form.get('input_value')
    results_data = {}

    if lookup_type == 'my_ips':
        # ✅ Get visitor’s real IP from Flask request
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        ipv4, ipv6 = get_public_ip()  # fallback
        results_data['local_ip'] = get_local_ip()
        results_data['public_ipv4'] = client_ip or ipv4
        results_data['public_ipv6'] = ipv6

        if client_ip:
            results_data.update(get_ip_details(client_ip))
        elif ipv4:
            results_data.update(get_ip_details(ipv4))

    elif lookup_type == 'single_ip':
        results_data = get_ip_details(input_value)

    elif lookup_type == 'phone_number':
        results_data = get_mobile_details(input_value)

    # Convert keys → labels
    pretty_results = []
    for key, value in results_data.items():
        label = label_map.get(key, key)  # fallback to original key if not mapped
        pretty_results.append((label, value))

    return render_template('results.html', results=pretty_results)

if __name__ == '__main__':
    app.run(debug=True)

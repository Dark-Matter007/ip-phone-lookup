import requests
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# -------------------------------
# Function to get public IPs
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
# Function to bulk lookup IPs from file
# -------------------------------
def bulk_ip_lookup(filename="ips.txt"):
    results = {}
    try:
        with open(filename, "r") as f:
            ips = [line.strip() for line in f if line.strip()]
        for ip in ips:
            results[ip] = get_ip_details(ip)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Create it and add IPs (one per line).")
    return results

# -------------------------------
# Function to get mobile details
# -------------------------------
def get_mobile_details(number):
    phone_number = phonenumbers.parse(number)
    details = {
        "International format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "National format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
        "E.164 format": phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164),
        "Location": geocoder.description_for_number(phone_number, "en"),
        "Carrier": carrier.name_for_number(phone_number, "en"),
        "Time Zones": timezone.time_zones_for_number(phone_number),
        "Valid Number": phonenumbers.is_valid_number(phone_number),
        "Possible Number": phonenumbers.is_possible_number(phone_number)
    }
    return details

# -------------------------------
# Main Script
# -------------------------------
if __name__ == "__main__":

    # 1. Get Local (Private) IP
    local_ip = get_local_ip()
    print("\nLocal IP (Private):", local_ip)

    # 2. Get Public IPs
    ipv4, ipv6 = get_public_ip()
    print("\nPublic IP Addresses")
    print("IPv4:", ipv4)
    print("IPv6:", ipv6)

    # 3. Get Details of your IP
    ip_to_lookup = ipv4 if ipv4 else ipv6
    if ip_to_lookup:
        ip_details = get_ip_details(ip_to_lookup)
        print("\nYour Public IP Details")
        print("IP:      ", ip_details.get("ip"))
        print("City:    ", ip_details.get("city"))
        print("Region:  ", ip_details.get("region"))
        print("Country: ", ip_details.get("country"))
        print("Loc:     ", ip_details.get("loc"))   # latitude,longitude
        print("Postal:  ", ip_details.get("postal"))
        print("Org/ISP: ", ip_details.get("org"))
    else:
        print("Could not detect any public IP address.")

    # 4. Lookup details of another single IP
    target_ip = "8.8.8.8"  # Example: Google DNS (replace with any known IP)
    print(f"\nDetails of Other IP ({target_ip})")
    target_details = get_ip_details(target_ip)
    for k, v in target_details.items():
        print(f"{k}: {v}")

    # 5. Bulk IP lookup from file
    print("\nBulk IP Lookup from 'ips.txt'")
    bulk_results = bulk_ip_lookup("ips.txt")
    for ip, details in bulk_results.items():
        print(f"\nIP: {ip}")
        for k, v in details.items():
            print(f"  {k}: {v}")

    # 6. Get Mobile Number Details
    number = "+919949961907"  # Replace with any number
    mobile_details = get_mobile_details(number)
    print("\nMobile Number Details")
    for key, value in mobile_details.items():
        print(f"{key}: {value}")

import threading
import time
import ssl
import re
import requests
import binascii
import urllib3
from flask import Flask, request, jsonify
import websocket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ==========================================
# ⚙️ CONFIGURATIONS (Apna Token aur UID yaha daalo)
# ==========================================
MY_UID = "4470446192" 
MY_TOKEN = "paqxIlY4D%2Bf3QaM4d5uYxf8ncrUfXJ5M%2FHVkQ3PPTTUshAoDFFrYGKf0XwuRMszb%2CnNM9ovMxw68QDV93ChKz3zo3fT5RCFv0L91AKx2sUI1ySktpYnMTOPUJwWs6n7ANcCxs12Y7lkbcNTurd6zisrsbQHSieeKgFAlKa8GXZx4UnUVONJ%2FuIScuILIZHVxXYiNmsfe5DQKtBbXNGCySZHC4ittdDCIOLuB7iVoPgnW0Jd7cCbeWTwf6uQbBuMWtjWRFPHc%2B9GUpISZ%2BhJq%2FCrb%2B5OX2S5QVMl%2FB%2Fe7mwMS75n7BpEZ90E5tPyL0hvOt9fojO4g1eym0SCpeDnDkmjQThlXDHvA3Zu9H0RxyPXSpWYDEWVlEn1eVCKqFdO1jA3idyQNaBw5Ol3EzqtfvfGl2uhTD5SS2YfJ4%2BEBiL7rRNJC4nH0kvqey%2BbN%2BBRNd%2FieblNP%2FvFLjzH8qp46T5OWdBRl4fqtQobgUxwaCv%2FjEZT3OJMWk0%2F0dUH%2FCQkmpJ8oltfrYQZQdDZxZ35A%2FBrafhTVAM%2BQpZmSX1JxMeyZ5GS2S7vJgWHyNJKLh1wsg"
WS_URL = f"wss://i-875.olaparty.com/ikxd_cproxy?token={MY_UID}"

HEADERS = {
    "X-App-Name": "olaparty",
    "X-Auth-Token": MY_TOKEN, 
    "Origin": "https://i-875.olaparty.com",
    "User-Agent": "com.live.partytill/2952 (Linux; U; Android 15; en_IN)"
}

current_active_ws = None

def string_to_hex(s):
    return binascii.hexlify(s.encode()).decode()

def uid_to_varint_hex(uid_str, target_length=6):
    try:
        number = int(uid_str)
        encoded_bytes = []
        while True:
            byte = number & 0x7F
            number >>= 7
            if number > 0:
                byte |= 0x80
                encoded_bytes.append(byte)
            else:
                encoded_bytes.append(byte)
                break
        while len(encoded_bytes) < target_length:
            last = encoded_bytes.pop()
            encoded_bytes.append(last | 0x80)
            encoded_bytes.append(0x00)
        return ' '.join([f'{b:02X}' for b in encoded_bytes])
    except: return None

def get_location_packet(target_uid):
    base_hex = "0A 4E 0A 19 6E 65 74 2E 69 68 61 67 6F 2E 63 68 61 6E 6E 65 6C 2E 73 72 76 2E 6D 67 72 10 C6 A7 A1 D5 C9 33 22 05 65 6E 5F 69 6E 3A 1A 43 68 61 6E 6E 65 6C 2E 47 65 74 43 75 72 72 65 6E 74 43 68 61 6E 6E 65 6C 73 42 05 30 2E 30 2E 30 48 01 1A 08 08 FA 9F D6 D3 10 10 01"
    old_time_varint = "C6 A7 A1 D5 C9 33"
    old_uid_varint = "FA 9F D6 D3 10"
    new_uid_varint = uid_to_varint_hex(target_uid, target_length=5)
    new_time_str = str(int(time.time() * 1000))
    new_time_varint = uid_to_varint_hex(new_time_str, target_length=6)
    if not new_uid_varint or not new_time_varint: return None
    packet_hex = base_hex.replace(old_uid_varint, new_uid_varint).replace(old_time_varint, new_time_varint)
    return bytes.fromhex(packet_hex.replace(" ", ""))

@app.route('/change_room', methods=['GET'])
def change_room():
    target_cid = request.args.get('cid')
    if not target_cid:
        return jsonify({"status": "error", "message": "No CID provided"}), 400
    
    # Yahan bot websocket ke through naye room me shift hone ka packet bhejta hai
    return jsonify({"status": "success", "message": f"Bot shifting to {target_cid}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
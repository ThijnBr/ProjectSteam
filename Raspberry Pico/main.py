import network
import time
import urequests
import ujson
from machine import Pin
import neopixel

# Wi-Fi configuration
ssid = "Yphone"
password = "yverthug"

# Create a WLAN object
wlan = network.WLAN(network.STA_IF)

# Activate the WLAN interface
wlan.active(True)

# Connect to the Wi-Fi hotspot
wlan.connect(ssid, password)

# Wait for the connection to be established
while not wlan.isconnected():
    time.sleep(1)

# Print Wi-Fi connection details
print("Wi-Fi connected")
print("IP address:", wlan.ifconfig()[0])

# Define NeoPixel pin and number of pixels
neopixel_pin = 15
num_pixels = 8

# Create a NeoPixel object
np = neopixel.NeoPixel(Pin(neopixel_pin), num_pixels)

# API request configuration
api_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=14B0152189C811A5DE80FE50EB4DA7CC&steamid=76561199477803639&relationship=friend"

# Blinking effect function
def blink_neopixel(color, duration):
    np[0] = color
    np.write()
    time.sleep(duration)
    np[0] = (0, 0, 0)
    np.write()

try:
    while True:
        # Make an API request to get the list of friends
        response = urequests.get(api_url)

        if response.status_code == 200:
            # Parse and print the list of friends
            friends_data = ujson.loads(response.text)
            friends = friends_data['friendslist']['friends']
            print("List of Friends:")
            for friend in friends:
                print(f"Friend: {friend['steamid']}, Relationship: {friend['relationship']}")

            # Check the online/offline status of each friend
            for friend in friends:
                friend_id = friend['steamid']
                friend_status_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=14B0152189C811A5DE80FE50EB4DA7CC&steamids={friend_id}"
                friend_status_response = urequests.get(friend_status_url)

                if friend_status_response.status_code == 200:
                    friend_status_data = ujson.loads(friend_status_response.text)
                    player = friend_status_data['response']['players'][0]
                    print(f"Friend {friend_id} - Online Status: {player['personastate']}")

                    # Control NeoPixel based on online/offline status
                    if friend_id == "76561198401205997" and player['personastate'] == 1:
                        print("Online animal!")
                        blink_neopixel((0, 255, 0), 0.5)  # Blink in green for 0.5 seconds
                    elif friend_id == "76561198401205997" and player['personastate'] == 0:
                        print("Offline animal!")
                        blink_neopixel((255, 0, 0), 0.5)  # Blink in red for 0.5 seconds

                else:
                    print(f"Error getting status for friend {friend_id}: {friend_status_response.status_code}")
                    print(friend_status_response.text)

        else:
            print("Error:", response.status_code)
            print(response.text)

finally:
    # Close the response connection
    if response:
        response.close()

    # Close the friend status response connection
    if friend_status_response:
        friend_status_response.close()

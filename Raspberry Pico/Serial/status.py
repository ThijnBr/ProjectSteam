import time
from serial.tools import list_ports
import serial
import requests


#steamid = '76561198058830724' #glenn
steamid = '76561198219094895' #Dieu
# steamid = '76561198401205997'

def getUserProfileState(steamid):
    apikey = '14B0152189C811A5DE80FE50EB4DA7CC'
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids={steamid}"

    response = requests.get(url)
    data = response.json()['response']['players'][0]

    try:
        info = 'Plays ' + data['gameextrainfo']
    except KeyError:
        info = None

    return data['personastate'], data['personaname'], info

def read_serial(port):
    """Read data from serial port and return as string."""
    line = port.read(1000)
    return line.decode()


# First manually select the serial port that connects to the Pico
serial_ports = list_ports.comports()

print("[INFO] Serial ports found:")
for i, port in enumerate(serial_ports):
    print(str(i) + ". " + str(port.device))

pico_port_index = int(input("Which port is the Raspberry Pi Pico connected to? "))
pico_port = serial_ports[pico_port_index].device

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    if serial_port.isOpen():
        print("[INFO] Using serial port", serial_port.name)
    else:
        print("[INFO] Opening serial port", serial_port.name, "...")
        serial_port.open()

    try:

        # Request user input
        commands = ['Status opgvragen ']
        # commands = ['off', 'on', 'exit', 'temp']
        while True:
            choice = input(" yes? [" + ", ".join(commands) + "] ")
            state = getUserProfileState(steamid)[0]
            name = getUserProfileState(steamid)[1]
            game = getUserProfileState(steamid)[2]
            if choice == "yes" and state in range(6):
                data = f"{state};{name};{game}\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + str(state) +' '+ str(name) + ' ' + str(game))


            else:
                print("[WARN] Unknown command.")

    except KeyboardInterrupt:

        print("[INFO] Ctrl+C detected. Terminating.")
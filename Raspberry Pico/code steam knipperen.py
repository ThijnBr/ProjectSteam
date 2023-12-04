import time
import machine
import os

# Constants and Configurations
KNOWN_FREE_GAMES = [
    "destiny 2", "dota 2", "alien swarm", "america's army 3", "arma ii free", "spacewar",
    # ... (remaining games)
]

LED_PIN = 18  # Adjust to the actual pin number
STATE_FILE = "state.txt"
BLINK_DURATION = 1  # Adjust blink duration as needed
DELAY_OBSERVE = 10  # Adjust delay time before exiting

# Function to control the LED
def control_led(state):
    machine.Pin(LED_PIN, machine.Pin.OUT).value(state)

# Function to check if the entered game name is in the list of known free games
def is_free_game(game_name):
    return any(game.lower() in game_name.lower() for game in KNOWN_FREE_GAMES)

# Function to check if input has been given
def is_input_given():
    """Check if input has been given."""
    return os.path.exists(STATE_FILE)

# Function to mark that input has been given
def mark_input_given():
    """Mark that input has been given."""
    with open(STATE_FILE, "w") as file:
        file.write("input_given")

# Main program logic
def main():
    """Main program logic."""
    while True:
        user_choice = input("Enter '1' to start blinking LED, '2' to turn off LED, or 'q' to quit: ")

        if user_choice.lower() == 'q':
            break
        elif user_choice == '1':
            game_name = input("Enter the name of the game: ")
            if is_free_game(game_name):
                print("LED is blinking...")
                control_led(1)  # Turn on the LED
                time.sleep(BLINK_DURATION)
                control_led(0)  # Turn off the LED
                mark_input_given()
            else:
                print("The entered game name is not in the list of free games.")
        elif user_choice == '2':
            print("LED turned off.")
            control_led(0)
            mark_input_given()
        else:
            print("Invalid choice. Please enter '1', '2', or 'q'.")

    if not is_input_given():
        print("Program ended without receiving input.")
    else:
        print("Already received input after reboot.")
        time.sleep(DELAY_OBSERVE)

if __name__ == "__main__":
    main()

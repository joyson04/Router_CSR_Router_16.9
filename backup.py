# backup_config.py
import paramiko
import time
from datetime import datetime

# Define the device parameters
host = '192.168.174.153'  # Replace with your router's IP
username = 'admin'  # Replace with your username
password = 'Cisco123'  # Replace with your password
commands = ["terminal length 0", "show running-config"]

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the device
    ssh.connect(host, username=username, password=password, look_for_keys=False, allow_agent=False)

    # Create an interactive shell
    shell = ssh.invoke_shell()

    # Wait for the shell to be ready
    time.sleep(1)

    # Send commands and wait for the output
    output = ''
    for cmd in commands:
        shell.send(f'{cmd}\n')  # Send the command
        time.sleep(2)  # Wait for the command to execute

        # Read the output
        while shell.recv_ready():
            output += shell.recv(1024).decode('utf-8')  # Decode bytes to string

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup-config_{timestamp}.txt"

    # Save the configuration to a file
    with open(backup_filename, 'w') as file:
        file.write(output)  # Write the string to the file

    print(f"Configuration backed up to {backup_filename}")

finally:
    # Close the SSH connection
    ssh.close()
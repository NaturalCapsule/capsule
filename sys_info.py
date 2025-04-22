import subprocess
import re


def check_gpu():
    try:
        result = subprocess.run(['nvidia-smi'],
                                stdout=subprocess.PIPE, text=True)
        check = result.stdout.strip()
        return f"{check}"
    except FileNotFoundError:
        return ''

def get_nvidia_gpu_usage():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                                stdout=subprocess.PIPE, text=True)
        usage = result.stdout.strip()
        return f"{usage}"
    except FileNotFoundError:
        return ''

def get_nvidia_total_vram():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        vram = result.stdout.strip()
        return f"{vram:.1}"
    except FileNotFoundError:
        return ''

def get_nvidia_used_vram():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        used_vram = result.stdout.strip()
        used_vram = int(used_vram) / 1000
        return f"{used_vram:.2f}"
    except FileNotFoundError:
        return ''

def get_nvidia_temp():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        temp = result.stdout.strip()
        return f"{temp}"
    except FileNotFoundError:
        return ''

def get_nvidia_powerdraw():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        power = result.stdout.strip()
        return f"{power}W"
    except FileNotFoundError:
        return ''

def get_nvidia_name():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        name = result.stdout.strip()
        return f"{name}"
    except FileNotFoundError:
        return ''

def get_nvidia_fanspeed(): 
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=fan.speed', '--format=csv,noheader,nounits']
,
                                stdout=subprocess.PIPE, text=True)
        fan = result.stdout.strip()
        return f"{fan}"
    except FileNotFoundError:
        return ''


def get_total_ram():
    result = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], stdout=subprocess.PIPE)
    total_ram_kb = int(result.stdout.decode().split()[1])
    total_ram_gb = round(total_ram_kb / 1024 / 1024, 2)
    return f"{total_ram_gb}"


def get_ram_usage():
    result = subprocess.run(
        ['awk', '/MemTotal/ {total=$2} /MemAvailable/ {avail=$2} END {print (total-avail)/1024/1024}', '/proc/meminfo'],
        capture_output=True,
        text=True
    )
    result = float(result.stdout.strip())
    return f"{result:.3f}"

def get_used_ram():
    result = subprocess.run(
    [
        'awk',
        '/MemTotal|MemFree|Buffers|^Cached|^SReclaimable/ {a[$1]=$2} '
        'END {used=(a["MemTotal:"]-a["MemFree:"]-a["Buffers:"]-a["Cached:"]-a["SReclaimable:"])/1024/1024; '
        'printf "%.2f", used}'
        ,
        '/proc/meminfo'
    ],
    capture_output=True,
    text=True
    )
    
    result = float(result.stdout.strip())
    return f"{result:.2f}"


def get_cpu_temp():
    result = subprocess.run(['sensors'], capture_output=True, text=True)
    temps = []

    # Regex patterns for Intel & AMD
    patterns = [
        r'(Core \d+):\s+\+([\d\.]+)°C',    
        r'Package id \d+:\s+\+([\d\.]+)°C',
        r'Tctl:\s+\+([\d\.]+)°C', 
        r'Tdie:\s+\+([\d\.]+)°C', 
    ]

    for line in result.stdout.splitlines():
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                if 'Core' in pattern:
                    core = match.group(1)
                    temp = match.group(2)
                    temps.append(f"{core}: {temp}°C")
                else:
                    temp = match.group(1)
                    temps.append(f"{temp}")

    if temps:
        return temps[0]
    else:
        return ["CPU temperature not found"]

def get_cpu_usage():
    result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('%Cpu(s)'):
            parts = line.split(',')
            user = float(parts[0].split()[1])
            system = float(parts[1].split()[0])
            total_usage = user + system
            return f"{total_usage:.1f}"

def get_cpu_info():
    result = subprocess.run(['lscpu'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('Model name'):
            return line.split(":")[1].strip()
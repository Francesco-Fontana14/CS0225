import socket

def PS(Pm, PM, target):
    print("Scannerizzando...", target, ", range: ", Pm, "-", PM)
    for port in range(Pm, PM + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        status = s.connect_ex((target, port))
        if (status == 0):
            print(f"Porta {port} APERTA")
        else:
            print(f"Porta {port} CHIUSA")
    return 0

def main():    
    target = input("Target ip: ")       
    while True:
        port_range = input("Range di porte nel formato p-P: ")
        lowport = int(port_range.split('-')[0])
        highport = int(port_range.split('-')[1])
        PS(lowport, highport, target)
    
if __name__ == "__main__":
    main()
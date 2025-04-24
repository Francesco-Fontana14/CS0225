import psutil
from datetime import datetime
import time

def get_active_connections():
    print(f"\n[+] Scan avviato alle {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 110)
    print("{:<20} {:<20} {:<12} {:<12} {:<15} {:<8} {:<20}".format(
        "IP Locale", "IP Remoto", "Porta Locale", "Porta Remota", "Stato", "PID", "Processo"
    ))
    print("-" * 110)

    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            l_ip, l_port = (conn.laddr.ip, conn.laddr.port) if conn.laddr else ("-", "-")
            r_ip, r_port = (conn.raddr.ip, conn.raddr.port) if conn.raddr else ("-", "-")
            pid = conn.pid if conn.pid else "-"
            try:
                proc_name = psutil.Process(conn.pid).name() if conn.pid else "-"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                proc_name = "N/D"
            print("{:<20} {:<20} {:<12} {:<12} {:<15} {:<8} {:<20}".format(
                l_ip, r_ip, l_port, r_port, conn.status, pid, proc_name
            ))

if __name__ == "__main__":
    try:
        while True:
            get_active_connections()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Interrotto dall'utente. Exit.")
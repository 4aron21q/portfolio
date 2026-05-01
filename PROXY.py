import sys, socket, threading
LIST_IP = '0.0.0.0'
LIST_PORT = 8080
def potok(new_sock, serv_sock):
    try:
        while True:
            data = new_sock.recv(4096)
            if not data:
                break
            serv_sock.sendall(data)
    except Exception:
        pass
def handle_client(new_sock, host_ip, host_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_ip, host_port))
        t1 = threading.Thread(target = potok, daemon = True, args = (sock, new_sock))
        t2 = threading.Thread(target = potok, daemon = True, args = (new_sock, sock))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        print(f"[!] Error -> {e}")
    finally:
        new_sock.close()
        sock.close()
def proxy():
    host_ip = str(input())
    host_port = int(input())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((LIST_IP, LIST_PORT))
        sock.listen(5)
        print(f"[*] Listen {LIST_IP}:{LIST_PORT}")
        while True:
            new_sock, addr_info = sock.accept()
            print(f"[+] Connect info {addr_info[0]}:{addr_info[1]}")
            th = threading.Thread(target = handle_client, daemon = True, args = (new_sock, host_ip, host_port))
            th.start()
    except:
        sock.close()
if __name__ == '__main__':
    proxy()

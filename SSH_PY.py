import paramiko, sys, threading, time

def output_def(shell_arg):
    try:
        while True:
            data = shell_arg.recv(4096)
            if not data:
                break
            sys.stdout.write(data.decode('utf-8', errors='ignore'))
            sys.stdout.flush()
    except Exception:
        pass
            
def ssh_client(target, port, usr, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(target, port=port, username=usr, password=passwd)
        shell = client.invoke_shell()
        print("[*] Шелл создан. Введите 'exit' для выхода")
        
        potok = threading.Thread(target=output_def, daemon=True, args=(shell,))
        # 2. ЗАПУСКАЕМ его!
        potok.start() 
        
        while True:
            cmd = input("")
            if cmd.lower() == 'exit':
                return
            shell.send(cmd + '\n')
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error msg: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    ssh_client("192.168.1.4", 22, "user", "password", "")

import socket
import threading

HOST = '127.0.0.1'    
PORT = 6924

trechos_disponiveis = {
    "Belém > Fortaleza": 10,
    "Fortaleza > São Paulo": 15,
    "São Paulo > Curitiba": 5
}

user_in = input('Insira o endereço IP ou pressione Enter:\n')
if user_in != '':
    HOST = user_in

user_in = input('Insira a porta de conexão com o servidor ou pressione ENTER\n')
if user_in != '':
    PORT = int(user_in)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

origem = (HOST, PORT)
tcp.bind(origem)
tcp.listen(1)

print("Servidor iniciado. Para encerrar, digite 'exit'.")


def handle_client(con, cliente):
    print(f'Conectado a: {cliente}')
    try:
        while True: 
            info = con.recv(1024).decode('utf-8')
            if not info:
                break
            if info == 'exit':
                print("Comando de encerramento recebido. Encerrando a conexão com o cliente...")
                con.sendall(str.encode('Conexão encerrada pelo cliente.'))
                break  
            if info in trechos_disponiveis and trechos_disponiveis[info] >= 1:
                    con.sendall(str.encode('True'))
                    resp = con.recv(1024).decode('utf-8')
                    if resp == 'S':
                        trechos_disponiveis[info] -= 1
                        con.sendall(str.encode('True'))
                    else:
                        con.sendall(str.encode('False'))
            else:
                con.sendall(str.encode('False'))
                print(f'Trecho {info} indisponível\n')

            print(f'{cliente} enviou a informação: {info}')
    except Exception as e:
        print(f'Erro com {cliente}: {e}')
    finally:
        print(f'Conexão com {cliente} encerrada')
        con.close()

while True:
    con, cliente = tcp.accept()
    client_thread = threading.Thread(target=handle_client, args=(con, cliente))
    client_thread.start()
    

    

import socket
import threading
import json

with open('rotas_voos_brasil.json', 'r') as json_file:
    trechos_disponiveis = json.load(json_file)

def get_server_info():
    """Solicita ao usuário o IP e a porta do servidor."""
    host = input('Insira o endereço IP ou pressione Enter para usar o padrão (127.0.0.1):\n') or '127.0.0.1'
    port = input('Insira a porta de conexão com o servidor ou pressione Enter para usar o padrão (6924):\n') or 6924
    return host, int(port)

def start_server(host, port):
    #Inicializa o servidor e começa a escutar conexões.
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind((host, port))
    tcp.listen(1)
    print(f"Servidor iniciado no IP {host} e porta {port}. Para encerrar, digite 'exit'.")
    return tcp

def handle_client(con, cliente):
    #Função para lidar com a comunicação com o cliente.
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

            if process_request(con, info):
                con.sendall(str.encode('True'))
            else:
                con.sendall(str.encode('False'))
                print(f'Trecho {info} indisponível\n')

            print(f'{cliente} enviou a informação: {info}')
    except Exception as e:
        print(f'Erro com {cliente}: {e}')
    finally:
        print(f'Conexão com {cliente} encerrada')
        con.close()

def process_request(con, info):
    #Processa a solicitação do cliente, verifica e atualiza a disponibilidade dos trechos.
    if info in trechos_disponiveis and trechos_disponiveis[info] >= 1:
        con.sendall(str.encode('True'))
        resp = con.recv(1024).decode('utf-8')
        if resp == 'S':
            
            trechos_disponiveis[info] -= 1

            with open('rotas_voos_brasil.json', 'w') as json_file:
                json.dump(trechos_disponiveis, json_file)
            return True
        else:
            return False
    return False

def accept_connections(tcp):
    #Aceita conexões de clientes e cria uma nova thread para cada um.
    while True:
        con, cliente = tcp.accept()
        client_thread = threading.Thread(target=handle_client, args=(con, cliente))
        client_thread.start()

def main():
    # Função principal que coordena a execução do servidor
    host, port = get_server_info()
    tcp = start_server(host, port)
    accept_connections(tcp)

if __name__ == '__main__':
    main()

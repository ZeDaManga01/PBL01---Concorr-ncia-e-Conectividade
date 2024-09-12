import socket

def get_server_info():
    """Solicita ao usuário o IP e a porta do servidor."""
    host = input('Insira o endereço IP ou pressione Enter para usar o padrão (127.0.0.1):\n') or '127.0.0.1'
    port = input('Insira a porta de conexão com o servidor ou pressione Enter para usar o padrão (6924):\n') or 6924
    return host, int(port)

def connect_to_server(host, port):
    """Conecta ao servidor TCP com o endereço fornecido."""
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (host, port)
    tcp.connect(server)
    print(f"Conectado ao servidor {host}:{port}. Pressione Ctrl+X para sair.")
    return tcp

def send_request(tcp, info):
    """Envia uma solicitação ao servidor e recebe a resposta."""
    tcp.sendall(str.encode(info))
    return tcp.recv(1024).decode('utf-8')

def process_purchase(tcp):
    """Gerencia o processo de compra do trecho."""
    resp = input('Trecho disponível!\n\nDeseja Comprar?\nS ou N\n')
    tcp.sendall(str.encode(resp))
    compra_resultado = tcp.recv(1024).decode('utf-8')
    
    if compra_resultado == 'True':
        print('Compra realizada\n')
    else:
        print('Compra não realizada\n')

def handle_interaction(tcp):
    """Loop principal de interação com o servidor."""
    info = "a"
    
    while info != '\x18':  # Ctrl+X para sair
        info = input('Informe o trecho do voo\n')
        if info == 'exit':
            print('Conexão com o servidor encerrada')
            tcp.close()
            break
        
        disp_info = send_request(tcp, info)

        if disp_info == 'True':
            process_purchase(tcp)
        else:
            print('Trecho indisponível\n')

def main():
    """Função principal que orquestra a execução do cliente."""
    host, port = get_server_info()
    tcp = connect_to_server(host, port)
    handle_interaction(tcp)
    tcp.close()

if __name__ == '__main__':
    main()

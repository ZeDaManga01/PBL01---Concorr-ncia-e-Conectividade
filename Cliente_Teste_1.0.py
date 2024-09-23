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


def process_purchase(tcp):
    """Gerencia o processo de compra do trecho."""
    resp = input('Trecho disponível!\n\nDeseja Comprar? (S/N)\n')
    print(f'log:{resp}')
    tcp.sendall(str.encode(resp))
    try:
        compra_resultado = tcp.recv(1024).decode('utf-8')
    except Exception as e:
            print(f'Erro ao processar a solicitação: {e}')
    finally:
        print('Deu')
    
    if compra_resultado == 'True':
        print('Compra realizada com sucesso!')
    elif compra_resultado == 'False':
        print('Compra não realizada.')
    else:
        print('Resposta do servidor não esperada.')

def handle_interaction(tcp):
    """Loop principal de interação com o servidor."""
    while True:
        info = input('Informe o trecho do voo no formato Origem>Destino\n')
        if info == 'exit':
            tcp.sendall(str.encode(info))
            print('Conexão com o servidor encerrada')
            tcp.close()
            break
        
        tcp.sendall(str.encode(info))
        resposta = tcp.recv(1024).decode('utf-8')

        if resposta == 'True':
            process_purchase(tcp)
        elif resposta == 'Trecho indisponível ou vagas esgotadas.\n':
            print('Trecho indisponível ou vagas esgotadas.')
        else:
            print('Resposta do servidor não esperada.')

def main():
    """Função principal que orquestra a execução do cliente."""
    host, port = get_server_info()
    tcp = connect_to_server(host, port)
    handle_interaction(tcp)
    tcp.close()

if __name__ == '__main__':
    main()

import socket
import threading
import json
from queue import Queue


mutex = threading.Lock()

fila_tarefas = Queue()

def login(id,senha):

    try:
        with open('usuários.json', 'r') as json_file:
            lista_de_usuarios = json.load(json_file)    

        for user in lista_de_usuarios:
            if id == user['ID'] and senha == user['Senha']:
                print(f'Usuário {id} conectou-se ao servidor com sucessor')
                return user
            else:
                print('ID ou senha incorretos')
                return False
            
    except FileNotFoundError:
        print("Arquivo usuarios.json não encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False


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
    tcp.listen(3)
    print(f"Servidor iniciado no IP {host} e porta {port}. Para encerrar, digite 'exit'.")
    return tcp

def handle_client(con, cliente):
    #Função para lidar com a comunicação com o cliente.
    print(f'Conectado a: {cliente}')
    try:
        while True:
            info = con.recv(1024).decode('utf-8')#Recebe a info do client
            if not info:#Se não tem é interrompido 
                break
            if info == 'exit': #Encerra se o cliente solicitar
                print("Comando de encerramento recebido. Encerrando a conexão com o cliente...")
                break

            fila_tarefas.put((con, info))

            print(f'{cliente} enviou a informação: {info}')
    except Exception as e:
        print(f'Erro com {cliente}: {e}')
    finally:
        print(f'Conexão com {cliente} encerrada')
        con.close()

def formata_info(info):
    info = info.lower()
    origem,destino = info.split('>')
    origem = origem.strip()
    destino = destino.strip()

    return origem, destino

def accept_connections(tcp):

    #Aceita conexões de clientes e cria uma nova thread para cada um.
    while True:
        con, cliente = tcp.accept()
        client_thread = threading.Thread(target=handle_client, args=(con, cliente))
        client_thread.start()

def atualiza_trechos(trecho):
    with mutex:
        with open('Trechos.json', 'r') as json_file:
            trechos_disponiveis = json.load(json_file)

        # Atualiza o trecho com menos uma vaga
        for t in trechos_disponiveis:
            if t['Origem'] == trecho['Origem'] and t['Destino'] == trecho['Destino']:
                t['Vagas'] -= 1
                break

        # Salva o arquivo atualizado
        with open('Trechos.json', 'w') as json_file:
            json.dump(trechos_disponiveis, json_file, ensure_ascii=False, indent=4)

def process_request(info): #Processa a solicitação do cliente, verifica e atualiza a disponibilidade dos trechos.

    #Formatando a infomação enviada pelo client
    origem,destino = formata_info(info)

    # Protege o acesso ao arquivo com mutex
    with mutex:
        with open('Trechos.json', 'r') as json_file:
            trechos_disponiveis = json.load(json_file)

        for trecho in trechos_disponiveis:
            if origem == trecho['Origem'] and destino == trecho['Destino']:
                if trecho['Vagas'] > 0:
                    return True  # Trecho disponível  
                else:
                    return False  # Vagas esgotadas
    return False  # Trecho não encontrado

def thread_fila():
    while True:
        con, info = fila_tarefas.get()
        try:
            disponivel = process_request(info)
            if disponivel:
                con.sendall(str.encode('True'))
                print('chegou')
                resposta = con.recv(1024).decode('utf-8')
                print('Chegou2')
                if resposta == 'S':
                    atualiza_trechos(formata_info(info))
                    con.sendall(str.encode('True'))
                else:
                    con.sendall(str.encode('False'))
            else:
                con.sendall(str.encode('Trecho indisponível ou vagas esgotadas.\n'))
        except Exception as e:
            print(f'Erro ao processar a solicitação: {e}')
        finally:
            fila_tarefas.task_done()
            con.close()        

def iniciar_threads_fila(num_thread_fila=3):
  for i in range(num_thread_fila):
        thread = threading.Thread(target=thread_fila, daemon=True)
        thread.start()

def main():

    # Função principal que coordena a execução do servidor
    host, port = get_server_info()
    tcp = start_server(host, port)
    iniciar_threads_fila(num_thread_fila=3)
    accept_connections(tcp)

if __name__ == '__main__':
    main()
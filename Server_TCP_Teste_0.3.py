import socket

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

try:
    while True:
        con, cliente = tcp.accept()
        print(f'Conectado a: {cliente}')
        while True: 
            try:
                info = con.recv(1024).decode('utf-8')
                if not info:
                    break
                
                if info == 'exit':  
                    print("Comando de encerramento recebido. Encerrando o servidor...")
                    con.sendall(str.encode('Servidor encerrando...'))
                    con.close()
                    tcp.close()
                    exit(0)  

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
            
            except ConnectionResetError:
                print(f'Conexão com {cliente} foi resetada inesperadamente')
                break
            except OSError as e:
                print(f'Erro de conexão: {e}')
                break
            except Exception as e:
                print(f'Erro inesperado: {e}')
                break

        print(f'Conexão com {cliente} encerrada\n')
        con.close()

except KeyboardInterrupt:
    print("\nServidor encerrado via interrupção do teclado.")
    tcp.close()

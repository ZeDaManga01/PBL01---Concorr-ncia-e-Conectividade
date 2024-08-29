import socket

HOST = '127.0.0.1'    
PORT = 6924

trechos_disponiveis = {
    "Belém > Fortaleza": 10,
    "Fortaleza > São Paulo": 15,
    "São Paulo > Curitiba": 5
}

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

user_in = input('Insira o endereço IP ou pressione Enter:\n')
if user_in != '':
    HOST = user_in

user_in = input('Insira a porta de conexão com o servidor ou pressione ENTER')
if user_in != '':
    PORT = int(user_in)

origem =  (HOST, PORT)  
tcp.bind(origem)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    print(f'Conectado á: {cliente}')
    while True: 
        info = con.recv(1024).decode('utf-8')
        if not info: break

        if info in trechos_disponiveis and trechos_disponiveis[info] >= 1:

            disponivel = 'S'
            tcp.sendall(str.encode(info))
            resp = con.recv(1024).decode('utf-8')
            if resp == 'S':
                trechos_disponiveis[info] -= 1
                compra_realizada = 'S'
                tcp.sendall(str.encode(compra_realizada))
            else:
                compra_realizada = 'N'
                tcp.sendall(str.encode(compra_realizada))

        
        else:
            print(f'Trecho {info} indisponivel\n')

        print(f'{cliente} enviou a informação: {info}')
    print(f'Conexão com {cliente} encerrada\n')
    con.close()

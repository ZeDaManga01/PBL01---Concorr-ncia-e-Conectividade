import socket

HOST = '127.0.0.1'    
PORT = 6924

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

user_in = input('Insira o endereço IP ou pressione Enter:\n')
if user_in != '':
    HOST = user_in

user_in = input('Insira a porta de conexão com o servidor ou pressione ENTER\n')
if user_in != '':
    PORT = int(user_in)

server =  (HOST, PORT)

tcp.connect(server)
print("Pressione Ctrl+X para sair\n")

info = input('Informe o trecho do voo\n')

while info != '\x18':

    tcp.sendall(str.encode(info))

    disp_info = tcp.recv(1024).decode('utf-8')

    if disp_info == 'S':
        resp = input('Trecho disponivel!\n\nDeseja Comprar?\nS ou N')
        tcp.sendall(str.encode(resp))
        compra_resultado = tcp.recv(1024).decode('utf-8')
        if compra_resultado == 'S':
            print('Compra realizada\n')
        else:
            print('Compra não realizada')
        
    info = input('Informe o trecho do voo\n')


tcp.close()


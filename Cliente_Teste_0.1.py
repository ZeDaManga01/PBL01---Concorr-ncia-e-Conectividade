import socket

HOST = '127.0.0.1'    
PORT = 6924

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

user_in = input('Insira o endereço IP ou pressione Enter:\n')
if user_in != '':
    HOST = user_in

user_in = input('Insira a porta de conexão com o servidor ou pressione ENTER')
if user_in != '':
    PORT = int(user_in)

server =  (HOST, PORT)

tcp.connect(server)
print("Pressione Ctrl+X para sair\n")

info = input('Informação para ser enviada\n')

while info != '\x18':
    tcp.send(str.encode(info))

    info = input('Informação para ser enviada\n')
tcp.close()


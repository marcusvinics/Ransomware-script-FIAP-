#cliente
from base64 import decode
import base64
from socket import *
from Crypto.Cipher import AES

servidor = "127.0.0.1"
porta = 54338
tmp = 0
chave = "FIAP2021FIAP2021"
alg = AES.new(chave, AES.MODE_ECB)

conexao = socket(AF_INET, SOCK_STREAM)
conexao.connect((servidor, porta))

def menu():
    resp = "SIM"
    while resp == "SIM":
        opcao = int(input("\nCENTRO DE COMANDO\n"
        +"\nEntre 1 para Receber arquivos do computador remoto: "
        +"\nEntre 2 para Enviar arquivos para o computador remoto: "
        +"\nEntre 3 para Executar comandos no computador remoto: "
        +"\nEntre 5 para Sair\n" ))

        if opcao == 1:
            enviaMensagem(opcao)
            recebeArquivo()
        elif opcao == 2:
            enviaMensagem(opcao)
            enviaArquivo()
        elif opcao == 3:
            enviaMensagem(opcao)            
            executaComando()
        elif opcao == 5:
            print("Até Logo")
            enviaMensagem(opcao)
            break
        else:
            print("Opcao inválida, tente novamente\n")

def enviaMensagem(opcao):
    global tmp
    global alg
    #Enviando
    data = str(opcao)
    print("Opcao a ser enviada: ", data)
    while len(data)%16 != 0:
        data = data + " "
        tmp = tmp + 1
    data_encriptado = alg.encrypt(data)
    msg_enviada = bytes(data_encriptado)   
    conexao.send(msg_enviada)
    #print("msg enviada criptografada: ", msg_enviada)

def recebeArquivo():
    global tmp
    global alg
    resp = "S"
    while resp == "S":
        #Enviando
        data = input("Nome do arquivo a receber: ")

        while len(data)%16 != 0:
            data = data + " "
            tmp = tmp + 1

        data_encriptado = alg.encrypt(data)
        msg_enviada = bytes(data_encriptado)
        conexao.send(msg_enviada)

        #Receber
        resposta = conexao.recv(10240)
        data_decriptado = alg.decrypt(resposta)
        data_string = str(data_decriptado)[2:-1]
        data_final = str(data_decriptado.rstrip(), "utf-8")
        restore_data_binario = base64.b64decode(data_final)
        print("teste:", restore_data_binario)

        #with open("dados.txt", "wb") as fig: #Original
        with open(data, "wb") as fig:
            fig.write(restore_data_binario)

        print("Dados Recebidos: ", data_final.rstrip())
        #resp = input("Digite S para continuar e N para terminar: ")
        resp = "N"

def enviaArquivo():
    global tmp
    global alg
    resp = "S"
    while resp == "S":
        data = input("Nome do arquivo a enviar: ")

        #while len(data)%16 != 0:
        #    data = data + " "
        #    tmp = tmp + 1

        with open(data, "rb+") as arquivo:
                binary_data = arquivo.read()
                base64_data = base64.b64encode(binary_data)
                data = base64_data.decode("utf-8")
        while len(data)%16 != 0:
            data = data + " "
        print(data)        
        data_encriptado = alg.encrypt(data)
        msg_enviada = bytes(data_encriptado)
        conexao.send(msg_enviada)
        resp = "N"

def executaComando():
    global tmp
    global alg
    resp = "S"
    while resp == "S":
        #Enviando
        data = input("Entre com o comando: ")
        while len(data)%16 != 0:
            data = data + " "
            tmp = tmp + 1
        data_encriptado = alg.encrypt(data)
        msg_enviada = bytes(data_encriptado)   
        conexao.send(msg_enviada)
        #Receber
        resposta = conexao.recv(1024)
        data_decriptado = alg.decrypt(resposta)
        data_string = str(data_decriptado)[2:-1]
        data1=data_decriptado.rstrip()
        data2 = str(data1, "utf-8")
        print(data2)
        #resp = input("Digite S para continuar e N para terminar: ")
        resp = "N"

menu()
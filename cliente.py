#Aluno: Alan Walace Silva Corrêa // Matrícula: 201604940022
import socket
import pickle

#Configurações do cliente
HOST = '127.0.0.1'
PORT = 64825
PROTOCOL = socket.SOCK_STREAM  # Use socket.SOCK_DGRAM para UDP

#Funções para chamar o procedimento remoto
def chamar_procedimento_remoto(operacao, a, b):
    #Criação de um socket do cliente
    with socket.socket(socket.AF_INET, PROTOCOL) as cliente_socket:
        cliente_socket.connect((HOST, PORT))

        #Prepara a solicitação em forma de dicionário
        solicita = {'funcao': operacao, 'a': a, 'b': b}

        #Serializa a solicitação usando pickle e envia para o servidor
        cliente_socket.sendall(pickle.dumps(solicita))

        #Recebe a resposta do servidor
        resposta_servidor = pickle.loads(cliente_socket.recv(1024))

        return resposta_servidor

#Menu de operações disponíveis
print('Operações disponíveis:')
print('1. Soma')
print('2. Subtração')
print('3. Multiplicação')
print('4. Divisão')

#Solicita ao usuário a escolha da operação
opcao = int(input('Escolha a operação: '))

#Mapeia a escolha para a operação
if opcao == 1:
    operacao = 'soma'
elif opcao == 2:
    operacao = 'subtracao'
elif opcao == 3:
    operacao = 'multiplicacao'
elif opcao == 4:
    operacao = 'divisao'
else:
    print('Opção inválida.')
    exit()

#Solicita ao usuário os operandos
a = float(input('Digite o primeiro número: '))
b = float(input('Digite o segundo número: '))

#Chamada do procedimento remoto com a operação selecionada
resultado = chamar_procedimento_remoto(operacao, a, b)
print(f'Resultado da operação: {resultado}')

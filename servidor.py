#Aluno: Alan Walace Silva Corrêa // Matrícula: 201604940022
import socket
import pickle

#Funções que serão chamadas remotamente
def somar(a, b):
    resultado = a + b 
    return f'A soma de {a} e {b} é {resultado}'

def subtrair(a, b):
    resultado = a - b
    return f'A subtração de {a} por {b} é {resultado}'

def multiplicar(a, b):
    resultado = a * b
    return f'A multiplicação de {a} por {b} é {resultado}'

def dividir(a, b):
    if b == 0:
        return 'Erro: Divisão por zero.'
    resultado = a / b
    return f'A divisão de {a} por {b} é {resultado}'

#Configurações do servidor
HOST = '127.0.0.1'
PORT = 64825
PROTOCOL = socket.SOCK_STREAM  # Use socket.SOCK_DGRAM para UDP

#Dicionário de funções disponíveis
funcoes_disponiveis = {
    'soma': somar,
    'subtracao': subtrair,
    'multiplicacao': multiplicar,
    'divisao': dividir,
}

#Criação de um socket do servidor
with socket.socket(socket.AF_INET, PROTOCOL) as servidor_socket:
    servidor_socket.bind((HOST, PORT))
    servidor_socket.listen()

    print(f'Servidor RPC está em execução --> {HOST}:{PORT}')

    while True:
        #Aguarda uma conexão
        conexao, endereco = servidor_socket.accept()
        with conexao:
            print(f'Conexão estabelecida com {endereco}\nE resposta enviada!')

            while True:
                try:
                    #Recebe a mensagem do cliente
                    data = conexao.recv(1024)
                    if not data:
                        break

                    #Desserializa a mensagem usando pickle
                    solicita = pickle.loads(data)

                    #Verifica se a função solicitada está disponível
                    if solicita['funcao'] not in funcoes_disponiveis:
                        conexao.sendall(pickle.dumps('Erro: Função não encontrada.'))
                        continue

                    #Chamada de função correspondente e obtém o resultado
                    resultado = funcoes_disponiveis[solicita['funcao']](solicita['a'], solicita['b'])

                    #Envia o resultado de volta para o cliente
                    conexao.sendall(pickle.dumps(resultado))
                except Exception as e:
                    print(f'Erro durante a execução do procedimento remoto: {str(e)}')
                    break

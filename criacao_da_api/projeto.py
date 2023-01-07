# Construir a API ---> Flask
from flask import Flask, request
# Lib para Datas
from datetime import datetime
# Lib para carregar o modelo
import joblib
# Lib para o banco sql
import sqlite3

# Instanciar o aplicativo
Aplicativo = Flask(__name__)

#---------------------- CARREGAMENTO DO MODELO --------------------------
# Carregar modelo
Modelo = joblib.load('/home/wanderson/Projetos/machine_learning_solucao_completa_end_to_end/criacao_da_api/Modelo_RandomForest_v1.pkl')

#---------------------- FUNÇÃO DA API --------------------------
# Função para receber nossa API
@Aplicativo.route('/API_Preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def Funcao_01( area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax ):

    Data_Inicio = datetime.now()

    # Recebendo os inputs da API
    Lista = [
        float(area), float(rooms), float(bathroom), float(parking_spaces), float(floor), float(animal), float(furniture), float(hoa), float(property_tax)
    ]
    
    # Tentativa de previsão
    try:
        
        # Predict
        Previsao = Modelo.predict( [Lista] )

        # Inserir o valor da Previsão
        Lista.append( str(Previsao) )

        # Concatenando a Lista
        Input = ''
        for Valor in Lista:
            Input = Input + ';' + str(Valor)

        # Termino do processo
        Data_Fim = datetime.now()
        Processamento = Data_Fim - Data_Inicio

        #---------------------- CONEXÃO BANCO DE DADOS --------------------------
        # Criar a conexão com o banco de dados: 
        Conexao_Banco = sqlite3.connect('/home/wanderson/Projetos/machine_learning_solucao_completa_end_to_end/criacao_da_api/Banco_Dados_API.db')
        Cursor = Conexao_Banco.cursor()

        # Query
        Query_Inserindo_Dados = f''' 
            INSERT INTO log_api ( inputs, incio, fim, processamento )
            VALUES ( '{ str(Input) }', '{Data_Inicio}' , '{Data_Fim}', '{Processamento}' )
        '''
        # Executar a Query
        Cursor.execute( Query_Inserindo_Dados )
        Conexao_Banco.commit()

        # Fechar a conexão com o banco de dados
        Cursor.close()

        # Retorno do Modelo
        return {'Valor_Aluguel': str(Previsao)}
    
    except:
        return {'Aviso': 'Deu algum erro!'}

if __name__ == '__main__':
    Aplicativo.run( debug=True )

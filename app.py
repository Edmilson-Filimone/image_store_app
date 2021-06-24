import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image


def encode_f(filer):
    try:
        with open(file=filer, mode='rb') as file:
            ficheiro = file.read()
        return ficheiro
    except Exception as error:
        print(error.args)
    finally:
        file.close()


def inserir(nome, titulo, data, ficheiro, imagem_1, imagem_2):
    """Cria a tabela se nao existir e inseri os dados passados pelo
    usuario atraves dos seus parametros"""

    try:
        conexao = sqlite3.connect('Documents\BASE.db')
        cursor = conexao.cursor()
        create = "CREATE TABLE IF NOT EXISTS One " \
                 "(nome text,titulo text," \
                 "data date,ficheiro blob,imagem_1 blob," \
                 "imagem_2 blob)"

        insert = "INSERT INTO One VALUES (?,?,?,?,?,?)"
        cursor.execute(create)
        cursor.execute(insert, (nome, titulo, data, ficheiro, imagem_1, imagem_2))
        conexao.commit()
    except Exception as erro:
        print(erro)
        print('o bife esta aqui')
    finally:
        conexao.close()


def selet_box():
    """Funcao que extrai dados das tres colunas da base de dados
     usadas como como criterio de pesquisa para a select_box, retorna
     uma lista de listas [[],[],...] composta por elementos de cada coluna"""

    try:
        conexao = sqlite3.connect('Documents\BASE.db')
        cursor = conexao.cursor()
        select = "SELECT * FROM One"
        cursor.execute(select)
        retorno = cursor.fetchall()
        print(retorno)
        nome_lista = []
        titulo_lista = []
        data_lista = []

        for tupla in retorno:
            nome_lista.append(tupla[0])  # guardando os dados da coluna nome na lista
            titulo_lista.append(tupla[1])  # guardando os dados da coluna titulo na lista
            data_lista.append(tupla[2])  # guardando os dados da coluna data na lista
            print(nome_lista, '\n', titulo_lista, '\n', data_lista)
        select_box_lista = [nome_lista, titulo_lista, data_lista]
        return select_box_lista
    except:
        print('ERRO_NA_QUERY')
    finally:
        conexao.close()



documento = ''


def query(nome, titulo, data):
    try:
        global documento
        conexao = sqlite3.connect('Documents\BASE.db')
        cursor = conexao.cursor()
        select = "SELECT ficheiro FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome,titulo, data))
        retorno = cursor.fetchall()
        print(retorno)

        # Para o documento
        for tupla in retorno:
           documento = tupla[0]

        with open('page_1.csv', 'wb') as file_1:
            done = file_1.write(documento)
            print(f'Documento decode_output: {done}')
            file_1.close()

        df = pd.read_csv('page_1.csv')
        st.header('Condicoes e componetes da PCR')
        st.dataframe(df)
    except:
        pass
    finally:
        conexao.close()


img_1 = ''


def query_2(nome, titulo, data):
    global img_1
    try:
        conexao = sqlite3.connect('Documents\BASE.db')
        cursor = conexao.cursor()
        select = "SELECT imagem_1 FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()
        #print(retorno)

        # Para a imagem 1
        for tupla in retorno:
            img_1 = tupla[0]

        with open('i1.jpg', 'wb') as file_2:
            image_1 = file_2.write(img_1)
            print(f'Imagem_1 decode_output: {image_1}')
            file_2.close()
        pil = Image.open('i1.jpg')
        st.header('Vizualizacao do Gel')
        st.write('')
        st.image(pil)
    except:
        pass
    finally:
        conexao.close()



img_2 = ''


def query_3(nome, titulo, data):
    global img_2
    try:
        conexao = sqlite3.connect('Documents\BASE.db')
        cursor = conexao.cursor()
        select = "SELECT imagem_2 FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()
        #print(retorno)

        # Para a imagem 2
        for tupla in retorno:
            img_2 = tupla[0]

        with open('image_2.jpg', 'wb') as file_3:
            image_2 = file_3.write(img_2)
            print(f'Imagem_2 decode_output: {image_2}')
            file_3.close()
        pil = Image.open('image_2.jpg')
        st.write('')
        st.image(pil)
    except:
        pass
    finally:
        conexao.close()

@st.cache
def jpg():
    try:
        with open('pic.jpg', 'rb') as pic:
            imagem = pic.read()
        return imagem
    except:
        pass

# Programa

# Main Window
st.title("RESULTADOS DA PCR")
#st.image(image=jpg())
txt = st.subheader('---------------[ Selecione uma das opcoes no Menu ]------------------')

# Sidebar-dados
dados = st.sidebar.checkbox('Inserir novos dados')

if dados:
    input_nome = st.sidebar.text_input(label='Nome')
    input_titulo = st.sidebar.text_input(label='Titulo')
    input_data = st.sidebar.date_input(label='Data')
    input_doc = st.sidebar.text_input('Caminho da documento')
    input_pic_1 = st.sidebar.text_input('Caminho da imagem 1')
    input_pic_2 = st.sidebar.text_input('Caminho da imagem 2')
    esquerda, direita = st.sidebar.beta_columns(2)
    submeter = esquerda.button('Submeter')
    apgar = direita.button('Limpar')

    if submeter:
        doc = encode_f(str(input_doc))
        pic_1 = encode_f(str(input_pic_1))
        pic_2 = encode_f(str(input_pic_2))

        inserir(nome=input_nome, titulo=input_titulo, data=input_data,
                ficheiro=doc, imagem_1=pic_1, imagem_2=pic_2)

    if apgar:
        pass


# Sidebar-Pesquisa
pesquisa = st.sidebar.checkbox('Pesquisar')

if pesquisa:
    sb_nome = st.sidebar.selectbox('Nome', selet_box()[0])
    sb_titulo = st.sidebar.selectbox('Titulo', selet_box()[1])
    sb_data = st.sidebar.selectbox('Data', selet_box()[2])
    ok_pesquisa = st.sidebar.button('Buscar')
    txt.text('---------->[ Modo pesquisa activado...Em breve teras os resultados :) ]<----------')
    if ok_pesquisa:
        query(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        query_2(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        query_3(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        txt.text('-------- Veja os resultados abaixo, caso nada apareca, entao nao ha nenhuma informacao disponivel --------')
#conda activate I:\Biotech-School\Web_Dev\web\envs\one
#streamlit run I:\Biotech-School\Web_Dev\Gestor.py

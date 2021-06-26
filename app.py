import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image


def encode_f(file):
    global fiche
    try:
        if file is not None:
            fiche = file.getvalue()
        return fiche
    except Exception as error:
        print(error)


def inserir(nome, titulo, data, ficheiro, imagem_1, imagem_2):
    """Cria a tabela se nao existir e inseri os dados passados pelo
    usuario atraves dos seus parametros"""

    global conexao
    try:
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        create = "CREATE TABLE IF NOT EXISTS One " \
                 "(nome text,titulo text," \
                 "data date,ficheiro blob,imagem_1 blob," \
                 "imagem_2 blob)"

        insert = "INSERT INTO One VALUES (?,?,?,?,?,?)"
        cursor.execute(create)
        cursor.execute(insert, (nome, titulo, data, ficheiro, imagem_1, imagem_2))
        conexao.commit()
        conexao.close()
    except Exception as erro:
        print(erro)


def selet_box():
    """Funcao que extrai dados das tres colunas da base de dados
     usadas como como criterio de pesquisa para a select_box, retorna
     uma lista de listas [[],[],...] composta por elementos de cada coluna"""

    global conexao
    try:
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        select = "SELECT * FROM One"
        cursor.execute(select)
        retorno = cursor.fetchall()
        conexao.close()
        nome_lista = []
        titulo_lista = []
        data_lista = []


        for tupla in retorno:
            nome_lista.append(tupla[0])  # guardando os dados da coluna nome na lista
            titulo_lista.append(tupla[1])  # guardando os dados da coluna titulo na lista
            data_lista.append(tupla[2])  # guardando os dados da coluna data na lista

        select_box_lista = [nome_lista, titulo_lista, data_lista]
        return select_box_lista
    except:
        print('ERRO_NA_QUERY')


def query(nome, titulo, data):
    try:
        global documento, conexao
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        select = "SELECT ficheiro FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()

        # Para o documento
        for tupla in retorno:
            documento = tupla[0]

        with open('page.csv', 'wb') as file_1:
            file_1.write(documento)
            file_1.close()
        df = pd.read_csv('page.csv')
        st.header('Condições e Componetes da PCR')
        st.dataframe(df)
        conexao.close()
        return documento
    except:
        pass


def non_query(nome, titulo, data):
    try:
        global conexao
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        select = "SELECT * FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()
        non = []
        # Para o documento
        for tupla in retorno:
            non.append(tupla[3])
            non.append(tupla[4])
            non.append(tupla[5])
            return non
    except:
        print('error_no_non_query')


def query_2(nome, titulo, data):
    global img_1, conexao
    try:
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        select = "SELECT imagem_1 FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()
        conexao.close()

        # Para a imagem 1
        for tupla in retorno:
            img_1 = tupla[0]

        with open('file1.jpg', 'wb') as file_2:
            file_2.write(img_1)
            file_2.close()
        pil = Image.open('file1.jpg')
        st.header('Imagens do Gel')
        st.write('')
        st.image(pil)
    except:
        pass


def query_3(nome, titulo, data):
    global img_2, conexao
    try:
        conexao = sqlite3.connect('BASE.db')
        cursor = conexao.cursor()
        select = "SELECT imagem_2 FROM One WHERE nome == (?) AND titulo == (?) AND data = (?)"
        cursor.execute(select, (nome, titulo, data))
        retorno = cursor.fetchall()
        conexao.close()

        # Para a imagem 2
        for tupla in retorno:
            img_2 = tupla[0]

        with open('file2.jpg', 'wb') as file_3:
            file_3.write(img_2)
            file_3.close()
        pil = Image.open('file2.jpg')
        st.write('')
        st.image(pil)
    except:
        pass


# Programa

# Main Window
st.title("GESTOR   DOS   DADOS   DA   PCR")
txt = st.markdown('**----------------------[ Selecione uma das opções do Menu ]----------------------**')

# Sidebar-dados
st.sidebar.title('Menu')
dados = st.sidebar.checkbox('Inserir novos dados')

if dados:
    txt.markdown('**-------------->[ Modo registrar activado...introduza os dados :) ]<--------------**')
    input_nome = st.sidebar.text_input(label='Nome')
    input_titulo = st.sidebar.text_input(label='Titulo')
    input_data = st.sidebar.date_input(label='Data')
    input_doc = st.sidebar.file_uploader('Carregar arquivo', 'csv')
    input_pic_1 = st.sidebar.file_uploader('Carregar imagem 1', 'jpg')
    input_pic_2 = st.sidebar.file_uploader('Carregar imagem 2', 'jpg')
    esquerda, direita = st.sidebar.beta_columns(2)
    submeter = esquerda.button('Guardar')
    apgar = direita.empty()

    if submeter:
        inserir(nome=input_nome, titulo=input_titulo, data=input_data,
                ficheiro=encode_f(input_doc), imagem_1=encode_f(input_pic_1),
                imagem_2=encode_f(input_pic_2))
        st.success('Dados salvos com sucesso')

    if apgar:
        pass

# Sidebar-Pesquisa
pesquisa = st.sidebar.checkbox('Pesquisar')

if pesquisa:
    sb_nome = st.sidebar.selectbox('Nome', selet_box()[0])
    sb_titulo = st.sidebar.selectbox('Titulo', selet_box()[1])
    sb_data = st.sidebar.selectbox('Data', selet_box()[2])
    ok_pesquisa = st.sidebar.button('Buscar')
    txt.markdown('**-------->[ Modo pesquisa activado...Em breve os seus resultados :) ]<---------**')
    if ok_pesquisa:
        query(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        query_2(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        query_3(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data))
        txt.markdown('**------------------------------- Veja os resultados abaixo ---------------------------**')

        if non_query(nome=str(sb_nome), titulo=str(sb_titulo), data=str(sb_data)) is None:
            st.error('Ups! seus dados não foram encontrados, veja se selecionou o nome,'
                     ' o título e a data exata que usou ao inserir os ficheiros e tente de novo.  ')

#Sidebar_info
info = st.sidebar.checkbox('Sobre')
if info:
    st.sidebar.markdown("""*"Olá, esta é uma web app (amadora),
desenvolvida de forma a auxiliar
a comunidade de investigadores 
no seu dia a dia através de um 
projecto simples e prático. 
Obrigado por ler e um até breve :)"*
                    
Edmilson Filimone
philimone99@gmail.com

26 de Junho de 2021""")

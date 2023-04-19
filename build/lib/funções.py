#################################################IMPORTAÇÕES##########################################################
print('olá mundo!')
from barcode import EAN13
from  barcode.writer import ImageWriter
from datetime import datetime
from datetime import date,timedelta
import reportlab
import PyQt5
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib import colors
import webbrowser
import os
from random import randint
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import sqlite3
from time import sleep
from num2words import num2words
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
import requests
import json
#import auto_py_to_exe
import sys
##################################################TELA DE LOGIN#########################################################


def chama_menu_principal():  ##FUNÇÃO PARA VALIDAR LOGIN COMO ADMINISTRADOR
    try:
        nome = login.txt_usuario.text()
        senha = login.txt_senha.text()
        if nome == 'administrador' and senha == '5760':
            login.close()
            menu.show()
            menu.frm01_permissao.show()
            hoje = date.today()
            data = hoje.strftime('%d/%m/%Y')
            menu.lbl03_data.setText(f'{data}')
            menu.lbl01_admin.setText('ADMINISTRADOR')
            menu.lbl_abre_caixa.setText('CAIXA FECHADO')

        if nome == "" or senha == "":
            QMessageBox.about(login, 'Alerta','Usuário ou senha não pode ficar vazio!')
        elif nome != 'administrador' or senha != '5760':
            QMessageBox.about(login, 'Alerta', 'Usuário ou senha incorreto!')
    except:
        QMessageBox.about(login, 'Alerta','Erro ao validar os dados, tente novamente!')


def login_usuario():   ## FUNÇÃO PARA VALIDAR LOGIN COMO USUÁRIO
    try:
        nome = str(login.txt_usuario.text().strip())
        senha = login.txt_senha.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT nome FROM tab_usuarios WHERE senha = {senha}');
        nome_bd = cursor.fetchall()
        nome_bd = (nome_bd[0][0])
        banco.close()
        if nome == nome_bd:
            login.close()
            menu.show()
            menu.frm01_permissao.close()
            hoje = date.today()
            data = hoje.strftime('%d/%m/%Y')
            menu.lbl03_data.setText(f'{data}')
            menu.lbl01_usuario.setText(f'{nome_bd}')
            menu.lbl_abre_caixa.setText('CAIXA FECHADO')
            menu.txt_operador.setFocus()
        else:
            QMessageBox.about(login, 'Alerta','usuário ou senha incorreto!')
    except:
        QMessageBox.about(login, 'Alerta','erro ao validar os dados!')


################################################TELA DE CADSTRO DE USUÁRIO##############################################


def cadastrar_usuario():  ## FUNÇÃO PARA CADASTRAR URUÁRIO
    try:
        USUARIO = menu.txt01_usuario.text().strip()
        SENHA = menu.txt01_senha.text().strip()
        PRODUTO = 'N'
        CLIENTE = 'N'
        CONTAS = 'N'
        CAIXA = 'N'
        if USUARIO or SENHA != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f'INSERT INTO tab_usuarios VALUES{USUARIO,SENHA,PRODUTO,CLIENTE,CONTAS,CAIXA}');
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Usuário cadastrado com sucesso!')
            menu.txt01_usuario.setText('')
            menu.txt01_senha.setText('')
        else:
            QMessageBox.about(menu, 'Alerta', 'Usuário ou senha não pode ficar vazio!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao inserir os dados, Talves Usuário e senha ja exista, tente outro!')


def excluir_usuario_senha():  ## FUNÇÃO PARRA EXCLUIR USUÁRIO E SENHA
    try:
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            usuario = menu.txt01_usuario.text().strip()
            senha = menu.txt01_senha.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f'DELETE FROM tab_usuarios WHERE senha = {senha}');
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Usuário excluído com sucesso!')
            menu.txt01_usuario.setText('')
            menu.txt01_senha.setText('')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao excluir dados, Talves Usuário e senha não exista!')


def alterar_usuarios_senha(): ## FUNÇÃO PARA ALTERAR SENHA DO USUÁRIO
    try:
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            usuario = menu.txt01_usuario.text().strip()
            senha = menu.txt01_senha.text().strip()
            novo_usuario = menu.txt01_novousuario.text().strip()
            nova_senha = menu.txt01_novasenha.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f'SELECT nome FROM tab_usuarios WHERE senha = {senha}');
            nome_bd = cursor.fetchall()
            nome_bd = (nome_bd[0][0])
            if usuario == nome_bd:
                cursor.execute(f"SELECT STATUS FROM tab_abertura WHERE OPERADOR = '{usuario}'")
                RESPOSTA = cursor.fetchall()
                for i in range(0,len(RESPOSTA)):
                    if RESPOSTA[i][0] == 'ABERTO':
                        msg = QMessageBox()
                        msg.setWindowTitle('ESTE REGISTRO NÃO PODE SER ALTERADO!')
                        msg.setInformativeText(f"EXISTE UM CAIXA ABERTO PARA  {usuario}  REALIZE O FECHAMENTO!")
                        msg.exec()
                        menu.txt01_usuario.setText('')
                        menu.txt01_senha.setText('')
                        menu.txt01_novasenha.setText('')
                        menu.txt01_novousuario.setText('')
                        return
                #if senha != nova_senha:
                cursor.execute(f"UPDATE tab_usuarios SET NOME = '{novo_usuario}' WHERE NOME = '{usuario}'");
                cursor.execute(f"UPDATE tab_usuarios SET SENHA = {nova_senha} WHERE SENHA = {senha}");
                banco.commit()
                banco.close()
                QMessageBox.about(menu, 'Alerta','Usuário alterado com sucesso!')
                menu.txt01_usuario.setText('')
                menu.txt01_senha.setText('')
                menu.txt01_novasenha.setText('')
                menu.txt01_novousuario.setText('')
            else:
                msg = QMessageBox()
                msg.setWindowTitle('ALERTA!')
                msg.setInformativeText('USUÁRIO OU SENHA NAO ENCONTRADO NA BASE!')
                msg.exec()
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def alterar_permissao_usuario():
    try:
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            senha = menu.txt01_senha.text().strip()
            PRODUTO = menu.txt01_produto.text().strip().upper()
            CLIENTE = menu.txt01_cliente.text().strip().upper()
            CONTAS = menu.txt01_contas.text().strip().upper()
            CAIXA = menu.txt01_caixa.text().strip().upper()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(F"UPDATE tab_usuarios SET PRODUTO = '{PRODUTO}' WHERE SENHA = {senha}");
            cursor.execute(F"UPDATE tab_usuarios SET CLIENTE = '{CLIENTE}' WHERE SENHA = {senha}");
            cursor.execute(F"UPDATE tab_usuarios SET CONTAS = '{CONTAS}' WHERE SENHA = {senha}");
            cursor.execute(F"UPDATE tab_usuarios SET CAIXA = '{CAIXA}' WHERE SENHA = {senha}");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Usuário alterado com sucesso!')
            menu.txt01_usuario.setText('')
            menu.txt01_senha.setText('')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')

def listar_usuario():  ## FUNÇÃO PARA LISTAR OS DADOS NA INTERFACE
    try:
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_usuarios')
        dados_lidos = cursor.fetchall()
        menu.tab01_tabela.clearContents()
        menu.tab01_tabela.setRowCount(len(dados_lidos) + 1)
        menu.tab01_tabela.setColumnCount(6)
        for i in range(0,len(dados_lidos)):
            for j in range(0,6):
                menu.tab01_tabela.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def carregar_campos_usuario():
    try:
        retorno = menu.tab01_tabela.selectionModel().currentIndex().siblingAtColumn(1).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_usuarios WHERE SENHA = '{retorno}'")
        dados_lidos = cursor.fetchall()
        menu.txt01_usuario.setText(str(dados_lidos[0][0]))
        menu.txt01_senha.setText(str(dados_lidos[0][1]))
        menu.txt01_produto.setText(str(dados_lidos[0][2]))
        menu.txt01_cliente.setText(str(dados_lidos[0][3]))
        menu.txt01_contas.setText(str(dados_lidos[0][4]))
        menu.txt01_caixa.setText(str(dados_lidos[0][5]))
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def permissao_usuario():
    try:
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT PRODUTO FROM tab_usuarios WHERE SENHA = '2020'")
        permissao = cursor.fetchall()
        if permissao[0][0] == 'N' or '':
            msg = QMessageBox()
            msg.setWindowTitle('PERMISSÃO')
            msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
            msg.exec()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def alterar_empresa():
    try:
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            EMPRESA = str(menu.txt_nome_empresa.text().strip().upper())
            ENDERECO = str(menu.txt_end_empresa.text().strip().upper())
            CEP = str(menu.txt_cep_empresa.text().strip().upper())
            EMAIL = str(menu.txt_email_empresa.text().strip())
            FONE = str(menu.txt_fone_empresa.text().strip().upper())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(F"UPDATE tab_empresa SET EMPRESA = '{EMPRESA}'");
            cursor.execute(F"UPDATE tab_empresa SET ENDERECO = '{ENDERECO}'");
            cursor.execute(F"UPDATE tab_empresa SET CEP = '{CEP}'");
            cursor.execute(F"UPDATE tab_empresa SET EMAIL = '{EMAIL}' ");
            cursor.execute(F"UPDATE tab_empresa SET FONE = '{FONE}' ");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','empresa alterado com sucesso!')
            menu.txt01_usuario.setText('')
            menu.txt01_senha.setText('')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def buscar_empresa():
    try:
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        menu.txt_nome_empresa.setText(str(dados_lidos[0][0]))
        menu.txt_end_empresa.setText(str(dados_lidos[0][1]))
        menu.txt_cep_empresa.setText(str(dados_lidos[0][2]))
        menu.txt_email_empresa.setText(str(dados_lidos[0][3]))
        menu.txt_fone_empresa.setText(str(dados_lidos[0][4]))
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def limpar_empresa():
    try:
        menu.txt_nome_empresa.setText('')
        menu.txt_end_empresa.setText('')
        menu.txt_cep_empresa.setText('')
        menu.txt_email_empresa.setText('')
        menu.txt_fone_empresa.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao limpar os dados !')


#############################################TELA DE CADASTRO DE PRODUTO################################################


def real():  ## FUNÇÃO PARA CALCULAR PREÇO EM REAL
    try:
        pr_custo = float(menu.txt02_prccusto.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        diferenca1 = float(menu.txt02_diferenca.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        pr_venda = pr_custo + diferenca1
        menu.txt02_prcvenda.setText(f'{pr_venda:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao calcular o preço, tente novamente!')

def porcento():  ## FUNÇÃO PARA CALCULAR PREÇO EM PORCENTAGEM
    try:
        pr_custo = float(menu.txt02_prccusto.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        diferenca1 = float(menu.txt02_diferenca.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        pr_venda = (float(pr_custo) + (float(pr_custo * diferenca1 / 100)))
        menu.txt02_prcvenda.setText(f'{pr_venda:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao calcular o preço, tente novamente!')


def p_custo():
    try:
        num = moeda(str(menu.txt02_prccusto.text().strip().replace('.', '').replace(',', '')))
        menu.txt02_prccusto.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')

def dif_p():
    try:
        num = moeda(str(menu.txt02_diferenca.text().strip().replace('.', '').replace(',', '')))
        menu.txt02_diferenca.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')

def data_produto():
        try:
            data = data_formatada(str(menu.txt02_dataentrada.text().strip()))
            menu.txt02_dataentrada.setText(f'{data}')
        except:
            QMessageBox.about(menu, 'Alerta', 'erro !')


def data_vencimento():
    try:
        data = data_formatada(str(menu.txt02_datavencimento.text().strip()))
        menu.txt02_datavencimento.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_prd_inicial():
    try:
        data = data_formatada(str(menu.txt02_datainicial.text().strip()))
        menu.txt02_datainicial.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_prd_final():
    try:
        data = data_formatada(str(menu.txt02_datafinal.text().strip()))
        menu.txt02_datafinal.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def cadastrar_produto():  ## FUNÇÃO PARA CADASTRAR PRODUTO
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT PRODUTO FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        id = menu.txt02_codigo.text().strip()
        descricao = menu.txt02_descricao.text().strip().upper()
        pr_custo = float(menu.txt02_prccusto.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        estoque = menu.txt02_estoque.text().strip()
        diferenca1 = float(menu.txt02_diferenca.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        pr_venda = float(menu.txt02_prcvenda.text().strip().replace('.', '_').replace('_','').replace(',','.'))
        fornecedor = menu.txt02_fornecedor.text().strip().upper()
        data_entrada = menu.txt02_dataentrada.text().strip()
        data_vencimento = menu.txt02_datavencimento.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_produto VALUES{int(id),descricao,pr_custo,estoque,diferenca1,pr_venda,fornecedor,data_entrada,data_vencimento}");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta','produto cadastrado com sucesso!')
        menu.txt02_codigo.setText('')
        menu.txt02_descricao.setText('')
        menu.txt02_prccusto.setText('')
        menu.txt02_diferenca.setText('')
        menu.txt02_prcvenda.setText('')
        menu.txt02_fornecedor.setText('')
        menu.txt02_dataentrada.setText('')
        menu.txt02_estoque.setText('')
        menu.txt02_datavencimento.setText('')
        menu.txt02_datainicial.setText('')
        menu.txt02_datafinal.setText('')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao inserir os dados, tente novamente!')


def novo_produto():
    try:
        menu.txt02_codigo.setText('')
        menu.txt02_descricao.setText('')
        menu.txt02_prccusto.setText('')
        menu.txt02_diferenca.setText('')
        menu.txt02_prcvenda.setText('')
        menu.txt02_fornecedor.setText('')
        menu.txt02_dataentrada.setText('')
        menu.txt02_estoque.setText('')
        menu.txt02_datavencimento.setText('')
        menu.txt02_datainicial.setText('')
        menu.txt02_datafinal.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao inserir os dados, tente novamente!')


def excluir_produto():  ## FUNÇÃO PARA EXCLUIR PRODUTO
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT PRODUTO FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            id = menu.txt02_codigo.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f'DELETE FROM tab_produto WHERE id = {id} ')
            banco.commit()
            banco.close()
            menu.txt02_codigo.setText('')
            menu.txt02_descricao.setText('')
            menu.txt02_prccusto.setText('')
            menu.txt02_diferenca.setText('')
            menu.txt02_prcvenda.setText('')
            menu.txt02_fornecedor.setText('')
            menu.txt02_dataentrada.setText('')
            menu.txt02_estoque.setText('')
            menu.txt02_datavencimento.setText('')
            QMessageBox.about(menu, 'Alerta','produto excluído com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao excluir os dados, tente novamente!')

def lista_dados():  ## FUNÇÃO PARA LISTAR OS DADOS NA INTERFACE
    try:
        venda = cont = custo = contestoque = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_produto')
        dados_lidos = cursor.fetchall()
        menu.tab02_listaproduto.clearContents()
        menu.tab02_listaproduto.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab02_listaproduto.setColumnCount(9)
        for i in range(0,len(dados_lidos)):
            cont += 1
            custo += (dados_lidos[i][2])
            contestoque += (dados_lidos[i][3])
            venda += (dados_lidos[i][5])
            for j in range(0,9):
                menu.tab02_listaproduto.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab02_listaproduto.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Total produtos {cont}')))
        menu.tab02_listaproduto.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais R$: {custo:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais: {contestoque}')))
        menu.tab02_listaproduto.setItem(linha,4,QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais R$: {venda:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtro():## FUNÇÃO PARA FILTRAR DADOS
    try:
        campo = menu.cmb02_filtro.currentText()
        pesquisa = menu.txt02_pesquisa.text().strip()
        venda = cont = custo = contestoque = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_produto WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.tab02_listaproduto.clearContents()
        menu.tab02_listaproduto.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab02_listaproduto.setColumnCount(9)
        for i in range(0,len(dados_lidos)):
            cont += 1
            custo += (dados_lidos[i][2])
            contestoque += (dados_lidos[i][3])
            venda += (dados_lidos[i][5])
            for j in range(0,9):
                menu.tab02_listaproduto.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab02_listaproduto.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Total produtos {cont}')))
        menu.tab02_listaproduto.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais R$: {custo:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais: {contestoque}')))
        menu.tab02_listaproduto.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais R$: {venda:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_produto_data():
    try:
        data_inicio = menu.txt02_datainicial.text().strip()
        data_final = menu.txt02_datafinal.text().strip()
        venda = cont = custo = contestoque = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_produto WHERE data_entrada BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.tab02_listaproduto.clearContents()
        menu.tab02_listaproduto.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab02_listaproduto.setColumnCount(9)
        for i in range(0, len(dados_lidos)):
            cont += 1
            custo += (dados_lidos[i][2])
            contestoque += (dados_lidos[i][3])
            venda += (dados_lidos[i][5])
            for j in range(0, 9):
                menu.tab02_listaproduto.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab02_listaproduto.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Total produtos {cont}')))
        menu.tab02_listaproduto.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais R$: {custo:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais: {contestoque}')))
        menu.tab02_listaproduto.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais R$: {venda:,.2f}')))
        menu.tab02_listaproduto.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab02_listaproduto.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def gerar_pdf(): ## FUNÇÃO PARA GERAR PDF.
    data = datetime.now()
    data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' +  str(data.minute) + ':' + str(f'{data.second}')
    try:
        dados = []
        all_dados = []
        for row in range(menu.tab02_listaproduto.rowCount()):
            for column in range(menu.tab02_listaproduto.columnCount()):
                dados.append(menu.tab02_listaproduto.item(row,column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf',pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold',20)
        cnv.drawString(385,790,'Relatóro de Produtos')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'código')
            cnv.drawString(70, 710,'descrição do produto')
            cnv.drawString(225, 710, 'p_custo')
            cnv.drawString(280, 710, 'estoque')
            cnv.drawString(320, 710, 'p_venda')
            cnv.drawString(380, 710, 'Fornercedor')
            cnv.drawString(485, 710, 'D_entrada')
            cnv.drawString(530, 710, 'D_vencimento')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20,705 - y, f'{lista[0]}')
            cnv.drawString(70, 705 - y, f'{lista[1]}')
            cnv.drawString(225, 705 - y, f'{lista[2]}')
            cnv.drawString(280, 705 - y, f'{lista[3]}')
            cnv.drawString(320, 705 - y, f'{lista[5]}')
            cnv.drawString(380, 705 - y, f'{lista[6]}')
            cnv.drawString(485, 705 - y, f'{lista[7]}')
            cnv.drawString(530, 705 - y, f'{lista[8]}')
        cnv.drawString(20,710 - y,'-'*280)
        cnv.rect(10,30,575,695,fill=False,stroke=True) ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def alterar_produto():  ## FUNÇÃO PARA ALTERAR PRODUTOS.
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT PRODUTO FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            id = menu.txt02_codigo.text().strip()
            descricao = menu.txt02_descricao.text().strip().upper()
            pr_custo = float(menu.txt02_prccusto.text().strip())
            diferenca1 = float(menu.txt02_diferenca.text().strip())
            pr_venda = float(menu.txt02_prcvenda.text().strip())
            fornecedor = menu.txt02_fornecedor.text().strip().upper()
            estoque = menu.txt02_estoque.text().strip()
            data_entrada = menu.txt02_dataentrada.text().strip()
            data_vencimento = menu.txt02_datavencimento.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(F"UPDATE tab_produto SET descricao = '{descricao}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET pr_custo = '{pr_custo}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET diferenca1 = '{diferenca1}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET pr_venda = '{pr_venda}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET estoque = '{estoque}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET fornecedor = '{fornecedor}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET data_entrada = '{data_entrada}' WHERE id = {id}");
            cursor.execute(f"UPDATE tab_produto SET data_vencimento = '{data_vencimento}' WHERE id = {id}");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','produto alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def pre_campos_produto(): ## FUNÇÃO PARA PREENCHER AS CAIXAS DE TEXTO ATRAVÉS DO ID.
    try:
        retorno = menu.tab02_listaproduto.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_produto WHERE id = {retorno}')
        dados_lidos = cursor.fetchall()
        menu.txt02_codigo.setText(str(dados_lidos[0][0]))
        menu.txt02_descricao.setText(dados_lidos[0][1])
        menu.txt02_prccusto.setText(str(dados_lidos[0][2]))
        menu.txt02_estoque.setText(str(dados_lidos[0][3]))
        menu.txt02_diferenca.setText(str(dados_lidos[0][4]))
        menu.txt02_prcvenda.setText(str(dados_lidos[0][5]))
        menu.txt02_fornecedor.setText(dados_lidos[0][6])
        menu.txt02_dataentrada.setText(dados_lidos[0][7])
        menu.txt02_datavencimento.setText(dados_lidos[0][8])
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados dados!')


def gerar_codigo(): ## FUNÇÃO PARA GERAR CODIGO DE BARRAS
    try:
        lista = []
        for i in range(0,12):
            codigo = randint(0,9)
            lista.append(codigo)
        al_lista = (f'{lista[0]}{lista[1]}{lista[2]}{lista[3]}{lista[4]}{lista[5]}{lista[6]}{lista[7]}{lista[8]}{lista[9]}{lista[10]}{lista[11]}')
        codbar = EAN13(al_lista,writer=ImageWriter())
        menu.txt02_codigo.setText(f'{codbar}')
        codbar.save('EAN11')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar código!')


#################################CADASTRO DE CLIENTE###################################################################


def data_cliente_inicial():
    try:
        data = data_formatada(str(menu.txtcliente_data_inicio.text().strip()))
        menu.txtcliente_data_inicio.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_cliente_final():
    try:
        data = data_formatada(str(menu.txtcliente_data_final.text().strip()))
        menu.txtcliente_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_cliente():
    try:
        data = data_formatada(str(menu.txtcliente_data.text().strip()))
        menu.txtcliente_data.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def cad_cliente():  ## FUNÇÃO PARA CADASTRAR CLIENTE
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        CPF = str(menu.txtcliente_cpf.text().strip().upper())
        NOME = str(menu.txtcliente_nome.text().strip().upper())
        LOGRADOURO = str(menu.txtcliente_logradouro.text().strip().upper())
        NUMERO = str(menu.txtcliente_numero.text().strip().upper())
        COMPLEMENTO = str(menu.txtcliente_complemento.text().strip().upper())
        BAIRRO = str(menu.txtcliente_bairro.text().strip().upper())
        MUNICIPIO = str(menu.txtcliente_municipio.text().strip().upper())
        UF = str(menu.txtcliente_uf.text().strip().upper())
        CEP = str(menu.txtcliente_cep.text().strip().upper())
        TELEFONE = str(menu.txtcliente_telefone.text().strip().upper())
        EMAIL = str(menu.txtcliente_email.text().strip())
        DATA = str(menu.txtcliente_data.text().strip().upper())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_cliente VALUES{CPF,NOME,LOGRADOURO,NUMERO,COMPLEMENTO,BAIRRO,MUNICIPIO,UF,CEP,TELEFONE,EMAIL,DATA}");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'cadastro realizado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro cadastrar os dados!')


def excluir_cliente(): ## FUNÇÃO PARA EXCLUIR CLIENTE
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CPF = str(menu.txtcliente_cpf.text().strip().lower())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"DELETE FROM tab_cliente WHERE CPF = '{CPF}'")
            banco.commit()
            banco.close()
            menu.txtcliente_cpf.setText('')
            menu.txtcliente_nome.setText('')
            menu.txtcliente_logradouro.setText('')
            menu.txtcliente_numero.setText('')
            menu.txtcliente_complemento.setText('')
            menu.txtcliente_bairro.setText('')
            menu.txtcliente_municipio.setText('')
            menu.txtcliente_uf.setText('')
            menu.txtcliente_cep.setText('')
            menu.txtcliente_telefone.setText('')
            menu.txtcliente_email.setText('')
            menu.txtcliente_data.setText('')
            QMessageBox.about(menu, 'Alerta','produto excluído com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao excluir os dados, tente novamente!')


def alterar_cliente(): ## FUNÇÃO PARA ALTERAR CLIENTE
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CPF = str(menu.txtcliente_cpf.text().strip().upper())
            NOME = str(menu.txtcliente_nome.text().strip().upper())
            LOGRADOURO = str(menu.txtcliente_logradouro.text().strip().upper())
            NUMERO = str(menu.txtcliente_numero.text().strip().upper())
            COMPLEMENTO = str(menu.txtcliente_complemento.text().strip().upper())
            BAIRRO = str(menu.txtcliente_bairro.text().strip().upper())
            MUNICIPIO = str(menu.txtcliente_municipio.text().strip().upper())
            UF = str(menu.txtcliente_uf.text().strip().upper())
            CEP = str(menu.txtcliente_cep.text().strip().upper())
            TELEFONE = str(menu.txtcliente_telefone.text().strip().upper())
            EMAIL = str(menu.txtcliente_email.text().strip())
            DATA = str(menu.txtcliente_data.text().strip().upper())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(F"UPDATE tab_cliente SET NOME = '{NOME}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET LOGRADOURO = '{LOGRADOURO}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET NUMERO = '{NUMERO}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET COMPLEMENTO = '{COMPLEMENTO}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET BAIRRO = '{BAIRRO}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET MUNICIPIO = '{MUNICIPIO}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET UF = '{UF}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET CEP = '{CEP}' WHERE CPF = {CPF}");
            cursor.execute(f"UPDATE tab_cliente SET TELEFONE = '{TELEFONE}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET EMAIL = '{EMAIL}' WHERE CPF = '{CPF}'");
            cursor.execute(f"UPDATE tab_cliente SET DATA = '{DATA}' WHERE CPF = '{CPF}'");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','cliente alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def busca_cliente(): ##FUNÇÃO PARA LISTAR OS DADOS NA INTERFACE
    try:
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_cliente')
        dados_lidos = cursor.fetchall()
        menu.lstcliente_tabela.clearContents()
        menu.lstcliente_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstcliente_tabela.setColumnCount(12)
        for i in range(0,len(dados_lidos)):
            cont += 1
            for j in range(0,12):
                menu.lstcliente_tabela.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstcliente_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'TOTAL CLIENTES {cont}')))
        menu.lstcliente_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 4,QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def novo_cliente():  ## FUNÇÃO PARA LIMPAR AS CAIXAS DE TEXTO
    try:
        menu.txtcliente_cpf.setText('')
        menu.txtcliente_nome.setText('')
        menu.txtcliente_logradouro.setText('')
        menu.txtcliente_numero.setText('')
        menu.txtcliente_complemento.setText('')
        menu.txtcliente_bairro.setText('')
        menu.txtcliente_municipio.setText('')
        menu.txtcliente_uf.setText('')
        menu.txtcliente_cep.setText('')
        menu.txtcliente_telefone.setText('')
        menu.txtcliente_email.setText('')
        menu.txtcliente_data.setText('')
    except:
        QMessageBox.about(menu, 'Alerta''ERRO')


def carregar_campos_cliente(): ## FUNÇÃO PARA LISTAR OS DADOS NAS CAIXAS DE TEXTO
    try:
        retorno = menu.lstcliente_tabela.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_cliente WHERE CPF = '{retorno}'")
        dados_lidos = cursor.fetchall()
        menu.txtcliente_cpf.setText(str(dados_lidos[0][0]))
        menu.txtcliente_nome.setText(str(dados_lidos[0][1]))
        menu.txtcliente_logradouro.setText(str(dados_lidos[0][2]))
        menu.txtcliente_numero.setText(str(dados_lidos[0][3]))
        menu.txtcliente_complemento.setText(str(dados_lidos[0][4]))
        menu.txtcliente_bairro.setText(str(dados_lidos[0][5]))
        menu.txtcliente_municipio.setText(str(dados_lidos[0][6]))
        menu.txtcliente_uf.setText(str(dados_lidos[0][7]))
        menu.txtcliente_cep.setText(str(dados_lidos[0][8]))
        menu.txtcliente_telefone.setText(str(dados_lidos[0][9]))
        menu.txtcliente_email.setText(str(dados_lidos[0][10]))
        menu.txtcliente_data.setText(str(dados_lidos[0][11]))
        return
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def pdf_cliente(): ## FUNÇÃO PARA GERAR PDF
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.lstcliente_tabela.rowCount()):
            for column in range(menu.lstcliente_tabela.columnCount()):
                dados.append(menu.lstcliente_tabela.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(385, 790, 'Relatóro de Clientes')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'CPF')
            cnv.drawString(60, 710, 'NOME')
            cnv.drawString(225, 710, 'LOGRADOURO')
            cnv.drawString(285, 710, 'Nº')
            cnv.drawString(305, 710, 'BAIRRO')
            cnv.drawString(390, 710, 'MUNICIPIO')
            cnv.drawString(450, 710, 'UF')
            cnv.drawString(465, 710, 'CEP')
            cnv.drawString(500, 710, 'FONE')
            cnv.drawString(545, 710, 'DATA')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(60, 705 - y, f'{lista[1]}')
            cnv.drawString(225, 705 - y, f'{lista[2]}')
            cnv.drawString(285, 705 - y, f'{lista[3]}')
            cnv.drawString(305, 705 - y, f'{lista[5]}')
            cnv.drawString(390, 705 - y, f'{lista[6]}')
            cnv.drawString(450, 705 - y, f'{lista[7]}')
            cnv.drawString(465, 705 - y, f'{lista[8]}')
            cnv.drawString(500, 705 - y, f'{lista[9]}')
            cnv.drawString(545, 705 - y, f'{lista[11]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def filtro_cliente():  ## FUNÇÃO PARA FILTRAR OS DADOS
    try:
        campo = menu.cbmcliente_filtro.currentText()
        pesquisa = menu.txtcliente_buscar.text().strip()
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_cliente WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.lstcliente_tabela.clearContents()
        menu.lstcliente_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstcliente_tabela.setColumnCount(12)
        for i in range(0,len(dados_lidos)):
            cont += 1
            for j in range(0,12):
                menu.lstcliente_tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstcliente_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Total Clientes {cont}')))
        menu.lstcliente_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_cliente_data(): ## FUNÇÃO PARA FILTRAR OS DADOS POR DATA
    try:
        if menu.txtcliente_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txtcliente_data_inicio.text()).strip()
        data_final = str(menu.txtcliente_data_final.text()).strip()
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_cliente WHERE  DATA BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.lstcliente_tabela.clearContents()
        menu.lstcliente_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstcliente_tabela.setColumnCount(12)
        for i in range(0, len(dados_lidos)):
            cont += 1
            for j in range(0, 12):
                menu.lstcliente_tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstcliente_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Totais de Itens:{cont}')))
        menu.lstcliente_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstcliente_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


#################################CADASTRO DE FORNECEDOR########################################


def data_fornecedor_inicial():
    try:
        data = data_formatada(str(menu.txtfornecedor_data_inicio.text().strip()))
        menu.txtfornecedor_data_inicio.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_fornecedor_final():
    try:
        data = data_formatada(str(menu.txtfornecedor_data_final.text().strip()))
        menu.txtfornecedor_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_fornecedor():
    try:
        data = data_formatada(str(menu.txtfornecedor_data.text().strip()))
        menu.txtfornecedor_data.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def api_cnpj(): ## FUNÇÃO PARA BUSCAR OS DADOS  ATRAVES DO CNPJ
    try:
        if menu.txtfornecedor_cnpj.text().strip() == '':
            return
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        CNPJ = str(menu.txtfornecedor_cnpj.text().strip())
        url = f"https://receitaws.com.br/v1/cnpj/{CNPJ}"
        quere = {f"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", "cnpj": f"{CNPJ}", "plugin": "RF"}
        response = requests.request("GET", url, params=quere)
        resp = json.loads(response.text)
        menu.txtfornecedor_empresa.setText(f"{resp['nome']}")
        menu.txtfornecedor_logradouro.setText(f"{resp['logradouro']}")
        menu.txtfornecedor_numero.setText(f"{resp['numero']}")
        menu.txtfornecedor_complemento.setText(f"{resp['complemento']}")
        menu.txtfornecedor_bairro.setText(f"{resp['bairro']}")
        menu.txtfornecedor_municipio.setText(f"{resp['municipio']}")
        menu.txtfornecedor_uf.setText(f"{resp['uf']}")
        menu.txtfornecedor_cep.setText(f"{resp['cep']}")
        menu.txtfornecedor_telefone.setText(f"{resp['telefone']}")
        menu.txtfornecedor_email.setText(f"{resp['email']}")
        menu.txtfornecedor_data.setText(f"{data}")
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')

def cad_fornecedor(): ## FUNÇÃO PARA CADASTRAR FORNECEDOR
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        CNPJ = str(menu.txtfornecedor_cnpj.text().strip().upper())
        EMPRESA = str(menu.txtfornecedor_empresa.text().strip().upper())
        LOGRADOURO = str(menu.txtfornecedor_logradouro.text().strip().upper())
        NUMERO = str(menu.txtfornecedor_numero.text().strip().upper())
        COMPLEMENTO = str(menu.txtfornecedor_complemento.text().strip().upper())
        BAIRRO = str(menu.txtfornecedor_bairro.text().strip().upper())
        MUNICIPIO = str(menu.txtfornecedor_municipio.text().strip().upper())
        UF = str(menu.txtfornecedor_uf.text().strip().upper())
        CEP = str(menu.txtfornecedor_cep.text().strip().upper().replace('.','').replace('-',''))
        TELEFONE = str(menu.txtfornecedor_telefone.text().strip().upper().replace('(','').replace(')','').replace('-','').replace('/',''))
        EMAIL = str(menu.txtfornecedor_email.text().strip())
        DATA = str(menu.txtfornecedor_data.text().strip().upper())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_fornecedor VALUES{CNPJ,EMPRESA,LOGRADOURO,NUMERO,COMPLEMENTO,BAIRRO,MUNICIPIO,UF,CEP,TELEFONE,EMAIL,DATA}");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'cadastro realizado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro cadastrar os dados!')


def excluir_fornecedor():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CNPJ = str(menu.txtfornecedor_cnpj.text().strip().upper())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"DELETE FROM tab_fornecedor WHERE CNPJ = '{CNPJ}'")
            banco.commit()
            banco.close()
            menu.txtfornecedor_cnpj.setText('')
            menu.txtfornecedor_empresa.setText('')
            menu.txtfornecedor_logradouro.setText('')
            menu.txtfornecedor_numero.setText('')
            menu.txtfornecedor_complemento.setText('')
            menu.txtfornecedor_bairro.setText('')
            menu.txtfornecedor_municipio.setText('')
            menu.txtfornecedor_uf.setText('')
            menu.txtfornecedor_cep.setText('')
            menu.txtfornecedor_telefone.setText('')
            menu.txtfornecedor_email.setText('')
            menu.txtfornecedor_data.setText('')
            QMessageBox.about(menu, 'Alerta','produto excluído com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao excluir os dados, tente novamente!')


def altera_fornecedor():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CLIENTE FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CNPJ = str(menu.txtfornecedor_cnpj.text().strip())
            EMPRESA = str(menu.txtfornecedor_empresa.text().strip().upper())
            LOGRADOURO = str(menu.txtfornecedor_logradouro.text().strip().upper())
            NUMERO = str(menu.txtfornecedor_numero.text().strip())
            COMPLEMENTO = str(menu.txtfornecedor_complemento.text().strip().upper())
            BAIRRO = str(menu.txtfornecedor_bairro.text().strip().upper())
            MUNICIPIO = str(menu.txtfornecedor_municipio.text().strip().upper())
            UF = str(menu.txtfornecedor_uf.text().strip().upper())
            CEP = str(menu.txtfornecedor_cep.text().strip())
            TELEFONE = str(menu.txtfornecedor_telefone.text().strip())
            EMAIL = str(menu.txtfornecedor_email.text().strip())
            DATA = str(menu.txtfornecedor_data.text().strip().upper())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(F"UPDATE tab_fornecedor SET EMPRESA = '{EMPRESA}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET LOGRADOURO = '{LOGRADOURO}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET NUMERO = '{NUMERO}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET COMPLEMENTO = '{COMPLEMENTO}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET BAIRRO = '{BAIRRO}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET MUNICIPIO = '{MUNICIPIO}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET UF = '{UF}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET CEP = '{CEP}' WHERE CNPJ = {CNPJ}");
            cursor.execute(f"UPDATE tab_fornecedor SET TELEFONE = '{TELEFONE}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET EMAIL = '{EMAIL}' WHERE CNPJ = '{CNPJ}'");
            cursor.execute(f"UPDATE tab_fornecedor SET DATA = '{DATA}' WHERE CNPJ = '{CNPJ}'");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','fornecedor alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def buscar_fornecedor():
    try:
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_fornecedor')
        dados_lidos = cursor.fetchall()
        menu.lstfornecedor_tabela.clearContents()
        menu.lstfornecedor_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstfornecedor_tabela.setColumnCount(12)
        for i in range(0, len(dados_lidos)):
            cont += 1
            for j in range(0, 12):
                menu.lstfornecedor_tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstfornecedor_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'TOTAL CLIENTES {cont}')))
        menu.lstfornecedor_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def novo_fornecedor():
    try:
        menu.txtfornecedor_cnpj.setText('')
        menu.txtfornecedor_empresa.setText('')
        menu.txtfornecedor_logradouro.setText('')
        menu.txtfornecedor_numero.setText('')
        menu.txtfornecedor_complemento.setText('')
        menu.txtfornecedor_bairro.setText('')
        menu.txtfornecedor_municipio.setText('')
        menu.txtfornecedor_uf.setText('')
        menu.txtfornecedor_cep.setText('')
        menu.txtfornecedor_telefone.setText('')
        menu.txtfornecedor_email.setText('')
        menu.txtfornecedor_data.setText('')
    except:
        QMessageBox.about(menu, 'Alerta''ERRO')


def carregar_campos_fornecedor():
    try:
        retorno = menu.lstfornecedor_tabela.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_fornecedor WHERE CNPJ = '{retorno}'")
        dados_lidos = cursor.fetchall()
        menu.txtfornecedor_cnpj.setText(str(dados_lidos[0][0]))
        menu.txtfornecedor_empresa.setText(str(dados_lidos[0][1]))
        menu.txtfornecedor_logradouro.setText(str(dados_lidos[0][2]))
        menu.txtfornecedor_numero.setText(str(dados_lidos[0][3]))
        menu.txtfornecedor_complemento.setText(str(dados_lidos[0][4]))
        menu.txtfornecedor_bairro.setText(str(dados_lidos[0][5]))
        menu.txtfornecedor_municipio.setText(str(dados_lidos[0][6]))
        menu.txtfornecedor_uf.setText(str(dados_lidos[0][7]))
        menu.txtfornecedor_cep.setText(str(dados_lidos[0][8]))
        menu.txtfornecedor_telefone.setText(str(dados_lidos[0][9]))
        menu.txtfornecedor_email.setText(str(dados_lidos[0][10]))
        menu.txtfornecedor_data.setText(str(dados_lidos[0][11]))
        return
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def pdf_fornecedor():
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.lstfornecedor_tabela.rowCount()):
            for column in range(menu.lstfornecedor_tabela.columnCount()):
                dados.append(menu.lstfornecedor_tabela.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(385, 790, 'Relatóro de Fornecedor')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'CNPJ')
            cnv.drawString(70, 710, 'EMPRESA')
            cnv.drawString(235, 710, 'LOGRADOURO')
            cnv.drawString(305, 710, 'Nº')
            cnv.drawString(325, 710, 'BAIRRO')
            cnv.drawString(390, 710, 'MUNICIPIO')
            cnv.drawString(450, 710, 'UF')
            cnv.drawString(465, 710, 'CEP')
            cnv.drawString(500, 710, 'FONE')
            cnv.drawString(545, 710, 'DATA')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(70, 705 - y, f'{lista[1]}')
            cnv.drawString(235, 705 - y, f'{lista[2]}')
            cnv.drawString(305, 705 - y, f'{lista[3]}')
            cnv.drawString(325, 705 - y, f'{lista[5]}')
            cnv.drawString(390, 705 - y, f'{lista[6]}')
            cnv.drawString(450, 705 - y, f'{lista[7]}')
            cnv.drawString(465, 705 - y, f'{lista[8]}')
            cnv.drawString(500, 705 - y, f'{lista[9]}')
            cnv.drawString(545, 705 - y, f'{lista[11]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def filtrar_fornecedor():
    try:
        campo = menu.cbmfornecedor_filtro.currentText()
        pesquisa = menu.txtfornecedor_buscar.text().strip()
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_fornecedor WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.lstfornecedor_tabela.clearContents()
        menu.lstfornecedor_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstfornecedor_tabela.setColumnCount(12)
        for i in range(0,len(dados_lidos)):
            cont += 1
            for j in range(0,12):
                menu.lstfornecedor_tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstfornecedor_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Total Clientes {cont}')))
        menu.lstfornecedor_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_fornecedor_data():
    try:
        if menu.txtfornecedor_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txtfornecedor_data_inicio.text()).strip()
        data_final = str(menu.txtfornecedor_data_final.text()).strip()
        cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_fornecedor WHERE  DATA BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.lstfornecedor_tabela.clearContents()
        menu.lstfornecedor_tabela.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lstfornecedor_tabela.setColumnCount(12)
        for i in range(0, len(dados_lidos)):
            cont += 1
            for j in range(0, 12):
                menu.lstfornecedor_tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lstfornecedor_tabela.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 1, QtWidgets.QTableWidgetItem(str(f'Totais de Itens:{cont}')))
        menu.lstfornecedor_tabela.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        menu.lstfornecedor_tabela.setItem(linha, 11, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


#03############################################TELA DE CAIXA############################################################


def gerar_id_venda():  ##FUNÇÃO PARA GERAR CÓDIGO DE VENDA
    try:
        menu.txt03_descricao.setFocus()
        lista = []
        for i in range(0,6):
            codigo = randint(0,9)
            lista.append(codigo)
        al_lista = (f'{lista[0]}{lista[1]}{lista[2]}{lista[3]}{lista[4]}{lista[5]}')
        menu.txt03_idvenda.setText(f'{al_lista}')
        menu.lbl03_rodape.setText('/1 -PESQUISAR  /2 -PAGAMENTO  /3 -CAN-ITEM')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar código!')


def pesquisa_produto():
    try:
        descricao = pesquisa.txt08_filtro.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_produto WHERE descricao LIKE '{}%'".format(f'{descricao}'))
        dados_lidos = cursor.fetchall()
        pesquisa.lst08_lista.clearContents()
        pesquisa.lst08_lista.setRowCount(len(dados_lidos))
        pesquisa.lst08_lista.setColumnCount(6)
        pesquisa.lst08_lista.setColumnWidth(1,400)# LARGURA DA COLUNA
        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisa.lst08_lista.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def pesquisa_prduto_codigo():
    try:

        id = pesquisa.txt08_filtro_codigo.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_produto WHERE id = {id}')
        dados_lidos = cursor.fetchall()
        pesquisa.lst08_lista.clearContents()
        pesquisa.lst08_lista.setRowCount(len(dados_lidos))
        pesquisa.lst08_lista.setColumnCount(6)
        pesquisa.lst08_lista.setColumnWidth(1,400)# LARGURA DA COLUNA
        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisa.lst08_lista.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')


def retorna_pesquisa():
    try:
        retorno = pesquisa.lst08_lista.selectionModel().currentIndex().siblingAtColumn(0).data()
        menu.txt03_descricao.setText(f'{retorno}')
        pesquisa.close()
        return
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados !')



def pre_campos():  ## FUNÇÃO PARA PREENCHER AS CAIXAS DE TEXTO ATRAVÉS DO ID.
    try:
        if menu.txt03_descricao.text().strip() == '/1':
            pesquisa.lst08_lista.clearContents()
            pesquisa.show()
            return
        if menu.txt03_descricao.text().strip() == '/2':
            menu.lbl03_status.setText('FINALIZANDO TRANSAÇÃO...!')
            menu.lbl03_rodape.setText('1 -DINHEIRO  2 -CARTÃO/CRÉDITO  3 -CARTÃO/DÉBITO  4 -PIX')
            menu.txt03_pagamento.setFocus()
            menu.txt03_descricao.setText('')
            return
        if menu.txt03_descricao.text().strip() == '/3':
            menu.txt03_num_item.setFocus()
            menu.txt03_descricao.setText('')
            return
        menu.txt03_qtd.setFocus()
        if menu.txt03_descricao.text() == ''.strip():
            return
        if  menu.txt03_id_produto.text() !='':
            return
        if menu.txt03_item.text() == '':
            item = 1
        if menu.txt03_item.text() != '':
            item = int(menu.txt03_item.text()) + 1
        menu.txt03_item.setText(f'{item}')
        if menu.txt03_total.text() == '':
            menu.lbl03_status.setText('CAIXA LIVRE!')
        if menu.txt03_descricao.text() != '':
            menu.lbl03_status.setText('VENDA!')
        id = menu.txt03_descricao.text().strip()
        menu.txt03_id_produto.setText(f'{id}')
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_produto WHERE id = {id}')
        dados_lidos = cursor.fetchall()
        menu.txt03_descricao.setText(f'{dados_lidos[0][1]}')
        menu.txt03_uni.setText(f'{dados_lidos[0][5]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        menu.txt03_estoque.setText(f'{dados_lidos[0][3]}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados dados!')


def calcular_quantidade():
    try:
        if menu.txt03_qtd.text() == ''.strip():
            return
        if menu.txt03_uni.text() == ''.strip():
            return
        if menu.txt03_subtotal.text() == '':
            subtotal = 0
        if menu.txt03_subtotal.text() != '':
            subtotal = float(menu.txt03_subtotal.text().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        total = 0
        quantidade = int(menu.txt03_qtd.text().strip())
        v_unitario = float(menu.txt03_uni.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        estoque = int(menu.txt03_estoque.text().strip())
        if quantidade > estoque:
            menu.txt03_qtd.setText('')
            menu.txt03_qtd.setFocus()
            msg = QMessageBox()
            msg.setWindowTitle('ALERTA DE ESTOQUE!')
            msg.setInformativeText('ESTOQUE INSUFICIENTE, DIGITE UMA QUANTIDADE MENOR OU IGUAL!')
            msg.exec()
            return
        total = quantidade * v_unitario
        subtotal += total
        estoque = estoque - quantidade
        menu.txt03_estoque.setText(f'{estoque}')
        menu.txt03_total.setText(str(f'{total:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        menu.txt03_subtotal.setText(str(f'{subtotal:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao calcular!')


def salve_venda():
    try:
        if menu.txt03_qtd.text() == ''.strip():
            return
        id_venda = int(menu.txt03_idvenda.text().strip())
        item = int(menu.txt03_item.text().strip())
        descricao = menu.txt03_descricao.text().strip()
        qtd = int(menu.txt03_qtd.text().strip())
        uni = float(menu.txt03_uni.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        total = float(menu.txt03_total.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        operador = menu.lbl03_operador.text().strip()
        data = menu.lbl03_data.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_venda VALUES{id_venda,item,descricao,qtd,uni,total,operador,data}");
        banco.commit()
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao inserir o inten!')


def salva_pagamento():
    try:
        menu.lbl03_status.setText('VENDA REALIZADA COM SUCESSO!')
        sleep(2)
        id_pagamento = int(menu.txt03_idvenda.text().strip())
        f_pagamento = menu.txt03_pagamento.text().strip()
        v_recebido = float(menu.txt03_vrecebido.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        troco = float(menu.txt03_troco.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        subtotal = float(menu.txt03_subtotal.text().strip().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        operador = str(menu.lbl03_operador.text())
        status = str('ABERTO')
        data = menu.lbl03_data.text()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_pagamento VALUES{id_pagamento,f_pagamento,v_recebido,troco,subtotal,data,operador,status}");
        banco.commit()
        banco.close()
        menu.lbl03_status.setText('EXIBINDO COMPROVANTE,AGUARDE...!')
        sleep(2)
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao realisar o pagamento!')


def lista_intens():
    try:
        if menu.txt03_qtd.text() == ''.strip():
            return
        if menu.txt03_descricao.text() == ''.strip():
            return
        item = menu.txt03_item.text()
        descricao = menu.txt03_descricao.text()
        quantidade = menu.txt03_qtd.text()
        v_unitario = menu.txt03_uni.text()
        total = menu.txt03_total.text()
        menu.lst03_listaintens.addItem(f'  {item}          {descricao}        {quantidade}        {v_unitario}        {total}')
        menu.txt03_descricao.setText('')
        menu.txt03_qtd.setText('')
        menu.txt03_id_produto.setText('')
        menu.txt03_descricao.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados!')


def f_pagamento():
    try:
        if menu.txt03_pagamento.text() == '':
            return
        subtotal = float(menu.txt03_subtotal.text().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        pagamento = menu.txt03_pagamento.text()
        if pagamento == '1':
            menu.txt03_pagamento.setText('DINHEIRO')
            menu.txt03_vrecebido.setFocus()
        if pagamento == '2':
            menu.txt03_pagamento.setText('CARTÃO CRÉDITO')
            menu.txt03_vrecebido.setText(f'{subtotal:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
            menu.txt03_troco.setText('0,00')
            menu.btn03_conf_venda.setFocus()
        if pagamento == '3':
            menu.txt03_pagamento.setText('CARTÃO DÉBITO')
            menu.txt03_vrecebido.setText(f'{subtotal:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
            menu.txt03_troco.setText('0,00')
            menu.btn03_conf_venda.setFocus()
        if pagamento == '4':
            menu.txt03_pagamento.setText('PIX')
            menu.txt03_vrecebido.setText(f'{subtotal:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
            menu.txt03_troco.setText('0,00')
            menu.btn03_conf_venda.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao setar o campo!')


def troco():
    try:
        if menu.txt03_vrecebido.text() == '':
            return
        subtotal = float(menu.txt03_subtotal.text().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        v_recebido = float(menu.txt03_vrecebido.text().replace('.', '_').replace('_','').replace(',','.'))#FLOAT
        tro  = v_recebido - subtotal
        menu.txt03_troco.setText(f'{tro:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        menu.btn03_conf_venda.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao calcular o valor!')


def alter_estoque():
    try:
        if menu.txt03_qtd.text() == ''.strip():
            return
        if menu.txt03_estoque.text() == '':
            return
        id_produto = menu.txt03_id_produto.text().strip()
        estoque = int(menu.txt03_estoque.text().strip())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(F"UPDATE tab_produto SET estoque = '{estoque}' WHERE id = {id_produto}");
        banco.commit()
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta!')


###################################################TELA DE CUPON NÃO FISCAL#############################################


def gera_cupon():
    try:
        id = menu.txt03_idvenda.text()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_venda WHERE id_venda = {id}')
        dados_lidos = cursor.fetchall()
        cursor.execute(f'SELECT * FROM tab_pagamento WHERE id_pagamento = {id}')
        formapag = cursor.fetchall()
        cupon.lst_cupon.addItem('{:=^50}'.format(' SUA EMPRESA '))
        cupon.lst_cupon.addItem('{:=^40}'.format('''Rua Novo Horizonte Nº3435-Parque Vitória / Angelim
        Cep:64.017-760 - Teresina-Pi
        Fone:(86)9 9452-0423'''))
        cupon.lst_cupon.addItem('=' * 50)
        cupon.lst_cupon.addItem('{}'.format('IDV''{:>80}'.format('ITEM''{:>70}'.format('DESCRIÇÃO''{:>50}'.format('QTD''{:>25}'.format('UNI''{:>10}'.format('TOTAL')))))))
        for i in range(0, len(dados_lidos)):
            cupon.lst_cupon.addItem('{}'.format(f'{dados_lidos[i][0]}''{:>45}'.format(f'{dados_lidos[i][2]}')))
            cupon.lst_cupon.addItem('{:>113}'.format(f'{dados_lidos[i][1]}''{:>98}'.format(
                f'{dados_lidos[i][3]}''{:>33}'.format(
                    f'{dados_lidos[i][4]}''{:>13}'.format(f'{dados_lidos[i][5]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))))#REAL
        cupon.lst_cupon.addItem('-' * 75)
        for j in range(0, len(formapag)):
            cupon.lst_cupon.addItem('{}'.format('VALOR TOTAL R$''{:>95}'.format(f'{formapag[j][4]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
            cupon.lst_cupon.addItem('{}'.format('VALOR A PAGAR R$''{:>91}'.format(f'{formapag[j][4]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
            cupon.lst_cupon.addItem('{}'.format('FORMA DE PAGAMENTO''{:>66}'.format('VALOR PAGO R$')))
            cupon.lst_cupon.addItem('{:^0}'.format(f'{formapag[j][1]}''{:>108}'.format(f'{formapag[j][2]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
            cupon.lst_cupon.addItem('{}'.format('TROCO''{:>113}'.format(f'{formapag[j][3]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
        cupon.lst_cupon.addItem('-' * 75)
        cupon.lst_cupon.addItem('{}'.format(formapag[j][5]))
        cupon.lst_cupon.addItem('{}'.format('OPERADOR:''{:>15}'.format(dados_lidos[i][6])))
        cupon.lst_cupon.addItem('{:=^50}'.format(' CUPON NÃO FISCAL '))
        cupon.lst_cupon.addItem('')
        cupon.lst_cupon.addItem('{}'.format('Desenvolvedor: F.Neponuceno (86)9 9452-0423'))
        cupon.lst_cupon.addItem('-' * 75)
        cupon.show()
    except:
        QMessageBox.about(menu,'Alerta','Erro ao emitir cupon não fiscal!')


def pdf_cupon():
    try:
        data = datetime.now()
        data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')
        id = menu.txt03_idvenda.text()
        soma = cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_venda WHERE id_venda = {id}')
        dados_lidos = cursor.fetchall()
        cursor.execute(f'SELECT * FROM tab_pagamento WHERE id_pagamento = {id}')
        formapag = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        RESP_EMPRESA = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Helvetica', 6)
        cnv.drawString(200, 790, f'{RESP_EMPRESA[0][0]}')
        cnv.drawString(200, 780, f'{RESP_EMPRESA[0][1]}')
        cnv.drawString(200, 770, f'CEP {RESP_EMPRESA[0][2]}')
        cnv.drawString(200, 760, f'{RESP_EMPRESA[0][3]}')
        cnv.drawString(200, 750, f'CPF/CNPJ {RESP_EMPRESA[0][4]}')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 740, f'==========================================')
        cnv.drawString(200, 730, f'IDV ITEM DESCRIÇÃO               QTD     UNI    TOTAL')
        cnv.drawString(200, 720, f'-------------------------------------------------------------------------')
        for i in range(0,len(dados_lidos)):
            y += 17
            cnv.setFont('Helvetica', 6)
            cnv.drawString(200, 730 - y, f'{dados_lidos[i][0]}') # codigo
            cnv.drawString(236, 730 - y, f'{dados_lidos[i][2]}') # descrição
            cnv.drawString(215, 722 - y, f'{dados_lidos[i][1]}') # item
            cnv.drawString(318, 722 - y, f'{dados_lidos[i][3]}') # qtd
            cnv.drawString(347, 722 - y, f'{dados_lidos[i][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL) # unitario
            cnv.drawString(372, 722 - y,  f'{dados_lidos[i][5]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL) # total
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 714 - y, '-------------------------------------------------------------------------')
        for j in range(0,len(formapag)):
            cnv.setFont('Helvetica', 6)
            cnv.drawString(200, 705 - y, 'Valor Total R$')
            cnv.drawString(372, 705 - y, f'{formapag[j][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 695 - y, 'Valor a Pagar R$')
            cnv.drawString(372, 695 - y, f'{formapag[j][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 685 - y, 'Forma de Pagamento')
            cnv.drawString(355, 685 - y, 'Valor Pago R$')
            cnv.drawString(200, 675 - y, f'{formapag[j][1]}')
            cnv.drawString(372, 675 - y, f'{formapag[j][2]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 665 - y, 'Troco')
            cnv.drawString(372, 665 - y, f'{formapag[j][3]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 657 - y, '-------------------------------------------------------------------------')
        cnv.drawString(200, 647 - y, 'Data')
        cnv.drawString(220, 647 - y, f'{formapag[j][5]}')
        cnv.drawString(270, 647 - y, 'Hora/Brasília')
        cnv.drawString(325, 647 - y, f'{data}')
        cnv.drawString(200, 637 - y, 'Operador:')
        cnv.drawString(240, 637 - y, f'{dados_lidos[i][6]}')
        cnv.drawString(200, 627 - y, '============ CUPON NÃO FISCAL ============')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 617 - y, 'Desenvolvedor: F.Neponuceno (86)9 9452-0423')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 607 - y, '-------------------------------------------------------------------------')
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def fecha_cupon():
    try:
        cupon.close()
        menu.txt03_idvenda.setText('')
        menu.txt03_id_produto.setText('')
        menu.txt03_item.setText('')
        menu.txt03_descricao.setText('')
        menu.txt03_qtd.setText('')
        menu.txt03_uni.setText('')
        menu.txt03_total.setText('')
        menu.txt03_estoque.setText('')
        menu.txt03_pagamento.setText('')
        menu.txt03_vrecebido.setText('')
        menu.txt03_troco.setText('')
        menu.txt03_subtotal.setText('')
        menu.lst03_listaintens.clear()
        cupon.lst_cupon.clear()
        menu.lbl03_status.setText('CAIXA LIVRE!')
        menu.txt03_idvenda.setFocus()
    except:
        QMessageBox.about(menu,'Alerta', 'Erro !')


def excluir_item():
    try:
        id_venda = menu.txt03_idvenda.text()
        item = menu.txt03_num_item.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_venda WHERE id_venda = {id_venda} AND item = {item}')
        resposta = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tab_produto WHERE descricao = '{resposta[0][2]}'")
        estoque = cursor.fetchall()
        msg = QMessageBox()
        msg.setWindowTitle(f'{resposta[0][2]}')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE ITEM?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            qtd = resposta[0][3]
            total = resposta[0][5]
            subtotal = float(menu.txt03_subtotal.text().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            subtotal = subtotal - total
            menu.txt03_subtotal.setText(f'{subtotal:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
            stok = estoque[0][3]
            stok = stok + qtd
            cursor.execute(F"UPDATE tab_produto SET estoque = '{stok}' WHERE descricao = '{resposta[0][2]}'");
            cursor.execute(f'DELETE FROM tab_venda WHERE id_venda = {id_venda} AND item = {item} ')
            banco.commit()
            banco.close()
            menu.txt03_num_item.setText('')
            menu.txt03_descricao.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao excluir item !')


def cancelar_venda():
    try:
        msg = QMessageBox()
        msg.setWindowTitle('CANCELAR VENDA!')
        msg.setInformativeText('DESEJA REALMENTE CANCELAR ESTA VENDA?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            id_venda = menu.txt03_idvenda.text()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT descricao, qtd FROM tab_venda WHERE id_venda = '{id_venda}'")
            resposta = cursor.fetchall()
            for i in range(0, len(resposta)):
                produto = resposta[i][0]
                qtd = resposta[i][1]
                cursor.execute(f"SELECT estoque FROM tab_produto WHERE descricao = '{produto}'")
                resposta2 = cursor.fetchall()
                resposta2 = resposta2[0][0]
                estoque = qtd + resposta2
                cursor.execute(F"UPDATE tab_produto SET estoque = '{estoque}' WHERE descricao = '{produto}'");
            cursor.execute(f'DELETE FROM tab_venda WHERE id_venda = {id_venda}')
            banco.commit()
            banco.close()
            msg = QMessageBox()
            msg.setWindowTitle('CANCELAMENTO!')
            msg.setInformativeText('CANCELAMENTO REALIZADO COM SUCESSO!')
            msg.exec()
            menu.txt03_idvenda.setText('')
            menu.txt03_item.setText('')
            menu.txt03_uni.setText('')
            menu.txt03_total.setText('')
            menu.txt03_estoque.setText('')
            menu.txt03_num_item.setText('')
            menu.txt03_subtotal.setText('')
            menu.txt03_pagamento.setText('')
            menu.txt03_vrecebido.setText('')
            menu.txt03_troco.setText('')
            menu.lst03_listaintens.clear()
            menu.txt03_idvenda.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao cancelar venda!')


def cancelar_venda_posterior():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CAIXA FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('CANCELAR VENDA!')
        msg.setInformativeText('DESEJA REALMENTE CANCELAR ESTA VENDA?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            id_venda = menu.txt04_cupon.text()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT descricao, qtd FROM tab_venda WHERE id_venda = '{id_venda}'")
            resposta = cursor.fetchall()
            for i in range(0, len(resposta)):
                produto = resposta[i][0]
                qtd = resposta[i][1]
                cursor.execute(f"SELECT estoque FROM tab_produto WHERE descricao = '{produto}'")
                resposta2 = cursor.fetchall()
                resposta2 = resposta2[0][0]
                estoque = qtd + resposta2
                cursor.execute(F"UPDATE tab_produto SET estoque = '{estoque}' WHERE descricao = '{produto}'");
            cursor.execute(f'DELETE FROM tab_venda WHERE id_venda = {id_venda}')
            banco.commit()
            banco.close()
            msg = QMessageBox()
            msg.setWindowTitle('CANCELAMENTO!')
            msg.setInformativeText('CANCELAMENTO REALIZADO COM SUCESSO!')
            msg.exec()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao cancelar venda!')


def faturamento():  ##### OBS. FATURAMENTO
    try:
        data_inicio = str(menu.txt_fat_inicio.text().strip())
        data_final = str(menu.txt_fat_final.text().strip())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT f_pagamento,subtotal FROM tab_pagamento WHERE  data BETWEEN '{data_inicio}' AND '{data_final}'");
        formapag = cursor.fetchall()
        dinheiro = c_credito = c_debito = pix = subtotal = 0
        for i in range(0, len(formapag)):
            if formapag[i][0] == 'DINHEIRO':
                dinheiro += float(formapag[i][1])
            if formapag[i][0] == 'CARTÃO CRÉDITO':
                c_credito += float(formapag[i][1])
            if formapag[i][0] == 'CARTÃO DÉBITO':
                c_debito += float(formapag[i][1])
            if formapag[i][0] == 'PIX':
                pix += float(formapag[i][1])
            subtotal += float(formapag[i][1])
        DIN = str(f'{dinheiro:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        DEBITO = str(f'{c_debito:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        CREDITO = str(f'{c_credito:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        PIX = str(f'{pix:.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        TOTAL = str(f'{subtotal:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        menu.tab_faturamento.clearContents()
        menu.tab_faturamento.setRowCount(1)
        menu.tab_faturamento.setColumnCount(5)
        menu.tab_faturamento.setItem(0, 0, QtWidgets.QTableWidgetItem(str(f'{DIN}')))
        menu.tab_faturamento.setItem(0, 1, QtWidgets.QTableWidgetItem(str(f'{DEBITO}')))
        menu.tab_faturamento.setItem(0, 2, QtWidgets.QTableWidgetItem(str(f'{CREDITO}')))
        menu.tab_faturamento.setItem(0, 3, QtWidgets.QTableWidgetItem(str(f'{PIX}')))
        menu.tab_faturamento.setItem(0, 4, QtWidgets.QTableWidgetItem(str(f'{TOTAL}')))
    except:
        QMessageBox.about(menu,'Alerta','Erro ao emitir relátorio!')


def pdf_faturamento():
    try:
        data = datetime.now()
        data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' +  str(data.minute) + ':' + str(f'{data.second}')
        dados = []
        all_dados = []
        for row in range(menu.tab_faturamento.rowCount()):
            for column in range(menu.tab_faturamento.columnCount()):
                dados.append(menu.tab_faturamento.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 15)
        cnv.drawString(385, 780, 'Relatório de Faturamento')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 15
            cnv.setFont('Helvetica', 10)
            cnv.drawString(20, 710 - y, 'TOTAIS EM DINHEIRO')
            cnv.drawString(20, 695 - y, 'TOTAIS EM CARTÃO DÉBITO')
            cnv.drawString(20, 680 - y, 'TOTAIS EM CARTÃO CRÉDITO')
            cnv.drawString(20, 665 - y, 'TOTAIS EM PIX')
            cnv.drawString(20, 650 - y, 'TOTAL FATURADO')
            cnv.setFont('Helvetica', 10)
            cnv.drawString(500, 710 - y, f':R$ {lista[0]}')
            cnv.drawString(500, 695 - y, f':R$ {lista[1]}')
            cnv.drawString(500, 680 - y, f':R$ {lista[2]}')
            cnv.drawString(500, 665 - y, f':R$ {lista[3]}')
            cnv.drawString(500, 650 - y, f':R$ {lista[4]}')
            cnv.setFont('Helvetica', 15)
            cnv.drawString(128, 710 - y, '.' * 89)
            cnv.drawString(160, 695 - y, '.' * 81)
            cnv.drawString(167, 680 - y, '.' * 80)
            cnv.drawString(96, 665 - y, '.' * 97)
            cnv.drawString(112, 650 - y,'.' * 93)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def abertura_passo1():
    try:
        menu.txt_operador.setFocus()
        menu.frm_autorizacao.close()
        fechar.close()
        menu.lbl_entrada_operador.setText('DIGITE (/1) PARA ABRIR')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao abrir o caixa!')


def abertura_passo2():
    try:
        hoje = date.today()
        data = hoje.strftime('%d/%m/%Y')
        if menu.txt_operador.text().strip() == '/1':
            menu.lbl_abre_caixa.setText('ABERTURA DE CAIXA')
            menu.txt_operador.setText('')
            menu.frm_autorizacao.show()
            menu.txt_usuario_caixa.setFocus()
        if menu.txt_operador.text() == f'{data}':
            conf_abertura.show()
        else:
            return
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro no fechamento!')


def confirmar_abertura():
    try:
        menu.lbl_abre_caixa.setText('CAIXA ABERTO')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao abrir o caixa!')


def abertura_passo3():
    try:
        data_hora = datetime.now()
        data_hora = str(data_hora.day) + '/' + str(data_hora.month) + '/' + str(data_hora.year) + ' ' + str(data_hora.hour) + ':' + str(
            data_hora.minute) + ':' + str(f'{data_hora.second}')
        nome = menu.txt_usuario_caixa.text().strip()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CAIXA FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        nome = menu.txt_usuario_caixa.text().strip()
        senha = menu.txt_senha_caixa.text().strip()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT nome FROM tab_usuarios WHERE senha = {senha}');
        nome_bd = cursor.fetchall()
        nome_bd = (nome_bd[0][0])
        banco.close()
        if nome == nome_bd:
            menu.frm_autorizacao.close()
            menu.txt_usuario_caixa.setText('')
            menu.txt_senha_caixa.setText('')
            fechar.show()
            fechar.lbl_fechamento_2.setText('LANÇAR FUNDO DE CAIXA / TROCO')
            fechar.lbl_fec_dabertura.setText(f'{data_hora}')
            fechar.lbl_fec_operador_2.setText(f'{nome_bd}')
            fechar.txt_fec_fundo_2.setFocus()
            hoje = date.today()
            data = hoje.strftime('%d/%m/%Y')
            menu.lbl03_data.setText(f'{data}')
            menu.lbl03_operador.setText(f'{nome_bd}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao abrir o caixa!')


def abertura_passo4():
    try:
        msg = QMessageBox()
        msg.setWindowTitle('ABERTURA DE CAIXA')
        msg.setInformativeText('DESEJA REALMENTE ABRIR O CAIXA?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            if str(fechar.txt_fec_fundo_2.text().strip()) == '':
                menu.txt_operador.setFocus()
                fechar.close()
                return
            hoje = date.today()
            data = hoje.strftime('%d/%m/%Y')
            menu.lbl_entrada_operador.setText('DATA DA ABERTURA, TECLE ENTER!')
            menu.txt_operador.setText(f'{data}')
            menu.txt_operador.setFocus()
            data = str(menu.lbl03_data.text())
            operador = str(menu.lbl03_operador.text())
            status = 'ABERTO'
            #fundo = str(fechar.txt_fec_fundo_2.text().strip())
            fundo = float(fechar.txt_fec_fundo_2.text().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"INSERT INTO tab_abertura VALUES{operador,data,status,fundo}");
            banco.commit()
            banco.close()
            fechar.txt_fec_fundo_2.setText('')
            fechar.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro no fechamento!')


def fechamento():
    try:
        data_hora = datetime.now()
        data_hora = str(data_hora.day) + '/' + str(data_hora.month) + '/' + str(data_hora.year) + ' ' + str(
            data_hora.hour) + ':' + str(
            data_hora.minute) + ':' + str(f'{data_hora.second}')
        msg = QMessageBox()
        msg.setWindowTitle('FECHAMENTO')
        msg.setInformativeText('DESEJA REALMENTE FECHAR O CAIXA?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            dia = str(menu.lbl03_data.text())
            operador = str(menu.lbl03_operador.text())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT fundo FROM tab_abertura WHERE operador = '{operador}' AND status = 'ABERTO'")
            resposta = cursor.fetchall()
            soma = 0
            for b in range(0,len(resposta)):
                soma += float(resposta[b][0])
            cursor.execute(f"SELECT * FROM tab_venda WHERE data = '{dia}' ")
            dados_lidos = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tab_pagamento WHERE operador = '{operador}' AND status = 'ABERTO'")
            formapag = cursor.fetchall()
            dinheiro = c_credito = c_debito = pix = subtotal = 0
            for i in range(0, len(formapag)):
                ('{}'.format(f'{formapag[i][1]}''{:>45}'.format(f'{formapag[i][4]}')))
                if formapag[i][1] == 'DINHEIRO':
                    dinheiro += float(formapag[i][4])
                if formapag[i][1] == 'CARTÃO CRÉDITO':
                    c_credito += float(formapag[i][4])
                if formapag[i][1] == 'CARTÃO DÉBITO':
                    c_debito += float(formapag[i][4])
                if formapag[i][1] == 'PIX':
                    pix += float(formapag[i][4])
                subtotal += float(formapag[i][4])
            OPERADOR = str(dados_lidos[0][6])
            FUNDO = soma
            DIN = str(f'{dinheiro:,.2f}'.replace(',', '_').replace('.', ',').replace('_','.'))  # REAL
            DEBITO = str(f'{c_debito:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
            CREDITO = str(f'{c_credito:,.2f}'.replace(',', '_').replace('.', ',').replace('_','.')) # REAL
            PIX = str(f'{pix:.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')) # REAL
            SUBTOTAL = str(f'{subtotal + FUNDO:,.2f}'.replace(',', '_').replace('.', ',').replace('_','.'))  # REAL
            fechar.lbl_fechamento_2.setText(f'FINALIZANDO CAIXA')
            fechar.lbl_fec_data_2.setText(f'{data_hora}')
            fechar.lbl_fec_operador_2.setText(f'{OPERADOR}')
            fechar.lbl_fec_avista_2.setText(f'{DIN}')
            fechar.lbl_fec_debito_2.setText(f'{DEBITO}')
            fechar.lbl_fec_credito_2.setText(f'{CREDITO}')
            fechar.lbl_fec_fundo_2.setText(f'{FUNDO}')
            fechar.txt_fec_fundo_2.setText(f'{FUNDO}')
            fechar.lbl_fec_pix_2.setText(f'{PIX}')
            fechar.lbl_fec_total_2.setText(f'{SUBTOTAL}')
            fechar.txt_fec_avista_2.setFocus()
            fechar.show()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro no fechamento!')


def format_avista():
    try:
        num = moeda(str(fechar.txt_fec_avista_2.text().strip().replace('.', '').replace(',', '')))
        fechar.txt_fec_avista_2.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')


def format_debito():
    try:
        num = moeda(str(fechar.txt_fec_debito_2.text().strip().replace('.', '').replace(',', '')))
        fechar.txt_fec_debito_2.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')


def format_credito():
    try:
        num = moeda(str(fechar.txt_fec_credito_2.text().strip().replace('.', '').replace(',', '')))
        fechar.txt_fec_credito_2.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')


def format_pix():
    try:
        num = moeda(str(fechar.txt_fec_pix_2.text().strip().replace('.', '').replace(',', '')))
        fechar.txt_fec_pix_2.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')


def format_fundo():
    try:
        num = moeda(str(fechar.txt_fec_fundo_2.text().strip().replace('.', '').replace(',', '')))
        fechar.txt_fec_fundo_2.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro !')


def fechamento_passo2():
    try:
        sleep(3)
        VRDIN = float(fechar.txt_fec_avista_2.text().replace('.', '_').replace('_','').replace(',','.')) # FLOAT
        VRDEBITO = str(fechar.txt_fec_debito_2.text().replace('.', '_').replace('_','').replace(',','.')) # FLOAT
        VRCREDITO = str(fechar.txt_fec_credito_2.text().replace('.', '_').replace('_','').replace(',','.')) # FLOAT
        VRPIX = str(fechar.txt_fec_pix_2.text().replace('.', '_').replace('_','').replace(',','.')) # FLOAT
        VRFUNDO = str(fechar.txt_fec_fundo_2.text())
        SUBTOT = float(VRDIN) + float(VRDEBITO) + float(VRCREDITO) + float(VRPIX) + float(VRFUNDO)
        SUBTOT = str(f'{SUBTOT:,.2f}'.replace(',', '_').replace('.', ',').replace('_','.'))# REAL
        fechar.txt_fec_total_2.setText(f'{SUBTOT}')
        FUNDO = float(fechar.lbl_fec_total_2.text().replace('.', '_').replace('_', '').replace(',', '.')) # FLOAT
        SUB = float(SUBTOT.replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
        if SUB >= FUNDO:
            QUEBRA = float(SUB) - float(FUNDO)
        else:
            QUEBRA = 0
        if FUNDO >= SUB:
            NEGATIVO = float(FUNDO) - float(SUB)
        else:
            NEGATIVO = 0
        QUEBRA = str(f'{QUEBRA:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        NEGATIVO = str(f'{NEGATIVO:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
        fechar.txt_fec_quebra_2.setText(f'{QUEBRA}')
        fechar.txt_fec_negativo_2.setText(f'{NEGATIVO}')
        if float(NEGATIVO.replace('.', '_').replace('_', '').replace(',', '.')) > 0:
            msg = QMessageBox()
            msg.setWindowTitle('FECHAMENTO')
            msg.setInformativeText(f'VOCÊ TEM SALDO NEGATIVO DE R$ {NEGATIVO} SERÁ GERADO UM RECIBO! ')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            resp = msg.exec()
            if resp == QMessageBox.Yes:
                NEGATIVO = float(NEGATIVO.replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
                SUB = SUB + NEGATIVO
                SUB = str(f'{SUB:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL
                fechar.txt_fec_total_2.setText(f'{SUB}')
                sleep(1)
                OPERADOR = str(fechar.lbl_fec_operador_2.text().strip())
                data = datetime.now()
                data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' + str(
                data.minute) + ':' + str(f'{data.second}')
                extenso = float(f'{NEGATIVO:,.2f}')
                num_extenso = num2words(extenso,lang='pt-br')
                NEGATIVO = f'{NEGATIVO:0>3,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')#REAL
                cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
                webbrowser.open('pdf_nomes.pdf')
                banco = sqlite3.connect('banco02.db')
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM tab_empresa ")
                dados_lidos = cursor.fetchall()
                cnv.setFont('Helvetica', 10)
                cnv.drawImage('logo.jpg', 20, 730, width=100, height=65)  ## IMAGEM DO RECIBO
                cnv.roundRect(8, 720, 424, 100, 10)  ## MOUDURA DO CABEÇALHO DO RECIBO
                cnv.drawString(130, 790, f'{dados_lidos[0][0]}')
                cnv.drawString(130, 775, f'{dados_lidos[0][1]}')
                cnv.drawString(130, 760, f'{dados_lidos[0][2]}')
                cnv.drawString(130, 745, f'{dados_lidos[0][3]}')
                cnv.drawString(130, 730, f'{dados_lidos[0][4]}')
                cnv.setFont('Times-Bold', 20)
                cnv.roundRect(435, 720, 150, 100, 10),cnv.drawString(450, 790, f'RECIBO ')  ## MOUDURA DO NUMERO DO RECIBO
                cnv.drawString(450, 750, f'CAIXA')
                cnv.roundRect(8, 450, 577, 267, 10)  ## MOUDURA DO CORPO DO RECIBO
                cnv.drawString(392, 688, 'R$ '),cnv.roundRect(425, 680, 150, 30, 10)  ## MOUDURA DO VALOR DO RECIBO
                cnv.drawString(450, 688,f'{NEGATIVO}')
                cnv.roundRect(18, 645, 557, 25, 5) ## MOUDURA DA DESCRIÇÃO 1
                cnv.setFont('Helvetica', 10)
                cnv.drawString(28, 654, f'RECEBI(EMOS) DE {OPERADOR.upper()}')
                cnv.roundRect(18, 615, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 2
                cnv.drawString(28, 625, f'A QUANTIA DE R$:   {num_extenso.upper()}')
                cnv.roundRect(18, 585, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 3
                cnv.drawString(28, 595, f'REF. SALDO NEGATIVO DE CAIXA.')
                cnv.roundRect(18, 525, 557, 55, 5)  ## MOUDURA DA DESCRIÇÃO 4
                cnv.drawString(25, 540, f'RECEBEDOR:  {dados_lidos[0][0]}')
                cnv.drawString(25, 530, f'DOCUMENTO: {dados_lidos[0][4]}')
                cnv.drawString(330, 480, '____________________________________________')
                cnv.drawString(410, 460, 'ASSINATURA')
                #cnv.drawString(18, 480, f'DATA DO PAGAMENTO  {dat}')
                cnv.drawString(18, 460, f'TERESINA(PI),  {data}')
                cnv.save()
                DATA_ABER = str(fechar.lbl_fec_dabertura.text().strip())
                DINHEIRO = float(fechar.txt_fec_avista_2.text().strip().replace(',', ''))  # FLOAT
                DEBITO = float(fechar.txt_fec_debito_2.text().strip().replace(',', ''))  # FLOAT
                CREDITO = float(fechar.txt_fec_credito_2.text().strip().replace(',', ''))  # FLOAT
                PIX = float(fechar.txt_fec_pix_2.text().strip().replace(',', ''))  # FLOAT
                FUNDO = float(fechar.txt_fec_fundo_2.text().strip().replace(',', ''))  # FLOAT
                FUNDO = float(f'{FUNDO:.2f}')
                QUEBRA = float(fechar.txt_fec_quebra_2.text().strip().replace(',', ''))  # FLOAT
                SUBTOTAL = float(fechar.txt_fec_total_2.text().strip().replace(',', ''))  # FLOAT
                DATA_FECHA = str(fechar.lbl_fec_data_2.text().strip())
                OPERADOR = str(fechar.lbl_fec_operador_2.text().strip())
                STATUS = 'FECHADO'
                banco = sqlite3.connect('banco02.db')
                cursor = banco.cursor()
                cursor.execute(
                    f"INSERT INTO tab_fechamento VALUES{DATA_ABER, DINHEIRO, DEBITO, CREDITO, PIX, FUNDO, QUEBRA, SUBTOTAL, DATA_FECHA, OPERADOR, STATUS}");
                operador = str(menu.lbl03_operador.text())
                cursor.execute(
                    F"UPDATE tab_pagamento SET status = 'FECHADO' WHERE operador = '{operador}' AND status = 'ABERTO'");
                cursor.execute(
                    F"UPDATE tab_abertura SET status = 'FECHADO' WHERE operador = '{operador}' AND status = 'ABERTO'");
                msg = QMessageBox()
                msg.setWindowTitle('FECHAMENTO')
                msg.setInformativeText('FECHAMENTO REALIZADO COM SUCESSO!')
                msg.exec()
                banco.commit()
                banco.close()
                fechar.close()
                menu.lbl_abre_caixa.setText('CAIXA FECHADO')
                menu.txt_operador.setText('')
                fechar.lbl_fec_data_2.setText('')
                fechar.lbl_fec_operador_2.setText('')
                fechar.lbl_fec_avista_2.setText('0')
                fechar.lbl_fec_debito_2.setText('0')
                fechar.lbl_fec_credito_2.setText('0')
                fechar.lbl_fec_fundo_2.setText('0')
                fechar.lbl_fec_pix_2.setText('0')
                fechar.lbl_fec_total_2.setText('0')
                fechar.lbl_fec_dabertura.setText('')
                fechar.txt_fec_avista_2.setText('0')
                fechar.txt_fec_debito_2.setText('0')
                fechar.txt_fec_credito_2.setText('0')
                fechar.txt_fec_pix_2.setText('0')
                fechar.txt_fec_fundo_2.setText('0')
                fechar.txt_fec_quebra_2.setText('0')
                fechar.txt_fec_total_2.setText('0')
                fechar.lbl_fec_data_2.setText('')
                fechar.lbl_fec_operador_2.setText('')
                menu.txt03_idvenda.setText('')
                menu.txt03_idvenda.setFocus()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('FECHAMENTO')
            msg.setInformativeText('DESEJA REALMENTE FECHAR O CAIXA?')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            resp = msg.exec()
            if resp == QMessageBox.Yes:
                DATA_ABER = str(fechar.lbl_fec_dabertura.text().strip())
                DINHEIRO = float(fechar.txt_fec_avista_2.text().strip().replace(',', ''))  # FLOAT
                DEBITO = float(fechar.txt_fec_debito_2.text().strip().replace(',', ''))  # FLOAT
                CREDITO = float(fechar.txt_fec_credito_2.text().strip().replace(',', ''))  # FLOAT
                PIX = float(fechar.txt_fec_pix_2.text().strip().replace(',', ''))  # FLOAT
                FUNDO = float(fechar.txt_fec_fundo_2.text().strip().replace(',', ''))  # FLOAT
                QUEBRA = float(fechar.txt_fec_quebra_2.text().strip().replace(',', ''))  # FLOAT
                SUBTOTAL = float(fechar.txt_fec_total_2.text().strip().replace(',', ''))  # FLOAT
                DATA_FECHA = str(fechar.lbl_fec_data_2.text().strip())
                OPERADOR = str(fechar.lbl_fec_operador_2.text().strip())
                STATUS = 'FECHADO'
                banco = sqlite3.connect('banco02.db')
                cursor = banco.cursor()
                cursor.execute(
                    f"INSERT INTO tab_fechamento VALUES{DATA_ABER,DINHEIRO,DEBITO,CREDITO,PIX,FUNDO,QUEBRA,SUBTOTAL,DATA_FECHA,OPERADOR,STATUS}");
                operador = str(menu.lbl03_operador.text())
                cursor.execute(F"UPDATE tab_pagamento SET status = 'FECHADO' WHERE operador = '{operador}' AND status = 'ABERTO'");
                cursor.execute(F"UPDATE tab_abertura SET status = 'FECHADO' WHERE operador = '{operador}' AND status = 'ABERTO'");
                msg = QMessageBox()
                msg.setWindowTitle('FECHAMENTO')
                msg.setInformativeText('FECHAMENTO REALIZADO COM SUCESSO!')
                msg.exec()
                banco.commit()
                banco.close()
                fechar.close()
                menu.lbl_abre_caixa.setText('CAIXA FECHADO')
                menu.txt_operador.setText('')
                fechar.lbl_fec_data_2.setText('')
                fechar.lbl_fec_operador_2.setText('')
                fechar.lbl_fec_avista_2.setText('0')
                fechar.lbl_fec_debito_2.setText('0')
                fechar.lbl_fec_credito_2.setText('0')
                fechar.lbl_fec_fundo_2.setText('0')
                fechar.lbl_fec_pix_2.setText('0')
                fechar.lbl_fec_total_2.setText('0')
                fechar.lbl_fec_dabertura.setText('')
                fechar.txt_fec_avista_2.setText('0')
                fechar.txt_fec_debito_2.setText('0')
                fechar.txt_fec_credito_2.setText('0')
                fechar.txt_fec_pix_2.setText('0')
                fechar.txt_fec_fundo_2.setText('0')
                fechar.txt_fec_quebra_2.setText('0')
                fechar.txt_fec_total_2.setText('0')
                fechar.lbl_fec_data_2.setText('')
                fechar.lbl_fec_operador_2.setText('')
                menu.txt03_idvenda.setText('')
                menu.txt03_idvenda.setFocus()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro no fechamento!')


#################################################TELA DE RELATORIO DE FECHAMENTO/CAIXA##################################


def data_rela_inicial():
    try:
        data = data_formatada(str(menu.txt04_data_inicio.text().strip()))
        menu.txt04_data_inicio.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_rela_final():
    try:
        data = data_formatada(str(menu.txt04_data_final.text().strip()))
        menu.txt04_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_fat_inicial():
    try:
        data = data_formatada(str(menu.txt_fat_inicio.text().strip()))
        menu.txt_fat_inicio.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_fat_final():
    try:
        data = data_formatada(str(menu.txt_fat_final.text().strip()))
        menu.txt_fat_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def relatorio_fechamento():
    try:
        cont = contar = venda = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_fechamento')
        dados_lidos = cursor.fetchall()
        menu.lst_tab_fechamento.clearContents()
        menu.lst_tab_fechamento.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lst_tab_fechamento.setColumnCount(11)
        for i in range(0, len(dados_lidos)):

            for j in range(0, 11):
                menu.lst_tab_fechamento.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lst_tab_fechamento.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_rel_fechamento():
    try:
        if menu.txt_rel_fechamento.text() == ''.strip():
            return
        pesquisa = menu.txt_rel_fechamento.text().strip()
        venda = cont = contar = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_fechamento WHERE OPERADOR LIKE '{}%'".format(pesquisa,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.lst_tab_fechamento.clearContents()
        menu.lst_tab_fechamento.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.lst_tab_fechamento.setColumnCount(11)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 11):
                menu.lst_tab_fechamento.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.lst_tab_fechamento.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 9, QtWidgets.QTableWidgetItem(str('===')))
        menu.lst_tab_fechamento.setItem(linha, 10, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def pdf_fechamento():
    try:
        data = datetime.now()
        data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' +  str(data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.lst_tab_fechamento.rowCount()):
            for column in range(menu.lst_tab_fechamento.columnCount()):
                dados.append(menu.lst_tab_fechamento.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 15)
        cnv.drawString(385, 780, 'Relatório de Fechamento caixa')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'DATA_ABER')
            cnv.drawString(90, 710, 'DINHEIRO')
            cnv.drawString(135, 710, 'DÉBITO')
            cnv.drawString(175, 710, 'CRÉDITO')
            cnv.drawString(220, 710, 'PIX')
            cnv.drawString(265, 710, 'F_TROCO')
            cnv.drawString(320, 710, 'TOTAL')
            cnv.drawString(370, 710, 'QURBRA_CAIXA')
            cnv.drawString(440, 710, 'DATA_FECHA')
            cnv.drawString(510, 710, 'OPERADOR')
            cnv.drawString(700, 710, 'STATUS')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(90, 705 - y, f'{lista[1]}')
            cnv.drawString(135, 705 - y, f'{lista[2]}')
            cnv.drawString(175, 705 - y, f'{lista[3]}')
            cnv.drawString(220, 705 - y, f'{lista[4]}')
            cnv.drawString(265, 705 - y, f'{lista[5]}')
            cnv.drawString(325, 705 - y, f'{lista[6]}')
            cnv.drawString(370, 705 - y, f'{lista[7]}')
            cnv.drawString(440, 705 - y, f'{lista[8]}')
            cnv.drawString(510, 705 - y, f'{lista[9]}')
            cnv.drawString(700, 705 - y, f'{lista[10]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


##################################################TELA DE RELATORIO DE VENDA############################################


def relatorio_venda():
    try:
        venda = cont = contar = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_venda')
        dados_lidos = cursor.fetchall()
        menu.tab04_relatorio.clearContents()
        menu.tab04_relatorio.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab04_relatorio.setColumnCount(8)
        for i in range(0, len(dados_lidos)):
            contar += 1
            cont += int((dados_lidos[i][3]))
            venda += float((dados_lidos[i][5]))
            for j in range(0, 8):
                menu.tab04_relatorio.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab04_relatorio.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais de Itens:{contar}')))
        menu.tab04_relatorio.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais vendidos:{cont}')))
        menu.tab04_relatorio.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Valor Total em Venda:{venda:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
        menu.tab04_relatorio.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_venda():
    try:
        if menu.txt04_filtro.text() == ''.strip():
            return
        campo = menu.cbm04_filtro.currentText()
        pesquisa = menu.txt04_filtro.text().strip()
        venda = cont = contar = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_venda WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.tab04_relatorio.clearContents()
        menu.tab04_relatorio.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab04_relatorio.setColumnCount(8)
        for i in range(0, len(dados_lidos)):
            contar += 1
            cont += int((dados_lidos[i][3]))
            venda += float((dados_lidos[i][5]))
            for j in range(0, 8):
                menu.tab04_relatorio.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab04_relatorio.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais de Itens:{contar}')))
        menu.tab04_relatorio.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais vendidos:{cont}')))
        menu.tab04_relatorio.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Valor Total em Venda:{venda:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
        menu.tab04_relatorio.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def segunda_via_cupon():
    try:
        if menu.txt04_cupon.text() == '':
            return

        data = datetime.now()
        data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' + str(
            data.minute) + ':' + str(f'{data.second}')
        id = menu.txt04_cupon.text()
        soma = cont = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f'SELECT * FROM tab_venda WHERE id_venda = {id}')
        dados_lidos = cursor.fetchall()
        cursor.execute(f'SELECT * FROM tab_pagamento WHERE id_pagamento = {id}')
        formapag = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        RESP_EMPRESA = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Helvetica', 6)
        cnv.drawString(200, 790, f'{RESP_EMPRESA[0][0]}')
        cnv.drawString(200, 780, f'{RESP_EMPRESA[0][1]}')
        cnv.drawString(200, 770, f'CEP {RESP_EMPRESA[0][2]}')
        cnv.drawString(200, 760, f'{RESP_EMPRESA[0][3]}')
        cnv.drawString(200, 750, f'CPF/CNPJ {RESP_EMPRESA[0][4]}')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 740, f'==========================================')
        cnv.drawString(200, 730, f'IDV ITEM DESCRIÇÃO               QTD     UNI    TOTAL')
        cnv.drawString(200, 720, f'-------------------------------------------------------------------------')
        for i in range(0, len(dados_lidos)):
            y += 17
            cnv.setFont('Helvetica', 6)
            cnv.drawString(200, 730 - y, f'{dados_lidos[i][0]}')  # codigo
            cnv.drawString(236, 730 - y, f'{dados_lidos[i][2]}')  # descrição
            cnv.drawString(215, 722 - y, f'{dados_lidos[i][1]}')  # item
            cnv.drawString(318, 722 - y, f'{dados_lidos[i][3]}')  # qtd
            cnv.drawString(347, 722 - y, f'{dados_lidos[i][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(372, 722 - y, f'{dados_lidos[i][5]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)  # total
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 714 - y, '-------------------------------------------------------------------------')
        for j in range(0, len(formapag)):
            cnv.setFont('Helvetica', 6)
            cnv.drawString(200, 705 - y, 'Valor Total R$')
            cnv.drawString(372, 705 - y, f'{formapag[j][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 695 - y, 'Valor a Pagar R$')
            cnv.drawString(372, 695 - y, f'{formapag[j][4]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 685 - y, 'Forma de Pagamento')
            cnv.drawString(355, 685 - y, 'Valor Pago R$')
            cnv.drawString(200, 675 - y, f'{formapag[j][1]}')
            cnv.drawString(372, 675 - y, f'{formapag[j][2]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
            cnv.drawString(200, 665 - y, 'Troco')
            cnv.drawString(372, 665 - y, f'{formapag[j][3]:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))  # REAL)
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 657 - y, '-------------------------------------------------------------------------')
        cnv.drawString(200, 647 - y, 'Data')
        cnv.drawString(220, 647 - y, f'{formapag[j][5]}')
        cnv.drawString(270, 647 - y, 'Hora/Brasília')
        cnv.drawString(325, 647 - y, f'{data}')
        cnv.drawString(200, 637 - y, 'Operador:')
        cnv.drawString(240, 637 - y, f'{dados_lidos[i][6]}')
        cnv.drawString(200, 627 - y, '============ CUPON NÃO FISCAL ============')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 617 - y, 'Desenvolvedor: F.Neponuceno (86)9 9452-0423')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(200, 607 - y, '-------------------------------------------------------------------------')
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def filtro_data():
    try:
        if menu.txt04_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txt04_data_inicio.text()).strip()
        data_final = str(menu.txt04_data_final.text()).strip()
        venda = cont = contar = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_venda WHERE  data BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.tab04_relatorio.clearContents()
        menu.tab04_relatorio.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab04_relatorio.setColumnCount(8)
        for i in range(0, len(dados_lidos)):
            contar += 1
            cont += int((dados_lidos[i][3]))
            venda += float((dados_lidos[i][5]))
            for j in range(0, 8):
                menu.tab04_relatorio.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab04_relatorio.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais de Itens:{contar}')))
        menu.tab04_relatorio.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais vendidos:{cont}')))
        menu.tab04_relatorio.setItem(linha, 4, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Valor Total em Venda:{venda:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))#REAL
        menu.tab04_relatorio.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab04_relatorio.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def pdf_venda():
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' +  str(data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.tab04_relatorio.rowCount()):
            for column in range(menu.tab04_relatorio.columnCount()):
                dados.append(menu.tab04_relatorio.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(385, 790, 'Relatório de Vendas')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'código')
            cnv.drawString(50, 710, 'Item')
            cnv.drawString(75, 710, 'descrição do produto')
            cnv.drawString(240, 710, 'qtd')
            cnv.drawString(310, 710, 'v_unitario')
            cnv.drawString(360, 710, 'total')
            cnv.drawString(475, 710, 'operador')
            cnv.drawString(550, 710, 'data')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(50, 705 - y, f'{lista[1]}')
            cnv.drawString(75, 705 - y, f'{lista[2]}')
            cnv.drawString(240, 705 - y, f'{lista[3]}')
            cnv.drawString(310, 705 - y, f'{lista[4]}')
            cnv.drawString(360, 705 - y, f'{lista[5]}')
            cnv.drawString(475, 705 - y, f'{lista[6]}')
            cnv.drawString(550, 705 - y, f'{lista[7]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


###############################################CADASTRO DE COMPRAS######################################################


def gera_codigo_compra():
    try:
        menu.txt05_descricao.setFocus()
        if menu.txt05_codigo.text() != '':
            return
        lista = []
        for i in range(0,6):
            codigo = randint(0,9)
            lista.append(codigo)
        al_lista = (f'{lista[0]}{lista[1]}{lista[2]}{lista[3]}{lista[4]}{lista[5]}')
        menu.txt05_codigo.setText('CC' + f'{al_lista}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar código!')


def data_compra_inicial():
    try:
        data = data_formatada(str(menu.txt05_data_inicio.text().strip()))
        menu.txt05_data_inicio.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_compra_final():
    try:
        data = data_formatada(str(menu.txt05_data_final.text().strip()))
        menu.txt05_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def formart_valor_compra():
    try:
        num = moeda(str(menu.txt05_valor.text().strip().replace('.', '').replace(',', '')))
        menu.txt05_valor.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def format_valor_entrada():
    try:
        num = moeda(str(menu.txt05_entrada.text().strip().replace('.', '').replace(',', '')))
        menu.txt05_entrada.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_compra():
    try:
        data = data_formatada(str(menu.txt05_data.text().strip()))
        menu.txt05_data.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_venc_primeira():
    try:
        data = data_formatada(str(menu.txt05_vencimento.text().strip()))
        menu.txt05_vencimento.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def cad_compras():
    try:
        hoje = date.today()
        DATA = str(menu.txt05_data.text().strip())
        DATA_PRIMEIRA = str(menu.txt05_vencimento.text().strip())
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        CODIGO = str(menu.txt05_codigo.text().strip())
        dia = int(DATA[0:2])
        mes = int(DATA[3:5])
        ano = int(DATA[6:10])
        DATA = hoje.replace(day=dia,month=mes,year=ano)
        DESCRICAO = str(menu.txt05_descricao.text().strip().upper())
        FORNECEDOR = str(menu.txt05_fornecedor.text().strip().upper())
        VALOR = float(menu.txt05_valor.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
        ENTRADA = float(menu.txt05_entrada.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
        NUM_PARCELA = int(menu.txt05_parcela.text().strip())
        diav = int(DATA_PRIMEIRA[0:2])
        mesv = int(DATA_PRIMEIRA[3:5])
        anov = int(DATA_PRIMEIRA[6:10])
        DATA_PRIMEIRA = hoje.replace(day=diav,month=mesv,year=anov)
        INTERVALO = int(menu.txt05_intervalo.text().strip())
        if DATA_PRIMEIRA < DATA:
            msg = QMessageBox()
            msg.setWindowTitle('ALERTA!')
            msg.setInformativeText('DATA DO VENCIMENTO MENOR QUE A DATA DA COMPRA!')
            msg.exec()
            return
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        soma = 0
        if DATA == DATA_PRIMEIRA:
            STATUS = 'LIQUIDADO'
        else:
            STATUS = 'ABERTO'
        SALDO  = VALOR - ENTRADA
        for i in range(1, NUM_PARCELA + 1):
            PARCELA = SALDO / NUM_PARCELA
            soma += INTERVALO
            VENCIMENTO = DATA_PRIMEIRA + timedelta(days=soma - INTERVALO)
            PARCELA = float(f'{PARCELA:,.2f}'.replace(',',''))  # FLOAT
            SALDO = float(f'{SALDO:,.2f}'.replace(',',''))  # FLOAT
            cursor.execute(f"INSERT INTO tab_contas_apagar VALUES{CODIGO,(F'{i}/{NUM_PARCELA}'),DATA.strftime('%d/%m/%Y'),VENCIMENTO.strftime('%d/%m/%Y'),PARCELA,SALDO,STATUS}")
            banco.commit()
        VALOR = str(f'{VALOR:,.2f}'.replace(',',''))
        ENTRADA = str(f'{ENTRADA:,.2f}'.replace(',',''))
        cursor.execute(f"INSERT INTO tab_compras VALUES{CODIGO,DATA.strftime('%d/%m/%Y'),DESCRICAO,FORNECEDOR,VALOR,ENTRADA,NUM_PARCELA,VENCIMENTO.strftime('%d/%m/%Y'),INTERVALO}");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'compra lançada com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao lançar compra!')


def editar_compra():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CODIGO = str(menu.txt05_codigo.text().strip())
            DATA = str(menu.txt05_data.text().strip())
            DESCRICAO = str(menu.txt05_descricao.text().strip().upper())
            FORNECEDOR = str(menu.txt05_fornecedor.text().strip().upper())
            VALOR = float(menu.txt05_valor.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            ENTRADA = float(menu.txt05_entrada.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            NUM_PARCELA = int(menu.txt05_parcela.text().strip())
            VENCIMENTO = str(menu.txt05_vencimento.text().strip())
            INTERVALO = int(menu.txt05_intervalo.text().strip())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT * FROM tab_contas_apagar WHERE CODIGO = '{CODIGO}'")
            RESP = cursor.fetchall()
            if RESP != []:
                msg = QMessageBox()
                msg.setWindowTitle('EXISTE DUPLICATA PARA ESTA CONTA!')
                msg.setInformativeText('E NECESSÁRIO EXCLUIR AS DUPLICATAS PARA ALTERAR ESTA CONTA')
                msg.exec()
                return
            VALOR = float(f'{VALOR:,.2f}'.replace(',', ''))  # FLOAT
            ENTRADA = float(f'{ENTRADA:,.2f}'.replace(',', ''))  # FLOAT
            cursor.execute(f"UPDATE tab_compras SET DATA = '{DATA}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET DESCRICAO = '{DESCRICAO}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET FORNECEDOR = '{FORNECEDOR}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET VALOR = '{VALOR}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET ENTRADA = '{ENTRADA}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET NUM_PARCELA = '{NUM_PARCELA}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET VENCIMENTO = '{VENCIMENTO}' WHERE CODIGO = '{CODIGO}'");
            cursor.execute(f"UPDATE tab_compras SET INTERVALO = '{INTERVALO}' WHERE CODIGO = '{CODIGO}'");
            banco.commit()

            hoje = date.today()
            DATA = str(menu.txt05_data.text().strip())
            DATA_PRIMEIRA = str(menu.txt05_vencimento.text().strip())
            ano_atual = datetime.today().year
            if len(DATA) != 10 or len(DATA_PRIMEIRA) != 10 or int(DATA[6:10]) < ano_atual or int(DATA_PRIMEIRA[6:10]) < ano_atual:
                msg = QMessageBox()
                msg.setWindowTitle('ALERTA! DATA INCORRETA!')
                msg.setInformativeText('INSIRA UMA DATA VÁLIDA! EXEMPLO: 00/00/0000')
                msg.exec()
                return
            CODIGO = str(menu.txt05_codigo.text().strip())
            dia = int(DATA[0:2])
            mes = int(DATA[3:5])
            ano = int(DATA[6:10])
            DATA = hoje.replace(day=dia, month=mes, year=ano)
            VALOR = float(menu.txt05_valor.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            ENTRADA = float(menu.txt05_entrada.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))  # FLOAT
            NUM_PARCELA = int(menu.txt05_parcela.text().strip())
            diav = int(DATA_PRIMEIRA[0:2])
            mesv = int(DATA_PRIMEIRA[3:5])
            anov = int(DATA_PRIMEIRA[6:10])
            DATA_PRIMEIRA = hoje.replace(day=diav, month=mesv, year=anov)
            INTERVALO = int(menu.txt05_intervalo.text().strip())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            soma = 0
            if DATA == DATA_PRIMEIRA:
                STATUS = 'LIQUIDADO'
            else:
                STATUS = 'ABERTO'
            SALDO = VALOR - ENTRADA
            for i in range(1, NUM_PARCELA + 1):
                PARCELA = SALDO / NUM_PARCELA
                soma += INTERVALO
                VENCIMENTO = DATA_PRIMEIRA + timedelta(days=soma - INTERVALO)
                PARCELA = float(f'{PARCELA:,.2f}'.replace(',', ''))  # FLOAT
                SALDO = float(f'{SALDO:,.2f}'.replace(',', ''))  # FLOAT
                cursor.execute(f"INSERT INTO tab_contas_apagar VALUES{CODIGO, (F'{i}/{NUM_PARCELA}'), hoje.strftime('%d/%m/%Y'), VENCIMENTO.strftime('%d/%m/%Y'), PARCELA, SALDO, STATUS}")
                banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Registro alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def preencher_campos():
    try:
        retorno = menu.tab05_listar.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_compras WHERE CODIGO = '{retorno}'")
        dados_lidos = cursor.fetchall()
        menu.txt05_codigo.setText(str(dados_lidos[0][0]))
        menu.txt05_data.setText(dados_lidos[0][1])
        menu.txt05_descricao.setText(str(dados_lidos[0][2]))
        menu.txt05_fornecedor.setText(str(dados_lidos[0][3]))
        menu.txt05_valor.setText(str(f'{dados_lidos[0][4]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')) # real
        menu.txt05_entrada.setText(str(f'{dados_lidos[0][5]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')) # real
        menu.txt05_parcela.setText(str(dados_lidos[0][6]))
        menu.txt05_vencimento.setText(str(dados_lidos[0][7]))
        menu.txt05_intervalo.setText(str(dados_lidos[0][8]))
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados dados!')


def excluir_compra():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CODIGO = menu.txt05_codigo.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT * FROM tab_contas_apagar WHERE CODIGO = '{CODIGO}'")
            RESP = cursor.fetchall()
            if RESP != []:
                msg = QMessageBox()
                msg.setWindowTitle('EXISTE DUPLICATA PARA ESTA CONTA!')
                msg.setInformativeText('E NECESSÁRIO EXCLUIR AS DUPLICATAS PARA EXCLUIR ESTA CONTA')
                msg.exec()
                return
            cursor.execute(f"DELETE FROM tab_compras WHERE CODIGO = '{CODIGO}'")
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta', ' compra excluído com sucesso!')
            menu.txt05_codigo.setText('')
            menu.txt05_data.setText('')
            menu.txt05_descricao.setText('')
            menu.txt05_fornecedor.setText('')
            menu.txt05_valor.setText('')
            menu.txt05_entrada.setText('')
            menu.txt05_parcela.setText('')
            menu.txt05_vencimento.setText('')
            menu.txt05_intervalo.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao excluir dados !')


def pesquisar_compra():
    try:
        cont = total = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_compras')
        dados_lidos = cursor.fetchall()
        menu.tab05_listar.clearContents()
        menu.tab05_listar.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab05_listar.setColumnCount(9)
        for i in range(0, len(dados_lidos)):
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 9):
                menu.tab05_listar.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab05_listar.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{cont}')))
        menu.tab05_listar.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Valor Total em compras:{total:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))
        menu.tab05_listar.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_compra():
    try:
        if menu.txt05_filtro.text() == ''.strip():
            return
        campo = menu.cmb05_opcoes.currentText()
        pesquisa = menu.txt05_filtro.text().strip()
        cont = total = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_compras WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.tab05_listar.clearContents()
        menu.tab05_listar.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab05_listar.setColumnCount(9)
        for i in range(0, len(dados_lidos)):
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 9):
                menu.tab05_listar.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab05_listar.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{cont}')))
        menu.tab05_listar.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Valor Total em compras:{total:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.'))) # REAL
        menu.tab05_listar.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_compra_data():
    try:
        if menu.txt05_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txt05_data_inicio.text()).strip()
        data_final = str(menu.txt05_data_final.text()).strip()
        cont = total = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_compras WHERE  DATA BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.tab05_listar.clearContents()
        menu.tab05_listar.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab05_listar.setColumnCount(9)
        for i in range(0, len(dados_lidos)):
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 9):
                menu.tab05_listar.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        menu.tab05_listar.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 2, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{cont}')))
        menu.tab05_listar.setItem(linha, 3, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Valor Total em compras:{total:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.')))  # REAL
        menu.tab05_listar.setItem(linha, 5, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 7, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab05_listar.setItem(linha, 8, QtWidgets.QTableWidgetItem(str('===')))
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def pdf_compra():
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.tab05_listar.rowCount()):
            for column in range(menu.tab05_listar.columnCount()):
                dados.append(menu.tab05_listar.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(385, 790, 'Relatório de Compras')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'CODIGO')
            cnv.drawString(60, 710, 'DATA')
            cnv.drawString(100, 710, 'DESCRIÇÃO')
            cnv.drawString(250, 710, 'FORNECEDOR')
            cnv.drawString(385, 710, 'VALOR')
            cnv.drawString(425, 710, 'ENTRADA')
            cnv.drawString(470, 710, 'QTD_PAR')
            cnv.drawString(520, 710, 'VENC')
            cnv.drawString(560, 710, 'ITVL')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(60, 705 - y, f'{lista[1]}')
            cnv.drawString(100, 705 - y, f'{lista[2]}')
            cnv.drawString(250, 705 - y, f'{lista[3]}')
            cnv.drawString(385, 705 - y, f'{lista[4]}')
            cnv.drawString(425, 705 - y, f'{lista[5]}')
            cnv.drawString(470, 705 - y, f'{lista[6]}')
            cnv.drawString(520, 705 - y, f'{lista[7]}')
            cnv.drawString(560, 705 - y, f'{lista[8]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def nova_compra():
    try:
        menu.txt05_codigo.setText('')
        menu.txt05_data.setText('')
        menu.txt05_descricao.setText('')
        menu.txt05_fornecedor.setText('')
        menu.txt05_valor.setText('')
        menu.txt05_entrada.setText('')
        menu.txt05_parcela.setText('')
        menu.txt05_vencimento.setText('')
        menu.txt05_intervalo.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro!')

##############################################TELA DE CONTAS A PAGAR####################################################


def data_pagar_inicial():
    try:
        data = data_formatada(str(menu.txt06_data_inicial.text().strip()))
        menu.txt06_data_inicial.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_pagar_final():
    try:
        data = data_formatada(str(menu.txt06_data_final.text().strip()))
        menu.txt06_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def venc_parcela():
    try:
        data = data_formatada(str(menu.txt06_vencimento.text().strip()))
        menu.txt06_vencimento.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_pagamento():
    try:
        data = data_formatada(str(menu.txt06_data_pagto.text().strip()))
        menu.txt06_data_pagto.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def editar_conta():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CODIGO = str(menu.txt06_codigo.text().strip())
            PARCELA = str(menu.txt06_n_parcela.text().strip())
            VENCIMENTO = str(menu.txt06_vencimento.text().strip())
            STATUS = str(menu.lbl06_status.text().strip())
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            if STATUS == 'LIQUIDADO':
                msg = QMessageBox()
                msg.setWindowTitle('DUPLICATA LIQUIDADA!')
                msg.setInformativeText('NÃO E POSSIVEL ALTERAR ESTE REGISTRO!')
                msg.exec()
                return
            cursor.execute(f"UPDATE tab_contas_apagar SET VENCIMENTO = '{VENCIMENTO}' WHERE PARCELA = '{PARCELA}' AND CODIGO = '{CODIGO}'");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Registro alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def vencimento():
    try:
        hoje = date.today()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT VENCIMENTO FROM tab_contas_apagar WHERE STATUS = 'ABERTO' ")
        VENC = cursor.fetchall()
        menu.lbl06_alerta.setText('')
        menu.lbl06_alerta.setStyleSheet(u"""QLabel{color: rgb(255, 255, 255);background-color: rgb(, , );}""")
        menu.lbl06_alerta2.setText('')
        menu.lbl06_alerta2.setStyleSheet(u"""QLabel{color: rgb(255, 255, 255);background-color: rgb(, , );}""")
        for i in range(0,len(VENC)):
            dia = int(VENC[i][0][0:2])
            mes = int(VENC[i][0][3:5])
            ano = int(VENC[i][0][6:10])
            VENCIMENTO = hoje.replace(day=dia, month=mes, year=ano)
            dif = VENCIMENTO - hoje
            if dif.days >= 0 and dif.days <= 5:
                menu.lbl06_alerta2.setText(f"EXISTE DUPLICATA COM MENOS DE {dif.days} DIA(S) PRO VENCIMENTO!")
                menu.lbl06_alerta2.setStyleSheet(u"""QLabel{color: rgb(0, 0, 0);background-color: rgb(255, 255, 0);}""")
            if dif.days < 0:
                menu.lbl06_alerta.setText(f" EXISTE DUPLICATA VENCIDA À {dif.days} DIA(S)".replace('-',''))
                menu.lbl06_alerta.setStyleSheet(u"""QLabel{color: rgb(255, 255, 255);background-color: rgb(255, 0, 0);}""")
    except:
        QMessageBox.about(menu, 'Alerta', 'não foi possível alterar os dados!')

def pre_campos_conta():
    try:
        retorno = menu.tab06_pesquisa.selectionModel().currentIndex().siblingAtColumn(1).data()
        codigo = menu.tab06_pesquisa.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_contas_apagar WHERE PARCELA = '{retorno}'")
        dados_lidos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tab_pag_conta WHERE codigo = '{codigo}'")
        pago = cursor.fetchall()
        menu.txt06_codigo.setText(str(dados_lidos[0][0]))
        menu.txt06_n_parcela.setText(dados_lidos[0][1])
        menu.txt06_data.setText(str(dados_lidos[0][2]))
        menu.txt06_vencimento.setText(str(dados_lidos[0][3]))
        menu.txt06_valor.setText(str(f'{dados_lidos[0][4]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.txt06_v_fatura.setText(str(f'{dados_lidos[0][5]:,.2f}').replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.lbl06_status.setText(str(dados_lidos[0][6]))
        if str(menu.lbl06_status.text().strip()) == 'LIQUIDADO':
            menu.txt06_data_pagto.setText(str(pago[0][1]))
            menu.txt06_valor_pgto.setText(str(pago[0][2]))
        else:
            menu.txt06_data_pagto.setText('')
            menu.txt06_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados dados!')


def excluir_conta_pagto():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUÍDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            CODIGO = menu.txt06_codigo.text().strip()
            PARCELA = menu.txt06_n_parcela.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"DELETE FROM tab_contas_apagar WHERE CODIGO = '{CODIGO}' AND PARCELA = '{PARCELA}'")
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta', ' conta excluído com sucesso!')
            menu.txt06_codigo.setText('')
            menu.txt06_data.setText('')
            menu.txt06_vencimento.setText('')
            menu.txt06_valor.setText('')
            menu.txt06_v_fatura.setText('')
            menu.txt06_n_parcela.setText('')
            menu.lbl06_status.setText('')
            menu.txt06_data_pagto.setText('')
            menu.txt06_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao excluir dados !')


def pesuisar_conta():
    try:
        cont = total = liq = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_contas_apagar')
        dados_lidos = cursor.fetchall()
        menu.tab06_pesquisa.clearContents()
        menu.tab06_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab06_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'LIQUIDADO':
                liq += float((dados_lidos[i][4]))
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 7):
                menu.tab06_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))#REAL
        menu.tab06_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{total}')))
        menu.tab06_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de contas:{cont}')))
        menu.tab06_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais pagas:{liq}')))
        menu.tab06_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl06_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_conta():
    try:
        if menu.txt06_filtro.text() == ''.strip():
            return
        campo = menu.cmb06_data.currentText()
        pesquisa = menu.txt06_filtro.text().strip()
        cont = total = liq = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_contas_apagar WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.tab06_pesquisa.clearContents()
        menu.tab06_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab06_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'LIQUIDADO':
                liq += float((dados_lidos[i][4]))
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 7):
                menu.tab06_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.tab06_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais apagar:{total}')))
        menu.tab06_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de contas:{cont}')))
        menu.tab06_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais pagas:{liq}')))
        menu.tab06_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl06_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_conta_data():
    try:
        if menu.txt06_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txt06_data_inicial.text()).strip()
        data_final = str(menu.txt06_data_final.text()).strip()
        cont = total = liq = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_contas_apagar WHERE  VENCIMENTO BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.tab06_pesquisa.clearContents()
        menu.tab06_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab06_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'LIQUIDADO':
                liq += float((dados_lidos[i][4]))
            cont += 1
            total += float((dados_lidos[i][4]))
            for j in range(0, 7):
                menu.tab06_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.tab06_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab06_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais apagar:{total}')))
        menu.tab06_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de contas:{cont}')))
        menu.tab06_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais pagas:{liq}')))
        menu.tab06_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl06_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def pdf_conta_pagto():
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        dados = []
        all_dados = []
        for row in range(menu.tab06_pesquisa.rowCount()):
            for column in range(menu.tab06_pesquisa.columnCount()):
                dados.append(menu.tab06_pesquisa.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(360, 790, 'Relatório Contas a pagar')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'CODIGO')
            cnv.drawString(70, 710, 'PARC')
            cnv.drawString(130, 710, 'EMISSÃO')
            cnv.drawString(200, 710, 'VENC')
            cnv.drawString(290, 710, 'VALOR')
            cnv.drawString(430, 710, 'TOTAL')
            cnv.drawString(530, 710, 'Status')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(70, 705 - y, f'{lista[1]}')
            cnv.drawString(130, 705 - y, f'{lista[2]}')
            cnv.drawString(200, 705 - y, f'{lista[3]}')
            cnv.drawString(290, 705 - y, f'{lista[4]}')
            cnv.drawString(430, 705 - y, f'{lista[5]}')
            cnv.drawString(530, 705 - y, f'{lista[6]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA

        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def nova_conta_pagto():
    try:
        menu.txt06_codigo.setText('')
        menu.txt06_data.setText('')
        menu.txt06_vencimento.setText('')
        menu.txt06_valor.setText('')
        menu.txt06_v_fatura.setText('')
        menu.txt06_n_parcela.setText('')
        menu.lbl06_status.setText('')
        menu.txt06_data_pagto.setText('')
        menu.txt06_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao limpar campos!')


def format_pag_conta():
    try:
        num = moeda(str(menu.txt06_valor_pgto.text().strip().replace('.', '').replace(',', '')))
        menu.txt06_valor_pgto.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def pag_conta():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        codigo = str(menu.txt06_codigo.text().strip())
        parcela = str(menu.txt06_n_parcela.text().strip())
        data = str(menu.txt06_data_pagto.text().strip())
        valor = float(menu.txt06_valor.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))
        valor_pagto = float(menu.txt06_valor_pgto.text().strip().replace('.', '_').replace('_', '').replace(',', '.'))
        if str(menu.lbl06_status.text().strip()) == 'LIQUIDADO':
            QMessageBox.about(menu, 'Alerta', 'Esta conta ja esta liquidada,tente outra!')
            return
        if valor_pagto == valor:
            menu.lbl06_status.setText('LIQUIDADO')
        if valor_pagto < valor:
            menu.lbl06_status.setText('PARCIAL')
        status = str(menu.lbl06_status.text().strip())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_pag_conta VALUES{codigo,data,str(valor_pagto)}");
        cursor.execute(f"UPDATE tab_contas_apagar SET STATUS = '{status}' WHERE CODIGO = '{codigo}' AND PARCELA = '{parcela}'");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'pagamento realizado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao pagar conta!')


#def recibo_pag():
    #try:
        #data = datetime.now()
        #data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        #data.minute) + ':' + str(f'{data.second}')
        #codigo = str(menu.txt06_codigo.text()).strip()
        #dat = str(menu.txt06_data_pagto.text()).strip()
        #valor = float(menu.txt06_valor_pgto.text())
        #descricao = str(menu.txt06_descricao.text()).strip()
        #fornecedor = str(menu.txt06_fornecedor.text()).strip()
        #extenso = valor
        #num_extenso = num2words(extenso,lang='pt-br')
        #valor = f'{valor:0>3,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')#REAL
        #cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        #webbrowser.open('pdf_nomes.pdf')
        #banco = sqlite3.connect('banco02.db')
        #cursor = banco.cursor()
        #cursor.execute(f"SELECT * FROM tab_empresa ")
        #dados_lidos = cursor.fetchall()
        #cnv.setFont('Helvetica', 10)
        #cnv.drawImage('logo.jpg', 20, 730, width=100, height=65)  ## IMAGEM DO RECIBO
        #cnv.roundRect(8, 720, 424, 100, 10)  ## MOUDURA DO CABEÇALHO DO RECIBO
        #cnv.drawString(130, 790, f'{dados_lidos[0][0]}')
        #cnv.drawString(130, 775, f'{dados_lidos[0][1]}')
        #cnv.drawString(130, 760, f'{dados_lidos[0][2]}')
        #cnv.drawString(130, 745, f'{dados_lidos[0][3]}')
        #cnv.drawString(130, 730, f'{dados_lidos[0][4]}')
        #cnv.setFont('Times-Bold', 20)
        #cnv.roundRect(435, 720, 150, 100, 10),cnv.drawString(450, 790, f'RECIBO ')  ## MOUDURA DO NUMERO DO RECIBO
        #cnv.drawString(450, 750, f'{codigo}')
        #cnv.roundRect(8, 450, 577, 267, 10)  ## MOUDURA DO CORPO DO RECIBO
        #cnv.drawString(392, 688, 'R$ '),cnv.roundRect(425, 680, 150, 30, 10)  ## MOUDURA DO VALOR DO RECIBO
        #cnv.drawString(450, 688,f'{valor}')
        #cnv.roundRect(18, 645, 557, 25, 5) ## MOUDURA DA DESCRIÇÃO 1
        #cnv.setFont('Helvetica', 10)
        #cnv.drawString(28, 654, f'RECEBI(EMOS) DE {dados_lidos[0][0]}')
        #cnv.roundRect(18, 615, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 2
        #cnv.drawString(28, 625, f'A QUANTIA DE R$:   {num_extenso.upper()}')
        #cnv.roundRect(18, 585, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 3
        #cnv.drawString(28, 595, f'REF. {descricao}')
        #cnv.roundRect(18, 525, 557, 55, 5)  ## MOUDURA DA DESCRIÇÃO 4
        #cnv.drawString(25, 540, f'RECEBEDOR:  {fornecedor}')
        #cnv.drawString(25, 530, 'DOCUMENTO:')
        #cnv.drawString(330, 480, '____________________________________________')
        #cnv.drawString(410, 460, 'ASSINATURA')
        #cnv.drawString(18, 480, f'DATA DO PAGAMENTO  {dat}')
        #cnv.drawString(18, 460, f'TERESINA(PI),  {data}')
        #cnv.save()
    #except:
        #QMessageBox.about(menu, 'Alerta', 'erro ao gerar recibo!')


#################################################TELA DE CADASTRO DE CONTA A RECEBER####################################


def codigo_conta_receber():
    try:
        if menu.txt07_codigo.text() != '':
            return
        lista = []
        for i in range(0,6):
            codigo = randint(0,9)
            lista.append(codigo)
        al_lista = (f'{lista[0]}{lista[1]}{lista[2]}{lista[3]}{lista[4]}{lista[5]}')
        menu.txt07_codigo.setText('CAR' + f'{al_lista}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar código!')


def format_valor_receber():
    try:
        num = moeda(str(menu.txt07_valor.text().strip().replace('.', '').replace(',', '')))
        menu.txt07_valor.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def format_valor_areceber():
    try:
        num = moeda(str(menu.txt07_valor_pgto.text().strip().replace('.', '').replace(',', '')))
        menu.txt07_valor_pgto.setText(f'{num}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_receber_venc():
    try:
        data = data_formatada(str(menu.txt07_vencimento.text().strip()))
        menu.txt07_vencimento.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_conta_receber():
    try:
        data = data_formatada(str(menu.txt07_data.text().strip()))
        menu.txt07_data.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_recebimento():
    try:
        data = data_formatada(str(menu.txt07_data_pagto.text().strip()))
        menu.txt07_data_pagto.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_receber_inicial():
    try:
        data = data_formatada(str(menu.txt07_data_inicial.text().strip()))
        menu.txt07_data_inicial.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def data_receber_final():
    try:
        data = data_formatada(str(menu.txt07_data_final.text().strip()))
        menu.txt07_data_final.setText(f'{data}')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


def cad_contas_receber():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        if str(menu.lbl07_status.text().strip()) != '':
            QMessageBox.about(menu, 'Alerta', 'Esta conta ja existe,tente outra!')
            return
        menu.lbl07_status.setText('EM ABERTO')
        codigo = str(menu.txt07_codigo.text().strip())
        data = str(menu.txt07_data.text().strip())
        vencimento = str(menu.txt07_vencimento.text().strip())
        valor = float(menu.txt07_valor.text().strip())
        descricao = str(menu.txt07_descricao.text().strip().upper())
        cliente = str(menu.txt07_cliente.text().strip().upper())
        status = str(menu.lbl07_status.text().strip())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_contas_receber VALUES{codigo,data,vencimento,valor,descricao,cliente,status}");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'conta lançada com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao lançar conta!')


def editar_receber():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ ALTERADO')
        msg.setInformativeText('DESEJA REALMENTE ALTERAR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            codigo = str(menu.txt07_codigo.text().strip())
            data = str(menu.txt07_data.text().strip())
            vencimento = str(menu.txt07_vencimento.text().strip())
            valor = float(menu.txt07_valor.text().strip())
            descricao = str(menu.txt07_descricao.text().strip().upper())
            cliente = str(menu.txt07_cliente.text().strip().upper())
            status = str(menu.lbl07_status.text().strip())

            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"UPDATE tab_contas_receber SET data = '{data}' WHERE codigo = '{codigo}'");
            cursor.execute(f"UPDATE tab_contas_receber SET vencimento = '{vencimento}' WHERE codigo = '{codigo}'");
            cursor.execute(f"UPDATE tab_contas_receber SET valor = '{valor}' WHERE codigo = '{codigo}'");
            cursor.execute(f"UPDATE tab_contas_receber SET descricao = '{descricao}' WHERE codigo = '{codigo}'");
            cursor.execute(f"UPDATE tab_contas_receber SET cliente = '{cliente}' WHERE codigo = '{codigo}'");
            cursor.execute(f"UPDATE tab_contas_receber SET status = '{status}' WHERE codigo = '{codigo}'");
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta','Registro alterado com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','não foi possível alterar os dados!')


def pre_campos_receber():
    try:
        retorno = menu.tab07_pesquisa.selectionModel().currentIndex().siblingAtColumn(0).data()
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_contas_receber WHERE codigo = '{retorno}'")
        dados_lidos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM tab_recebe_conta WHERE codigo = '{retorno}'")
        recebido = cursor.fetchall()
        menu.txt07_codigo.setText(str(dados_lidos[0][0]))
        menu.txt07_data.setText(dados_lidos[0][1])
        menu.txt07_vencimento.setText(str(dados_lidos[0][2]))
        menu.txt07_valor.setText(str(dados_lidos[0][3]))
        menu.txt07_descricao.setText(str(dados_lidos[0][4]))
        menu.txt07_cliente.setText(str(dados_lidos[0][5]))
        menu.lbl07_status.setText(str(dados_lidos[0][6]))
        if str(menu.lbl07_status.text().strip()) == 'RECEBIDO':
            menu.txt07_data_pagto.setText(str(recebido[0][1]))
            menu.txt07_valor_pgto.setText(str(recebido[0][2]))
        else:
            menu.txt07_data_pagto.setText('')
            menu.txt07_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao listar os dados dados!')


def excluir_conta_receber():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        msg = QMessageBox()
        msg.setWindowTitle('ESTE REGISTRO SERÁ EXCLUIDO')
        msg.setInformativeText('DESEJA REALMENTE EXCLUIR ESTE REGISTRO?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            codigo = menu.txt07_codigo.text().strip()
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"DELETE FROM tab_contas_receber WHERE codigo = '{codigo}'")
            banco.commit()
            banco.close()
            QMessageBox.about(menu, 'Alerta', ' conta excluído com sucesso!')
            menu.txt07_codigo.setText('')
            menu.txt07_data.setText('')
            menu.txt07_vencimento.setText('')
            menu.txt07_valor.setText('')
            menu.txt07_descricao.setText('')
            menu.txt07_cliente.setText('')
            menu.lbl07_status.setText('')
            menu.txt07_data_pagto.setText('')
            menu.txt07_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao excluir dados !')


def pesuisar_conta_receber():
    try:
        cont = total = liq = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM tab_contas_receber')
        dados_lidos = cursor.fetchall()
        menu.tab07_pesquisa.clearContents()
        menu.tab07_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab07_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'RECEBIDO':
                liq += float((dados_lidos[i][3]))
            cont += 1
            total += float((dados_lidos[i][3]))
            for j in range(0, 7):
                menu.tab07_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.tab07_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{total}')))
        menu.tab07_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de compras:{cont}')))
        menu.tab07_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais recebido:{liq}')))
        menu.tab07_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl07_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_conta_receber():
    try:
        if menu.txt07_filtro.text() == ''.strip():
            return
        campo = menu.cmb07_data.currentText()
        pesquisa = menu.txt07_filtro.text().strip()
        cont = total = liq =  0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM tab_contas_receber WHERE {} LIKE '{}%'".format(campo,pesquisa))
        dados_lidos = cursor.fetchall()
        menu.tab07_pesquisa.clearContents()
        menu.tab07_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab07_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'RECEBIDO':
                liq += float((dados_lidos[i][3]))
            cont += 1
            total += float((dados_lidos[i][3]))
            for j in range(0, 7):
                menu.tab07_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.tab07_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{total}')))
        menu.tab07_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de compras:{cont}')))
        menu.tab07_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais recebido:{liq}')))
        menu.tab07_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl07_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def filtrar_conta_receber_data():
    try:
        if menu.txt07_data_final.text() == ''.strip():
            return
        data_inicio = str(menu.txt07_data_inicial.text()).strip()
        data_final = str(menu.txt07_data_final.text()).strip()
        cont = total = liq = 0
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_contas_receber WHERE  data BETWEEN '{data_inicio}' AND '{data_final}'");
        dados_lidos = cursor.fetchall()
        menu.tab07_pesquisa.clearContents()
        menu.tab07_pesquisa.setRowCount(len(dados_lidos) + 1)
        linha = (len(dados_lidos))
        menu.tab07_pesquisa.setColumnCount(7)
        for i in range(0, len(dados_lidos)):
            if str((dados_lidos[i][6])) == 'RECEBIDO':
                liq += float((dados_lidos[i][3]))
            cont += 1
            total += float((dados_lidos[i][3]))
            for j in range(0, 7):
                menu.tab07_pesquisa.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        saldo = total - liq
        liq = str(f'{liq:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        saldo = str(f'{saldo:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        total = str(f'{total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
        menu.tab07_pesquisa.setItem(linha, 0, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 1, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 2, QtWidgets.QTableWidgetItem(str('===')))
        menu.tab07_pesquisa.setItem(linha, 3, QtWidgets.QTableWidgetItem(str(f'Totais comprados:{total}')))
        menu.tab07_pesquisa.setItem(linha, 4, QtWidgets.QTableWidgetItem(str(f'Totais de compras:{cont}')))
        menu.tab07_pesquisa.setItem(linha, 5, QtWidgets.QTableWidgetItem(str(f'Totais recebido:{liq}')))
        menu.tab07_pesquisa.setItem(linha, 6, QtWidgets.QTableWidgetItem(str('===')))
        menu.lbl07_saldo.setText(f'{saldo}')
        banco.close()
    except:
        QMessageBox.about(menu, 'Alerta', 'Erro ao listar os dados, tente novamente!')


def pdf_conta_receber():
    try:
        data = datetime.now()
        data = str(data.day) + ' / ' + str(data.month) + ' / ' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')
        dados = []
        all_dados = []
        for row in range(menu.tab07_pesquisa.rowCount()):
            for column in range(menu.tab07_pesquisa.columnCount()):
                dados.append(menu.tab07_pesquisa.item(row, column).text())
            all_dados.append(dados)
            dados = []
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        y = 0
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        cnv.setFont('Times-Bold', 20)
        cnv.drawString(345, 790, 'Relatório Contas a Receber')
        cnv.setFont('Helvetica', 8)
        cnv.drawString(10, 805, f'{data}')
        cnv.drawString(10, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(10, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(10, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(10, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(10, 730, f'{dados_lidos[0][4]}')
        for lista in all_dados:
            y += 10
            cnv.setFont('Helvetica', 8)
            cnv.drawString(20, 710, 'Código')
            cnv.drawString(70, 710, 'Data')
            cnv.drawString(130, 710, 'Vencimento')
            cnv.drawString(200, 710, 'Valor')
            cnv.drawString(290, 710, 'Descrição')
            cnv.drawString(430, 710, 'Cliente')
            cnv.drawString(530, 710, 'Status')
            cnv.setFont('Helvetica', 6)
            cnv.drawString(20, 705 - y, f'{lista[0]}')
            cnv.drawString(70, 705 - y, f'{lista[1]}')
            cnv.drawString(130, 705 - y, f'{lista[2]}')
            cnv.drawString(200, 705 - y, f'{lista[3]}')
            cnv.drawString(290, 705 - y, f'{lista[4]}')
            cnv.drawString(430, 705 - y, f'{lista[5]}')
            cnv.drawString(530, 705 - y, f'{lista[6]}')
        cnv.drawString(20, 710 - y, '-' * 280)
        cnv.rect(10, 30, 575, 695, fill=False, stroke=True)  ## CÓDIGO PARA GERAR A MOLDURA
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def nova_conta_receber():
    try:
        menu.txt07_codigo.setText('')
        menu.txt07_data.setText('')
        menu.txt07_vencimento.setText('')
        menu.txt07_valor.setText('')
        menu.txt07_descricao.setText('')
        menu.txt07_cliente.setText('')
        menu.lbl07_status.setText('')
        menu.txt07_data_pagto.setText('')
        menu.txt07_valor_pgto.setText('')
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao limpar campos!')


def recebe_conta():
    try:
        nome = menu.lbl01_usuario.text()
        if nome != '':
            banco = sqlite3.connect('banco02.db')
            cursor = banco.cursor()
            cursor.execute(f"SELECT CONTAS FROM tab_usuarios WHERE NOME = '{nome}'")
            permissao = cursor.fetchall()
            if (permissao[0][0]) == "N":
                msg = QMessageBox()
                msg.setWindowTitle('PERMISSÃO')
                msg.setInformativeText('USUÁRIO SEM PERMISSÃO PARA ESTA OPERAÇÃO!')
                msg.exec()
                return
        codigo = str(menu.txt07_codigo.text().strip())
        data = str(menu.txt07_data_pagto.text().strip())
        valor = float(menu.txt07_valor.text().strip())
        valor_pagto = float(menu.txt07_valor_pgto.text().strip())
        if str(menu.lbl07_status.text().strip()) == 'RECEBIDO':
            QMessageBox.about(menu, 'Alerta', 'Esta conta ja foi recebida,tente outra!')
            return
        if valor_pagto == valor:
            menu.lbl07_status.setText('RECEBIDO')
        if valor_pagto < valor:
            menu.lbl07_status.setText('PARCIAL')
        status = str(menu.lbl07_status.text().strip())
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"INSERT INTO tab_recebe_conta VALUES{codigo,data,str(valor_pagto)}");
        cursor.execute(f"UPDATE tab_contas_receber SET status = '{status}' WHERE codigo = '{codigo}'");
        banco.commit()
        banco.close()
        QMessageBox.about(menu, 'Alerta', 'débito  recebido com sucesso!')
    except:
        QMessageBox.about(menu, 'Alerta','Erro ao receber conta!')


def recibo_ceceber():
    try:
        data = datetime.now()
        data = str(data.day) + '/' + str(data.month) + '/' + str(data.year) + ' ' + str(data.hour) + ':' + str(
        data.minute) + ':' + str(f'{data.second}')

        dat = str(menu.txt07_data_pagto.text()).strip()
        codigo = str(menu.txt07_codigo.text()).strip()
        valor = float(menu.txt07_valor_pgto.text())
        descricao = str(menu.txt07_descricao.text()).strip()
        cliente = str(menu.txt07_cliente.text()).strip()
        extenso = valor
        num_extenso = num2words(extenso, lang='pt-br')
        valor = f'{valor:0>3,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        cnv = canvas.Canvas('pdf_nomes.pdf', pagesize=A4)
        webbrowser.open('pdf_nomes.pdf')
        banco = sqlite3.connect('banco02.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM tab_empresa ")
        dados_lidos = cursor.fetchall()
        cnv.setFont('Helvetica', 10)
        cnv.drawImage('logo.jpg', 20, 730, width=100, height=65)  ## IMAGEM DO RECIBO
        cnv.roundRect(8, 720, 424, 100, 10)  ## MOUDURA DO CABEÇALHO DO RECIBO
        cnv.drawString(130, 790, f'{dados_lidos[0][0]}')
        cnv.drawString(130, 775, f'{dados_lidos[0][1]}')
        cnv.drawString(130, 760, f'{dados_lidos[0][2]}')
        cnv.drawString(130, 745, f'{dados_lidos[0][3]}')
        cnv.drawString(130, 730, f'{dados_lidos[0][4]}')
        cnv.setFont('Times-Bold', 20)
        cnv.roundRect(435, 720, 150, 100, 10), cnv.drawString(450, 790, f'RECIBO ')  ## MOUDURA DO NUMERO DO RECIBO
        cnv.drawString(450, 750, f'{codigo}')
        cnv.roundRect(8, 450, 577, 267, 10)  ## MOUDURA DO CORPO DO RECIBO
        cnv.drawString(392, 688, 'R$ '), cnv.roundRect(425, 680, 150, 30, 10)  ## MOUDURA DO VALOR DO RECIBO
        cnv.drawString(450, 688, f'{valor}')
        cnv.roundRect(18, 645, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 1
        cnv.setFont('Helvetica', 10)
        cnv.drawString(28, 654, f'RECEBI(EMOS) DE {cliente}')
        cnv.roundRect(18, 615, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 2
        cnv.drawString(28, 625, f'A QUANTIA DE R$:   {num_extenso.upper()}')
        cnv.roundRect(18, 585, 557, 25, 5)  ## MOUDURA DA DESCRIÇÃO 3
        cnv.drawString(28, 595, f'REF. {descricao}')
        cnv.roundRect(18, 525, 557, 55, 5)  ## MOUDURA DA DESCRIÇÃO 4
        cnv.drawString(25, 540, f'RECEBEDOR: {dados_lidos[0][0]}')
        cnv.drawString(25, 530, f'DOCUMENTO: {dados_lidos[0][4]}')
        cnv.drawString(330, 480, '____________________________________________')
        cnv.drawString(410, 460, 'ASSINATURA')
        cnv.drawString(18, 480, f'DATA DO RECEBIMENTO  {dat}')
        cnv.drawString(18, 460, f'TERESINA(PI),  {data}')
        cnv.save()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro ao gerar pdf!')


def moeda(valor):
    try:
        if valor.strip() == '':
            return 'R$ 0,00'
        if len(valor) == 1:
            valor2 = '0,0' + valor[0]
        if len(valor) == 2:
            valor2 = '0,' + valor[0:2]
        if len(valor) == 3:
            valor2 = valor[0] + ',' + valor[1:3]
        if len(valor) == 4:
            valor2 = valor[0:2] + ',' + valor[2:4]
        if len(valor) == 5:
            valor2 = valor[0:3] + ',' + valor[3:5]
        if len(valor) == 6:
            valor2 = valor[0] + '.' + valor[1:4] + ',' + valor[4:6]
        if len(valor) == 7:
            valor2 = valor[0:2] + '.' + valor[2:5] + ',' + valor[5:7]
        if len(valor) == 8:
            valor2 = valor[0:3] + '.' + valor[3:6] + ',' + valor[6:8]
        if len(valor) == 9:
            valor2 = valor[0] + '.' + valor[1:4] + '.' + valor[4:7] + ',' + valor[7:9]
        if len(valor) == 10:
            valor2 = valor[0:2] + '.' + valor[2:5] + '.' + valor[5:8] + ',' + valor[8:10]
        if len(valor) == 11:
            valor2 = valor[0:3] + '.' + valor[3:6] + '.' + valor[6:9] + ',' + valor[9:11]
        if len(valor) == 12:
            valor2 = valor[0] + '.' + valor[1:4] + '.' + valor[4:7] + '.' + valor[7:10] + ',' + valor[10:12]
        if len(valor) > 12:
            return 'R$ 0,00'
        return valor2
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')



def data_formatada(valor):
    hoje = date.today()
    valor = valor.replace('/','')
    try:
        if len(valor) == 2:
            valor = valor[0:2] + '/'
        if len(valor) == 4:
            valor = valor[0:2] + '/' + valor[2:4] + '/'
        if len(valor) == 8:
            valor = valor[0:2] + '/' + valor[2:4] + '/' + valor[4:8]
            dia = int(valor[0:2])
            mes = int(valor[3:5])
            ano = int(valor[6:10])
            data2 = hoje.replace(day=dia, month=mes, year=ano)
        return valor
    except:
        msg = QMessageBox()
        msg.setWindowTitle('ALERTA! DATA INCORRETA!')
        msg.setInformativeText('INSIRA UMA DATA VÁLIDA!')
        msg.exec()


############################################MENU ANIMADO###########################################################


def menu_animado():
    try:
        width = menu.frm_menu.width()
        if width == 0:
            newWidth = 200
        else:
            newWidth = 0
        menu.animation = QPropertyAnimation(menu.frm_menu, b"maximumWidth")
        menu.animation.setStartValue(width)
        menu.animation.setEndValue(newWidth)
        menu.animation.setDuration(500)
        menu.animation.setEasingCurve(QEasingCurve.InOutQuart)
        menu.animation.start()
    except:
        QMessageBox.about(menu, 'Alerta', 'erro !')


#####################################COMANDOS PARA EXECULTAR AS INTERFACEs GRÁFICAS##########################
app=QtWidgets.QApplication([])
login = uic.loadUi('systembar.ui')
menu = uic.loadUi('paginas.ui')
cupon = uic.loadUi('cupon.ui')
pesquisa = uic.loadUi('pesquisa.ui')
conf_abertura = uic.loadUi('conf_abertura.ui')
fechar = uic.loadUi('fechamento.ui')
#######################################BOTÕES PARA EXIBIR AS PAGINAS#########################################
try:
    menu.btn_menu_logo.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_logo))
    menu.btn_menu_usuario.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_usuario))
    menu.btn_menu_produto.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_produto))
    menu.btn_menu_consvenda.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_consvenda))
    menu.btn_menu_contas.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_contas))
    menu.btn_menu_cliente.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_cliente))
    menu.btn_menu_pdv.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_abre_caixa))

    conf_abertura.btn_conf_abertura.clicked.connect(lambda: menu.pg_mestre_2.setCurrentWidget(menu.pg_pdv))
    conf_abertura.btn_conf_abertura.clicked.connect(conf_abertura.close)
    conf_abertura.btn_can_abertura.clicked.connect(conf_abertura.close)
    menu.btn_menu_animado.clicked.connect(menu_animado)
    menu.btn_menu_pdv.clicked.connect(abertura_passo1)
    #########################################################################################################
    menu.btn_menu_logo.clicked.connect(menu_animado)
    menu.btn_menu_usuario.clicked.connect(menu_animado)
    menu.btn_menu_produto.clicked.connect(menu_animado)
    menu.btn_menu_consvenda.clicked.connect(menu_animado)
    menu.btn_menu_pdv.clicked.connect(menu_animado)
    menu.btn_menu_contas.clicked.connect(menu_animado)
    menu.btn_menu_cliente.clicked.connect(menu_animado)
except:
    QMessageBox.about(menu, 'Alerta', 'erro ao abrir a pagina!')
#############################################################################################################
########################################BOTÕES DA TELA CADASTRO DE CLIENTE###################################
try:
    menu.btncliente_salvar.clicked.connect(cad_cliente)
    menu.btncliente_excluir.clicked.connect(excluir_cliente)
    menu.btncliente_alterar.clicked.connect(alterar_cliente)
    menu.btncliente_buscar.clicked.connect(busca_cliente)
    menu.btncliente_imprimir.clicked.connect(pdf_cliente)
    menu.btncliente_novo.clicked.connect(novo_cliente)
    menu.lstcliente_tabela.cellPressed.connect(carregar_campos_cliente)
    menu.txtcliente_buscar.editingFinished.connect(filtro_cliente)
    menu.txtcliente_data_final.editingFinished.connect(filtrar_cliente_data)
    menu.txtcliente_data.textChanged.connect(data_cliente)
    menu.txtcliente_data_inicio.textChanged.connect(data_cliente_inicial)
    menu.txtcliente_data_final.textChanged.connect(data_cliente_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')
########################################BOTOES DA TELA DE CADASTRO DE FORNECEDOR###############################
try:
    menu.btnfornecedor_salvar.clicked.connect(cad_fornecedor)
    menu.btnfornecedor_excluir.clicked.connect(excluir_fornecedor)
    menu.btnfornecedor_alterar.clicked.connect(altera_fornecedor)
    menu.btnfornecedor_buscar.clicked.connect(buscar_fornecedor)
    menu.btnfornecedor_imprimir.clicked.connect(pdf_fornecedor)
    menu.btnfornecedor_novo.clicked.connect(novo_fornecedor)
    menu.lstfornecedor_tabela.cellPressed.connect(carregar_campos_fornecedor)
    menu.txtfornecedor_buscar.editingFinished.connect(filtrar_fornecedor)
    menu.txtfornecedor_data_final.editingFinished.connect(filtrar_fornecedor_data)
    menu.txtfornecedor_cnpj.editingFinished.connect(api_cnpj)
    menu.txtfornecedor_data.textChanged.connect(data_fornecedor)
    menu.txtfornecedor_data_inicio.textChanged.connect(data_fornecedor_inicial)
    menu.txtfornecedor_data_final.textChanged.connect(data_fornecedor_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')
############################BOTÕES DA TELA DE LOGIN DE ADMINISTRADOR###################################################
try:
    login.btn_entrar.clicked.connect(chama_menu_principal)  #botão para logar como administrador
    login.btn_usuario.clicked.connect(login_usuario)  # botão para logar como usuário

except:
    QMessageBox.about(menu, 'Alerta', 'erro')
##############################BOTÕES DA TELA DE CADASTRO DE USUÁRIO######################################################
try:
    menu.btn01_cadastrar.clicked.connect(cadastrar_usuario)  # botão para cadastrar usuário
    menu.btn01_excluir.clicked.connect(excluir_usuario_senha)  #  botão para excluir senha de usuário
    menu.btn01_alterar.clicked.connect(alterar_usuarios_senha)  #  botão para alterar senha de usuário
    menu.btn01_buscar.clicked.connect(listar_usuario)
    menu.btn01_permissao.clicked.connect(alterar_permissao_usuario)
    menu.tab01_tabela.cellPressed.connect(carregar_campos_usuario)
    menu.btn_alterar_empresa.clicked.connect(alterar_empresa)
    menu.btn_buscar_empresa.clicked.connect(buscar_empresa)
    menu.btn_limpar_empresa.clicked.connect(limpar_empresa)

except:
    QMessageBox.about(menu, 'Alerta', 'erro')
##############################BOTÕES DA TELA DE CADASTRO DE PRODUTO###################################################
try:
    menu.btn02_salvar.clicked.connect(cadastrar_produto)  #  botão para cadastrar produto
    menu.btn02_pesquisar.clicked.connect(lista_dados)  # botão para listar os dados
    menu.rb02_real.clicked.connect(real)  # botao para calcular preço em real
    menu.tab02_listaproduto.cellPressed.connect(pre_campos_produto)
    menu.rb02_porcento.clicked.connect(porcento)  # botão para calcular preço em porcentagem
    menu.btn02_excluir.clicked.connect(excluir_produto)  #  botão para excluir produto
    menu.btn02_imprimir.clicked.connect(gerar_pdf)
    menu.txt02_pesquisa.textChanged.connect(filtro)  ## pesqquisa na caixa de testo
    menu.btn02_editar.clicked.connect(alterar_produto)  ## botão para alterar os dados
    menu.btn02_gerarcodigo.clicked.connect(gerar_codigo)  ## botão para alterar os dados
    menu.txt02_datafinal.editingFinished.connect(filtrar_produto_data)
    menu.btn02_novo.clicked.connect(novo_produto)
    menu.txt02_prccusto.editingFinished.connect(p_custo)
    menu.txt02_diferenca.editingFinished.connect(dif_p)
    menu.txt02_dataentrada.textChanged.connect(data_produto)
    menu.txt02_datavencimento.textChanged.connect(data_vencimento)
    pesquisa.txt08_filtro_codigo.editingFinished.connect(pesquisa_prduto_codigo)
    menu.txt02_datainicial.textChanged.connect(data_prd_inicial)
    menu.txt02_datafinal.textChanged.connect(data_prd_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')

##########################################BOTÕES DA TELA DE RELATORIO DE VENDA#####################################
try:
    menu.btn04_pesquisar.clicked.connect(relatorio_venda)
    menu.txt04_filtro.editingFinished.connect(filtrar_venda)
    menu.btn04_via_cupom.clicked.connect(segunda_via_cupon)
    menu.txt04_data_final.editingFinished.connect(filtro_data)
    menu.btn04_imprimir.clicked.connect(pdf_venda)
    menu.btn_rel_fecha_buscar.clicked.connect(relatorio_fechamento)
    menu.txt_rel_fechamento.editingFinished.connect(filtrar_rel_fechamento)
    menu.btn_rel_fecha_imprimir.clicked.connect(pdf_fechamento)
    menu.txt_fat_final.editingFinished.connect(faturamento)
    menu.btn_fat_imprimir.clicked.connect(pdf_faturamento)
    menu.btn04_can_venda.clicked.connect(cancelar_venda_posterior)
    menu.txt04_data_inicio.textChanged.connect(data_rela_inicial)
    menu.txt04_data_final.textChanged.connect(data_rela_final)
    menu.txt_fat_inicio.textChanged.connect(data_fat_inicial)
    menu.txt_fat_final.textChanged.connect(data_fat_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')
##########################################BOTÕES DA TELA DE COMPRAS#####################################################
try:
    menu.btn05_salvar.clicked.connect(cad_compras)
    menu.btn05_gerar_codigo.clicked.connect(gera_codigo_compra)
    menu.btn05_editar.clicked.connect(editar_compra)
    menu.tab05_listar.cellPressed.connect(preencher_campos)
    menu.btn05_excluir.clicked.connect(excluir_compra)
    menu.btn05_pesquisar.clicked.connect(pesquisar_compra)
    menu.txt05_filtro.editingFinished.connect(filtrar_compra)
    menu.txt05_data_final.editingFinished.connect(filtrar_compra_data)
    menu.btn05_imprimir.clicked.connect(pdf_compra)
    menu.btn05_novo.clicked.connect(nova_compra)
    menu.txt05_valor.editingFinished.connect(formart_valor_compra)
    menu.txt05_entrada.editingFinished.connect(format_valor_entrada)
    menu.txt05_data.textChanged.connect(data_compra)
    menu.txt05_data_inicio.textChanged.connect(data_compra_inicial)
    menu.txt05_data_final.textChanged.connect(data_compra_final)
    menu.txt05_vencimento.textChanged.connect(data_venc_primeira)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')

########################################BOTÕES DA TELA DE CONTAS A PAGAR################################################
try:
    menu.btn06_editar.clicked.connect(editar_conta)
    menu.tab06_pesquisa.cellPressed.connect(pre_campos_conta)
    menu.btn06_excluir.clicked.connect(excluir_conta_pagto)
    menu.btn06_pesquisar.clicked.connect(pesuisar_conta)
    menu.txt06_filtro.editingFinished.connect(filtrar_conta)
    menu.txt06_data_final.editingFinished.connect(filtrar_conta_data)
    menu.btn06_imprimir.clicked.connect(pdf_conta_pagto)
    menu.btn06_novo.clicked.connect(nova_conta_pagto)
    menu.btn_menu_contas.clicked.connect(vencimento)
    menu.btn06_pagar.clicked.connect(pag_conta)
    menu.txt06_valor_pgto.editingFinished.connect(format_pag_conta)
    menu.txt06_vencimento.textChanged.connect(venc_parcela)
    menu.txt06_data_pagto.textChanged.connect(data_pagamento)
    menu.txt06_data_inicial.textChanged.connect(data_pagar_inicial)
    menu.txt06_data_final.textChanged.connect(data_pagar_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')
############################################BOTÕES DA TELA DE CONTAS A RECEBER##########################################
try:
    menu.btn07_codigo.clicked.connect(codigo_conta_receber)
    menu.btn07_salvar.clicked.connect(cad_contas_receber)
    menu.btn07_editar.clicked.connect(editar_receber)
    menu.tab07_pesquisa.cellPressed.connect(pre_campos_receber)
    menu.btn07_excluir.clicked.connect(excluir_conta_receber)
    menu.btn07_pesquisar.clicked.connect(pesuisar_conta_receber)
    menu.txt07_filtro.editingFinished.connect(filtrar_conta_receber)
    menu.txt07_data_final.editingFinished.connect(filtrar_conta_receber_data)
    menu.btn07_imprimir.clicked.connect(pdf_conta_receber)
    menu.btn07_novo.clicked.connect(nova_conta_receber)
    menu.btn07_receber.clicked.connect(recebe_conta)
    menu.btn07_recibo.clicked.connect(recibo_ceceber)
    menu.txt07_valor.editingFinished.connect(format_valor_receber)
    menu.txt07_valor_pgto.editingFinished.connect(format_valor_areceber)
    menu.txt07_data.textChanged.connect(data_conta_receber)
    menu.txt07_vencimento.textChanged.connect(data_receber_venc)
    menu.txt07_data_pagto.textChanged.connect(data_recebimento)
    menu.txt07_data_inicial.textChanged.connect(data_receber_inicial)
    menu.txt07_data_final.textChanged.connect(data_receber_final)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')
###############################################BOTÕES DA TELA DE CAIXA##################################################
try:
    menu.txt03_descricao.editingFinished.connect(pre_campos)
    menu.txt03_qtd.editingFinished.connect(calcular_quantidade)
    menu.txt03_qtd.editingFinished.connect(alter_estoque)
    menu.txt03_qtd.editingFinished.connect(salve_venda)
    menu.txt03_qtd.editingFinished.connect(lista_intens)
    menu.txt03_pagamento.editingFinished.connect(f_pagamento)
    menu.txt03_vrecebido.editingFinished.connect(f_pagamento)
    menu.txt03_vrecebido.editingFinished.connect(troco)
    menu.txt03_idvenda.editingFinished.connect(gerar_id_venda)
    menu.btn03_fecha_caixa.clicked.connect(fechamento)
    menu.btn03_conf_venda.clicked.connect(salva_pagamento)
    menu.btn03_conf_venda.clicked.connect(gera_cupon)
    cupon.btn_cupon_cancelar.clicked.connect(fecha_cupon)
    pesquisa.txt08_filtro.editingFinished.connect(pesquisa_produto)
    pesquisa.lst08_lista.cellPressed.connect(retorna_pesquisa)###########
    menu.txt_operador.editingFinished.connect(abertura_passo2)
    menu.txt_senha_caixa.editingFinished.connect(abertura_passo3)
    fechar.btn_fec_abrir_2.clicked.connect(abertura_passo4)
    fechar.btn_fec_cancelar_2.clicked.connect(fechar.close)
    conf_abertura.btn_conf_abertura.clicked.connect(confirmar_abertura)
    fechar.btn_fec_fechar_2.clicked.connect(fechamento_passo2)
    menu.btn03_cancelar.clicked.connect(excluir_item)
    menu.btn03_can_venda.clicked.connect(cancelar_venda)
    cupon.btn_cupon_imprimir.clicked.connect(pdf_cupon)
    cupon.btn_cupon_imprimir.clicked.connect(fecha_cupon)
    fechar.txt_fec_avista_2.editingFinished.connect(format_avista)
    fechar.txt_fec_debito_2.editingFinished.connect(format_debito)
    fechar.txt_fec_credito_2.editingFinished.connect(format_credito)
    fechar.txt_fec_pix_2.editingFinished.connect(format_pix)
    fechar.txt_fec_fundo_2.editingFinished.connect(format_fundo)
except:
    QMessageBox.about(menu, 'Alerta', 'erro')

###########################################-FIM-########################################################################

login.show()
app.exec()

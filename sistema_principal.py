import pyautogui
import json
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
import time
import keyboard
import qrcode
import keyboard
import requests
from pynput.keyboard import Listener,Key
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import win32print
import win32api
import subprocess
import auto_py_to_exe
import xml.etree.ElementTree as ET
from xml.dom import minidom
#app=QtWidgets.QApplication([])
#login = uic.loadUi('systembar.ui')
#menu = uic.loadUi('progeto.ui')
#cad_usuario = uic.loadUi('cad_usuario.ui')

#imagem = qrcode.make(86994520423)  # %d/%m/%y:%h:%m:%s')
#imagem.save('primeiro_qrcode.jpg')


#process = subprocess.run('ls -lha',shell=True,check=True,stdout=subprocess.PIPE,universal_newlines=True)
#output = process.stdout
#print(output)


## FUNÇÃO PARA IMPRIMIR CUPOM

#try:
    #id = 843139
    #soma = cont = 0
    #banco = sqlite3.connect('banco02.db')
    #cursor = banco.cursor()
    #cursor.execute(f'SELECT * FROM tab_venda WHERE id_venda = {id}')
    #dados_lidos = cursor.fetchall()
    #cursor.execute(f'SELECT * FROM tab_pagamento WHERE id_pagamento = {id}')
    #formapag = cursor.fetchall()

    #print('{:=^50}'.format(' SUA EMPRESA '))
    #print('{:=^40}'.format('''Rua Novo Horizonte Nº3435-Parque Vitória / Angelim
    #Cep:64.017-760 - Teresina-Pi
    #Fone:(86)9 9452-0423'''))

    #print('='*50)
    #print('{}'.format('IDV'),end='')
    #print('{:>5}'.format('ITEM'),end='')
    #print('{:>10}'.format('DESCRIÇÃO'),end='')
    #print('{:>10}'.format('QTD'),end='')
    #print('{:>10}'.format('UNI'),end='')
    #print('{:>12}'.format('TOTAL'))
    #print('-'*50)
    #for i in range(0,len(dados_lidos)):
        #print(dados_lidos[i][0],end='   '),print('{}'.format(dados_lidos[i][2]))
        #print('{:>5}'.format(dados_lidos[i][1]), end='')
        #print('{:>22}'.format(dados_lidos[i][3]),end='')
        #print('{:11}'.format(dados_lidos[i][4]).replace('.', ','),end='')
        #print('{:12}'.format(dados_lidos[i][5]).replace('.', ','))
    #print('-'*50)
    #for j in range(0,len(formapag)):
        #print('{}'.format('Valor Total R$'),end=''),print('{:>36}'.format(formapag[j][4]).replace('.', ','))
        #print('{}'.format('Valor a Pagar R$'),end=''),print('{:>34}'.format(formapag[j][4]).replace('.', ','))
        #print('{}'.format('FORMA DE PAGAMENTO'),end=''),print('{:>32}'.format('VALOR PAGO R$'))
        #print('{:14}'.format(formapag[j][1]), end='')
        #print('{:36}'.format(formapag[j][2]).replace('.', ','))
        #print('{}'.format('Troco'),end='')
        #print('{:>45}'.format(formapag[j][3]).replace('.', ','))
    #print('-'*50)
    #print('{}'.format(formapag[j][5]))
    #print('{}'.format('Operador:'),end=' '),print('{}'.format(dados_lidos[i][6]))
    #print('{:=^50}'.format(' CUPON NÃO FISCAL '))
    #print('')


    #print('{}'.format('Desenvolvedor: F.Neponuceno (86)9 9452-0423'))
    #print('-'*50)
#except:
    #QMessageBox.about('Alerta', 'Erro ao emitir cupon não fiscal!')


##=======================================TESTE==========================================================


#app=QtWidgets.QApplication([])
#cupon = uic.loadUi('cupon.ui')

#try:##FUNÇÃO PARA VISUALIZAR CUPON NA TELA

    #cupon.lst_cupon.addItem('{:=^50}'.format(' SUA EMPRESA '))
    #cupon.lst_cupon.addItem('{:=^40}'.format('''Rua Novo Horizonte Nº3435-Parque Vitória / Angelim
    #Cep:64.017-760 - Teresina-Pi
    #Fone:(86)9 9452-0423'''))
    #cupon.lst_cupon.addItem('='*50)
    #cupon.lst_cupon.addItem('{}'.format('IDV''{:>80}'.format('ITEM''{:>70}'.format('DESCRIÇÃO''{:>50}'.format('QTD''{:>25}'.format('UNI''{:>10}'.format('TOTAL')))))))
    #for i in range(0, len(dados_lidos)):
        #cupon.lst_cupon.addItem('{}'.format(f'{dados_lidos[i][0]}''{:>45}'.format(f'{dados_lidos[i][2]}')))
        #cupon.lst_cupon.addItem('{:>113}'.format(f'{dados_lidos[i][1]}''{:>98}'.format(f'{dados_lidos[i][3]}''{:>33}'.format(f'{dados_lidos[i][4]}''{:>13}'.format(f'{dados_lidos[i][5]}').replace('.', ',')))))
    #cupon.lst_cupon.addItem('-' * 75)
    #for j in range(0,len(formapag)):
        #cupon.lst_cupon.addItem('{}'.format('VALOR TOTAL R$''{:88}'.format(formapag[j][4]).replace('.', ',')))
        #cupon.lst_cupon.addItem('{}'.format('VALOR A PAGAR R$''{:84}'.format(formapag[j][4]).replace('.', ',')))
        #cupon.lst_cupon.addItem('{}'.format('FORMA DE PAGAMENTO''{:>61}'.format('VALOR PAGO R$')))
        #cupon.lst_cupon.addItem('{:^0}'.format(f'{formapag[j][1]}''{:^166}'.format(f'{formapag[j][2]}').replace('.', ',')))
        #cupon.lst_cupon.addItem('{}'.format('TROCO''{:>111}'.format(f'{formapag[j][3]}').replace('.', ',')))
    #cupon.lst_cupon.addItem('-'*75)
    #cupon.lst_cupon.addItem('{}'.format(formapag[j][5]))
    #cupon.lst_cupon.addItem('{}'.format('OPERADOR:''{:>15}'.format(dados_lidos[i][6])))
    #cupon.lst_cupon.addItem('{:=^50}'.format(' CUPON NÃO FISCAL '))
    #cupon.lst_cupon.addItem('')
    #cupon.lst_cupon.addItem('{}'.format('Desenvolvedor: F.Neponuceno (86)9 9452-0423'))
    #cupon.lst_cupon.addItem('-'*75)
#except:
    #QMessageBox.about('Alerta', 'Erro ao emitir cupon não fiscal!')


#cupon.btn_cupon_cancelar.clicked.connect(cupon.close)
#cupon.show()
#app.exec()



##//////////////////////////////////////FUÇÃO PARA INDENTIFICAR A IMPRESSORA////////////////////////////////
#lista_impressoras = win32print.EnumPrinters(2)
#impressora = lista_impressoras[2]
#print(impressora[2])

#imp = subprocess.Popen(f"{impressora[2]}",stdin=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='UTF-8')
#imp.stdin.write('Fui enviado para a IMPRESSORA\n')
#imp.stdin.write('Essa é a segunda linha')


####################################################FUNÇÃO PARA GERAR DUPLICATA#################################

#soma = 0
#hoje = date.today()
#valor = float(input('digite o valor da nota R$'))
#dia = int(input('dia '))
#mes = int(input('digite o mes'))
#ano = int(input('digite o ano'))
#quantidade = int(input('digite a quantidade de parcelas'))
#intervalo = int(input('digite o intervalo'))
#data_primeira = hoje.replace(day=dia,month=mes,year=ano)
#for i in range(1,quantidade + 1):
    #parcela = valor / quantidade
    #soma += intervalo
    #vencimento = data_primeira + timedelta(days=soma - intervalo)
    #vencimento = vencimento.strftime("%d/%m/%Y")
    #print(f" {i}ª Parcela: Data Emissão {hoje.strftime('%d/%m/%Y')}, Data Vencimento {vencimento} Valor {parcela:,.2f}")
#dif = data_primeira - hoje
#if dif.days >= 0 <= 5:
    #print(f'faltam {dif.days} dias pro vencimento desta conta!')
#if dif.days < 0:
    #print(str(f"esta conta esta vencida à  {dif.days} dia(s)").replace('-',''))


############################################AUTOMAÇÃO GNRE######################################################


def gnre():
    xml = open("mod.xml")
    nfe = minidom.parse(xml)
##########################################DADOS DO EMITENTE#########################################################
    num_nfe = nfe.getElementsByTagName('nNF')
    CNPJ = nfe.getElementsByTagName('CNPJ')
    NOME = nfe.getElementsByTagName('xNome')
    END_AV = nfe.getElementsByTagName('xLgr')
    END_NUMERO = nfe.getElementsByTagName('nro')
    END_BAIRRO = nfe.getElementsByTagName('xBairro')
    UF = nfe.getElementsByTagName('UF')
    CIDADE = nfe.getElementsByTagName('xMun')
    CEP = nfe.getElementsByTagName('CEP')
    TELEFONE = nfe.getElementsByTagName('fone')
    CHAVE_NFe = nfe.getElementsByTagName('chNFe')
    print(num_nfe[0].firstChild.data)
    print(CNPJ[0].firstChild.data)
    print(NOME[0].firstChild.data)
    print(END_AV[0].firstChild.data)
    print(END_NUMERO[0].firstChild.data)
    print(END_BAIRRO[0].firstChild.data)
    print(UF[0].firstChild.data)
    print(CIDADE[0].firstChild.data)
    print(CEP[0].firstChild.data)
    print(TELEFONE[0].firstChild.data)
    print(CHAVE_NFe[0].firstChild.data)
###################################DADOS DO DESTINATARIO#######################################################
    DESTINATARIO = nfe.getElementsByTagName('dest')
    dado = []
    for i in DESTINATARIO:
        CPF_CNPJ = nfe.getElementsByTagName('CPF')
        UF_DEST = nfe.getElementsByTagName('UF')
        CPF_CNPJ = nfe.getElementsByTagName('x')
        NOME = nfe.getElementsByTagName('nNF')
        CID_DEST = nfe.getElementsByTagName('nNF')
        VALOR_IMPOSTO = nfe.getElementsByTagName('nNF')
        print(UF_DEST[0].firstChild.data)
        print(CPF_CNPJ[0].firstChild.data)

    #webbrowser.open('https://www.gnre.pe.gov.br:444/gnre/v/guia/digitar')
    #time.sleep(5)
    #for i in range(0,23):
        #pyautogui.press('tab')
    #pyautogui.write('RJ')
gnre()




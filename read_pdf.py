import PyPDF2 as pypdf #pip install PyPDF2
import os
#********************************************************************************#
def processa_retorna_array_arquivos(caminho):
    print(' ')
    print('######### Processa arquivos do caminho: ' + caminho)
    print(' ')
    processa_transforma_arquivos_pdf(caminho)
    

#********************************************************************************#
def processa_transforma_arquivos_pdf(caminho):

    arquivos_processados = []
    arquivos_pdf = pega_arquivos_pdf(caminho) 
    #print(pypdf.__version__)
    for arquivo_pdf in arquivos_pdf:
        with open(caminho+arquivo_pdf, 'rb') as pdf_aberto:
            arquivo_lido = pypdf.PdfReader(pdf_aberto)
            print(len(arquivo_lido.pages))
            #for pagina in arquivo_lido.pages():
                #print(pagina)
            #print(arquivo_lido.metadata.author)

            
            #for linha in linhas_arquivo:
            #    print(linha.title)
        
        #processa_paginas_pdf(arquivo_lido)
        
    return arquivos_processados

#********************************************************************************#
def processa_paginas_pdf(arquivo_lido):
    sessoes = arquivo_lido.outline()
    print(sessoes)
    #for sessao in sessoes:
    #    titulo = sessao.title 
    #    print(f"Teste:"'{titulo}')

#********************************************************************************#
def pega_arquivos_pdf(caminho):
    
    arquivos = os.listdir(caminho)
    arquivos_pdf = []
    
    for arquivo in arquivos:
        if is_pdf(arquivo):
            arquivos_pdf.append(arquivo)

    return arquivos_pdf

#********************************************************************************#
def is_pdf(arquivo):
    return '.pdf' in arquivo
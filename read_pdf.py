import PyPDF2 as pypdf #pip install PyPDF2
import os

POSICAO_PALAVRA  = 0
POSICAO_CONTADOR = 1
#********************************************************************************#
def processa_retorna_array_arquivos(caminho, destino_txt):
    processa_transforma_arquivos_pdf(caminho, destino_txt)

#********************************************************************************#
def processa_transforma_arquivos_pdf(caminho, destino_txt):

    arquivos_processados = []
    arquivos_pdf = pega_arquivos_pdf(caminho) 
    if not cria_diretorio(destino_txt):
        return
    
    palavras_recorrentes = []
    top10_palavras_recorrentes = []    
    for arquivo_pdf in arquivos_pdf:
        print("##############################################################")
        with open(caminho+arquivo_pdf, 'rb') as pdf_aberto:
            print("Lendo arquivo: "+ arquivo_pdf)
            pagina_referencias = -1
            inicio_pagina_objective = -1
            inicio_pagina_problem = -1
            inicio_pagina_method = -1
            inicio_pagina_contributes = -1

            arquivo_lido = pypdf.PdfReader(pdf_aberto)
            total_paginas = len(arquivo_lido.pages)
            lista_texto_arquivo = []
            
            for numero_pagina in range(total_paginas):
            
                texto = arquivo_lido.pages[numero_pagina].extract_text()
                lista_texto_arquivo.append(texto.splitlines())
                #for pagina in lista_texto_arquivo:
                #    for linha in pagina:
                #        adiciona_lista_palavras(palavras_recorrentes, linha)
                #if is_possivel_referencia(texto):
                #    pagina_referencias = numero_pagina
                #    print("Referencia "+arquivo_pdf+" começa na pagina: "+ str(pagina_referencias+1))
                #    adiciona_lista_palavras = False
                #else:
                #    for pagina in lista_texto_arquivo:
                #        for linha in pagina:
                #            adiciona_lista_palavras(palavras_recorrentes, linha)
                if is_possivel_referencia(texto):
                    pagina_referencias = numero_pagina
                    print("Referencia "+arquivo_pdf+" começa na pagina: "+ str(pagina_referencias+1))
                else:
                    if pagina_referencias > 0:
                        for pagina in lista_texto_arquivo:
                            for linha in pagina:
                                adiciona_lista_palavras(palavras_recorrentes, linha)

            texto_referencias = ''    
            if pagina_referencias != -1:
                for numero_pagina in range(pagina_referencias, total_paginas):
                    texto_referencias += arquivo_lido.pages[numero_pagina].extract_text()

            nome_arquivo = pega_nome_arquivo(arquivo_lido, destino_txt)
            
            print(nome_arquivo)
            with open(nome_arquivo, 'w', encoding='utf-8') as novo_arquivo:
                for linha_split in lista_texto_arquivo:
                    for linha in linha_split:
                        adiciona_lista_palavras(top10_palavras_recorrentes, linha)
#
                        novo_arquivo.write(linha + ";;")
                        novo_arquivo.write("\n")
        print("\n")
                
    top10_palavras_recorrentes = rank_top10(palavras_recorrentes)
    for palavra in top10_palavras_recorrentes:
        print(palavra)                
        
                        
    return arquivos_processados

#********************************************************************************#
def rank_top10(lista_palavras):

    lista_ordenada = sorted(lista_palavras,key=lambda x: x[1], reverse=True)
    top_10 = []
    i = 0
    for classificacao in lista_ordenada:
        #print(classificacao)
        top_10.append(classificacao)
        i = i+1
        if i > 8:
            return top_10

#********************************************************************************#
def adiciona_lista_palavras(lista_palavras, linha):
    
    lista_palavras_linha = linha.split()
    for palavra in lista_palavras_linha:

        palavra_verificar = replace_caracteres_invalido(palavra, "")
        if len(palavra_verificar) > 3 and not is_palavra_irrelevante(palavra_verificar):
            if not palavra_adicionada(lista_palavras, palavra_verificar):
                lista_palavras.append([ palavra_verificar, 1])

#********************************************************************************#
def is_palavra_irrelevante(palavra):
    
    relative_pronouns = ["that", "which", "where", "when", "why", "what", "whom", "whose"]
    for pronome in relative_pronouns:
        if palavra.upper() == pronome.upper():
            return True

    possesive_pronouns = [ "mine", "yours", "his", "hers", "theirs", "its" ]
    for pronome in possesive_pronouns:
        if palavra.upper() == pronome.upper():
            return True
        
    reflexive_pronouns = [ "myself", "yourself", "herself", "himself", "oneself", "itself", "ourselves", "themselves", "yourselves" ] 
    for pronome in reflexive_pronouns:
        if palavra.upper() == pronome.upper():
            return True    
        
    demonstrative_pronouns = [ "this", "that", "these", "those" ]
    for pronome in demonstrative_pronouns:
        if palavra.upper() == pronome.upper():
            return True        

    interrogative_pronouns = [ "who", "what", "when", "why", "where" ]
    for pronome in interrogative_pronouns:
        if palavra.upper() == pronome.upper():
            return True        

    indefinite_pronouns = [ "someone", "somebody", "somewhere", "something", "anyone", "anybody", "anywhere", "anything", "no one", "nobody", "nowhere", "everyone", "everybody", "everywhere", "everything", "each", "none", "few", "many" ]
    for pronome in indefinite_pronouns:
        if palavra.upper() == pronome.upper():
            return True            
        
    personal_pronouns = [ "i", "you", "he", "she", "we", "they", "him", "her", "he", "she", "us", "them" ]
    for pronome in personal_pronouns:
        if palavra.upper() == pronome.upper():
            return True                

    subject_pronouns = [ "I", "you", "we", "he", "she", "it", "they", "one" ]
    for pronome in subject_pronouns:
        if palavra.upper() == pronome.upper():
            return True            

    object_pronouns = [ "me", "us", "him", "her", "them" ]
    for pronome in object_pronouns:
        if palavra.upper() == pronome.upper():
            return True                    
    
    lista_preposicoes = [ "Of", "From", "Out", "By", "Against", "About", "During", "Like", "Without", "With", "Through", "Before", "After", "Under", "Between", "Among" ]
    for preposicao in lista_preposicoes:
        if palavra.upper() == preposicao.upper():
            return True

    return False

#********************************************************************************#
def segundo_valor(lista):
    return lista[POSICAO_CONTADOR]

#********************************************************************************#
def palavra_adicionada(lista_palavras, palavra):

    for classificacao in lista_palavras:
        if classificacao[POSICAO_PALAVRA] == palavra:
            classificacao[POSICAO_CONTADOR] = classificacao[POSICAO_CONTADOR]+1
            return True
        
    return False

#********************************************************************************#
def is_possivel_abstract(texto):
    return ('Abstract' in texto )

#********************************************************************************#
def is_possivel_index_Terms(texto):
    return ('Index Terms' in texto )

#********************************************************************************#
def is_possivel_objective(texto):
    return ('Objective' in texto )

#********************************************************************************#
def is_possivel_referencia(texto):
    return ('References' in texto ) or ('REFERENCES' in texto) or ("\nR\nEFERENCES" in texto)

#********************************************************************************#
def cria_diretorio(diretorio_destino):

    try:
        os.makedirs(diretorio_destino)
        print("Diretório criado:", diretorio_destino)
        return True
    
    except FileExistsError:
        print("Diretório já existe:", diretorio_destino)
        return True
    
    except Exception as e:
        print("Erro ao criar diretório:", e)

    return False

#********************************************************************************#
def pega_nome_arquivo(arquivo_lido, destino_txt):
    if not os.path.exists(destino_txt):
        os.makedirs(destino_txt)
    texto_primeira_pagina = arquivo_lido.pages[0].extract_text()
    texto_primeira_linha = texto_primeira_pagina.split('\n')[0]
    return destino_txt + replace_caracteres_invalido(texto_primeira_linha, "_") +'.txt'

#********************************************************************************#
def replace_caracteres_invalido(texto_arquivo, string_replace):
    novo_texto = texto_arquivo.replace( " ", string_replace )
    novo_texto = novo_texto.replace( ".", string_replace )
    novo_texto = novo_texto.replace( ",", string_replace )
    novo_texto = novo_texto.replace( "%", string_replace )
    novo_texto = novo_texto.replace( "[", string_replace )
    novo_texto = novo_texto.replace( "]", string_replace )
    novo_texto = novo_texto.replace( "(", string_replace )
    novo_texto = novo_texto.replace( ")", string_replace )
    return novo_texto

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
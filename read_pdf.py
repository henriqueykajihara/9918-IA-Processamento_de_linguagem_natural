import PyPDF2 as pypdf
import os
import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

POSICAO_PALAVRA  = 0
POSICAO_CONTADOR = 1

#********************************************************************************#
def processa_transforma_arquivos_pdf(caminho, destino_txt):

    arquivos_processados = []
    arquivos_pdf = pega_arquivos_pdf(caminho) 
    if not cria_diretorio(destino_txt):
        return
    arquivos_sucesso = []
    #pagina_referencias = -1
    palavras_recorrentes = []
    for arquivo_pdf in arquivos_pdf:
        palavras_recorrentes_arquivo = []
        print("##############################################################")
        with open(caminho+arquivo_pdf, 'rb') as pdf_aberto:
            print("Lendo arquivo: "+ arquivo_pdf +"\n")
            
            arquivo_lido = pypdf.PdfReader(pdf_aberto)
            total_paginas = len(arquivo_lido.pages)
            lista_texto_arquivo = []
            
            texto_inteiro = ''            
            for numero_pagina in range(total_paginas):
            
                texto = arquivo_lido.pages[numero_pagina].extract_text()
                lista_texto_arquivo.append(texto.splitlines())
                texto_inteiro += texto

            texto_referencias = ''    
            texto_introducao = ''              
            is_referencia = False 
            is_introducao = False   
            for pagina in lista_texto_arquivo:
                for linha in pagina:

                    if  is_possivel_referencia(linha):
                        is_referencia = True

                    if not is_referencia:
                        
                        #RETIRANDO A INTRODUCAO DO TEXTO
                        if is_possivel_introducao(linha):
                            #print("INICIO INTRO: " + linha)
                            is_introducao = True

                        if is_introducao and is_possivel_final_introducao(linha):
                            #print("FINAL INTRO: " + linha)
                            is_introducao = False
                        if is_introducao:
                            texto_introducao += linha + '\n'
#ESCREVE TODO O TEXTO NESTE PONTO
                        texto_inteiro += linha+ '\n'
                        adiciona_lista_palavras(palavras_recorrentes, linha)
                        adiciona_lista_palavras(palavras_recorrentes_arquivo, linha)
                    else:
#ADICIONA O TEXTO DE REFERÊNCIAS SÓ PARA TESTAR DEPOIS
                        texto_referencias += linha + '\n'

            encontrou_tudo = True
            objetivo = retorna_informacoes_objetivo(texto_introducao, texto_inteiro)
            if lista_vazia(objetivo):
                objetivo.append("OBJECTIVE - INFORMATION NOT FOUND")
                print("OBJECTIVE - INFORMATION NOT FOUND")
                encontrou_tudo = False

            problema = retorna_informacoes_problemas(texto_introducao, texto_inteiro)
            if lista_vazia(problema):
                problema.append("PROBLEM - INFORMATION NOT FOUND")
                print("PROBLEM - INFORMATION NOT FOUND")
                encontrou_tudo = False

            metodologia = retorna_informacoes(texto_inteiro, ["method", "interviews, survey, content, analysis"])
            if lista_vazia(metodologia):
                metodologia.append("METHOD - INFORMATION NOT FOUND")
                print("METHOD - INFORMATION NOT FOUND")
                encontrou_tudo = False

            contribuicao = retorna_informacoes(texto_inteiro, ["Contributions", "contributes to", "contribuitions"])
            if lista_vazia(contribuicao):
                contribuicao.append("CONTRIBUTES TO - INFORMATION NOT FOUND")
                print("CONTRIBUTES TO - INFORMATION NOT FOUND")
                encontrou_tudo = False

            texto_formatado = formata_informacoes_para_escrever(objetivo, problema, metodologia, contribuicao)
            nome_arquivo = pega_nome_arquivo(arquivo_lido, destino_txt)
            escreve_conteudo_em_arquivo_txt(nome_arquivo, texto_formatado)
            if encontrou_tudo:
                arquivos_sucesso.append(nome_arquivo)
            
    mostra_top_10(palavras_recorrentes)
                  
    print( str(len(arquivos_sucesso))+' arquivos lidos com sucesso')
    for arquivo in arquivos_sucesso:
        print(arquivo)

    return arquivos_processados

#********************************************************************************#
def formata_informacoes_para_escrever(objetivo, problema, metodologia, contribuicao):
    texto_formatado = 'Objetivo: '+ objetivo[0] + ';;\n'
    texto_formatado += 'Problema: '+ problema[0] + ';;\n'
    texto_formatado += 'Metodologia: '+ metodologia[0] + ';;\n'
    texto_formatado += 'Contribuicao: '+ contribuicao[0] + ';;\n'

    return texto_formatado
#********************************************************************************#
def retorna_informacoes_problemas(texto_introducao, texto_inteiro):

    lista_problemas = ["limitation", "issue", "problem", "challenge", "dilemma", "obstacle", "difficulty"]
    problema_sentencas = retorna_informacoes(texto_introducao, lista_problemas)
    if lista_vazia(problema_sentencas):
        problema_sentencas = retorna_informacoes(texto_inteiro ,lista_problemas)
    return problema_sentencas

#********************************************************************************#
def retorna_informacoes_objetivo(texto_introducao, texto_inteiro):
    
    lista_objetivos = [ "objective", "purposed", "purpose", "intention" ]
    objetivos_sentencas = retorna_informacoes(texto_introducao, lista_objetivos)
    if lista_vazia(objetivos_sentencas):
        objetivos_sentencas = retorna_informacoes(texto_inteiro ,lista_objetivos)
    return objetivos_sentencas
    
#********************************************************************************#
def retorna_informacoes(texto_introducao, lista_palavras_referencia):

    nlp = spacy.load("en_core_web_sm")
    documento = nlp(texto_introducao)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    lista_patterns = []
    for palavra_referencia in lista_palavras_referencia:
        lista_patterns.append(nlp(palavra_referencia))
              
    for palavra_referencia in lista_palavras_referencia:
        matcher.add(palavra_referencia, None, *lista_patterns)
    
    sentencas = []
    for sentenca in documento.sents:
        if matcher(nlp(sentenca.text)):
            sentencas.append(sentenca.text)
            if len(sentencas) > 0:
                break

    return sentencas

#********************************************************************************#
def escreve_conteudo_em_arquivo_txt(nome_arquivo, texto_inteiro):

    with open(nome_arquivo, 'w', encoding='utf-8') as novo_arquivo:
        for linha in texto_inteiro:
            novo_arquivo.write(linha)
        #novo_arquivo.write(";;")

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
def mostra_top_10(palavras_recorrentes):

    top10_palavras_recorrentes = rank_top10(palavras_recorrentes)
    print('Rank de palavras mais encontradas:')
    for palavra in top10_palavras_recorrentes:
        print(palavra)               

#********************************************************************************#
def adiciona_lista_palavras(lista_palavras, linha):
    
    lista_palavras_linha = linha.split()
    for palavra in lista_palavras_linha:

        palavra_verificar = replace_caracteres_invalido(palavra.lower(), "")
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
        
    if palavra.upper() == 'IEEE':
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
def is_possivel_referencia(texto):
    return ('References' in texto ) or ('REFERENCES' in texto) or ("\nR\nEFERENCES" in texto) or ("EFERENCES" in texto)

#********************************************************************************#
def is_possivel_introducao(texto):
    return ('INTRODUCTION' in texto)

#********************************************************************************#
def is_possivel_final_introducao(texto):
    return ('A.' in texto) or ('II.' in texto)

#********************************************************************************#
def empty_text(text):
    return text == ''

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
    texto_primeira_linha = texto_primeira_pagina.split('\n')[1]
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
    novo_texto = novo_texto.replace( "/", string_replace )
    
    return novo_texto

#********************************************************************************#
def processa_paginas_pdf(arquivo_lido):
    sessoes = arquivo_lido.outline()
    print(sessoes)

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

#********************************************************************************#
def lista_vazia(lista):
    return len(lista) == 0

#********************************************************************************#
def page_rank():
    return print("ta pra fazer")

#********************************************************************************#
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
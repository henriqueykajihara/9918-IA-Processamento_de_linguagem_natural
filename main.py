import read_pdf
import os

#********************************************************************************#
def nivelValido(nivel):
    return ( nivel in ['0', '1', '2', '3'] )
#********************************************************************************#
def main():
    
    nivel = 99
    while nivel != '0':
        read_pdf.cls()

        print('+--------------------------------------------------+')
        print('+--------- Processamento de artigos em PDF --------+')
        print('+--------------------------------------------------+')
        print('+ Selecione o tema ():                             +')
        print('+ 1 - Processamento de imagens                     +')
        print('+ 2 - Inteligência artificial                      +')
        print('+ 3 - Machine Learning                             +')
        print('+ 0 - Sair                                         +')
        print('+--------------------------------------------------+')
        nivel = input('Selecione o tema ou ZERO para sair: ')
        print('+--------------------------------------------------+\n')
        if nivelValido(nivel):
            #diretorio_raiz_arquivos = "F:/9918_ia_trabalho2/arquivos/"
            diretorio_raiz_arquivos = os.getcwd()+"/arquivos/"
            #diretorio_txt = "F:/9918_ia_trabalho2/txt/"
            diretorio_txt = diretorio_raiz_arquivos + "/txt/"
            if nivel == '1':
                opcao_selecionada_string = '1 - Processamento de imagens'
                opcao = diretorio_raiz_arquivos+"image/"
                destino_txt = diretorio_txt + "image/"
            if nivel == '2':
                opcao_selecionada_string = '2 - Inteligência artificial'
                opcao = diretorio_raiz_arquivos+"ia/"
                destino_txt = diretorio_txt+"ia/"
            if nivel == '3':
                opcao_selecionada_string = '3 - Machine Learning'
                opcao = diretorio_raiz_arquivos+"machine_learning/"
                destino_txt = diretorio_txt+"machine_learning/"

            if nivel == '0':
                opcao = '0'

            if os.path.exists(opcao):
                read_pdf.cls()
                print('+--------------------------------------------------+')
                print('Você selecionou a opção: ' + opcao_selecionada_string )
                print('+--------------------------------------------------+')
                print('+ 1 - Processar artigos pdf                        +')
                print('+ 2 - Page Rank                                    +')
                print('+ 0 - Voltar                                       +')
                print('+--------------------------------------------------+')
                opcao_processamento = input('Selecione a opção ou ZERO para sair: ')
                if opcao_processamento == '1':
                    read_pdf.processa_transforma_arquivos_pdf( opcao, destino_txt )
                    input("Pressione uma tecla para continuar...")
                elif opcao_processamento == '2':
                    palavra_procurada = input("Digite a palavra desejada:")
                    read_pdf.page_rank(destino_txt, palavra_procurada)
                    input("Pressione uma tecla para continuar...")
                elif opcao_processamento == '0':
                    nivel = 99
                    continue
            else:
                if opcao == '0':
                    print(" --- Fim do programa ---")
                    return
                else:
                    print("Arquivo " + opcao +" nao encontrado!")                   
        else:
            read_pdf.cls()
            print('Opção ',nivel,' invalida!')
        #os.system('cls')

#********************************************************************************#
if __name__ == "__main__":
    
    main()
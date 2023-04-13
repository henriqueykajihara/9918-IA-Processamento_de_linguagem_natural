
import read_pdf
import os
#********************************************************************************#
def nivelValido(nivel):
    return ( nivel in ['0', '1', '2', '3'] )
#********************************************************************************#
def main_():
    nivel = 99
    while nivel != '0':

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
        print('+--------------------------------------------------+')
        if nivelValido(nivel):
            if nivel == '1':
                opcao = "F:/9918_ia_trabalho2/arquivos/image/"
                destino_txt = "F:/9918_ia_trabalho2/txt/image/"
                print('Nivel 1111111111')
            if nivel == '2':
                opcao = "F:/9918_ia_trabalho2/arquivos/ia/"
                destino_txt = "F:/9918_ia_trabalho2/txt/ia/"
            if nivel == '3':
                opcao = "F:/9918_ia_trabalho2/arquivos/machine_learning/"
                destino_txt = "F:/9918_ia_trabalho2/txt/machine_learning/"
            if nivel == '0':
                opcao = '0'

            if os.path.exists(opcao):
                os.system('cls')
                read_pdf.processa_retorna_array_arquivos( opcao, destino_txt )
            else:
                if opcao == '0':
                    print(" --- Fim do programa :) ---")
                    return
                else:
                    print("Arquivo " + opcao +" nao encontrado!")                   
        else:
            os.system('cls')
            print('Opção ',nivel,' invalida!')
        #os.system('cls')

def main():
    read_pdf.processa_retorna_array_arquivos( "F:/9918_ia_trabalho2/arquivos/image/", "F:/9918_ia_trabalho2/txt/image/" )

#********************************************************************************#
if __name__ == "__main__":
    
    main()
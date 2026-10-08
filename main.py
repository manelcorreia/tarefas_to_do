from leitor import Leitor
from repositorio import Repositorio
from exportador import Exportador

def main():
    leitor = Leitor("tarefas_to_do.csv")
    repo = Repositorio()
    exportador = Exportador()


    tarefas = leitor.ler_ficheiro()
    for tarefa in tarefas:
        repo.tarefas.append(tarefa)

    while True:
        print("--- TAREFAS TO DO ---")
        print("1 - Adicionar tarefa")
        print("2 - Remover tarefa")
        print("3 - Mudar prioridade de uma tarefa")
        print("4 - Marcar como concluida")
        print("5 - Guardar tarefas concluidas")
        print("6 - Guardar e sair do programa")

        opcao = int(input("Opção (1 a 6): "))

        if opcao == 1:
            nome_tarefa = input("Nome do tarefa: ")
            prioridade = int(input("Prioridade: "))
            repo.nova_tarefa(nome_tarefa, prioridade)

        elif opcao == 2:
            nome_tarefa = input("Nome do tarefa: ")

        elif opcao == 3:
            nome_tarefa = input("Nome do tarefa: ")
            nova_prioridade = int(input("Nova Prioridade: "))
            repo.mudar_prioridade(nome_tarefa, nova_prioridade)

        elif opcao == 4:
            nome_tarefa = input("Nome do tarefa: ")
            repo.marcar_como_concluida(nome_tarefa)

        elif opcao == 5:
            exportador.ficheiro_tarefas_concluidas(repo.tarefas)

        elif opcao == 6:
            exportador.guardar_dados(repo.tarefas)
            break

        else:
            print("Opção inválida. Digite um número entre 1 e 6")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

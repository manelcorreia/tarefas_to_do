from engine import SessionLocal, engine
from models.tarefa_model import Base
from repository.repositorio import Repositorio
from schemas.tarefa_base_model import TarefaCreate, TarefaUpdate


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:

        repo = Repositorio(session)

        while True:
            print("--- TAREFAS TO DO ---")
            print("1 - Adicionar tarefa")
            print("2 - Remover tarefa")
            print("3 - Atualizar tarefa")
            print("4 - Ver todas as tarefas")
            print("5 - Ver tarefas concluidas")
            print("6 - Guardar e sair do programa")

            opcao = int(input("Opção (1 a 6): "))

            if opcao == 1:
                nome_tarefa = input("Nome do tarefa: ")
                prioridade = int(input("Prioridade: "))
                tarefa_schema = TarefaCreate(nome=nome_tarefa, prioridade=prioridade)
                repo.nova_tarefa(tarefa_schema)

            elif opcao == 2:
                try:
                    id_tarefa = int(input("Id da tarefa: "))
                    if repo.remover(id_tarefa):
                        print("Tarefa removida com sucesso!")
                    else:
                        print("Tarefa não encontrada")
                except ValueError:
                    print("ID tem de ser número inteiro")

            elif opcao == 3:
                try:
                    tarefa_id = int(input("Tarefa ID: "))
                except ValueError:
                    print("ID tem de ser número inteiro")
                    continue

                if not repo.obter_por_id(tarefa_id):
                    print("Tarefa não encontrada")
                    continue

                while True:
                    print("1 - Alterar nome")
                    print("2 - Alterar prioridade")
                    print("3 - Marcar como concluida")
                    print("4. Alterar tudo")
                    print("5 - Voltar")

                    sub_opcao = int(input("Opção (1 a 5): "))

                    if sub_opcao == 1:
                        novo_nome = input("Nome do tarefa: ")
                        tarefa_update = TarefaUpdate(nome=novo_nome)
                        repo.atualizar(tarefa_id,tarefa_update)

                    elif sub_opcao == 2:
                        nova_prioridade = int(input("Prioridade do tarefa: "))
                        tarefa_update = TarefaUpdate(prioridade=nova_prioridade)
                        repo.atualizar(tarefa_id,tarefa_update)

                    elif sub_opcao == 3:
                        tarefa_update = TarefaUpdate(concluida=True)
                        repo.atualizar(tarefa_id,tarefa_update)

                    elif sub_opcao == 4:
                        novo_nome = input("Nome do tarefa: ")
                        nova_prioridade = int(input("Prioridade do tarefa: "))
                        tarefa_update = TarefaUpdate(nome=novo_nome,prioridade=nova_prioridade,concluida=True)
                        repo.atualizar(tarefa_id,tarefa_update)
                        break

                    elif sub_opcao == 5:
                        break

                    else:
                        print("Opção inválida, digite entre 1 e 5")

            elif opcao == 4:
                tarefas = repo.ver_todas_tarefas()
                print("\n--- Lista de tarefas ---")
                for tarefa in tarefas:
                    print(tarefa)

            elif opcao == 5:
                concluidas = repo.ver_tarefas_concluidas()
                print("\n--- Tarefas concluidas ---")
                for tarefa in concluidas:
                    print(tarefa)

            elif opcao == 6:
                session.commit()
                break

            else:
                print("Opção inválida. Digite um número entre 1 e 8")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

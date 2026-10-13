from pydantic import ValidationError

from engine import SessionLocal, engine
from models.tarefa_model import Base
from repository.tarefa_repositorio import TarefaRepositorio
from repository.utilizador_repositorio import UtilizadorRepositorio
from schemas.tarefa_base_model import TarefaCreate, TarefaUpdate
from schemas.utilizador_base_model import UtilizadorCreate, UtilizadorUpdate


def main():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        repo_utilizador = UtilizadorRepositorio(session)

        utilizador = None

        while True:
            print("--- Bem-Vindo ---")
            print("\n1. Fazer Login")
            print("2. Fazer Registo")
            print("3. Sair")

            try:
                opcao_usuario = int(input("Opção (1 a 3): "))
            except ValueError:
                print("Opção tem de ser um número inteiro")
                continue

            if opcao_usuario == 1:
                email_utilizador = input("Digite o email do utilizador: ")
                password_utilizador = input("Digite o password do utilizador: ")

                utilizador = repo_utilizador.fazer_login(email_utilizador, password_utilizador)

                if utilizador:
                    print("Login sucesso!")
                    break

                else:
                    print("Email ou password incorretos.")

            elif opcao_usuario == 2:
                nome = input("Digite o nome: ")
                nome_utilizador = input("Digite o nome do utilizador: ")
                email_utilizador = input("Digite o email do utilizador: ")
                password_utilizador = input("Digite o password do utilizador: ")

                try:
                    dados = UtilizadorCreate(
                        nome=nome,
                        nome_utilizador=nome_utilizador,
                        email=email_utilizador,
                        password=password_utilizador,
                    )
                except ValidationError as e:
                    for erro in e.errors():
                        print(f"Erro em '{erro['loc'][0]}': {erro['msg']}")
                    continue

                if repo_utilizador.obter_por_email(dados.email):
                    print("Esse email já está registado")
                    continue

                if repo_utilizador.obter_por_nome_utilizador(dados.nome_utilizador):
                    print("Nome utilizado já está registado")
                    continue

                repo_utilizador.registar_utilizador(dados)
                print("Registo feito com sucesso! Faça login")

            elif opcao_usuario == 3:
                print("Até à próxima!")
                return

            else:
                print("Opção inválida, digite entre 1 e 3.")


        repo = TarefaRepositorio(session)

        while True:
            print("--- TAREFAS TO DO ---")
            print("1 - Adicionar tarefa")
            print("2 - Remover tarefa")
            print("3 - Atualizar tarefa")
            print("4 - Ver todas as tarefas")
            print("5 - Ver tarefas concluidas")
            print("6 - Guardar e sair do programa")

            try:
                opcao = int(input("Opção (1 a 6): "))
            except ValueError:
                print("Opção tem de ser um número inteiro")
                continue

            if opcao == 1:
                nome_tarefa = input("Nome do tarefa: ")
                if repo.obter_por_nome(utilizador.id, nome_tarefa):
                    print(f"Aviso: Já tens uma tarefa registada com o nome '{nome_tarefa}'.")
                else:
                    try:
                        prioridade = int(input("Prioridade: "))
                        tarefa_schema = TarefaCreate(nome=nome_tarefa, prioridade=prioridade, utilizador_id=utilizador.id)
                        nova_tarefa = repo.nova_tarefa(tarefa_schema)
                        print(f"Tarefa '{nova_tarefa.nome}' criada com sucesso! [ID: {nova_tarefa.id}]")


                    except ValueError as e:
                        print(f"Erro nos dados inseridos: {e}")

                    except Exception as e:
                        print(f"Erro inesperado ao criar tarefa: {e}")


            elif opcao == 2:
                try:
                    id_tarefa = int(input("Id da tarefa: "))
                    if repo.remover(utilizador.id,id_tarefa):
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

                if not repo.obter_por_id(utilizador.id, tarefa_id):
                    print("Tarefa não encontrada")
                    continue

                while True:
                    print("1 - Alterar nome")
                    print("2 - Alterar prioridade")
                    print("3 - Marcar como concluida")
                    print("4. Alterar tudo")
                    print("5 - Voltar")

                    try:
                        sub_opcao = int(input("Opção (1 a 5): "))
                    except ValueError:
                        print("Opção tem de ser um número inteiro")
                        continue

                    if sub_opcao == 1:
                        try:
                            novo_nome = input("Nome do tarefa: ")
                            tarefa_update = TarefaUpdate(nome=novo_nome)
                            repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                        except ValueError as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif sub_opcao == 2:
                        try:
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(prioridade=nova_prioridade)
                            repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                        except ValueError as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif sub_opcao == 3:
                        tarefa_update = TarefaUpdate(concluida=True)
                        repo.atualizar(utilizador.id,tarefa_id,tarefa_update)

                    elif sub_opcao == 4:
                        try:
                            novo_nome = input("Nome do tarefa: ")
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(nome=novo_nome,prioridade=nova_prioridade,concluida=True)
                            repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                            break
                        except ValueError as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif sub_opcao == 5:
                        break

                    else:
                        print("Opção inválida, digite entre 1 e 5")

            elif opcao == 4:
                tarefas = repo.ver_todas_tarefas(utilizador.id)
                if not tarefas:
                    print("Sem tarefas guardadas")

                print("\n--- Lista de tarefas ---")
                for tarefa in tarefas:
                    print(tarefa)

            elif opcao == 5:
                concluidas = repo.ver_tarefas_concluidas(utilizador.id)
                if not concluidas:
                    print("Sem tarefas guardadas")
                print("\n--- Tarefas concluidas ---")
                for tarefa in concluidas:
                    print(tarefa)

            elif opcao == 6:
                break

            else:
                print("Opção inválida. Digite um número entre 1 e 8")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

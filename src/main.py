import datetime

from pydantic import ValidationError

from src.core.engine import SessionLocal
from src.repositories.tarefa_repositorio import TarefaRepositorio
from src.repositories.utilizador_repositorio import UtilizadorRepositorio
from src.schemas.tarefa_base_model import TarefaCreate, TarefaUpdate, TarefaResponse
from src.schemas.utilizador_base_model import UtilizadorCreate, UtilizadorDetalhe, UtilizadorUpdate
from src.services.tarefa_service import TarefaService

def main():
    # Base.metadata.create_all(engine)

    with SessionLocal() as session:
        repo_utilizador = UtilizadorRepositorio(session)
        tarefa_repositorio = TarefaRepositorio(session)
        servico_tarefa = TarefaService(session, tarefa_repositorio)

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
            print("6 - Meu perfil")
            print("7 - Guardar e sair do programa")

            try:
                opcao = int(input("Opção (1 a 7): "))
            except ValueError:
                print("Opção tem de ser um número inteiro")
                continue

            if opcao == 1:
                try:
                    nome_tarefa = input("Nome do tarefa: ")
                    prioridade = int(input("Prioridade: "))
                    tarefa_schema = TarefaCreate(nome=nome_tarefa, prioridade=prioridade, utilizador_id=utilizador.id, data_registo=datetime.date.today())
                    tarefa_criada = servico_tarefa.adicionar_nova_tarefa(tarefa_schema)
                    print(f"Tarefa '{tarefa_criada.nome}' criada com sucesso")

                except ValidationError as e:
                    for erro in e.errors():
                        print(f"Erro: {erro['loc'][0]}: {erro['msg']}")
                except ValueError as e:
                    print(f"Erro: {e}")
                except Exception as e:
                    print(f"Erro inesperado: {e}")

            elif opcao == 2:
                try:
                    id_tarefa = int(input("Id da tarefa: "))
                    servico_tarefa.remover_tarefa(utilizador.id, id_tarefa)
                    print(f"Tarefa removida com sucesso")
                except ValidationError as e:
                    print(f"Erro: {e}")

                except ValueError as e:
                    print(f"Erro: {e}")

                except Exception as e:
                    print(f"Erro inesperado: {e}")

            elif opcao == 3:
                try:
                    tarefa_id = int(input("Tarefa ID: "))
                    servico_tarefa.obter_tarefa_por_id(utilizador.id, tarefa_id)
                except ValueError:
                    print(f"Opção tem de ser número inteiro")
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

                    try:
                        if sub_opcao == 1:
                            novo_nome = input("Nome do tarefa: ")
                            tarefa_update = TarefaUpdate(nome=novo_nome)
                            tarefa_atualizada = servico_tarefa.atualizar_tarefa(utilizador.id, tarefa_id, tarefa_update)
                            print(f"Nome da tarefa atualizada com sucesso para {tarefa_atualizada.nome}")

                        elif sub_opcao == 2:
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(prioridade=nova_prioridade)
                            atualizada_tarefa = servico_tarefa.atualizar_tarefa(utilizador.id, tarefa_id, tarefa_update)
                            print(f"Prioridade tarefa atualizada com sucesso para {atualizada_tarefa.prioridade}")

                        elif sub_opcao == 3:
                            tarefa_update = TarefaUpdate(concluida=True)
                            update_tarefa = servico_tarefa.atualizar_tarefa(utilizador.id,tarefa_id,tarefa_update)
                            print(f"Tarefa está concluída? {update_tarefa.concluida}")

                        elif sub_opcao == 4:
                            novo_nome = input("Nome do tarefa: ")
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(nome=novo_nome,prioridade=nova_prioridade,concluida=True)
                            tarefa_update = servico_tarefa.atualizar_tarefa(utilizador.id,tarefa_id,tarefa_update)
                            print(f"Informações da tarefa atualizados com sucesso! Nome: {tarefa_update.nome} | Prioridade: {tarefa_update.prioridade} | Concluida: {tarefa_update.concluida}")
                            break

                        elif sub_opcao == 5:
                            break

                        else:
                            print("Opção inválida, digite entre 1 e 5")

                    except ValidationError as e:
                        print(f"Erro: {e}")
                    except ValueError as e:
                        print(f"Erro: {e}")
                    except Exception as e:
                        print(f"Erro inesperado: {e}")

            elif opcao == 4:
                try:
                    tarefas = servico_tarefa.listar_todas_tarefas(utilizador.id)
                    if not tarefas:
                        print("Sem tarefas guardadas")
                    else:
                        print("\n--- Lista de tarefas ---")
                        for tarefa in tarefas:
                            estado = "[X]" if tarefa.concluida else "[ ]"
                            print(f"ID {tarefa.id}: ({estado}) {tarefa.nome} | Prioridade: {tarefa.prioridade}")

                except Exception as e:
                    print(f"Erro inesperado: {e}")

            elif opcao == 5:
                try:
                    concluidas = servico_tarefa.listar_todas_tarefas_concluidas(utilizador.id)
                    if not concluidas:
                        print("Sem tarefas guardadas")
                    else:
                        print("\n--- Tarefas concluidas ---")
                        for tarefa in concluidas:
                            print(tarefa.nome)
                except Exception as e:
                    print(f"Erro inesperado: {e}")

            elif opcao == 6:
                while True:
                    print("--- Meu Perfil ---")
                    perfil_utilizador = UtilizadorDetalhe.model_validate(utilizador)
                    print(f"Nome: {perfil_utilizador.nome}")
                    print(f"Nome Utilizador: {perfil_utilizador.nome_utilizador}")
                    print(f"Email: {perfil_utilizador.email}")
                    print(f"Número de tarefas: {len(perfil_utilizador.tarefas)}")

                    print("\n1. Alterar nome")
                    print("2. Alterar email")
                    print("3. Alterar password")
                    print("4. Apagar conta")
                    print("5. Voltar")

                    try:
                        opcao_utilizador = int(input("Opção (1 a 5): "))
                    except ValueError:
                        print("Digite um número inteiro!")
                        continue

                    if opcao_utilizador == 1:
                        try:
                            nome_novo = input("Nome: ")
                            dados_atualizacao = UtilizadorUpdate(nome=nome_novo)
                            password_confirmacao = input("Digite password para confirmar alterações: ")
                            if repo_utilizador.confirmar_com_password(utilizador.id, password_confirmacao):
                                repo_utilizador.atualizar_dados_utilizador(dados_atualizacao, utilizador)
                                print("\nAlterado com sucesso!")
                            else:
                                print("Password errada.")
                        except (ValueError, ValidationError) as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif opcao_utilizador == 2:
                        try:
                            email_novo = input("Email: ")
                            atualizacao_dados = UtilizadorUpdate(email=email_novo)

                            if repo_utilizador.obter_por_email(atualizacao_dados.email):
                                print("Esse email já se encontra em uso.")
                                continue

                            confirmacao_pass = input("Digite password para confirmar alterações: ")
                            if repo_utilizador.confirmar_com_password(utilizador.id, confirmacao_pass):
                                repo_utilizador.atualizar_dados_utilizador(atualizacao_dados, utilizador)
                                print("\nAlterado com sucesso!")
                            else:
                                print("Password errada.")
                        except (ValueError, ValidationError) as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif opcao_utilizador == 3:
                        try:
                            password_novo = input("Password: ")
                            nova_pass = UtilizadorUpdate(password=password_novo)
                            update_pass = input("Digite password para confirmar as alterações: ")
                            if repo_utilizador.confirmar_com_password(utilizador.id, update_pass):
                                repo_utilizador.atualizar_dados_utilizador(nova_pass, utilizador)
                                print("\nAlterado com sucesso!")
                            else:
                                print("Password errada.")
                        except (ValueError, ValidationError) as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif opcao_utilizador == 4:
                        try:
                            password = input("Password: ")
                            if repo_utilizador.confirmar_com_password(utilizador.id, password):
                                repo_utilizador.apagar_utilizador(utilizador)
                                print("\nConta apagada")
                                utilizador = None
                                break
                            else:
                                print("Password errada.")
                        except (ValueError, ValidationError) as e:
                            print(f"Erro nos dados inseridos: {e}")


                    elif opcao_utilizador == 5:
                        break

                    else:
                        print("Opção inválida, digite um número inteiro entre 1 e 5!")

            if utilizador is None:
                break

            elif opcao == 7:
                break

            else:
                print("Opção inválida. Digite um número entre 1 e 7")

if __name__ == '__main__':
    main()

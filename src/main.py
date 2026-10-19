from pydantic import ValidationError

from src.core.engine import SessionLocal
from src.repositories.tarefa_repositorio import TarefaRepositorio
from src.repositories.utilizador_repositorio import UtilizadorRepositorio
from src.schemas.tarefa_base_model import TarefaCreate, TarefaUpdate, TarefaResponse
from src.schemas.utilizador_base_model import UtilizadorCreate, UtilizadorDetalhe, UtilizadorUpdate


def main():
    # Base.metadata.create_all(engine)

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
            print("6 - Meu perfil")
            print("7 - Guardar e sair do programa")

            try:
                opcao = int(input("Opção (1 a 7): "))
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
                        if not nova_tarefa:
                            print("Tarefa não foi criada")
                        tarefa_response = TarefaResponse.model_validate(nova_tarefa)
                        print(f"Tarefa '{tarefa_response.nome}' criada com sucesso! [ID: {tarefa_response.id}]")


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
                            tarefa_atualizada = repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                            response_tarefa = TarefaResponse.model_validate(tarefa_atualizada)
                            print(f"Nome da tarefa atualizada com sucesso para {response_tarefa.nome}")
                        except ValueError as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif sub_opcao == 2:
                        try:
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(prioridade=nova_prioridade)
                            atualizada_tarefa = repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                            response_schema = TarefaResponse.model_validate(atualizada_tarefa)
                            print(f"Prioridade tarefa atualizada com sucesso para {response_schema.prioridade}")
                        except ValueError as e:
                            print(f"Erro nos dados inseridos: {e}")

                    elif sub_opcao == 3:
                        tarefa_update = TarefaUpdate(concluida=True)
                        update_tarefa = repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                        resposta_tarefa = TarefaResponse.model_validate(update_tarefa)
                        print(f"Tarefa está concluída? {resposta_tarefa.concluida}")


                    elif sub_opcao == 4:
                        try:
                            novo_nome = input("Nome do tarefa: ")
                            nova_prioridade = int(input("Prioridade do tarefa: "))
                            tarefa_update = TarefaUpdate(nome=novo_nome,prioridade=nova_prioridade,concluida=True)
                            tarefa_update = repo.atualizar(utilizador.id,tarefa_id,tarefa_update)
                            tarefa_resposta = TarefaResponse.model_validate(tarefa_update)
                            print(f"Informações da tarefa atualizados com sucesso! Nome: {tarefa_resposta.nome} | Prioridade: {tarefa_resposta.prioridade} | Concluida: {tarefa_resposta.concluida}")
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
                    tarefa_response_schema = TarefaResponse.model_validate(tarefa)
                    print(tarefa_response_schema)

            elif opcao == 5:
                concluidas = repo.ver_tarefas_concluidas(utilizador.id)
                if not concluidas:
                    print("Sem tarefas guardadas")
                print("\n--- Tarefas concluidas ---")
                for tarefa in concluidas:
                    schema_response_tarefa = TarefaResponse.model_validate(tarefa)
                    print(schema_response_tarefa)

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

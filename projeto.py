# ==============================================================================
# CHECKPOINT: Arquivos e JSON - Passagem de Plantão
# Integrantes da Dupla:
# - Nome Integrante 1 (RMXXXXX)
# - Nome Integrante 2 (RMYYYYY)
# Turma: 1TDSR / 1ESR (ajuste para a sua turma)
# Contexto escolhido: Sistema de E-Commerce / Loja Virtual
# ==============================================================================

import json

ARQUIVO_JSON = "ocorrencias.json"
ARQUIVO_DIARIO = "diario.txt"
ARQUIVO_PASSAGEM = "passagem.txt"
NOME_SISTEMA = "Sistema de Loja Virtual (E-Commerce)"


# ------------------------------------------------------------------------------
# Ocorrências (JSON)
# ------------------------------------------------------------------------------
def carregar_ocorrencias():
    """Lê o JSON. Retorna lista (vazia se o arquivo não existir) ou None se o JSON for inválido."""
    try:
        arquivo = open(ARQUIVO_JSON, "r", encoding="utf-8")
        lista = json.load(arquivo)
        arquivo.close()
        return lista
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("\n[ERRO] O arquivo 'ocorrencias.json' contém um JSON inválido!")
        print("Corrija o arquivo para usar esta funcionalidade.")
        return None


def salvar_ocorrencias(ocorrencias):
    """Grava a lista completa de ocorrências no JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(ocorrencias, arquivo, ensure_ascii=False, indent=4)


def ler_texto_obrigatorio(mensagem):
    """Repete a pergunta até o usuário digitar algo não vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo não pode ficar vazio!")


def registrar_ocorrencia():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        print("-> Operação cancelada devido a erro no arquivo JSON.")
        return

    print("\n--- REGISTRAR OCORRÊNCIA ---")
    servico = ler_texto_obrigatorio("Módulo afetado (ex: Login, Pagamento, Relatório): ")
    descricao = ler_texto_obrigatorio("Descrição do problema e efeito para o usuário: ")

    prioridade = ""
    while prioridade not in ["alta", "media", "baixa"]:
        prioridade = input("Prioridade (alta, media, baixa): ").strip().lower()
        if prioridade not in ["alta", "media", "baixa"]:
            print("Prioridade inválida! Tente novamente.")

    status = ""
    while status not in ["aberto", "resolvido"]:
        status = input("Status (aberto, resolvido): ").strip().lower()
        if status not in ["aberto", "resolvido"]:
            print("Status inválido! Tente novamente.")

    if status == "resolvido":
        proxima_acao = "nenhuma"
        print("Status resolvido: próxima ação definida como 'nenhuma'.")
    else:
        proxima_acao = ler_texto_obrigatorio("Próxima ação que a equipe deve realizar: ")

    nova_ocorrencia = {
        "servico": servico,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "proxima_acao": proxima_acao
    }

    ocorrencias.append(nova_ocorrencia)
    salvar_ocorrencias(ocorrencias)
    print("\nOcorrência registrada com sucesso!")


def consultar_ocorrencias():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        print("-> Operação cancelada devido a erro no arquivo JSON.")
        return

    print("\n--- CONSULTA DE OCORRÊNCIAS ---")
    if len(ocorrencias) == 0:
        print("Não há ocorrências registradas.")
        return

    numero = 1
    for oc in ocorrencias:
        print("\n[ Ocorrência #" + str(numero) + " ]")
        print("  Serviço:      " + oc["servico"])
        print("  Descrição:    " + oc["descricao"])
        print("  Prioridade:   " + oc["prioridade"])
        print("  Status:       " + oc["status"])
        print("  Próxima ação: " + oc["proxima_acao"])
        numero += 1


# ------------------------------------------------------------------------------
# Diário (TXT)
# ------------------------------------------------------------------------------
def registrar_diario():
    print("\n--- REGISTRAR ANOTAÇÃO NO DIÁRIO ---")
    servico = ler_texto_obrigatorio("Serviço / Módulo: ")
    anotacao = ler_texto_obrigatorio("Anotação (ex: Reinício testado sem sucesso): ")

    with open(ARQUIVO_DIARIO, "a", encoding="utf-8") as arquivo:
        arquivo.write(servico + " — " + anotacao + "\n")

    print("Anotação inserida no diário!")


def consultar_diario():
    print("\n--- DIÁRIO DE AÇÕES ---")
    try:
        with open(ARQUIVO_DIARIO, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        if conteudo.strip() == "":
            print("Nenhuma anotação registrada.")
        else:
            print(conteudo)
    except FileNotFoundError:
        print("Nenhuma anotação registrada.")


# ------------------------------------------------------------------------------
# Passagem de plantão
# ------------------------------------------------------------------------------
def gerar_passagem_plantao():
    ocorrencias = carregar_ocorrencias()
    if ocorrencias is None:
        print("-> Operação cancelada devido a erro no arquivo JSON.")
        return

    # Filtra as abertas e conta as de prioridade alta
    abertas = []
    abertas_alta = 0
    for oc in ocorrencias:
        if oc["status"] == "aberto":
            abertas.append(oc)
            if oc["prioridade"] == "alta":
                abertas_alta += 1

    with open(ARQUIVO_PASSAGEM, "w", encoding="utf-8") as arquivo:
        arquivo.write("PASSAGEM DE PLANTÃO - " + NOME_SISTEMA + "\n")
        arquivo.write("Total de ocorrências abertas: " + str(len(abertas)) + "\n")
        arquivo.write("Abertas com prioridade alta: " + str(abertas_alta) + "\n")
        arquivo.write("-" * 50 + "\n")

        if len(abertas) == 0:
            arquivo.write("Nenhuma pendência para o próximo plantão\n")
        else:
            arquivo.write("PENDÊNCIAS ABERTAS:\n\n")
            for oc in abertas:
                arquivo.write("Serviço: " + oc["servico"] + "\n")
                arquivo.write("Descrição: " + oc["descricao"] + "\n")
                arquivo.write("Prioridade: " + oc["prioridade"] + "\n")
                arquivo.write("Próxima ação: " + oc["proxima_acao"] + "\n")
                arquivo.write("-" * 30 + "\n")

    print("\nPassagem de plantão gerada com sucesso!\n")
    print("=" * 50)
    with open(ARQUIVO_PASSAGEM, "r", encoding="utf-8") as arquivo:
        print(arquivo.read())
    print("=" * 50)


# ------------------------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------------------------
def main():
    opcao = ""
    while opcao != "6":
        print("\n==========================================")
        print("      PASSAGEM DE PLANTÃO - MENU")
        print("==========================================")
        print("1 - Registrar ocorrência")
        print("2 - Consultar ocorrências")
        print("3 - Registrar anotação no diário")
        print("4 - Consultar diário")
        print("5 - Gerar passagem de plantão")
        print("6 - Sair")
        print("==========================================")

        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            registrar_ocorrencia()
        elif opcao == "2":
            consultar_ocorrencias()
        elif opcao == "3":
            registrar_diario()
        elif opcao == "4":
            consultar_diario()
        elif opcao == "5":
            gerar_passagem_plantao()
        elif opcao == "6":
            print("\nEncerrando o programa. Bom plantão!")
        else:
            print("\nOpção inválida! Digite um número de 1 a 6.")


main()

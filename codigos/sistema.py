from produtos import Produto
import estoque
from abc import ABC, abstractmethod
import os
import pandas as pd
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")
except AttributeError:
    pass

if os.name == "nt":
    os.system("chcp 65001 > nul")


def limpar_tela():  # limpa a tela do terminal
    os.system("cls" if os.name == "nt" else "clear")


class Usuario(ABC):

    def __init__(self, nome: str):
        self.nome = nome

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        if not nome:
            raise ValueError("Erro: Nome vazio.")
        self._nome = nome.strip()


class Funcionario(Usuario):

    def __init__(self, nome: str, senha: str):
        super().__init__(nome)
        self.__senha = senha

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        if not senha:
            raise ValueError("Erro: Senha vazia.")
        self.__senha = senha


class Cliente(Usuario):

    def __init__(self, nome: str, cpf: str):
        super().__init__(nome)
        self.__cpf = cpf

    @property
    def cpf(self):
        return self.__cpf


class Sistema:  # classe principal do sistema, controla toda a interface

    def __init__(self):
        self.estoque = estoque.Estoque()

        if os.path.exists("../arquivos/funcionarios.txt"):
            with open("../arquivos/funcionarios.txt", "r", encoding="utf-8") as f:
                self.funcionarios = f.readlines()
        else:
            open("../arquivos/funcionarios.txt", "w", encoding="utf-8").close()
            self.funcionarios = []

        if os.path.exists("../arquivos/clientes.txt"):
            with open("../arquivos/clientes.txt", "r", encoding="utf-8") as f:
                self.clientes = f.readlines()
        else:
            open("../arquivos/clientes.txt", "w", encoding="utf-8").close()
            self.clientes = []

        self.ordenar_funcionarios()
        self.ordenar_clientes()

    def ordenar_funcionarios(self):  # ordena os funcionarios em ordem alfabetica
        self.funcionarios.sort(key=lambda x: x.split(" - ")[0].lower())

        with open("../arquivos/funcionarios.txt", "w", encoding="utf-8") as f:
            f.writelines(self.funcionarios)

    def ordenar_clientes(self):  # ordena os clientes em ordem alfabetica
        self.clientes.sort(key=lambda x: x.split(" - ")[0].lower())

        with open("../arquivos/clientes.txt", "w", encoding="utf-8") as f:
            f.writelines(self.clientes)

    def listar_funcionarios(self):  # lista os funcionarios utilizando dataframe pandas
        print("Funcionarios cadastrados:")

        if self.funcionarios:
            df = pd.DataFrame(
                [func.strip().split(" - ")[0] for func in self.funcionarios],
                columns=["Nome"]
            )
        else:
            df = pd.DataFrame(columns=["Nome"])

        print(df)

    def listar_clientes(self):  # lista os clientes utilizando dataframe pandas
        print("Clientes cadastrados:")

        if self.clientes:
            df = pd.DataFrame(
                [cliente.strip().split(" - ")[0] for cliente in self.clientes],
                columns=["Nome"]
            )
        else:
            df = pd.DataFrame(columns=["Nome"])

        print(df)

    def cadastrar_funcionario(self):
        nome = input("Nome do funcionario: ")
        senha = input("Senha do funcionario: ")

        funcionario = Funcionario(nome, senha)

        self.funcionarios.append(f"{funcionario.nome} - {funcionario.senha}\n")
        self.ordenar_funcionarios()

        print("Funcionario cadastrado.")

    def cadastrar_cliente(self):
        nome = input("Nome do cliente: ")
        cpf = input("CPF do cliente: ")

        cliente = Cliente(nome, cpf)

        self.clientes.append(f"{cliente.nome} - {cliente.cpf}\n")
        self.ordenar_clientes()

        print("Cliente cadastrado.")

    def acesso_funcionario(self):  # realiza login do funcionario a partir da senha
        senha = input("Digite a senha do funcionario: ")
        limpar_tela()

        for func in self.funcionarios:
            if func.strip().split(" - ")[1] == senha:
                print(f"Bem-vindo, {func.strip().split(' - ')[0]}!")
                self.menu_funcionario()
                return

        print("Senha incorreta. Acesso negado.")

    def menu_funcionario(self):
        while True:
            print("\nMenu do Funcionario:")
            print("Gerenciar estoque (1)")
            print("Cadastrar funcionario (2)")
            print("Sair (3)")

            escolha = str(input("Escolha uma opcao: "))
            limpar_tela()

            if escolha == "1":
                self.gerenciar_estoque()
            elif escolha == "2":
                self.cadastrar_funcionario()
            elif escolha == "3":
                print("Saindo do menu do funcionario...")
                break
            else:
                print("Opcao invalida. Tente novamente.")

    def gerenciar_estoque(self):
        while True:
            limpar_tela()

            print("\nGerenciar estoque:")
            print("Adicionar produto (1)")
            print("Repor produto (2)")
            print("Remover produto (3)")
            print("Sair (4)")

            escolha = str(input("Escolha uma opcao: "))
            limpar_tela()

            if escolha == "1":
                self.estoque.adicionar_produto()

            elif escolha == "2":
                nome = input("Nome do produto a ser reposto: ")
                item_encontrado = self.estoque.buscar_produto(nome)

                if item_encontrado:
                    nome_produto = item_encontrado.strip().split(" - ")[0]

                    while True:
                        try:
                            qtd = float(input("Quantidade a ser adicionada: "))

                            if qtd <= 0:
                                print("Quantidade deve ser maior que zero!")
                                continue

                            break

                        except ValueError:
                            print("Entrada invalida. Digite um numero.")

                    self.estoque.adicionar_qtd(nome_produto, qtd)

                    print("Quantidade adicionada com sucesso!")
                    input("Pressione Enter para continuar.")

                else:
                    print("Produto nao encontrado!")
                    input("Pressione Enter para continuar.")

            elif escolha == "3":
                self.estoque.listar_estoque()

                nome = input("Nome do produto a ser removido: ")
                item_encontrado = self.estoque.buscar_produto(nome)

                if item_encontrado:
                    nome_produto = item_encontrado.strip().split(" - ")[0]
                    self.estoque.remover_produto(nome_produto)

                    print("Produto removido com sucesso!")
                    input("Pressione Enter para continuar.")

                else:
                    print("Produto nao encontrado!")
                    input("Pressione Enter para continuar.")

            elif escolha == "4":
                print("Saindo do gerenciamento de estoque...")
                break

            else:
                print("Opcao invalida. Tente novamente.")
                input("Pressione Enter para continuar.")

    def acesso_cliente(self):  # realiza login de cliente a partir de cpf ou cria um novo login
        print("Acesso de cliente:")

        escolha = input("Voce e um cliente cadastrado? (s/n): ").lower()
        limpar_tela()

        if escolha == "s":
            cpf = input("Digite o CPF do cliente: ")
            limpar_tela()

            for cliente in self.clientes:
                if cliente.strip().split(" - ")[1] == cpf:
                    print(f"Bem-vindo, {cliente.strip().split(' - ')[0]}!")
                    self.menu_cliente()
                    return

            print("CPF nao encontrado.")
            input("Pressione Enter para continuar.")

        elif escolha == "n":
            escolha_cadastro = input("Deseja se cadastrar? (s/n): ").lower()
            limpar_tela()

            if escolha_cadastro == "s":
                self.cadastrar_cliente()

                print("Cadastro realizado com sucesso.")
                input("Pressione Enter para continuar.")
                limpar_tela()

                self.menu_cliente()
            else:
                self.menu_cliente()

        else:
            print("Opcao invalida. Retornando ao menu principal.")

    def menu_cliente(self):  # menu do cliente para fazer compras
        carrinho = []

        while True:
            self.estoque.listar_estoque()

            produto = input("Digite o nome do produto que deseja comprar (ou 'sair' para encerrar): ")

            if produto.lower() == "sair":
                break

            else:
                item_encontrado = self.estoque.buscar_produto(produto)

                if item_encontrado:
                    partes = item_encontrado.strip().split(" - ")

                    nome_produto = partes[0]
                    preco_str = partes[1].replace("R$", "")
                    preco = float(preco_str)
                    qtd_disponivel = float(partes[2].split()[0])

                    while True:
                        try:
                            qtd = float(input(f"Digite a quantidade desejada (disponivel: {qtd_disponivel}): "))

                            if qtd <= 0:
                                print("Erro: A quantidade deve ser maior que zero.")
                            elif qtd > qtd_disponivel:
                                print("Quantidade indisponivel.")
                            else:
                                break

                        except ValueError:
                            print("Erro: Digite um numero valido.")

                    carrinho.append({
                        "nome": nome_produto,
                        "quantidade": qtd,
                        "preco": preco
                    })

                    self.estoque.remover_qtd(nome_produto, qtd)

                    limpar_tela()
                    print(f"{qtd} x {nome_produto} adicionado ao carrinho!")

                else:
                    print("Produto nao encontrado")
                    input("Pressione Enter para continuar.")
                    limpar_tela()

        if carrinho:
            limpar_tela()

            print("Resumo da compra:")

            total = 0

            for item in carrinho:
                subtotal = item["quantidade"] * item["preco"]
                total += subtotal

                print(f"{item['nome']}: {item['quantidade']} x R${item['preco']:.2f} = R${subtotal:.2f}")

            print(f"TOTAL: R${total:.2f}")

            self.finalizar_compra(total)

        limpar_tela()

    def iniciar_sistema(self):  # inicia o menu principal do sistema
        while True:
            print("\nMenu:")
            print("Acesso de funcionario (1)")
            print("Acesso de cliente (2)")
            print("Sair (3)")

            escolha = input("Escolha uma opcao: ")
            limpar_tela()

            if escolha == "1":
                self.acesso_funcionario()
            elif escolha == "2":
                self.acesso_cliente()
            elif escolha == "3":
                print("Saindo do sistema...")
                break
            else:
                print("Opcao invalida. Tente novamente.")

    def finalizar_compra(self, total):  # finaliza a compra com o metodo de pagamento desejado
        while True:
            try:
                escolha = int(input(
                    "Escolha uma forma de pagamento(numero):\n"
                    "1- Dinheiro\n"
                    "2- Cartao de Credito\n"
                    "3- Cartao de Debito\n"
                    "4- PIX\n"
                    "Metodo de pagamento: "
                ))

                if escolha == 1:
                    tipo = "dinheiro"
                    break
                elif escolha == 2:
                    tipo = "cartao de credito"
                    break
                elif escolha == 3:
                    tipo = "cartao de debito"
                    break
                elif escolha == 4:
                    tipo = "PIX"
                    break
                else:
                    print("Escolha invalida.")

            except ValueError:
                print("Entrada invalida. Digite apenas numeros.")

        print(f"Pagamento realizado com {tipo}.")
        input("Aperte Enter para continuar.")


def main():
    sistema = Sistema()
    sistema.iniciar_sistema()


if __name__ == "__main__":
    main()
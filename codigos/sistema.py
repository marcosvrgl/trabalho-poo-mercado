from abc import ABC, abstractmethod
import os
import pandas as pd
import estoque


def limpar_tela():
    """
    Limpa a tela do terminal de acordo com o sistema operacional.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class Usuario(ABC):
    """
    Classe abstrata que representa um usuário genérico do sistema.
    Serve como classe mãe para Cliente e Funcionario.
    """

    def __init__(self, nome: str):
        self.nome = nome

    @property
    def nome(self):
        """
        Retorna o nome do usuário.
        """
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        """
        Valida e altera o nome do usuário.
        """
        if not nome or nome.strip() == "":
            raise ValueError("O nome não pode ser vazio.")
        self.__nome = nome.strip()

    @abstractmethod
    def exibir_dados(self):
        """
        Método abstrato que deve ser implementado pelas classes filhas.
        """
        pass


class Funcionario(Usuario):
    """
    Classe que representa um funcionário do mercado.
    Herda da classe abstrata Usuario.
    """

    def __init__(self, nome: str, senha: str):
        super().__init__(nome)
        self.senha = senha

    @property
    def senha(self):
        """
        Retorna a senha do funcionário.
        """
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        """
        Valida e altera a senha do funcionário.
        """
        if not senha or senha.strip() == "":
            raise ValueError("A senha não pode ser vazia.")
        self.__senha = senha.strip()

    def exibir_dados(self):
        """
        Exibe os dados básicos do funcionário.
        """
        return f"Funcionário: {self.nome}"


class Cliente(Usuario):
    """
    Classe que representa um cliente do mercado.
    Herda da classe abstrata Usuario.
    """

    def __init__(self, nome: str, cpf: str):
        super().__init__(nome)
        self.cpf = cpf

    @property
    def cpf(self):
        """
        Retorna o CPF do cliente.
        """
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        """
        Valida e altera o CPF do cliente.
        """
        cpf = cpf.strip()

        if not cpf:
            raise ValueError("O CPF não pode ser vazio.")

        if not cpf.isdigit():
            raise ValueError("O CPF deve conter apenas números.")

        if len(cpf) != 11:
            raise ValueError("O CPF deve conter 11 dígitos.")

        self.__cpf = cpf

    def exibir_dados(self):
        """
        Exibe os dados básicos do cliente.
        """
        return f"Cliente: {self.nome} - CPF: {self.cpf}"


class Sistema:
    """
    Classe principal do sistema.
    Controla o acesso de funcionários, clientes, estoque e compras.
    """

    def __init__(self):
        """
        Inicializa o sistema, carregando os dados de estoque,
        funcionários e clientes a partir dos arquivos de texto.
        """
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

    def ordenar_funcionarios(self):
        """
        Ordena os funcionários em ordem alfabética e atualiza o arquivo.
        """
        self.funcionarios.sort(key=lambda x: x.split(" - ")[0].lower())

        with open("../arquivos/funcionarios.txt", "w", encoding="utf-8") as f:
            f.writelines(self.funcionarios)

    def ordenar_clientes(self):
        """
        Ordena os clientes em ordem alfabética e atualiza o arquivo.
        """
        self.clientes.sort(key=lambda x: x.split(" - ")[0].lower())

        with open("../arquivos/clientes.txt", "w", encoding="utf-8") as f:
            f.writelines(self.clientes)

    def listar_funcionarios(self):
        """
        Lista os funcionários cadastrados no sistema.
        """
        print("Funcionários cadastrados:")

        if self.funcionarios:
            df = pd.DataFrame(
                [func.strip().split(" - ")[0] for func in self.funcionarios],
                columns=["Nome"]
            )
        else:
            df = pd.DataFrame(columns=["Nome"])

        print(df)

    def listar_clientes(self):
        """
        Lista os clientes cadastrados no sistema.
        """
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
        """
        Cadastra um novo funcionário no sistema, validando nome e senha.
        """
        while True:
            try:
                nome = input("Nome do funcionário: ")
                senha = input("Senha do funcionário: ")

                funcionario = Funcionario(nome, senha)

                self.funcionarios.append(f"{funcionario.nome} - {funcionario.senha}\n")
                self.ordenar_funcionarios()

                print("Funcionário cadastrado.")
                break

            except ValueError as erro:
                print(f"Erro ao cadastrar funcionário: {erro}")

    def cadastrar_cliente(self):
        """
        Cadastra um novo cliente no sistema, validando nome e CPF.
        """
        while True:
            try:
                nome = input("Nome do cliente: ")
                cpf = input("CPF do cliente: ")

                for cliente_cadastrado in self.clientes:
                    cpf_cadastrado = cliente_cadastrado.strip().split(" - ")[1]

                    if cpf_cadastrado == cpf:
                        print("CPF já cadastrado.")
                        return

                cliente = Cliente(nome, cpf)

                self.clientes.append(f"{cliente.nome} - {cliente.cpf}\n")
                self.ordenar_clientes()

                print("Cliente cadastrado.")
                break

            except ValueError as erro:
                print(f"Erro ao cadastrar cliente: {erro}")

    def acesso_funcionario(self):
        """
        Realiza o acesso de funcionário por senha.
        """
        senha = input("Digite a senha do funcionário: ")
        limpar_tela()

        for func in self.funcionarios:
            dados = func.strip().split(" - ")

            if len(dados) >= 2 and dados[1] == senha:
                print(f"Bem-vindo, {dados[0]}!")
                self.menu_funcionario()
                return

        print("Senha incorreta. Acesso negado.")

    def menu_funcionario(self):
        """
        Exibe o menu de opções disponíveis para funcionários.
        """
        while True:
            print("\nMenu do Funcionário:")
            print("Gerenciar estoque (1)")
            print("Cadastrar funcionário (2)")
            print("Listar funcionários (3)")
            print("Listar clientes (4)")
            print("Sair (5)")

            escolha = input("Escolha uma opção: ")
            limpar_tela()

            if escolha == "1":
                self.gerenciar_estoque()

            elif escolha == "2":
                self.cadastrar_funcionario()

            elif escolha == "3":
                self.listar_funcionarios()
                input("Aperte Enter para continuar...")

            elif escolha == "4":
                self.listar_clientes()
                input("Aperte Enter para continuar...")

            elif escolha == "5":
                print("Saindo do menu do funcionário...")
                break

            else:
                print("Opção inválida. Tente novamente.")

    def gerenciar_estoque(self):
        """
        Exibe o menu de gerenciamento de estoque.
        """
        while True:
            limpar_tela()
            print("\nGerenciar estoque:")
            print("Adicionar produto (1)")
            print("Repor produto (2)")
            print("Remover produto (3)")
            print("Listar estoque (4)")
            print("Sair (5)")

            escolha = input("Escolha uma opção: ")
            limpar_tela()

            if escolha == "1":
                self.estoque.adicionar_produto()

            elif escolha == "2":
                nome = input("Nome do produto a ser reposto: ")

                while True:
                    try:
                        qtd = float(input("Quantidade a ser adicionada: "))

                        if qtd <= 0:
                            print("A quantidade deve ser maior que zero.")
                            continue

                        break

                    except ValueError:
                        print("Entrada inválida. Digite um número.")

                self.estoque.adicionar_qtd(nome, qtd)

            elif escolha == "3":
                self.estoque.listar_estoque()
                nome = input("Nome do produto a ser removido: ")
                self.estoque.remover_produto(nome)

            elif escolha == "4":
                self.estoque.listar_estoque()
                input("Aperte Enter para continuar...")

            elif escolha == "5":
                print("Saindo do gerenciamento de estoque...")
                break

            else:
                print("Opção inválida. Tente novamente.")

    def acesso_cliente(self):
        """
        Realiza o acesso de cliente por CPF ou permite cadastro de novo cliente.
        """
        print("Acesso de cliente:")
        escolha = input("Você é um cliente cadastrado? (s/n): ").lower()
        limpar_tela()

        if escolha == "s":
            cpf = input("Digite o CPF do cliente: ")
            limpar_tela()

            for cliente in self.clientes:
                dados = cliente.strip().split(" - ")

                if len(dados) >= 2 and dados[1] == cpf:
                    print(f"Bem-vindo, {dados[0]}!")
                    self.menu_cliente()
                    return

            print("CPF não encontrado.")

        elif escolha == "n":
            escolha_cadastro = input("Deseja se cadastrar? (s/n): ").lower()
            limpar_tela()

            if escolha_cadastro == "s":
                self.cadastrar_cliente()
                self.menu_cliente()
            else:
                self.menu_cliente()

        else:
            print("Opção inválida. Retornando ao menu principal.")

    def menu_cliente(self):
        """
        Exibe o menu de compra para o cliente.
        Permite escolher produtos, adicionar ao carrinho e finalizar a compra.
        """
        carrinho = []

        while True:
            self.estoque.listar_estoque()

            produto_digitado = input(
                "Digite o nome do produto que deseja comprar "
                "(ou 'sair' para encerrar): "
            )

            if produto_digitado.lower() == "sair":
                break

            produto_encontrado = False

            for item in self.estoque.estoque:
                partes = item.strip().split(" - ")

                if len(partes) < 3:
                    continue

                nome_produto = partes[0]
                preco_str = partes[1].replace("R$", "")
                preco = float(preco_str)
                qtd_disponivel = float(partes[2].split()[0])

                if nome_produto.lower().startswith(produto_digitado.lower()):
                    produto_encontrado = True

                    while True:
                        try:
                            qtd = float(input(
                                f"Digite a quantidade desejada "
                                f"(disponível: {qtd_disponivel}): "
                            ))

                            if qtd <= 0:
                                print("A quantidade deve ser maior que zero.")
                                continue

                            break

                        except ValueError:
                            print("Entrada inválida. Digite um número.")

                    if qtd <= qtd_disponivel:
                        carrinho.append({
                            "nome": nome_produto,
                            "quantidade": qtd,
                            "preco": preco
                        })

                        self.estoque.remover_qtd(nome_produto, qtd)

                        limpar_tela()
                        print(f"{qtd} x {nome_produto} adicionado ao carrinho!")
                        break

                    else:
                        print("Quantidade indisponível.")
                        break

            if not produto_encontrado:
                print("Produto não encontrado.")

        if carrinho:
            limpar_tela()
            print("Resumo da compra:")

            total = 0

            for item in carrinho:
                subtotal = item["quantidade"] * item["preco"]
                total += subtotal

                print(
                    f"{item['nome']}: {item['quantidade']} x "
                    f"R${item['preco']:.2f} = R${subtotal:.2f}"
                )

            print(f"TOTAL: R${total:.2f}")

            self.finalizar_compra(total)

        limpar_tela()

    def finalizar_compra(self, total):
        """
        Finaliza a compra do cliente, permitindo a escolha da forma de pagamento.
        Possui tratamento de erro para impedir que o sistema quebre se o usuário
        digitar letras ou opções inválidas.
        """
        while True:
            try:
                escolha = int(input(
                    "Escolha uma forma de pagamento(número):\n"
                    "1- Dinheiro\n"
                    "2- Cartão de Crédito\n"
                    "3- Cartão de Débito\n"
                    "4- PIX\n"
                    "Metodo de pagamento: "
                ))

                if escolha == 1:
                    tipo = "dinheiro"
                    break

                elif escolha == 2:
                    tipo = "cartão de crédito"
                    break

                elif escolha == 3:
                    tipo = "cartão de débito"
                    break

                elif escolha == 4:
                    tipo = "PIX"
                    break

                else:
                    print("Escolha inválida. Digite uma opção entre 1 e 4.")

            except ValueError:
                print("Entrada inválida. Digite apenas números.")

        print(f"Pagamento realizado com {tipo}.")
        input("Aperte Enter para continuar.")

    def iniciar_sistema(self):
        """
        Inicia o sistema e exibe o menu principal.
        """
        while True:
            print("\nMenu:")
            print("Acesso de funcionario (1)")
            print("Acesso de cliente (2)")
            print("Sair (3)")

            escolha = input("Escolha uma opção: ")
            limpar_tela()

            if escolha == "1":
                self.acesso_funcionario()

            elif escolha == "2":
                self.acesso_cliente()

            elif escolha == "3":
                print("Saindo do sistema...")
                break

            else:
                print("Opção inválida. Tente novamente.")


def main():
    """
    Função principal do programa.
    Cria o sistema e inicia o menu principal.
    """
    sistema = Sistema()
    sistema.iniciar_sistema()


if __name__ == "__main__":
    main()
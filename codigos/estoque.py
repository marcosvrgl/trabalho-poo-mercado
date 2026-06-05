import produtos
import os
import pandas as pd

class Estoque:

    def __init__(self):
        arquivo_path = "../arquivos/estoque.txt"

        if os.path.exists(arquivo_path): # verifica se o arquivo existe, se sim, lê o conteúdo e armazena em estoque, caso contrario, cria um arquivo vazio
            self.estoque = open(arquivo_path, "r").readlines()

        else:
            open(arquivo_path, "w").close()
            self.estoque = []

        self.ordenar_estoque() # ordena o estoque ao iniciar a classe

    def ordenar_estoque(self):
        self.estoque.sort(key=lambda x: x.split(" - ")[0].lower()) # ordena o produto de forma alfabética / lambda é uma função oculta que recebe um produto e retorna o nome em letras minusculas para comparação

        with open("../arquivos/estoque.txt", "w") as f: # reescreve o arquivo com o estoque ordenado
            f.writelines(self.estoque)

    def adicionar_produto(self):
        # tratamento para o tipo do produto
        while True:
            try:
                tipo = int(input("Tipo do produto (1 - Frutas e Verduras, 2 - Itens): "))
                if tipo in [1, 2]:
                    break
                else:
                    print("Opção inválida. Digite 1 ou 2.")
            except ValueError:
                print("Entrada inválida. Digite 1 ou 2.")
        
        nome = str(input("Nome do produto: "))
        
        if tipo == 1:
            # tratamento para preço
            while True:
                try:
                    preco = float(input("Preço do produto (por kg): "))
                    break
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            
            # tratamento para peso
            while True:
                try:
                    peso = float(input("Quantidade (kg): "))
                    break
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            
            produto = produtos.FrutasEVerduras(nome, preco, peso)

        elif tipo == 2:
            # tratamento para preço
            while True:
                try:
                    preco = float(input("Preço do produto: "))
                    break
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            
            # tratamento para quantidade
            while True:
                try:
                    quantidade = int(input("Quantidade (unidades): "))
                    break
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")
            
            produto = produtos.Itens(nome, preco, quantidade)
        
        self.estoque.append(f"{produto}\n")
        self.ordenar_estoque()
        print(f"Produto adicionado.")
        continuar = input("Aperte Enter para continuar...")

    def adicionar_qtd(self, nome: str, qtd: float):
        for i, produto in enumerate(self.estoque): # percorre o estoque com indice e valor
            if produto.startswith(nome):
                partes = produto.strip().split(" - ")
                qtd_atual = float(partes[2].split()[0])
                nova_qtd = qtd_atual + qtd

                if "kg" in partes[2]:
                    self.estoque[i] = f"{partes[0]} - {partes[1]} - {nova_qtd} kg\n"
                else:
                    self.estoque[i] = f"{partes[0]} - {partes[1]} - {int(nova_qtd)} unidades\n"

                with open("../arquivos/estoque.txt", "w") as f:
                    f.writelines(self.estoque)
                break # sai do loop após encontrar o produto
        else:
            print("Produto não encontrado no estoque. Deseja adicionar o produto? (s/n)")
            resposta = input().lower()
            if resposta == "s":
                self.adicionar_produto()
    
    def remover_qtd(self, nome: str, qtd: float):
        for i, produto in enumerate(self.estoque): # percorre o estoque com indice e valor
            if produto.startswith(nome):
                partes = produto.strip().split(" - ")
                qtd_atual = float(partes[2].split()[0])
                nova_qtd = qtd_atual - qtd

                if nova_qtd > 0:
                    if "kg" in partes[2]:
                        self.estoque[i] = f"{partes[0]} - {partes[1]} - {nova_qtd} kg\n"
                    else:
                        self.estoque[i] = f"{partes[0]} - {partes[1]} - {int(nova_qtd)} unidades\n"
                else:
                    self.remover_produto(nome)

                with open("../arquivos/estoque.txt", "w") as f:
                    f.writelines(self.estoque)
                break # sai do loop após encontrar o produto

    def remover_produto(self, nome: str):
        # percorre a lista de estoque e remove o produto que começa com o nome fornecido
        self.estoque = [produto for produto in self.estoque if not produto.startswith(nome)]
        open("../arquivos/estoque.txt", "w").write("".join(self.estoque))
        print(f"{nome} removido do estoque.")
        continuar = input("Aperte Enter para continuar...")

    def listar_estoque(self):
        
        ordenado = sorted(self.estoque, key=lambda x: x.split(" - ")[0])

        # dataframe da biblioteca pandas utilizado para organização
        df = pd.DataFrame([produto.strip().split(" - ") for produto in self.estoque], columns=["Nome", "Preço", "Quantidade"])
        print(df)

def main():
    estoque = Estoque()
    estoque.listar_estoque()
    estoque.adicionar_produto()
    estoque.adicionar_qtd("Banana", 2)
    estoque.remover_qtd("Banana", 1)
    estoque.listar_estoque()

if __name__ == "__main__":
    main()

        

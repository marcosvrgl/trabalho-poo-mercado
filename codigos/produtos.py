from abc import ABC, abstractmethod

class Produto(ABC):

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        if not novo_nome:
            print("Nome inválido.")
        else:
            self._nome = novo_nome

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, novo_preco: float):
        if novo_preco <= 0:
            print("Valor inválido.")
        else:
            self._preco = novo_preco

    def alterar_preco(self, novo_preco: float):
        self.preco = novo_preco

    def calcular_preco_total(self):
        pass

class FrutasEVerduras(Produto):

    def __init__(self, nome: str, preco: float, peso: float):
        super().__init__(nome, preco)
        self.peso = peso

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, novo_peso: float):
        if novo_peso <= 0:
            print("Peso inválido.")
        else:
            self._peso = novo_peso

    def alterar_peso(self, novo_peso: float):
        self.peso = novo_peso

    def calcular_preco_total(self):
        return self.preco * self.peso

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.peso} kg"

class Itens(Produto): # produtos comprados em quantidade. ex: shampoo, macarrão, etc.
    
    def __init__(self, nome: str, preco: float, quantidade: int):
        super().__init__(nome, preco)
        self.quantidade = quantidade

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, nova_quantidade: int):
        if nova_quantidade <= 0:
            print("Quantidade inválida.")
        else:
            self._quantidade = nova_quantidade

    def alterar_quantidade(self, nova_quantidade: int):
        self.quantidade = nova_quantidade

    def calcular_preco_total(self):
        return self.preco * self.quantidade

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.quantidade} unidades"

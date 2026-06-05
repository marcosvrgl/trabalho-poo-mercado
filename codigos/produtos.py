from abc import ABC, abstractmethod

class Produto(ABC):

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco
    
    def mudar_preco(self, novo_preco: float):
        self.preco = novo_preco

class FrutasEVerduras(Produto):

    def __init__(self, nome: str, preco: float, peso: float):
        super().__init__(nome, preco)
        self.peso = peso

    def mudar_peso(self, novo_peso: float):
        self.peso = novo_peso

    def calcular_preco_total(self):
        return self.preco * self.peso

    def __str__(self):
            return f"{self.nome} - R${self.preco:.2f} - {self.peso} kg"

class Itens(Produto): # produtos comprados em quantidade. ex: shampoo, macarrão, etc.
    
    def __init__(self, nome: str, preco: float, quantidade: int):
        super().__init__(nome, preco)
        self.quantidade = quantidade

    def mudar_quantidade(self, nova_quantidade: int):
        self.quantidade = nova_quantidade

    def calcular_preco_total(self):
        return self.preco * self.quantidade

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.quantidade} unidades"
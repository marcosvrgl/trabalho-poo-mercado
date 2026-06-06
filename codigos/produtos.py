from abc import ABC, abstractmethod


class Produto(ABC):
    """
    Classe abstrata que representa um produto genérico do mercado.
    Serve como classe mãe para produtos vendidos por peso ou por unidade.
    """

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco

    @property
    def nome(self):
        """Retorna o nome do produto."""
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        """Valida e altera o nome do produto."""
        if not nome or nome.strip() == "":
            raise ValueError("O nome do produto não pode ser vazio.")
        self.__nome = nome.strip()

    @property
    def preco(self):
        """Retorna o preço do produto."""
        return self.__preco

    @preco.setter
    def preco(self, preco: float):
        """Valida e altera o preço do produto."""
        if preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        self.__preco = preco

    def mudar_preco(self, novo_preco: float):
        """Altera o preço do produto utilizando o setter."""
        self.preco = novo_preco

    @abstractmethod
    def calcular_preco_total(self):
        """
        Método abstrato que deve ser implementado pelas classes filhas.
        Cada tipo de produto calcula o preço total de uma forma.
        """
        pass


class FrutasEVerduras(Produto):
    """
    Classe que representa frutas e verduras vendidas por peso.
    Exemplo: banana, tomate, batata.
    """

    def __init__(self, nome: str, preco: float, peso: float):
        super().__init__(nome, preco)
        self.peso = peso

    @property
    def peso(self):
        """Retorna o peso do produto."""
        return self.__peso

    @peso.setter
    def peso(self, peso: float):
        """Valida e altera o peso do produto."""
        if peso <= 0:
            raise ValueError("O peso deve ser maior que zero.")
        self.__peso = peso

    def mudar_peso(self, novo_peso: float):
        """Altera o peso do produto utilizando o setter."""
        self.peso = novo_peso

    def calcular_preco_total(self):
        """Calcula o preço total com base no peso."""
        return self.preco * self.peso

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.peso} kg"


class Itens(Produto):
    """
    Classe que representa produtos vendidos por unidade.
    Exemplo: shampoo, macarrão, molho de tomate.
    """

    def __init__(self, nome: str, preco: float, quantidade: int):
        super().__init__(nome, preco)
        self.quantidade = quantidade

    @property
    def quantidade(self):
        """Retorna a quantidade do produto."""
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: int):
        """Valida e altera a quantidade do produto."""
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self.__quantidade = quantidade

    def mudar_quantidade(self, nova_quantidade: int):
        """Altera a quantidade do produto utilizando o setter."""
        self.quantidade = nova_quantidade

    def calcular_preco_total(self):
        """Calcula o preço total com base na quantidade."""
        return self.preco * self.quantidade

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.quantidade} unidades"
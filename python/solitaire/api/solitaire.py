import random

from . import envs
from .card import Card
from .pile import TableauPile, FoundationPile, StockPile, WastePile

class Solitaire():
    def __init__(self) -> None:
        # stock
        self._stock = StockPile()

        # wast
        self._waste = WastePile()

        # cards
        self._cards = []
        for family in envs.CARDS_FAMILIES:
            for rank in envs.CARDS_RANKS:
                self._cards.append(Card(family, rank))

        # foundation
        self._foundation = []
        for i in range(envs.NB_FOUNDATION_PILES):
            self._foundation.append(FoundationPile())

        # tableau
        self._tableau = []
        for i in range(envs.NB_TABLEAU_PILES):
            self._tableau.append(TableauPile())

    def new_game(self) -> None:
        cards = [card.copy() for card in self._cards]

        # randomize cards
        random.shuffle(cards)

        # foundation
        for pile in self._foundation:
            pile.clear()

        # tableau
        nb_card = 1  
        for tableau_pile in self._tableau:
            tableau_pile.clear()

            for j in range(nb_card) :
                card = cards.pop(-1)
                if j < nb_card - 1:
                    card.set_down_turned(True) # DownTurn cards except the last one
                tableau_pile.add_card(card)

            nb_card += 1

        # waste
        self._waste.clear()
        self._waste.add_card(cards.pop(-1))  

        # stock
        self._stock.clear()
        while cards:
            self._stock.add_card(cards.pop(-1))

    def get_foundation_piles(self) -> list[FoundationPile]:
        return self._foundation
    
    def get_tableau_piles(self) -> list[TableauPile]:
        return self._tableau

    def get_stock_pile(self) -> StockPile:
        return self._stock
    
    def get_wast_pile(self) -> WastePile:
        return self._waste

    def draw_next(self) -> None:
        card = self._stock.get_last_card()
        if not card:
            for card in self._waste.get_cards():
                self._stock.add_card(card)
            card = self._stock.get_last_card()
        if card:
            self._waste.add_card(card)
from .card import Card
from . import envs

class Pile():
    def __init__(self) -> None:
        self._cards = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}( )"
    
    def clear(self) -> None:
        self._cards = []

    def is_child_acceptable(self, card:Card) -> bool:
        return False
    
    def add_card(self, card:Card) -> None:
        pile = card.get_pile()
        if pile:
            pile.remove_card(card)
        self._cards.append(card)
        card.set_pile(self)

    def remove_card(self, card:Card) -> None:
        if card in self._cards:
            self._cards.remove(card)
            if self._cards and self._cards[-1].is_down_turned():
                self._cards[-1].set_down_turned(False)
    
    def get_last_card(self) -> Card:
        if self._cards:
            return self._cards[-1]
    
    def get_cards(self) -> list[Card]:
        return self._cards
    
class TableauPile(Pile):
    def is_child_acceptable(self, child:Card) -> bool:
        last_child = self.get_last_card()
        if last_child:
            if not child.is_down_turned():
                return  child.get_value() == last_child.get_value() - 1  \
                    and child.get_color() != last_child.get_color()
            return False
        else:
            if child.get_rank() != envs.CARDS_RANKS[-1]:
                return False
        return True
    
    def add_card(self, card:Card) -> None:
        cards = [card]
        cards.extend(card.get_children())
        for card in cards:
            super().add_card(card)

class StockPile(Pile):
    def add_card(self, card:Card) -> None:
        super().add_card(card)
        card.set_down_turned(True)

class WastePile(Pile):
    def add_card(self, card:Card) -> None:
        super().add_card(card)
        card.set_down_turned(False)

class FoundationPile(Pile):
    def is_child_acceptable(self, child:Card) -> bool:
        last_child = self.get_last_card()
        if last_child:
            return  child.get_value() == last_child.get_value() + 1  \
                and child.get_family() == last_child.get_family()
        return child.get_rank() == envs.CARDS_RANKS[0]
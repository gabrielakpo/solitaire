from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pile import Pile

from . import envs

class Card():
    def __init__(self, family:str, rank:str, is_down_turned:bool=False, pile:Pile=None) -> None:
        self._family = family
        self._rank = rank
        self._value = envs.CARDS_RANKS.index(self._rank)
        self._color = envs.CARDS_COLORS[family]
        self._is_down_turned = is_down_turned
        self._pile = pile
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._family}, {self._rank})'
    
    def get_children(self) -> list[Card]:
        children = []
        if self._pile and not self.is_last_card():
            index = self._pile._cards.index(self)
            children.extend(self._pile._cards[index:])
        return children

    def get_value(self) -> int:
        return self._value

    def get_color(self) -> str:
        return self._color

    def get_family(self) -> str:
        return self._family
    
    def get_rank(self) -> str:
        return self._rank
    
    def is_last_card(self) -> bool:
        return self is self._pile.get_last_card() if self._pile else False
    
    def get_pile(self) -> Pile:
        return self._pile
    
    def set_pile(self, pile:Pile) -> None:
        self._pile = pile
    
    def is_child_acceptable(self, child:Card) -> bool:
        return  self._pile.is_child_acceptable(child)
    
    def is_down_turned(self) -> bool:
        return self._is_down_turned
    
    def set_down_turned(self, downturned:bool) -> None:
        self._is_down_turned = downturned

    def add_child(self, child:Card) -> None:
        if self.is_child_acceptable(child):
            self._children.append()

    def copy(self) -> Card:
        return self.__class__(
            family=self._family, 
            rank=self._rank, 
            is_down_turned=self._is_down_turned,
            pile=self._pile)
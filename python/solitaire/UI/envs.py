import os
from .Qt import QtGui #type: ignore

CARD_WIDTH = 80
CARD_HEIGHT = 100

TABLEAU_PILE_SPACING = 20
TABLEAU_PILE_HEIGHT = 400

class DirFiles(dict):
    def __init__(self, *args, **kwargs):
        self._root = os.path.join(os.path.dirname(__file__), "icons")
        super(DirFiles, self).__init__(*args, **kwargs)
        
    def __getitem__(self, __k):
        if __k in self:
            return os.path.join(self._root, 
                                super(DirFiles, self).__getitem__(__k))

    def get(self, __k, default=None):
        if __k in self:
            return self.__getitem__(__k)
        return default

FILES = DirFiles({
    "card_downTurned": "card_downTurned.png",
    "clubs_10": "clubs_10.png",
    "clubs_2": "clubs_2.png",
    "clubs_3": "clubs_3.png",
    "clubs_4": "clubs_4.png",
    "clubs_5": "clubs_5.png",
    "clubs_6": "clubs_6.png",
    "clubs_7": "clubs_7.png",
    "clubs_8": "clubs_8.png",
    "clubs_9": "clubs_9.png",
    "clubs_as": "clubs_as.png",
    "clubs_jack": "clubs_jack.png",
    "clubs_king": "clubs_king.png",
    "clubs_queen": "clubs_queen.png",
    "diamonds_10": "diamonds_10.png",
    "diamonds_2": "diamonds_2.png",
    "diamonds_3": "diamonds_3.png",
    "diamonds_4": "diamonds_4.png",
    "diamonds_5": "diamonds_5.png",
    "diamonds_6": "diamonds_6.png",
    "diamonds_7": "diamonds_7.png",
    "diamonds_8": "diamonds_8.png",
    "diamonds_9": "diamonds_9.png",
    "diamonds_as": "diamonds_as.png",
    "diamonds_jack": "diamonds_jack.png",
    "diamonds_king": "diamonds_king.png",
    "diamonds_queen": "diamonds_queen.png",
    "Fancy Back": "Fancy Back.jpg",
    "hearts_10": "hearts_10.png",
    "hearts_2": "hearts_2.png",
    "hearts_3": "hearts_3.png",
    "hearts_4": "hearts_4.png",
    "hearts_5": "hearts_5.png",
    "hearts_6": "hearts_6.png",
    "hearts_7": "hearts_7.png",
    "hearts_8": "hearts_8.png",
    "hearts_9": "hearts_9.png",
    "hearts_as": "hearts_as.png",
    "hearts_jack": "hearts_jack.png",
    "hearts_king": "hearts_king.png",
    "hearts_queen": "hearts_queen.png",
    "spades_10": "spades_10.png",
    "spades_2": "spades_2.png",
    "spades_3": "spades_3.png",
    "spades_4": "spades_4.png",
    "spades_5": "spades_5.png",
    "spades_6": "spades_6.png",
    "spades_7": "spades_7.png",
    "spades_8": "spades_8.png",
    "spades_9": "spades_9.png",
    "spades_as": "spades_as.png",
    "spades_jack": "spades_jack.png",
    "spades_king": "spades_king.png",
    "spades_queen": "spades_queen.png"
})

class CacheIcons(dict):
    def __getitem__(self, __k):
        if not __k:
            return QtGui.QIcon()

        if __k not in self:
            if not os.path.isfile(__k):
                super(CacheIcons, self).__setitem__(__k, QtGui.QIcon(FILES[__k]))
            else:
                super(CacheIcons, self).__setitem__(__k, QtGui.QIcon(__k))
                
        return super(CacheIcons, self).__getitem__(__k)

ICONS = CacheIcons()
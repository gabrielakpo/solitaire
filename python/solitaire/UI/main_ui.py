from .Qt import QtWidgets, QtCore
from .pile_ui import StockPileWidget, FoundationPileWidget, \
                     TableauPileWidget, WastPileWidget
from .customs_ui import CustomToolbar

from solitaire.api import Solitaire

class SolitaireUI(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        self._game = Solitaire()
        self._tableau_piles = []
        self._foundation_piles = []

        super(SolitaireUI, self).__init__(*args, **kwargs)

        self.setWindowTitle('Solitaire')
        self.setFixedSize(618, 600)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.new_game()

    def create_widgets(self):
        # menu bar 
        self.menu_bar = CustomToolbar()
        self.menu_bar.addAction("new game", self.on_new_game_requested)

        # wast
        self.wast_pile_wdg = WastPileWidget(self._game.get_wast_pile())

        # stock
        self.stock_pile_wdg = StockPileWidget(self._game.get_stock_pile())

        # tableau
        for pile in self._game.get_tableau_piles():
            self._tableau_piles.append(TableauPileWidget(pile))

        # foundation
        for pile in self._game.get_foundation_piles():
            self._foundation_piles.append(FoundationPileWidget(pile))

    def create_layouts(self):
        stock_layout = QtWidgets.QHBoxLayout()
        stock_layout.addWidget(self.stock_pile_wdg)
        stock_layout.addWidget(self.wast_pile_wdg)

        # foundation 
        foundation_layout = QtWidgets.QHBoxLayout()
        for widget in self._foundation_piles:
            foundation_layout.addWidget(widget)

        # top 
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setAlignment(QtCore.Qt.AlignTop)
        top_layout.addLayout(stock_layout)
        top_layout.addStretch(0)
        top_layout.addLayout(foundation_layout)

        # tableau
        tableau_layout = QtWidgets.QHBoxLayout()
        for widget in self._tableau_piles:
            tableau_layout.addWidget(widget)
        tableau_layout.addStretch(0)

        # MAIN
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.menu_bar)
        self.layout().addLayout(top_layout)
        self.layout().addSpacing(40)
        self.layout().addLayout(tableau_layout)
        self.layout().addStretch(0)

    def create_connections(self):
        self.stock_pile_wdg.card_clicked.connect(self.on_stock_cliked) 
        self.wast_pile_wdg.card_double_clicked.connect(self.on_card_double_cliked)
        for widget in self._tableau_piles:
            widget.card_double_clicked.connect(self.on_card_double_cliked)

    def _update(self):
        # wast
        self.wast_pile_wdg._update()

        # foundation 
        for widget in self._foundation_piles:
            widget._update()

        # tableau 
        for widget in self._tableau_piles:
            widget._update()

    def new_game(self):
        self._game.new_game()
        self._update()

    def on_new_game_requested(self):
        self.new_game()

    def on_card_double_cliked(self, card):
        for widget in self._foundation_piles:
            pile = widget.get_pile()
            if pile.is_child_acceptable(card):
                pile.add_card(card)
                widget._update()
                break

    def on_stock_cliked(self, card):
        self._game.draw_next()
        self.wast_pile_wdg._update()

def launch_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    solitaireUI = SolitaireUI()
    solitaireUI.show()
    app.exec_()
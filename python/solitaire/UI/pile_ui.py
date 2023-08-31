from PySide2 import QtWidgets, QtCore, QtGui
import PySide2.QtGui
from .card_ui import CardWidget, BaseCardWidget
from . import envs

from functools import partial

class CardSlotLayout(QtWidgets.QLayout):
    def __init__(self, height=envs.CARD_HEIGHT, spacing=0, *args, **kwargs):
        self._list = []
        super(CardSlotLayout, self).__init__(*args, **kwargs)
        self.height = height
        self.setSpacing(spacing)
        self.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(QtCore.Qt.AlignTop)

    def itemAt(self, index):
        if index >= 0 and  index < len(self._list):
            return  self._list[index]
        else :
            return None

    def takeAt(self, index):
        if index >= 0 and index < len(self._list):
            return self._list.pop(index) 
        else :
            return 0

    def items(self):
        return self._list

    def count(self):
        return len(self._list)

    def addItem(self, item):
        item.setAlignment(QtCore.Qt.AlignTop)
        self._list.append(item)

    def setGeometry(self, r):
        super(CardSlotLayout, self).setGeometry(r)
        
        count = len(self._list)
        if count == 0:
            return

        w = r.width() 
        h = r.height() - (count - 1) * self.spacing()
        i = 0
        while i < count :
            o = self._list[i]
            geom = QtCore.QRect(r.x(), r.y() + i * self.spacing(), w, h);
            o.setGeometry(geom)
            i += 1

    def sizeHint(self):
        return QtCore.QSize(envs.CARD_WIDTH, self.height)
    
    def minimumSize(self):
        s = QtCore.QSize(0,0)
        n = len(self._list)
        i = 0
        while i < n:
            o = self._list[i]
            s = s.expandedTo(o.minimumSize())
            i += 1
        
        return s + n * QtCore.QSize(self.spacing(), self.spacing())
    
class PileWidget(QtWidgets.QWidget):
    card_double_clicked = QtCore.Signal(object)
    card_clicked = QtCore.Signal(object)

    def __init__(self, pile,
                       spacing=0, 
                       width=envs.CARD_WIDTH, 
                       height=envs.CARD_HEIGHT, 
                       *args, **kwargs):
        
        self._pile = pile
        self._color = QtGui.QColor(0, 0, 0)

        super().__init__(*args, **kwargs)

        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(width, height)

        self.setLayout(CardSlotLayout(height))
        self.layout().setSpacing(spacing)
        
        self.setAcceptDrops(True)

    def _update(self):
        self.clear()

        for card in self._pile.get_cards():
            card_widget = CardWidget(card)
            card_widget.double_clicked.connect(partial(self.on_card_double_clicked, card_widget))
            card_widget.clicked.connect(partial(self.on_card_clicked, card_widget))
            self.layout().addWidget(card_widget)

    def clear(self):
        while self.layout().itemAt(0):
            item = self.layout().takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def get_pile(self):
        return self._pile

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        rect = self.rect()
        rect.setHeight(envs.CARD_HEIGHT)
        painter.fillRect(rect, self._color)

    def dragEnterEvent(self, event):
        source = event.source()
        if isinstance(source, CardWidget) and not self._pile.get_cards():
            card = source.get_card()
            if self._pile.is_child_acceptable(card):
                self._color = QtGui.QColor(0, 255, 0)
                self.update()
                event.acceptProposedAction()
                event.accept()
                return super().dragEnterEvent(event)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._color = QtGui.QColor(0, 0, 0)
        self.update()
        return super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self._color = QtGui.QColor(0, 0, 0)
        self.update()
        source = event.source()
        self._pile.add_card(source.get_card())
        self._update()

    def on_card_double_clicked(self, widget):
        pass

    def on_card_clicked(self, widget):
        pass

class TableauPileWidget(PileWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(spacing=envs.TABLEAU_PILE_SPACING, 
                         height=envs.TABLEAU_PILE_HEIGHT, 
                         *args, **kwargs)
        
    def on_card_double_clicked(self, widget):
        card = widget.get_card()
        if card.is_last_card():
            self.card_double_clicked.emit(card)
            self._update()
            
class FoundationPileWidget(PileWidget):
    pass

class StockPileWidget(PileWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        card_widget = BaseCardWidget(envs.ICONS["card_downTurned"])
        card_widget.clicked.connect(partial(self.on_card_clicked, card_widget))
        self.layout().addWidget(card_widget)

    def on_card_clicked(self, widget):
        self.card_clicked.emit(None)

class WastPileWidget(PileWidget):
    def on_card_double_clicked(self, widget):
        card = widget.get_card()
        self.card_double_clicked.emit(card)
        self._update()



from PySide2 import QtWidgets, QtCore, QtGui
import os

class BaseCard(QtWidgets.QPushButton):
    WIDTH = 80
    HEIGHT = 100
    ICONS_DIR = 'icons'
    ICON_EXTENSION  = 'png'
    CARDS_FAMILIES = ['hearts', 'diamonds', 'spades', 'clubs']
    CARDS_RANKS = ['as', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    CARD_DOWNTURNED = 'card_downTurned'
    is_downturned = False
    family = None
    rank = None
    
    def __init__(self, *args, **kwargs):
        super(BaseCard, self).__init__(*args[2:], **kwargs)

    def set_size(self, width = WIDTH, height = HEIGHT):
        self.setFixedSize(width, height)

    def set_icon(self, icon_path):
        icon = QtGui.QImage(icon_path)
        icon = icon.scaled(self.width(), self.height(),  QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.pixmap = QtGui.QPixmap()
        self.pixmap.convertFromImage(icon)

        self.update()

    def get_icon_path(self, downTurned = False):
        if downTurned:
            base_name = self.CARD_DOWNTURNED
        else:
            base_name = '{0}_{1}'.format(self.family, self.rank)

        file_name = '{0}.{1}'.format(base_name, self.ICON_EXTENSION)
        path = self.get_file_path(file_name)

        return path

    def get_file_path(self, fileName, folder = ICONS_DIR):
        path = os.path.dirname(__file__)
        path = os.path.split(path)[0]
        path = os.path.join(path, folder, fileName)
        path = os.path.realpath(path)
        return path

    def paintEvent(self, e):
        super(BaseCard, self).paintEvent(e)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

class Card(BaseCard):
    cards = {}
    stack_slot_list  = [] #To add card on double click

    def __new__(cls, *args, **kwargs):
        if not args : #new
            cls.cards = {}
            cls.stack_slot_list  = []

        elif len(args) == 1 : # get card
            card = cls.cards.get(args[0]) 
            if card :
                return card
            else:
                raise RuntimeError('{0} not found in registry'.format(card))

        return super(Card, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.family = args[0]
            self.rank = args[1]

            super(Card, self).__init__(*args[2:], **kwargs)
            
            self.set_size()
            icon_path = self.get_icon_path()
            self.icon_path = icon_path
            self.set_icon(self.icon_path)

            Card.cards[str(self)] = self

    def __repr__(self):
        return 'Card_{0}_{1}'.format(self.family, self.rank)

    @classmethod
    def add_stack_slot(cls, stack_slot):
        cls.stack_slot_list.append(stack_slot)

    def set_downturned(self):
        if not self.is_downturned:
            self.set_icon(self.get_icon_path(downTurned = True))
            self.is_downturned = True

    def turn_up(self):
        if not self.get_children([]):
            if self.is_downturned:
                self.set_icon(self.icon_path)
                self.is_downturned = False


    def get_children(self, children = []):
        parent_widget = self.parentWidget()
        if parent_widget :
            if parent_widget.length() > 1:
                widgets = parent_widget.cards()
                index = widgets.index(self) + 1
                if index < parent_widget.length() :
                    card_child = widgets[index]
                    children.append(card_child)
                    card_child.get_children(children)
        return children

    def get_value(self):
        index = self.CARDS_RANKS.index(self.rank)
        return index

    def get_card_color(self):
        if self.family in self.CARDS_FAMILIES[:2]:
            return 'red'
        else :
            return 'black'

    def get_family(self):
        return self.family

    def get_slot(self):
        return self.parentWidget()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton :
            self.dragStartPosition = QtCore.QPoint(0, 0)

            if not self.is_downturned:
                self.dragStartPosition = event.pos()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton :
            if self.get_value() == 0 : # AS

                if self.get_slot() not in self.stack_slot_list : # If not already in a stack slot:

                    empty_stack_slots = [stack_slot for stack_slot in self.stack_slot_list if stack_slot.length() == 0]
                    if empty_stack_slots :

                        preview_slot = self.get_slot() # get previews slot
                        
                        empty_stack_slots[0].add_card(self)

                        if preview_slot.length() > 0: #turn Up last card of previews slot
                            preview_slot.cards()[-1].turn_up()
            else:
                for stack_slot in self.stack_slot_list: # Other than AS

                    if not stack_slot.length():
                        continue

                    firt_card = stack_slot.cards()[0]

                    if stack_slot.is_compatible(self, firt_card):
                        preview_slot = self.get_slot() # get previews slot

                        stack_slot.add_card(self)

                        if preview_slot.length() > 0: #turn Up last card of previews slot
                            preview_slot.cards()[-1].turn_up()

    def mouseMoveEvent(self, event):
        if self.is_downturned:
            return 
        if not event.buttons() and QtCore.Qt.LeftButton :
            return
        if (event.pos() - self.dragStartPosition).manhattanLength() < QtWidgets.QApplication.startDragDistance() :
            return

        drag = QtGui.QDrag(self);
        mimeData = QtCore.QMimeData()

        mimeData.setText(str(self))
        drag.setMimeData(mimeData)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
        # if dropAction:
        #     self.delete()
        #     self.leaveLayout.emit()

    def delete(self):
        self.close()
        self.deleteLater()

    @classmethod
    def get_cards(cls):
        return cls.cards


class StockCard(BaseCard): # show next card on stock pile, put previews under

    def __new__(cls, *args, **kwargs):
        return super(StockCard, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super(StockCard, self).__init__(*args[2:], **kwargs)
        self.set_size()
        icon_path = self.get_icon_path(downTurned = True)
        self.set_icon(icon_path)
        


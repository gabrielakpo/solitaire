from .Qt import QtWidgets, QtCore, QtGui
from . import envs

class BaseCardWidget(QtWidgets.QPushButton):
    def __init__(self, icon_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(envs.CARD_WIDTH, envs.CARD_HEIGHT)

        self.setIcon(icon_path)
        self.setIconSize(QtCore.QSize(envs.CARD_WIDTH - 5, envs.CARD_HEIGHT - 5))

    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        return super().mouseReleaseEvent(event)

class CardWidget(BaseCardWidget):
    double_clicked = QtCore.Signal()

    def __init__(self, card, *args, **kwargs):
        self._card = card

        if card.is_down_turned():
            icon_path = envs.ICONS["card_downTurned"]
        else:
            icon_path = envs.ICONS[f"{card.get_family()}_{card.get_rank()}"]
            
        super().__init__(icon_path, *args, **kwargs)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(QtCore.Qt.green))
        self.setPalette(palette)
        
        self.setAcceptDrops(True)

    def set_down_turned(self, downturned):
        self._card.set_down_turned(downturned)

    def is_down_turned(self):
        return self._card.is_down_turned()
    
    def is_last_card(self):
        return self._card.is_last_card()
    
    def get_card(self):
        return self._card
    
    def activate_accept_color(self, activate):
        self.setAutoFillBackground(activate)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton :
            self.dragStartPosition = QtCore.QPoint(0, 0)

            if not self.is_down_turned():
                self.dragStartPosition = event.pos()

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.pos() - self.dragStartPosition).manhattanLength() < QtWidgets.QApplication.startDragDistance() \
        or self.is_down_turned() \
        or not event.buttons() and QtCore.Qt.LeftButton:
            return
        
        self.setHidden(True)

        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        pixmap = self.grab()

        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        drag.exec_(QtCore.Qt.MoveAction)

        self.parent()._update()

    def mouseReleaseEvent(self, event):
        if not event.isAccepted():
            self.setVisible(True)
        return super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        source = event.source()
        if isinstance(source, CardWidget):
            card = source.get_card()
            if self._card.is_last_card() and self._card.is_child_acceptable(card):
                self.activate_accept_color(True)
                event.acceptProposedAction()
                event.accept()
                return super().dragEnterEvent(event)
        event.ignore()

    def dragLeaveEvent(self, event):
        self.activate_accept_color(False)
        return super().dragLeaveEvent(event)
    
    def dropEvent(self, event):
        source = event.source()
        self._card.get_pile().add_card(source.get_card())
        self.parent()._update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.double_clicked.emit()

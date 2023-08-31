from .Qt import QtWidgets, QtCore

class CustomToolbar(QtWidgets.QToolBar):
    def __init__(self, *args, **kwargs):
        super(CustomToolbar, self).__init__(*args, **kwargs)
        self.setIconSize(QtCore.QSize(30, 30))

    def add_menu(self, icon=None, text="", menu=None, mode=QtWidgets.QToolButton.InstantPopup):
        button = QtWidgets.QToolButton()
        button.setPopupMode(mode)
        button.setToolButtonStyle(self.toolButtonStyle())
        button.setText(text)
        if text:
            button.setToolTip(text)
        if icon:
            button.setIcon(icon)
        if not menu:
            menu = QtWidgets.QMenu()
        action = QtWidgets.QWidgetAction(button)
        action.setDefaultWidget(menu)
        button.addAction(action)
        self.addWidget(button)
        return menu
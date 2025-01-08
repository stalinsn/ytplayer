import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QPushButton
)
from PyQt5.QtGui import QIcon
from ytplayer.config_manager import load_close_action, save_close_action

class SettingsDialog(QDialog):
    """
    Janela de configurações para escolher entre:
    - Minimizar para tray (default)
    - Fechar completamente
    """
    def __init__(self, parent=None, icon_path="icon.png"):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Configurações")
        self.setFixedSize(300, 150)
        self.setWindowIcon(QIcon(icon_path))
        self.icon_path = icon_path

        self.initUI()
        self.load_settings()

    def initUI(self):
        layout = QVBoxLayout()

        self.group = QButtonGroup(self)
        self.rb_minimize_to_tray = QRadioButton("Minimizar para a bandeja (Tray)")
        self.rb_close_completely = QRadioButton("Fechar completamente")

        self.group.addButton(self.rb_minimize_to_tray)
        self.group.addButton(self.rb_close_completely)

        layout.addWidget(self.rb_minimize_to_tray)
        layout.addWidget(self.rb_close_completely)

        button_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.save_settings)
        button_layout.addWidget(btn_ok)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_settings(self):
        close_action = load_close_action()
        if close_action == "tray":
            self.rb_minimize_to_tray.setChecked(True)
        else:
            self.rb_close_completely.setChecked(True)

    def save_settings(self):
        if self.rb_minimize_to_tray.isChecked():
            save_close_action("tray")
        else:
            save_close_action("close")

        self.accept()  # Fecha a janela de configurações

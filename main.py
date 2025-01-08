import sys
import os
from PyQt5.QtWidgets import QApplication
from ytplayer.single_instance import SingleInstance
from ytplayer.main_window import MainWindow

def resource_path(relative_path: str) -> str:
    """ 
    Ajusta o caminho para rodar tanto empacotado (PyInstaller) 
    quanto em modo desenvolvimento.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

def load_dark_style():
    """
    Carrega um arquivo QSS para estilo dark, se existir.
    """
    qss_file = resource_path(os.path.join("resources", "dark_style.qss"))
    if os.path.exists(qss_file):
        with open(qss_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """
        /* Estilo global */
        * {
            font-family: Arial, sans-serif;
            color: #ffffff;
            background-color: #2d2d2d;
        }

        /* Janela Principal */
        QMainWindow {
            background-color: #2d2d2d;
        }

        /* Barra de Título */
        #TitleBar {
            background-color: #1e1e1e;
            min-height: 25px; /* altura menor */
        }
        #TitleLabel {
            padding-left: 10px;
        }
        #BtnTitleBar {
            background-color: #2d2d2d;
            border: none;
            width: 30px;
            height: 25px; /* ajusta altura também */
        }
        #BtnTitleBar:hover {
            background-color: #444444;
        }

        /* Dialogs (Como o SettingsDialog) */
        QDialog {
            background-color: #2d2d2d;
        }
        QRadioButton {
            font-size: 14px;
        }
        QPushButton {
            background-color: #2d2d2d;
            border: 1px solid #444;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #3d3d3d;
        }
        """

def main():
    # Verifica se já existe uma instância
    single_instance = SingleInstance()
    if single_instance.already_running():
        print("O programa já está em execução.")
        sys.exit(0)

    app = QApplication(sys.argv)

    # Configura estilo global
    qss = load_dark_style()
    app.setStyleSheet(qss)

    window = MainWindow(icon_path="icon.png")
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

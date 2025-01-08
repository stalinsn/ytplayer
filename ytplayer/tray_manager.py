import threading
from PIL import Image
import pystray
from pystray import MenuItem as item
from PyQt5.QtCore import QTimer

class TrayManager:
    """
    Gerencia o ícone na bandeja do sistema utilizando pystray.
    """
    def __init__(self, icon_path, on_restore, on_exit):
        """
        :param icon_path: Caminho para o arquivo de ícone
        :param on_restore: Função/callback para restaurar a janela principal
        :param on_exit: Função/callback para sair completamente do programa
        """
        self.icon_path = icon_path
        self.on_restore = on_restore
        self.on_exit = on_exit
        self.icon = None
        self.thread = None

    def start(self):
        """
        Inicia o ícone na bandeja em uma thread separada.
        """
        if self.thread is None:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def _run(self):
        try:
          print("[TrayManager] Iniciando Tray...")
          icon_img = Image.open(self.icon_path)
          menu = (
              item("Restaurar", self._on_restore_click),
              item("Sair", self._on_exit_click)
          )
          self.icon = pystray.Icon("ytplayer_tray", icon_img, "YT Music Player", menu)
          self.icon.run()
        except Exception as e:
          print("[TrayManager] ERRO:", e)

    def _on_restore_click(self, icon=None, item=None):
        """
        Chamado quando o usuário clica em "Restaurar" no menu do tray.
        Usamos QTimer.singleShot(0, ...) para executar na thread principal do Qt.
        """
        QTimer.singleShot(0, self.on_restore)

    def _on_exit_click(self, icon=None, item=None):
        """
        Chamado quando o usuário clica em "Sair" no menu do tray.
        """
        QTimer.singleShot(0, self.on_exit)

    def stop(self):
        """
        Para remover o ícone do tray corretamente antes de sair.
        """
        if self.icon is not None:
            print("[TrayManager] Parando Tray...")
            self.icon.stop()
            self.icon = None

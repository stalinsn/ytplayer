import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QApplication
)
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from ytplayer.settings_dialog import SettingsDialog
from ytplayer.config_manager import load_close_action
from ytplayer.tray_manager import TrayManager

class ResizeGrip(QWidget):
    """
    Widget que serve como "faixa de redimensionamento".
    Dependendo de orientation (right/bottom/corner), redimensiona
    a largura, a altura ou ambos.
    """
    def __init__(self, orientation="right", grip_size=6, parent=None):
        super().__init__(parent)
        self.orientation = orientation
        self.grip_size = grip_size
        self._resizing = False
        self._start_pos = QPoint()

        # Define tamanho fixo e cursor específico
        if self.orientation == "right":
            self.setFixedWidth(self.grip_size)
            self.setCursor(Qt.SizeHorCursor)
        elif self.orientation == "bottom":
            self.setFixedHeight(self.grip_size)
            self.setCursor(Qt.SizeVerCursor)
        elif self.orientation == "corner":
            self.setFixedSize(self.grip_size, self.grip_size)
            self.setCursor(Qt.SizeFDiagCursor)

        # Adiciona um estilo visível (borda pontilhada)
        # para você enxergar onde está a faixa/canto
        self.setStyleSheet("""
            background-color: rgba(255, 0, 0, 0.1);
            border: 1px dotted #ff0000;
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._resizing = True
            self._start_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._resizing and event.buttons() == Qt.LeftButton:
            # Pega a janela principal
            main_window = self.window()
            if isinstance(main_window, QMainWindow):
                self.do_resize(event.globalPos(), main_window)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._resizing = False

    def do_resize(self, global_pos, main_window):
        """
        Redimensiona a janela de acordo com a orientação.
        """
        geometry = main_window.geometry()
        dx = global_pos.x() - self._start_pos.x()
        dy = global_pos.y() - self._start_pos.y()

        new_width = geometry.width()
        new_height = geometry.height()

        if self.orientation in ("right", "corner"):
            new_width += dx
        if self.orientation in ("bottom", "corner"):
            new_height += dy

        # Impede de ficar menor que o mínimo configurado na janela
        new_width = max(new_width, main_window.minimumWidth())
        new_height = max(new_height, main_window.minimumHeight())

        # Aplica o novo tamanho
        main_window.resize(new_width, new_height)

        # Atualiza o ponto inicial para não "acumular" o delta
        self._start_pos = global_pos

class MainWindow(QMainWindow):
    def __init__(self, icon_path="icon.png"):
        super().__init__()
        self.icon_path = icon_path
        self.setWindowIcon(QIcon(self.icon_path))
        self.setWindowTitle("YT Music Player")
        self.resize(1000, 600)

        # Define um tamanho mínimo
        self.setMinimumSize(600, 400)

        # Carrega configurações
        self.close_action = load_close_action()

        # Retira a moldura padrão
        self.setWindowFlag(Qt.FramelessWindowHint)

        # ========== Layout principal em GRID ========== #
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Usamos QGridLayout para dividir em [conteúdo, right_grip] x [bottom_grip, corner]
        main_layout = QGridLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ========== Conteúdo principal ========== #
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # ---- Barra de Título ----
        title_bar = QWidget()
        title_bar.setObjectName("TitleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)

        # Botões de navegação
        self.btn_back = QPushButton("←")
        self.btn_back.clicked.connect(self.navigate_back)
        self.btn_forward = QPushButton("→")
        self.btn_forward.clicked.connect(self.navigate_forward)
        self.btn_reload = QPushButton("↻")
        self.btn_reload.clicked.connect(self.navigate_reload)

        # Botão fechar
        btn_close = QPushButton("✕")
        btn_close.setObjectName("BtnCloseBar")
        btn_close.clicked.connect(self.handle_close)

        # Botão minimizar
        btn_minimize = QPushButton("–")
        btn_minimize.setObjectName("BtnMinimizeBar")
        btn_minimize.clicked.connect(self.minimize_to_tray)

        # Botão configurações
        btn_settings = QPushButton("⚙")
        btn_settings.setObjectName("BtnSettingsBar")
        btn_settings.clicked.connect(self.show_settings)

        # Título
        self.title_label = QLabel("YT Music Player - by devmosts2")
        self.title_label.setObjectName("TitleLabel")

        # Monta layout da barra
        title_bar_layout.addWidget(self.btn_back)
        title_bar_layout.addWidget(self.btn_forward)
        title_bar_layout.addWidget(self.btn_reload)
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(btn_settings)
        title_bar_layout.addWidget(btn_minimize)
        title_bar_layout.addWidget(btn_close)

        content_layout.addWidget(title_bar)

        # ---- Browser ----
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://music.youtube.com"))
        content_layout.addWidget(self.browser)

        # Conecta urlChanged para atualizar botões de navegação
        self.browser.urlChanged.connect(self.update_nav_buttons)
        self.update_nav_buttons()

        # Adiciona o "content_widget" (barra + browser) ao layout
        main_layout.addWidget(content_widget, 0, 0)  # row=0, col=0

        # Permite que a célula [0,0] expanda
        main_layout.setRowStretch(0, 1)
        main_layout.setColumnStretch(0, 1)

        # ========== Borda Direita ========== #
        self.right_grip = ResizeGrip("right", grip_size=6, parent=central_widget)
        # Adiciona no grid
        main_layout.addWidget(self.right_grip, 0, 1)  # row=0, col=1

        # ========== Borda Inferior ========== #
        self.bottom_grip = ResizeGrip("bottom", grip_size=6, parent=central_widget)
        main_layout.addWidget(self.bottom_grip, 1, 0)  # row=1, col=0

        # ========== Canto (diagonal) ========== #
        self.corner_grip = ResizeGrip("corner", grip_size=6, parent=central_widget)
        main_layout.addWidget(self.corner_grip, 1, 1)  # row=1, col=1

        # Tray Manager
        self.tray_manager = TrayManager(
            self.icon_path,
            on_restore=self.restore_from_tray,
            on_exit=self.close_application
        )
        self.tray_manager.start()

    # ========== Permitir arrastar a janela pela barra de título ========== #
    def mousePressEvent(self, event):
        # Se clicou na parte superior (barra de título), arrasta janela
        # (Poderia checar se event.y() < algo, mas aqui é simples.)
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    # ========== Navegação ========== #
    def navigate_back(self):
        if self.browser.page().history().canGoBack():
            self.browser.back()

    def navigate_forward(self):
        if self.browser.page().history().canGoForward():
            self.browser.forward()

    def navigate_reload(self):
        self.browser.reload()

    def update_nav_buttons(self):
        history = self.browser.page().history()
        self.btn_back.setEnabled(history.canGoBack())
        self.btn_forward.setEnabled(history.canGoForward())

    # ========== Botões Minimizar/Fechar/Config ========== #
    def show_settings(self):
        dialog = SettingsDialog(self, icon_path=self.icon_path)
        if dialog.exec_():
            self.close_action = load_close_action()

    def handle_close(self):
        if self.close_action == "tray":
            self.minimize_to_tray()
        else:
            self.close_application()

    def minimize_to_tray(self):
        self.hide()

    def restore_from_tray(self):
        if not self.isVisible():
            self.showNormal()
            self.raise_()
            self.activateWindow()

    def close_application(self):
        self.tray_manager.stop()
        QApplication.quit()

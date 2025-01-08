import sys
from PyQt5.QtCore import QSharedMemory

class SingleInstance:
    """
    Classe para garantir que apenas uma instância do programa seja executada.
    Usa QSharedMemory para checar se existe um segmento de memória compartilhada.
    """
    def __init__(self, key="ytplayer_single_instance_key"):
        self.key = key
        self.shared_memory = QSharedMemory(self.key)

    def already_running(self):
        if self.shared_memory.attach():
            # Já existe outra instância
            return True

        if not self.shared_memory.create(1):
            # Não foi possível criar o segmento de memória
            return True

        return False

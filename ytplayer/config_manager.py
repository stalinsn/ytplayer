import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ytplayer_config.json")

def load_close_action():
    """
    Lê a configuração do arquivo JSON.
    Retorna "tray" se não existir.
    """
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("close_action", "tray")
        except:
            return "tray"
    return "tray"

def save_close_action(action):
    """
    Salva a ação de fechamento (ex: "tray" ou "close") no arquivo JSON.
    """
    data = {
        "close_action": action
    }
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Erro ao salvar configurações:", e)

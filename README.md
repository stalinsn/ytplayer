# YT Music Player

![image](https://github.com/user-attachments/assets/ce7536bf-bbca-4423-9530-113351459201)


Player de música **frameless** em **PyQt5** que incorpora o site [YouTube Music](https://music.youtube.com), com bandeja (tray icon), configuração de ação ao fechar, e opção de **dark theme** customizado.

## Recursos Principais

- **Janela frameless** (sem barra de título nativa), com barra personalizada.  
- **Integração** com site do YouTube Music (via `QWebEngineView`).  
- **Minimizar** para bandeja (tray), com ícone e menu de contexto.  
- **Opções** de fechar completamente ou minimizar para bandeja (definido em configurações).  
- **Tema Dark** custom (carregando arquivo `.qss`).  
- **Redimensionamento** manual (barras e cantos) para janelas frameless.  
- **Apenas uma instância** por vez (via `SingleInstance`).  

---

## Requisitos

### Em desenvolvimento (rodar via Python)

- **Windows 10** ou superior (funciona em outras versões do Windows também).  
- **Python 3.7+** (recomendado Python 3.10 ou superior).  
- Bibliotecas Python instaladas (ver seção [Dependências](#dependências)).  

### Executável (pós-compilação)

- **Somente** o `.exe` gerado, **não precisa** de Python instalado.  
- Em alguns casos, o **Visual C++ Redistributable** (VC Runtime) pode ser necessário (geralmente já vem no Windows 10).  

---

## Dependências

No desenvolvimento, as seguintes bibliotecas Python são necessárias:

- **PyQt5** (GUI)  
- **PyQtWebEngine** (Navegador embutido)  
- **pystray** (Ícone na bandeja)  
- **Pillow** (Manipulação de imagens para pystray)  
- **PyInstaller** (opcional, mas usado para gerar executável)

Exemplo de `requirements.txt`:
```
PyQt5>=5.15
PyQtWebEngine>=5.15
pystray
Pillow
```

*(A versão exata pode variar, mas 5.15 é estável.)*

---

## Como Executar (Modo Desenvolvimento)

1. **Clonar** ou baixar o projeto em uma pasta local, por exemplo `C:\YTPlayer\`.  
2. **Abrir** um **Prompt de Comando** ou **Powershell** nessa pasta.  
3. **Instalar** as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   ou manualmente:
   ```bash
   pip install PyQt5 PyQtWebEngine pystray Pillow
   ```
4. **Executar** o programa:
   ```bash
   python main.py
   ```
   - A janela principal será aberta, carregando [music.youtube.com].  
   - O estilo Dark será aplicado, se o arquivo `resources/dark_style.qss` for encontrado.  

---

## Como Compilar (Gerar Executável)

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Rodar o PyInstaller

Na raiz do projeto (onde está `main.py`), execute um comando como:
```bash
pyinstaller --noconsole --onefile --icon=icon.ico main.py
```
- `--noconsole`: não mostra janela de console ao iniciar.  
- `--onefile`: empacota tudo em um único arquivo `.exe`.  
- `--icon=icon.ico`: define ícone para o executável (caso deseje).  

Se você **usa** arquivos extras como `.qss` (tema) ou imagens que precisam ser incluídas no executável, use `--add-data`. Exemplo:

```bash
pyinstaller --noconsole --onefile --icon=icon.ico \
    --add-data "resources/dark_style.qss;resources" \
    --add-data "icon.png;." \
    main.py
```
No **Windows**, separe `origem;destino` com ponto-e-vírgula. (Em Linux/macOS, use `:`.)

### 3. Verificar a pasta `dist/`

- Será criada a pasta `dist/`, onde estará **`main.exe`** (ou o nome do seu script).  
- **Teste** executando:
  ```bash
  dist\main.exe
  ```

### 4. Distribuindo o Executável

- Você pode **copiar** a pasta `dist/` para outro PC com Windows 10 e rodar `main.exe` sem precisar instalar Python.  
- Se o Windows do usuário **não** tiver o Visual C++ Redistributable atualizado, talvez seja necessário instalar. Normalmente, no Windows 10+ isso já vem incluso.

---

## Observações

- Se ao rodar o executável não carregar o tema (qss), verifique se o **caminho de recursos** está usando algo como `sys._MEIPASS` (ver `resource_path` no código).  
- O **ícone do tray** pode demorar alguns segundos para aparecer na bandeja em algumas versões do Windows.  
- Para **depurar** ou ver `print()` no console do Windows, gere o executável **sem** `--noconsole` ou rode-o via prompt.

---

## Licença

hihi


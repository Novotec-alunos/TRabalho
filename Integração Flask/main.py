import threading
import time
from flask import Flask, render_template
import PySimpleGUI as sg
from teste import gerar_link_pagamento

app = Flask(__name__)

# Variável global para armazenar o status do pagamento
status_pagamento = None

@app.route("/")
def homepage():
    link_iniciar_pagamento = gerar_link_pagamento()
    return render_template("homepage.html", link_pagamento=link_iniciar_pagamento)

@app.route("/compracerta")
def compra_certa():
    global status_pagamento
    status_pagamento = "sucesso"
    return "Pagamento concluído com sucesso!"

@app.route("/compraerrada")
def compra_errada():
    global status_pagamento
    status_pagamento = "erro"
    return "Pagamento não foi concluído!"

# Função para iniciar o servidor Flask em uma thread separada
def iniciar_flask():
    app.run(port=5000, debug=False, use_reloader=False)

# Inicia o Flask em uma thread
thread_flask = threading.Thread(target=iniciar_flask)
thread_flask.daemon = True
thread_flask.start()

# Interface PySimpleGUI
layout = [
    [sg.Text("Aguardando pagamento...", key="-STATUS-", size=(40, 1))],
    [sg.Button("Verificar Status"), sg.Button("Sair")],
]

janela = sg.Window("Pagamento com Flask e PySimpleGUI", layout)

# Loop principal do PySimpleGUI
while True:
    evento, valores = janela.read(timeout=100)  # Checa eventos a cada 100ms

    if evento == sg.WINDOW_CLOSED or evento == "Sair":
        break

    if evento == "Verificar Status":
        # Atualiza o status com base na variável global
        if status_pagamento == "sucesso":
            janela["-STATUS-"].update("Pagamento realizado com sucesso!")
        elif status_pagamento == "erro":
            janela["-STATUS-"].update("Pagamento falhou. Tente novamente.")
        else:
            janela["-STATUS-"].update("Aguardando pagamento...")

    # Atualização automática (se necessário)
    if status_pagamento == "sucesso":
        janela["-STATUS-"].update("Pagamento realizado com sucesso!")
    elif status_pagamento == "erro":
        janela["-STATUS-"].update("Pagamento falhou. Tente novamente.")

janela.close()

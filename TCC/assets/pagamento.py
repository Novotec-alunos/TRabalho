import mercadopago
import PySimpleGUI as sg
import webbrowser


def gerar_link_pagamento():
    sdk = mercadopago.SDK("APP_USR-875399821833975-111822-d83e217e7f2d9cc31574a794c030b41f-2107004610")

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
    }

    payment_data = {
        "items": [
            #Produto1 -------------------------
            {
                "id": "1",
                "title": "Aula de natação", 
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 49.99
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:5000/compracerta",
            "failure": "http://127.0.0.1:5000/compraerrada",
            "pending": "http://127.0.0.1:5000/compraerrada",
        },
        "auto_return": "approved"
    }
    
        
    result = sdk.preference().create(payment_data, request_options)
    payment = result["response"]
    link_iniciar_pagamento = payment['init_point']
    print(payment)
    return link_iniciar_pagamento















# Layout da interface gráfica
layout = [
    [sg.Text("Clique no botão para iniciar o pagamento:")],
    [sg.Button("Pagar agora", key="PAGAR")]
]

# Criação da janela
window = sg.Window("Tela de Pagamento", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    if event == "PAGAR":
        link = gerar_link_pagamento()
        sg.popup("Redirecionando para o pagamento...", auto_close=True)
        webbrowser.open(link)

window.close()
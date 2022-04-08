import json
import requests

# Exemplo GET
resposta_hoteis = requests.request('GET', 'http://127.0.0.1:5000/hoteis')
print(resposta_hoteis.status_code)
print(resposta_hoteis.json())

# Exemplo POST
body_cadastro = {
    'login': 'teste',
    'senha': '12345'
}

header_cadastro = {
    'Content-Type': 'application/json'
}

resposta_cadastro = requests.request('POST', 'http://127.0.0.1:5000/cadastro', json=body_cadastro, headers=header_cadastro)
print(resposta_cadastro.status_code)
print(resposta_cadastro.json())

# Exemplo POST Login
body_login = {
        "login": "maura",
        "senha": "12345"
}

header_login = {
    'Content-Type': 'application/json'
}

resposta_login = requests.request('POST', 'http://127.0.0.1:5000/login', json=body_login, headers=header_login)
access_token = resposta_login.json()['access_token']
print(resposta_login.status_code)
print(f'Access_Token {access_token}')

# Exemplo POST Hotel
body_hotel = {
    "nome": "Meu Hotel",
    "estrelas": 3.0,
    "diaria": 400.0,
    "cidade": "Recife",
    "site_id": 2
}

header_hotel = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
}

resposta_hotel = requests.request('POST', 'http://127.0.0.1:5000/hoteis/meuhotel', json=body_hotel, headers=header_hotel)
print(resposta_hotel.status_code)
print(resposta_hotel.json())

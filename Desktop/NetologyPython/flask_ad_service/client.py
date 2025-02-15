import requests

# response = requests.post('http://127.0.0.1:5000/api/v1/user',
#                          json={'name': 'user_1', 'password': 'дDлыт1а', 'email': 'blag@mail.com'},
#                          )

# response = requests.get('http://127.0.0.1:5000/api/v1/user/1')

# response = requests.delete('http://127.0.0.1:5000/api/v1/user/1')

# response = requests.post('http://127.0.0.1:5000/api/v1/advertisement',
#                          json={'header': 'adv_1', 'description': 'chto-to', 'id_user': 1},
#                          )

# response = requests.delete('http://127.0.0.1:5000/api/v1/advertisement/1?owner=1')

# response = requests.patch('http://127.0.0.1:5000/api/v1/advertisement/1?owner=1',
#                           json={'description': 'lodka'},
#                           )

# response = requests.get('http://127.0.0.1:5000/api/v1/advertisement/1')

print(response.status_code)
if response.request.method == 'POST' or response.request.method == 'GET' or response.request.method == 'PATCH':
    print(response.json())
if response.request.method == 'DELETE':
    print(response.text)

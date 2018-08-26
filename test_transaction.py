import requests
import json
import sys

data = {"sender": "1DBYzJQ6v6qW17m8jH8KjBgJtcXfEUf7YV",
        "recipient": "1EPhga3t6PCAxs1fGJAQSnh3jKKbxewzNM",
        "amount": 30, "comment": "test transaction"}

r = requests.post("http://127.0.0.1:5000/transactions/new", json=data)

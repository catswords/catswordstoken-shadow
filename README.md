# catswordstoken-shadow
CatswordsToken Shadow is PoC, integrate to other blockchain networks

## requirements (pip install x)
- flask
- base58

## step by step
1. python server.py
2. python test_transaction.py
3. python test_mine.py
4. python test_chain.py

## spec
- new transaction: /transaction/new, POST, fields: sender, recipent, amount, comment
- mine: /mine, GET
- chain: /chain, GET
- address: /address/new, GET

## CatswordsToken
- https://github.com/catswords/catswordstoken

## contact us
- Go Namhyeon <gnh1201@gmail.com>

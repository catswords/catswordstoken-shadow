# catswordstoken-shadow
CatswordsToken Shadow is PoC, integrate to other blockchain networks

## Requirements (pip install x)
- flask
- base58

## Step by step
1. python server.py
2. python test_transaction.py
3. python test_mine.py
4. python test_chain.py

## API Specification
- new transaction: /transaction/new, POST, fields: sender, recipent, amount, comment
- mine: /mine, GET
- chain: /chain, GET
- address: /address/new, GET

## CatswordsToken
- https://github.com/catswords/catswordstoken

## See also
- https://github.com/gnh1201/reasonableframework

## Contact us
- Go Namhyeon <gnh1201@gmail.com>

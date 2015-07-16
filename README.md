# Morpy
## A python tool for finding independent chess positions

Takes rectangular chess board dimensions and numbers of each piece type,
returns all the positions that utilize all the pieces while keeping them independent
(not threatening each other).

Morpy is named after [Paul Morphy](https://en.wikipedia.org/wiki/Paul_Morphy).

## Usage example
```bash
$ morpy.py --help
usage: morpy.py [-h] [--kings n] [--queens n] [--bishops n] [--knights n]
                [--rooks n] [--print-pieces]
                N M

positional arguments:
  N               First board dimension
  M               Second board dimension

optional arguments:
  -h, --help      show this help message and exit
  --kings n       Number of king pieces to place on the board
  --queens n      Number of queen pieces to place on the board
  --bishops n     Number of bishop pieces to place on the board
  --knights n     Number of knight pieces to place on the board
  --rooks n       Number of rook pieces to place on the board
  --print-pieces  Print the pieces to be placed on the board
```

```bash
$ time morpy.py 7 7 --kings 2 --queens 2 --bishops 2 --knights 1
3063828

real	1m36.006s
user	1m35.092s
sys	0m0.864s
```

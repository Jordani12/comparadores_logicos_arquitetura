# Comparadores Lógicos — Grupo 9

Trabalho de Arquitetura e Organização de Computadores.
Integrantes: Gustavo, Arthur, Kauã e Gabriel.

## Descrição
Simulação em Python de um **comparador binário de 4 bits** construído apenas com portas lógicas (NOT, AND, OR, XNOR). O circuito recebe dois números A e B (4 bits) e ativa exatamente uma saída: **A>B**, **A=B** ou **A<B**.

Lógica:
- `xi = Ai XNOR Bi` (1 quando os bits da posição i são iguais)
- `A=B = x3·x2·x1·x0`
- `A>B = A3·B3' + x3·A2·B2' + x3·x2·A1·B1' + x3·x2·x1·A0·B0'`
- `A<B = NOR(A>B, A=B)`

O código também traz o comparador de 1 bit e um teste automático das 256 combinações possíveis, conferido contra os operadores do Python.

## Como executar
Requisito: Python 3.8 ou superior (sem bibliotecas externas).

```bash
python comparador.py          # exemplo (A=11, B=9), tabela de 1 bit e teste das 256 combinações
python comparador.py 5 12     # compara A=5 com B=12 (valores de 0 a 15)
```

## Exemplo de saída
```
ENTRADA
  A = 1011 (11)
  B = 1001 (9)
PROCESSAMENTO
  xi = Ai XNOR Bi (x3..x0) = 1101
SAÍDA
  A>B = 1 | A=B = 0 | A<B = 0
```

## Estrutura
- `comparador.py`: portas lógicas, comparadores de 1 e 4 bits, demonstração e teste.
- `README.md`: este arquivo.

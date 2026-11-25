"""Comparador lógico de 4 bits construído apenas com portas lógicas.

Saídas: A>B, A=B, A<B (exatamente uma delas vale 1).
Uso:
    python comparador.py            # exemplo + tabela de 1 bit + teste das 256 combinações
    python comparador.py 11 9       # compara A=11 com B=9 (valores de 0 a 15)
"""
import sys
from itertools import product


# ---------- Portas lógicas (entradas e saídas: 0 ou 1) ----------
def NOT(a):
    return 1 - a


def AND(*entradas):
    r = 1
    for e in entradas:
        r &= e
    return r


def OR(*entradas):
    r = 0
    for e in entradas:
        r |= e
    return r


def XNOR(a, b):
    # 1 quando os bits são iguais: (A AND B) OR (NOT A AND NOT B)
    return OR(AND(a, b), AND(NOT(a), NOT(b)))


def comparador_1bit(a, b):
    """Retorna (A>B, A=B, A<B)."""
    maior = AND(a, NOT(b))
    igual = XNOR(a, b)
    menor = AND(NOT(a), b)
    return maior, igual, menor


def comparador_4bits(A, B):
    """A e B são tuplas (bit3, bit2, bit1, bit0), do MSB para o LSB.
    Retorna (A>B, A=B, A<B) e o vetor x de empates por bit."""
    a3, a2, a1, a0 = A
    b3, b2, b1, b0 = B

    # xi = 1 quando Ai == Bi (empate no bit i)
    x3, x2, x1, x0 = XNOR(a3, b3), XNOR(a2, b2), XNOR(a1, b1), XNOR(a0, b0)

    igual = AND(x3, x2, x1, x0)
    maior = OR(
        AND(a3, NOT(b3)),
        AND(x3, a2, NOT(b2)),
        AND(x3, x2, a1, NOT(b1)),
        AND(x3, x2, x1, a0, NOT(b0)),
    )
    menor = NOT(OR(maior, igual))  # NOR: nem maior, nem igual
    return (maior, igual, menor), (x3, x2, x1, x0)


# ---------- Utilitários ----------
def para_bits(n):
    """Inteiro 0..15 -> tupla (b3, b2, b1, b0)."""
    return tuple((n >> i) & 1 for i in (3, 2, 1, 0))


def mostrar(a, b):
    A, B = para_bits(a), para_bits(b)
    (maior, igual, menor), x = comparador_4bits(A, B)
    print("ENTRADA")
    print(f"  A = {''.join(map(str, A))} ({a})")
    print(f"  B = {''.join(map(str, B))} ({b})")
    print("PROCESSAMENTO")
    print(f"  xi = Ai XNOR Bi (x3..x0) = {''.join(map(str, x))}")
    print("SAÍDA")
    print(f"  A>B = {maior} | A=B = {igual} | A<B = {menor}")


def tabela_1bit():
    print("Tabela-verdade do comparador de 1 bit")
    print(" A B | A>B A=B A<B")
    for a, b in product((0, 1), repeat=2):
        g, e, l = comparador_1bit(a, b)
        print(f" {a} {b} |  {g}   {e}   {l}")


def testar_tudo():
    """Compara o circuito com os operadores do Python em todas as 256 combinações."""
    erros = 0
    for a, b in product(range(16), repeat=2):
        (g, e, l), _ = comparador_4bits(para_bits(a), para_bits(b))
        esperado = (int(a > b), int(a == b), int(a < b))
        if (g, e, l) != esperado or g + e + l != 1:
            erros += 1
            print(f"ERRO: A={a} B={b} obtido={(g, e, l)} esperado={esperado}")
    print(f"Teste das 256 combinações: {'OK, 0 erros' if erros == 0 else f'{erros} erros'}")
    return erros


if __name__ == "__main__":
    if len(sys.argv) == 3:
        a, b = int(sys.argv[1]), int(sys.argv[2])
        if not (0 <= a <= 15 and 0 <= b <= 15):
            sys.exit("Use valores de 0 a 15.")
        mostrar(a, b)
    else:
        mostrar(11, 9)
        print()
        tabela_1bit()
        print()
        sys.exit(1 if testar_tudo() else 0)

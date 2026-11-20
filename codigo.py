import random
import time
import unittest


def normalizar(item, modo="exato"):
    if modo == "exato" or not isinstance(item, str):
        return item
    if modo == "texto":
        return item.strip().lower()
    if modo == "anagrama":
        return tuple(sorted(item.replace(" ", "").lower()))
    raise ValueError(f"Modo desconhecido: {modo}")


def tem_duplicata_lenta(lista, modo="exato"):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if normalizar(lista[i], modo) == normalizar(lista[j], modo):
                return True
    return False


def tem_duplicata_rapida(lista, modo="exato"):
    vistos = set()
    for item in lista:
        chave = normalizar(item, modo)
        if chave in vistos:
            return True
        vistos.add(chave)
    return False


class TestesDuplicata(unittest.TestCase):
    def test_modos(self):
        casos = [
            ([], "exato"),
            ([1, 2, 3, 2], "exato"),
            (["Ana", " ana "], "texto"),
            (["amor", "roma"], "anagrama"),
            (["amor", "casa", "sol"], "anagrama"),
        ]
        for entrada, modo in casos:
            self.assertEqual(
                tem_duplicata_rapida(entrada, modo),
                tem_duplicata_lenta(entrada, modo),
            )


def medir(funcao, entrada, modo="exato", repeticoes=3):
    melhor = float("inf")
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(entrada, modo)
        melhor = min(melhor, time.perf_counter() - inicio)
    return melhor


if __name__ == "__main__":
    unittest.main(exit=False)

    print("\nn       | Lenta O(n²) | Rápida O(n)")
    print("-" * 38)
    for n in [1_000, 10_000, 50_000]:
        dados = list(range(n))
        random.shuffle(dados)
        t_lenta = medir(tem_duplicata_lenta, dados)
        t_rapida = medir(tem_duplicata_rapida, dados)
        print(f"{n:<7} | {t_lenta:<13.6f} | {t_rapida:<12.6f}")
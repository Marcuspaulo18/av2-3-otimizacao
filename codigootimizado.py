import time
import random
import unittest
# ---------------------------------------------------------------------------
# NORMALIZAÇÃO DE CHAVES (RELATÓRIO: explica equivalência e anagramas)
# Converte itens brutos em uma representação padrão ("chave canônica") para
# permitir detectar duplicatas de texto ou anagramas usando estrutura de hash.
# - "exato": mantém o valor original.
# - "texto": padroniza espaços e caixa (ex.: "Ana" == " ana ").
# - "anagrama": remove espaços, coloca em minúsculas, ordena os caracteres e
#   converte para tuple (imutável/hashável), fazendo anagramas gerarem a mesma chave.
# ---------------------------------------------------------------------------
def normalizar(item, modo="exato"):
    if modo == "exato" or not isinstance(item, str):
        return item
    if modo == "texto":
        return item.strip().lower()
    if modo == "anagrama":
        return tuple(sorted(item.replace(" ", "").lower()))
    raise ValueError(f"Modo desconhecido: {modo}")

# ---------------------------------------------------------------------------
# VERSÃO ORIGINAL - O(n²) NO PIOR CASO (RELATÓRIO: diagnóstico e gargalo)
# Compara todos os pares possíveis (i, j) com dois laços aninhados.
# Gargalo: no pior caso (sem duplicatas), faz n*(n-1)/2 comparações, tornando
# o crescimento quadrático conforme 'n' aumenta. Espaço auxiliar: O(1).
# ---------------------------------------------------------------------------
def vduplicataoriginal(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False

# ---------------------------------------------------------------------------
# VERSÃO OTIMIZADA - O(n) MÉDIO COM SET (RELATÓRIO: otimização e trade-off)
# Substitui a busca par a par por um 'set' (tabela hash), onde consulta ('in')
# e inserção ('add') levam O(1) em média. Percorre a lista uma única vez.
# Trade-off: ganha muito em tempo, mas usa até O(n) de memória extra em
# 'vistos' (e exige que as chaves sejam hasháveis).
# ---------------------------------------------------------------------------
def vduplicataotimizada(lista, modo="exato"):
    vistos = set()
    for item in lista:
        chave = normalizar(item, modo)
        if chave in vistos:
            return True
        vistos.add(chave)
    return False

# ---------------------------------------------------------------------------
# TESTES AUTOMATIZADOS (RELATÓRIO: comprovação de correção e equivalência)
# Garante que a versão otimizada mantém o mesmo resultado da original no modo
# "exato" e valida os comportamentos esperados nos modos "texto" e "anagrama".
# Nota: métodos de teste no unittest precisam começar com "test_".
# ---------------------------------------------------------------------------
class testeduplicata(unittest.TestCase):
    def casosentradas(self):
        casosexatos = [
            [],
            [1, 2, 3],
            [1, 2, 3, 4, 5, 6, 5, 3, 2],
        ]
        for entrada in casosexatos:
            self.assertEqual(
                vduplicataoriginal(entrada),
                vduplicataotimizada(entrada, "exato")
            )

        self.assertFalse(vduplicataotimizada(["pata", "peta", "pita", "pota", "mario"], "texto"))
        self.assertTrue(vduplicataotimizada(["roma", "amor", "amora", "romana"], "anagrama"))
        self.assertTrue(vduplicataotimizada(["caixa", "caxias", "rua", "ura", "faz", "urro"], "anagrama"))

# ---------------------------------------------------------------------------
# MEDIÇÃO DE DESEMPENHO (RELATÓRIO: metodologia de benchmark)
# Usa time.perf_counter() para alta precisão, repete várias vezes para reduzir
# ruído do ambiente e registra o menor tempo obtido. **kwargs permite passar
# argumentos extras (como modo="exato") apenas às funções que aceitam.
# ---------------------------------------------------------------------------
def medir(funcao, entrada, repeticoes=3, **kwargs):
    melhor = float("inf")
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao(entrada, **kwargs)
        melhor = min(melhor, time.perf_counter() - inicio)
    return melhor

if __name__ == '__main__':
    # Roda os testes antes do benchmark para assegurar correção funcional
    unittest.main(exit=False)
    # Avalia escalabilidade para tamanhos crescentes de entrada 'n'
    print("\nn | Lenta O(n²) Segundos | Rápida O(n) Segundos")
    print("-" * 38)
    for n in [1_000, 10_000, 50_000]:
        # Lista sem duplicatas e embaralhada: força o pior caso na versão O(n²)
        dados = list(range(n))
        random.shuffle(dados)
        original = medir(vduplicataoriginal, dados)
        otimizada = medir(vduplicataotimizada, dados, modo="exato")
        print(f"{n:<7} | {original:<13.6f} | {otimizada:<12.6f}")

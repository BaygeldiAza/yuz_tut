import time
from llm_fallback import llm_fallback

queries = [
    "golumden gan gelyar dermanhana gerek",
    "arzan restoran gozleyan",
    "iň gowy gije işleýän market",
    "saç kesdirmek isleyarin",
    "banka golayda barmy",
    "ertir dogan gunum bar sylag almak isleyan gymmat bolmasyn",
    "maşynym doňdy golayda ussahana barmy hazir açykmy",
    "kiçi gyzym üçin dogum gününe şar we tort gerek",
    "dişim agyrýar haýal etmän bejertmeli, golaýda haýsy ýer bar",
    "öýe iýmit sargyt etjek emma gije işleýän ýer bolsun",
]

for i, q in enumerate(queries):
    start = time.time()
    result = llm_fallback(q)
    elapsed = time.time() - start
    print(f"[{i}] {elapsed:.2f}s | query: {q!r} | result: {result}")
import json, re, subprocess
from datetime import datetime

REGEX = r"^(feat|fix|docs|chore|refactor|test|style)(\(.+\))?!?: .+$"

saida = subprocess.run(["git", "log", "--pretty=format:%h|%an|%s"], capture_output=True, text=True).stdout
linhas = [l for l in saida.splitlines() if l]

celula = {}
print("[AUDITORIA] Commits:")

for linha in linhas:
    h, autor, msg = linha.split("|", 2)
    valido = bool(re.match(REGEX, msg))
    
    if autor not in celula:
        celula[autor] = {"total": 0, "validos": 0, "hashes": []}
        
    celula[autor]["total"] += 1
    celula[autor]["validos"] += int(valido)
    celula[autor]["hashes"].append(h)
    
    print(f" {'[OK]' if valido else '[FALHA]'} [{h}] {autor}: {msg}")

total_geral = len(linhas)
relatorio = {
    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_commits": total_geral,
    "membros": {
        autor: {
            "commits": d["total"],
            "participacao": f"{(d['total'] / total_geral * 100):.1f}%" if total_geral else "0%",
            "conformidade": f"{(d['validos'] / d['total'] * 100):.1f}%",
            "hashes": d["hashes"]
        } for autor, d in celula.items()
    }
}

with open("docs/relatorio_rastreabilidade.json", "w", encoding="utf-8") as f:
    json.dump(relatorio, f, indent=2, ensure_ascii=False)

print("\n[RESUMO DA CELULA]")
for autor, dados in relatorio["membros"].items():
    print(f"Autor: {autor} | Commits: {dados['commits']} ({dados['participacao']}) | Aderencia: {dados['conformidade']} | Hashes: {', '.join(dados['hashes'])}")

print("\nConcluido: docs/relatorio_rastreabilidade.json gerado.")
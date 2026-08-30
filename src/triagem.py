PESO_SCORE_SOCIAL = 0.80
PESO_RENDA_FORMAL = 0.20
RENDA_REFERENCIA = 3000.0
NOTA_CORTE = 55.0

def normalizar_renda(renda_formal: float) -> float:
    if renda_formal <= 0:
        return 0.0
    nota = (renda_formal / RENDA_REFERENCIA) * 100
    return min(nota, 100.0)

def calcular_score_final(score_social: float, renda_formal: float) -> float:
    nota_renda = normalizar_renda(renda_formal)
    score_final = (score_social * PESO_SCORE_SOCIAL) + (nota_renda * PESO_RENDA_FORMAL)
    print(f"score_social x peso {score_social * PESO_SCORE_SOCIAL}, nota_renda x peso {nota_renda * PESO_RENDA_FORMAL}")
    return round(score_final, 2)

def validar_aprovacao(score_final: float) -> None:
    if score_final >= NOTA_CORTE:
        print("Resultado: Aprovado")
    else:
        print("Resultado: Reprovado")

def calcular_triagem():
    print("--- SISTEMA DE MICROCRÉDITO INCLUSIVO UniFAP ---")

    while True:
        score_social = float(input("Digite o Score Social Alternativo (0-100): "))
        if 0 <= score_social <= 100: break
        print("Score inválido. Digite um valor entre 0 e 100.")
    while True:
        renda_formal = float(input("Digite a Renda Formal CLT (R$): "))
        if renda_formal >= 0: break
        print("Renda inválida. Digite um valor maior ou igual a R$ 0.")

    score_social = max(0.0, min(score_social, 100.0))
    renda_formal = max(0.0, renda_formal)

    score_final = calcular_score_final(score_social, renda_formal)

    print(f"Score Final Ponderado: {score_final}")

    validar_aprovacao(score_final)

if __name__ == "__main__":
    calcular_triagem()
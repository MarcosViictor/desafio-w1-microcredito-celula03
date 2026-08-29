# Sistema de Microcrédito Inclusivo — UniFAP LaunchLab

## 1. O problema que este sistema resolve

O sistema antigo reprovava automaticamente qualquer cliente sem renda formal
comprovada (CLT), mesmo com excelente histórico de pagamento no bairro. Isso
excluía cerca de 95% das mulheres chefes de família da comunidade, que
trabalham no mercado informal (costureiras, feirantes, diaristas etc.).

A correção não é apenas "trocar o número de corte" — é mudar a **ordem e o
peso** dos critérios: o comportamento de pagamento informal passa a ser o
critério principal, e a renda formal vira um fator complementar, nunca
eliminatório.

## 2. Fluxo do processo de negócio

```
Cliente solicita crédito
        │
        ▼
Coleta do Score Social Alternativo (0-100)
 (histórico de pagamento no bairro: contas de consumo,
  fiado no comércio local, grupos de poupança/consórcio informal,
  referências de vizinhança, tempo de atividade do negócio)
        │
        ▼
Coleta da Renda Formal CLT (pode ser R$ 0,00)
        │
        ▼
Normalização da renda formal em nota 0-100
 (renda = 0 gera nota 0, mas NÃO reprova sozinha)
        │
        ▼
Cálculo do Score Final Ponderado:
   Score Final = (Score Social × 0.80) + (Nota Renda × 0.20)
        │
        ▼
Score Final >= 55 ?
   ├── Sim → Aprovado
   └── Não → Reprovado
```

### Por que esses pesos (80% / 20%)?

- **Score Social = 80%**: é a variável que melhor reflete a realidade da
  comunidade atendida. Um histórico consistente de pagamento no comércio
  local é um preditor de risco tão ou mais confiável quanto um contracheque,
  especialmente para quem nunca teve vínculo CLT.
- **Renda Formal = 20%**: continua tendo valor informativo (ajuda a
  desempatar casos limítrofes e a dimensionar o limite de crédito), mas não
  pode ser filtro de entrada, porque isso é exatamente o que excluía a
  maioria das clientes.
- **Nota de corte = 55**: calibrada para que um score social a partir de
  ~69 pontos já aprove o cliente **mesmo com renda formal R$ 0,00**,
  eliminando a exclusão automática do mercado informal.
- A renda formal, mesmo sendo R$ 0, é normalizada para nota 0 e não para
  "erro" ou "reprovação automática" — ela simplesmente deixa de somar pontos
  extras, mas nunca subtrai o que o cliente já conquistou com seu score social.

## 3. Compliance e LGPD

O Score Social Alternativo é construído a partir de dados sensíveis sobre o
comportamento financeiro e social do cliente (histórico de pagamento,
localização, rede de relacionamento no bairro). Isso exige cuidados
específicos:

- **Finalidade específica**: os dados coletados (score social, renda) são
  usados exclusivamente para a análise de crédito, conforme o princípio da
  finalidade (Art. 6º, I, LGPD). Não são compartilhados com terceiros para
  outros fins (marketing, por exemplo) sem consentimento explícito e
  separado.
- **Minimização**: o sistema coleta apenas as duas variáveis necessárias
  para o cálculo (score social e renda formal), evitando coleta excessiva
  de dados pessoais sensíveis (Art. 6º, III).
- **Não discriminação**: o modelo foi desenhado para **não** usar variáveis
  proxy que possam reproduzir discriminação indireta (endereço/CEP, gênero,
  raça) como fator de exclusão automática — o objetivo é reduzir viés, não
  automatizá-lo (Art. 6º, IX, princípio da não discriminação).
- **Transparência e explicabilidade**: o cliente reprovado tem direito a
  entender o motivo (Art. 20, LGPD — decisões automatizadas). Recomenda-se
  que o sistema em produção exiba o score final e os componentes do
  cálculo, não apenas "Aprovado/Reprovado".
- **Segurança e armazenamento**: em produção, os dados de score social e
  renda devem ser armazenados criptografados em repouso e em trânsito, com
  controle de acesso por perfil (apenas analistas de crédito autorizados),
  e política de retenção definida (apagar ou anonimizar dados após
  encerramento da relação com o cliente, salvo obrigação legal de guarda).
- **Consentimento**: a coleta do histórico informal (ex.: referências do
  comércio local) deve ser feita com consentimento informado do cliente,
  explicando como esse dado será usado no cálculo do score.

## 4. Análise de viabilidade financeira (estimativa)

Premissas ilustrativas para a cooperativa (ajustar com dados reais):

| Métrica | Cenário Antigo | Cenário Novo (estimado) |
|---|---|---|
| Taxa de rejeição de informais com bom histórico | ~95% | ~30-40%* |
| Clientes informais elegíveis (base de 1.000 solicitantes) | ~50 aprovados | ~600-700 aprovados |
| Ticket médio de microcrédito | R$ 1.500 | R$ 1.500 |
| Novo volume de crédito liberado | ~R$ 75.000 | ~R$ 900.000 - 1.050.000 |
| Inadimplência esperada (histórico informal bom = baixo risco) | N/A | Estimada próxima à carteira formal, dado que o score social já filtra maus pagadores |

*A taxa de 30-40% de reprovação residual refere-se a clientes com score
social baixo (mau histórico de pagamento), não a exclusão por ausência de
renda formal — que é o objetivo do projeto.

**Impacto esperado**: ao redirecionar o critério de decisão para o
comportamento de pagamento real (em vez da formalização do vínculo
empregatício), a cooperativa passa a capturar uma demanda reprimida de
clientes bons pagadores que hoje são 100% rejeitados. Isso aumenta a
carteira ativa e a receita de juros, sem necessariamente aumentar a
inadimplência — desde que o score social seja validado estatisticamente
(recomenda-se rodar um piloto com acompanhamento de 6-12 meses antes de
escalar).

## 5. Como executar

```bash
python3 src/triagem.py
```

O programa solicitará o Score Social Alternativo (0-100) e a Renda Formal
CLT (em R$, pode ser 0), e exibirá `Resultado: Aprovado` ou
`Resultado: Reprovado`, junto com o score final calculado.

# 5LTEP-L3 · Benchmark de modelos

[![Modelo recomendado](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Flsp3cesarschool%2F5ltep-layer3-modeltest%2Fmain%2Fresults%2Fstatus.pt.json)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/benchmark.yml) [![Tests](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml/badge.svg)](https://github.com/lsp3cesarschool/5ltep-layer3-modeltest/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[English](README.md) · **Português**

**Qual LLM local deve julgar as anomalias do [5ltep-layer3](https://github.com/lsp3cesarschool/5ltep-layer3/blob/main/LEIAME.md)?**
Um benchmark mensal e reproduzível de modelos abertos pequenos no prompt de produção, com um gabarito
cujas respostas certas são conhecidas por construção.

| Recurso | O que tem lá |
|---|---|
| 🏆 **Classificação** | [abaixo](#classificação), atualizada a cada execução |
| 📌 **Recomendação atual** | [recommendation.json](https://raw.githubusercontent.com/lsp3cesarschool/5ltep-layer3-modeltest/main/results/recommendation.json): legível por máquina, lida por toda instância da Camada 3 |
| 🏛️ **Instâncias que o usam** | [5ltep-layer3](https://github.com/lsp3cesarschool/5ltep-layer3/blob/main/LEIAME.md) (IBAMA) e [5ltep-layer3-aneel](https://github.com/lsp3cesarschool/5ltep-layer3-aneel/blob/main/LEIAME.md) (ANEEL, caso de controle) |
| 🔒 **Segurança** | [SECURITY.md](SECURITY.md): o que não é confiável (o modelo, o portal de dados, fontes da web), como o kit o contém, e como relatar uma vulnerabilidade |

## O que se pede aos modelos

A Camada 3 do 5L-TEP (Pirâmide de Engenharia da Confiança em Cinco Camadas) observa séries mensais
montadas a partir de dados abertos governamentais (ex.: o número de autos de infração do IBAMA por mês)
e sinaliza **anomalias**: meses que fogem do padrão habitual. Um *ensemble* estatístico as encontra; um
**LLM-as-a-Judge** então lê cada anomalia com seu contexto (o mesmo mês nos anos anteriores, eventos
conhecidos como leis novas, sinais nos próprios registros) e diz qual de quatro causas a explica
melhor:

| Código | Categoria | Exemplo | Por que importa |
|---|---|---|---|
| **PDC** | Mudança por política (*Policy-Driven Change*) | os autos caem logo depois de um novo decreto mudar o processo sancionador | explicada por um evento conhecido: documentar, sem correção |
| **SP** | Padrão sazonal (*Seasonal Pattern*) | janeiro tem menos autos quase todo ano (férias, ciclo orçamentário) | comportamento esperado: nenhuma ação |
| **DQE** | Evento de qualidade de dados (*Data-Quality Event*) | um mês quase sem registros numa série ativa, ou uma rajada de registros sem identificador | um **problema nos dados**: sempre enviado a um gestor humano, primeiro na fila de correção |
| **GES** | Mudança genuína de fiscalização (*Genuine Enforcement Shift*) | um aumento gradual e duradouro, sem evento, sem sazonalidade e sem sinais nos dados | uma mudança real que ninguém explicou ainda: vale investigar |

O objetivo da Camada 3 é dizer às pessoas **por onde começar**: as anomalias que nada explica e,
sobretudo, as que parecem problemas nos dados. Um bom juiz precisa, portanto, aplicar esses critérios
de forma consistente. É isso que este benchmark mede, para cada modelo candidato, no hardware gratuito
em que o pipeline de fato roda.

## Classificação

<!-- LEADERBOARD:START -->
*Atualizado em 2026-10-01 17:46 UTC · 30 casos do gabarito · 3 sementes cada · prompt de produção em `1554bc4`*

**Recomendação:** o modelo de produção é o melhor candidato elegível.

| # | Modelo | Motor | macro-F1 [IC 95%] | Acurácia | Consist. | Válidas | Latência p50 / p90 (s) | Anomalias/h | Situação |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | **1,00** [1,0; 1,0] | 1,00 | 1,00 | 100% | 1875,6 / 2308,1 | 0,6 | não elegível: cobriu 13% dos casos no tempo disponível; latência p90 de 2308 s; experimento |
| 2 | gemma4:12b | ollama | **0,93** [0,804; 1,0] | 0,93 | 0,99 | 100% | 79,0 / 307,7 | 8,0 | não elegível: latência p90 de 308 s |
| 3 | qwen3:4b | ollama | **0,81** [0,658; 0,935] | 0,83 | 0,86 | 99% | 33,8 / 92,6 | 24,0 | elegível |
| 4 | qwen3.5:9b | ollama | **0,79** [0,615; 0,921] | 0,80 | 0,88 | 100% | 52,5 / 98,3 | 19,0 | elegível |
| 5 | ministral-3:3b | ollama | **0,67** [0,509; 0,819] | 0,70 | 0,83 | 100% | 26,4 / 53,3 | 37,7 | elegível |
| 6 | qwen3:4b (llama.cpp) | llamacpp | **0,66** [0,501; 0,797] | 0,70 | 0,87 | 100% | 21,2 / 72,5 | 32,6 | elegível |
| 7 | granite4.2:8b | ollama | **0,62** [0,438; 0,755] | 0,57 | 0,79 | 42% | 92,6 / 183,0 | 10,5 | não elegível: respostas válidas 42%; latência p90 de 183 s |
| 8 | qwen3:8b | ollama | **0,59** [0,418; 0,744] | 0,63 | 0,88 | 100% | 38,7 / 139,8 | 17,2 | elegível |
| 9 | qwen3:4b-q4_K_M | ollama | **0,58** [0,408; 0,711] | 0,60 | 0,80 | 100% | 23,5 / 82,4 | 28,5 | elegível |
| 10 | ministral-3:8b | ollama | **0,57** [0,43; 0,665] | 0,63 | 0,90 | 100% | 50,5 / 165,1 | 14,1 | não elegível: latência p90 de 165 s |
| 11 | gemma3n:e2b | ollama | **0,54** [0,336; 0,685] | 0,53 | 0,70 | 100% | 14,5 / 61,8 | 41,1 | elegível |
| 12 | granite4.2:3b | ollama | **0,53** [0,4; 0,634] | 0,60 | 0,68 | 70% | 25,4 / 38,6 | 51,5 | não elegível: respostas válidas 70% |
| 13 | qwen3.5:4b | ollama | **0,50** [0,357; 0,645] | 0,57 | 0,86 | 100% | 25,7 / 107,7 | 23,9 | elegível |
| 14 | qwen3.5:2b-q4_K_M | ollama | **0,43** [0,276; 0,588] | 0,47 | 0,79 | 100% | 9,4 / 37,7 | 67,1 | elegível |
| 15 | gemma3:4b (llama.cpp) | llamacpp | **0,40** [0,22; 0,565] | 0,43 | 0,83 | 100% | 25,1 / 81,6 | 28,2 | elegível |
| 16 | qwen3:1.7b | ollama | **0,39** [0,229; 0,521] | 0,43 | 0,77 | 100% | 13,5 / 28,6 | 69,0 | elegível |
| 17 | lfm2.5:8b-a1b | ollama | **0,39** [0,259; 0,498] | 0,47 | 0,78 | 100% | 5,7 / 25,8 | 101,3 | elegível |
| 18 | gemma3:12b | ollama | **0,35** [0,271; 0,417] | 0,47 | 0,98 | 100% | 50,0 / 188,1 | 12,8 | não elegível: latência p90 de 188 s |
| 19 | qwen3.5:2b | ollama | **0,35** [0,179; 0,484] | 0,37 | 0,73 | 100% | 12,2 / 47,3 | 52,6 | elegível |
| 20 | qwen3.5:0.8b | ollama | **0,34** [0,177; 0,48] | 0,40 | 0,68 | 100% | 5,3 / 20,4 | 120,6 | elegível |
| 21 | Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | **0,34** [0,183; 0,452] | 0,40 | 0,77 | 100% | 38,9 / 121,9 | 19,0 | elegível |
| 22 | phi4-mini:3.8b | ollama | **0,30** [0,163; 0,431] | 0,37 | 0,73 | 100% | 18,8 / 61,7 | 38,9 | elegível |
| 23 | gemma3:4b (prompt v1) | ollama | **0,29** [0,161; 0,375] | 0,40 | 0,92 | 100% | 25,6 / 43,4 | 41,2 | não elegível: experimento |
| 24 | llama3.1:8b | ollama | **0,20** [0,083; 0,31] | 0,30 | 0,90 | 100% | 25,6 / 72,6 | 31,4 | elegível |
| 25 | gemma4:e2b | ollama | **0,20** [0,071; 0,308] | 0,30 | 0,97 | 100% | 13,4 / 60,8 | 42,5 | elegível |
| 26 | granite4:7b-a1b-h | ollama | **0,16** [0,059; 0,261] | 0,27 | 0,84 | 100% | 7,7 / 36,2 | 72,5 | elegível |
| 27 | llama3.2:3b | ollama | **0,10** [0,048; 0,15] | 0,23 | 0,90 | 100% | 19,5 / 50,7 | 42,9 | elegível |
| – | gemma3:4b | ollama | | | | | | | ainda não executado |
| – | gemma3n:e4b | ollama | | | | | | | ainda não executado |

### Mesmo modelo, motores ou formatos diferentes

**gemma3:4b no Ollama × llama.cpp.** Os mesmos pesos de 4 bits do Gemma 3 4B servidos por dois motores, com o mesmo prompt, sementes e temperatura.

| Candidato | Motor | Arquivo / tag do modelo | macro-F1 [IC 95%] | Consist. | Latência p50 / p90 (s) |
|---|---|---|---|---|---|
| gemma3:4b | | | ainda não medido | | |
| gemma3:4b (llama.cpp) | llamacpp | `gemma-3-4b-it-Q4_K_M` | 0,40 [0,22; 0,565] | 0,83 | 25,1 / 81,6 |

**qwen3:4b no Ollama × llama.cpp.** Qwen3 4B da biblioteca do Ollama (duas tags) e o GGUF oficial da Qwen no llama.cpp; raciocínio desligado em todos. As tags podem apontar para builds diferentes (ver os digests em results/leaderboard.json).

| Candidato | Motor | Arquivo / tag do modelo | macro-F1 [IC 95%] | Consist. | Latência p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:4b | ollama | `qwen3:4b` | 0,81 [0,658; 0,935] | 0,86 | 33,8 / 92,6 |
| qwen3:4b-q4_K_M | ollama | `qwen3:4b-q4_K_M` | 0,58 [0,408; 0,711] | 0,80 | 23,5 / 82,4 |
| qwen3:4b (llama.cpp) | llamacpp | `Qwen3-4B-Q4_K_M` | 0,66 [0,501; 0,797] | 0,87 | 21,2 / 72,5 |

**8B a 4 bits × 8B a ~2 bits (ternário).** Um modelo 8B convencional de 4 bits no Ollama e um 8B ternário (Bonsai) no fork PrismML do llama.cpp.

| Candidato | Motor | Arquivo / tag do modelo | macro-F1 [IC 95%] | Consist. | Latência p50 / p90 (s) |
|---|---|---|---|---|---|
| qwen3:8b | ollama | `qwen3:8b` | 0,59 [0,418; 0,744] | 0,88 | 38,7 / 139,8 |
| Ternary-Bonsai-8B (PQ2_0) | llamacpp-prism | `Ternary-Bonsai-8B-PQ2_0` | 0,34 [0,183; 0,452] | 0,77 | 38,9 / 121,9 |

**27B comprimido para caber no runner.** O Ternary-Bonsai-2-27B (5,95 GB) é uma versão ternária do Qwen3.8-27B, cuja versão de 4 bits não cabe em 16 GB de RAM. Medido só numa amostra (4 casos, 1 semente): as chamadas levam muitos minutos em 4 vCPUs.

| Candidato | Motor | Arquivo / tag do modelo | macro-F1 [IC 95%] | Consist. | Latência p50 / p90 (s) |
|---|---|---|---|---|---|
| Ternary-Bonsai-2-27B (PTQ1_0) | llamacpp-prism | `Ternary-Bonsai-2-27B-PTQ1_0` | 1,00 [1,0; 1,0] | 1,00 | 1875,6 / 2308,1 |
| Qwen3.8-27B a 4 bits (qwen3.8:27b-q4_K_M, 18 GB) | | | não cabe no runner gratuito | | |
<!-- LEADERBOARD:END -->

**Como ler a tabela.** Cada linha é um candidato, executado em todos os casos do gabarito com três
sementes. **#** é a posição por macro-F1. **Modelo** é a tag do Ollama ou o arquivo GGUF testado;
**Motor** é o mecanismo de inferência (`ollama`, `llamacpp` para a build oficial do llama.cpp,
`llamacpp-prism` para o fork da PrismML que roda os modelos ternários Bonsai). **macro-F1 [IC 95%]** é
a pontuação principal: para cada caso, o rótulo escolhido pela maioria das três execuções é comparado
com o rótulo do gabarito, calcula-se um F1 por categoria (PDC, SP, DQE, GES) e tira-se a média das
quatro, de modo que cada categoria pesa o mesmo; os colchetes dão o intervalo de confiança de 95% por
*bootstrap* sobre os casos (intervalos que se sobrepõem indicam que a diferença pode ser ruído).
**Acurácia** é a simples proporção de casos rotulados corretamente. **Consist.** é a proporção das três
execuções que concordam com a maioria (1,00 = sempre a mesma resposta). **Válidas** é a proporção de
respostas em JSON bem formado com uma categoria conhecida. **Latência p50 / p90** é a mediana e o
percentil 90 do tempo de uma chamada no runner gratuito, em segundos, e **Anomalias/h** o número de
anomalias (três chamadas cada) julgadas por hora na latência média. **Situação** diz se o candidato
pode ser recomendado (válidas ≥ 95%, cobertura ≥ 90% dos casos dentro do tempo disponível, latência
p90 ≤ 150 s, não ser um experimento) ou por que não.

## Por que um benchmark separado

A Camada 3 classifica cada anomalia estatística com um LLM-as-a-Judge (categorias PDC, SP, DQE, GES,
[acima](#o-que-se-pede-aos-modelos)). O modelo roda no runner de CPU gratuito do GitHub Actions, então
precisa ser pequeno, rápido e confiável. Modelos pequenos novos aparecem todo mês, e as respostas de um
modelo de 4B dependem muito do prompt (em produção, uma revisão do prompt mudou 17 rótulos de uma vez).
Escolher o modelo por impressão, ou por rankings de propósito geral, não basta: ele precisa ser medido
**nesta tarefa, com este prompt, neste hardware**.

## Como funciona

```
descobrir ──► planejar ──► executar (um job por candidato, em paralelo) ──► pontuar ──► recommendation.json
 biblioteca    só o que mudou:          gabarito × 3 sementes,               macro-F1 + IC, consistência,
 do Ollama     digest do modelo,        prompt de produção,                  validade, latência; tabela
 (tags novas)  código do prompt         mesmas sementes e temperatura        do README e do LEIAME
               ou gabarito
```

1. **Descobrir** (`bench/discover.py`): lista as tags das famílias acompanhadas e dos modelos mais
   novos da biblioteca, mantém as tags de tamanho simples que cabem no runner (1–9 GB) e as registra em
   `results/discovered.json`. A lista curada fica em [`candidates.json`](candidates.json).
2. **Planejar** (`bench/plan.py`): resolve a build de cada candidato (digest do manifesto do Ollama ou
   hash do arquivo GGUF) e a impressão digital do código do prompt de produção no `main` atual do
   5ltep-layer3. Um candidato só é executado de novo se um desses, ou o gabarito, mudou.
3. **Executar** (`bench/run.py`): o prompt de cada caso do gabarito é montado pelo **código de
   produção** (`src/judge.py` do 5ltep-layer3, no commit planejado) e enviado com as sementes de
   produção (11, 22, 33), a temperatura (0,7) e o mesmo esquema JSON. Cada candidato tem um tempo
   disponível (5 h por padrão); uma execução que não termina é mantida, marcada como parcial.
4. **Pontuar** (`bench/score.py`): métricas, elegibilidade, recomendação, a tabela deste LEIAME e do
   README.

## Gabarito

[`gold/cases.json`](gold/cases.json), construído por [`gold/build_gold.py`](gold/build_gold.py) a
partir das séries mensais de autos de infração do IBAMA commitadas no 5ltep-layer3. Cada caso traz a
evidência completa que o juiz recebe (série, votos dos detectores recalculados sobre os dados do caso,
eventos) e um **rótulo conhecido por construção**, seguindo os critérios que o próprio prompt de
produção enuncia:

| Categoria | Casos | Como são construídos |
|---|---|---|
| SP | reais | anomalias cujo mês do calendário desviou no mesmo sentido em ≥ 8 dos 10 anos anteriores; nenhum evento em 6 meses; nenhum sinal de qualidade de dados |
| PDC | sintéticos | um mês calmo recebe uma mudança persistente (×2,5 a ×4, ou ×0,4 a ×0,25), e o calendário recebe um evento de política nesse mês |
| DQE | sintéticos | um mês calmo cai para 3% do seu nível (falha de registro), ou é multiplicado por 2,2 a 4 com 45% dos registros sem identificador e 3× cancelamentos (lote duplicado); nenhum evento |
| GES | sintéticos | uma rampa gradual de três meses (até ×2 a ×3, ou ×0,5 a ×0,33) que persiste; nenhum evento, nenhuma sazonalidade, nenhum sinal de qualidade de dados |

Conjunto atual: 30 casos (7 SP, 8 PDC, 8 DQE, 7 GES). Um caso sintético só é mantido se o *ensemble*
sinalizar seu mês, como em produção; variantes mais fortes só são tentadas quando nenhum mês calmo é
sinalizado na mais fraca, e uma categoria fica com menos casos em vez de repetir um (rampas graduais
raramente são sinalizadas, daí 7 GES). O gabarito mede se um modelo **aplica os critérios enunciados à
evidência**; não mede conhecimento de mundo e não substitui anomalias reais revisadas por gestores. Se
gestores registrarem decisões nos repositórios principais, essas decisões podem ser acrescentadas como
novos casos, reais, de mais de um portal.

## Métricas e recomendação

| Métrica | Significado |
|---|---|
| macro-F1 [IC 95%] | pontuação principal: rótulo da maioria das três sementes × rótulo do gabarito, com média nas quatro categorias; IC por *bootstrap* sobre os casos |
| acurácia, recall por categoria | visões complementares das mesmas respostas |
| consistência | proporção das três execuções que concordam com a maioria (1 = sempre o mesmo rótulo) |
| válidas | proporção de respostas que podem ser lidas e usam uma categoria conhecida |
| latência p50 / p90, anomalias/h | custo no runner gratuito (4 vCPU, 16 GB, só CPU) |
| cobertura | casos concluídos dentro do tempo disponível |

Um candidato é **elegível** com ≥ 95% de respostas válidas, ≥ 90% de cobertura e latência p90 ≤ 150 s
por chamada. O modelo **recomendado** é o candidato elegível, não experimental, com o maior macro-F1
(desempate: consistência, depois velocidade). Uma **troca** do modelo de produção só é recomendada
quando o vencedor o supera por pelo menos 0,05 de macro-F1 e o IC 95% por *bootstrap* pareado da
diferença está acima de zero. Quando isso acontece, o vencedor vira a nova referência de produção do
benchmark (`production` em [`candidates.json`](candidates.json)), de modo que os meses seguintes
comparam os candidatos com o modelo que as instâncias de fato usam.

## Como os repositórios principais o usam

Nenhum token passa entre repositórios: cada instância da Camada 3 lê o arquivo público
[`results/recommendation.json`](results/recommendation.json). Seu campo **`use`** é o modelo aprovado
para produção (o anterior, até uma troca ser recomendada).

- **Automático (padrão):** com `LLM_MODEL=auto`, cada execução de uma instância começa lendo `use` e
  julga com esse modelo e suas opções (ex.: raciocínio desligado). A aprovação acontece aqui, pela regra
  estatística acima.
- **Fixado:** com `LLM_MODEL` definido como uma tag, a instância mantém esse modelo; seu *Model check*
  mensal abre uma issue quando este benchmark recomendar outro.

Nos dois casos, **os julgamentos anteriores são mantidos**: cada um registra o modelo e a versão do
prompt que o produziram, e um modelo novo só julga anomalias novas ou cujos dados mudaram. Rejulgar o
histórico com o modelo atual é uma escolha separada e explícita (a entrada `rejudge` do workflow da
Camada 3 da instância).

## Motores de inferência

| Motor | Usado para |
|---|---|
| **Ollama** | motor de produção; todos os modelos da biblioteca |
| **llama.cpp** (build oficial Ubuntu x64) | o mesmo modelo do Ollama, para comparar motores (velocidade e respostas): gemma3:4b e qwen3:4b |
| **llama.cpp, fork da PrismML** (compilado do código-fonte, em cache) | modelos *Bonsai* ternários / de 1 bit (ex.: [Ternary-Bonsai-2-27B](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf), um modelo de 27B em 5,95 GB), cujos formatos não estão no llama.cpp principal nem no Ollama |

A classificação ordena todos os candidatos; as tabelas **"Mesmo modelo, motores ou formatos
diferentes"** abaixo dela colocam lado a lado os candidatos que diferem só no motor ou na compressão,
como declarado em `comparisons` no [`candidates.json`](candidates.json). Primeiros achados
(30/09/2026): os mesmos pesos do Gemma 3 4B marcaram 0,50 no Ollama e 0,40 no llama.cpp, com a mesma
velocidade e intervalos sobrepostos, então não há motivo para deixar o Ollama.

**Variação entre execuções.** As respostas não se repetem nem no mesmo motor: uma mudança no código de produção (não no
texto do prompt) forçou uma segunda execução de todos os candidatos no mesmo dia e, com o mesmo digest
do modelo, a mesma versão do
Ollama (0.35.0) e as mesmas sementes, nenhuma resposta do `qwen3:4b` ou do `gemma3:4b` foi idêntica (0
de 90 em cada), o rótulo majoritário coincidiu em apenas 23 e 22 dos 30 casos, e o macro-F1 foi de 0,81
para 0,75 (`qwen3:4b`) e de 0,50 para 0,52 (`gemma3:4b`). O intervalo por *bootstrap* cobre a escolha
dos casos, não essa variação; por isso, diferenças menores que cerca de 0,05–0,10 entre dois modelos, ou
entre duas execuções, devem ser lidas como ruído. A regra de troca (margem ≥ 0,05 e intervalo pareado
acima de zero) protege contra parte disso.

Modelos grandes hipercomprimidos respondem a uma pergunta real neste cenário: com a mesma memória, um
27B a ~1,75 bit/peso é melhor que um 4B a 4 bits? Num runner de CPU, o preço é a velocidade: cada token
lê todos os 27B de pesos. Na primeira execução, o Ternary-Bonsai-2-27B carregou no runner de 16 GB, mas
nenhuma chamada terminou em 15 minutos; por isso agora ele é medido só numa amostra pequena, como
experimento.

## Custo: gratuito, mas lento

**Gratuito.** Tudo aqui roda nos runners hospedados padrão do GitHub de um repositório **público**,
pelos quais o GitHub não cobra: *"GitHub Actions usage is free for self-hosted runners and for public
repositories that use standard GitHub-hosted runners"* ([About billing for GitHub Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions)),
e *"Use of the standard GitHub-hosted runners is free and unlimited on public repositories"*, num runner
Linux com 4 CPUs e 16 GB de RAM ([GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)).
Sem GPU, sem chave de API, sem serviço pago.

**Lento.** Os modelos rodam nessas CPUs: de dezenas de segundos a minutos por chamada. A coluna
*Anomalias/h* da [classificação](#classificação), atualizada a cada execução, mostra quantas anomalias
(três chamadas cada) cada modelo julga por hora neste runner: algumas dezenas nos modelos pequenos, bem
menos nos grandes.

**Por que lento serve bem a este projeto.** A Camada 3 observa séries *mensais*: os dados são avaliados
mês a mês, então só há algo novo para julgar uma vez por mês, e em geral só um punhado de anomalias.
Mesmo a primeira execução sobre todo o histórico do IBAMA (44 anomalias desde 1980, 132 chamadas, em
setembro de 2026) levou cerca de uma hora e meia de julgamento, em dois lotes. E o prazo é folgado: os dados do mês seguinte só
chegam um mês depois, então uma execução poderia levar o mês inteiro e ainda estaria em dia. Os lotes se
encadeiam sozinhos (cada job é limitado a 6 horas), então a velocidade do runner nunca impede um
resultado; ela só ocupa parte de uma janela muito maior que o necessário. Para este caso de uso, um
runner gratuito e só com CPU não é uma concessão, e sim o tamanho certo: custo zero e capacidade de
sobra.

**Este benchmark** segue a mesma lógica. Roda uma vez por mês (dia 20), antes do *Model check* dos
repositórios principais (dia 22) e da próxima execução mensal deles (dia 5). Cada candidato é um job
separado, com até 20 rodando ao mesmo tempo, então mesmo uma execução completa de todos os candidatos
leva só algumas horas.

**Limites que moldam o desenho.** Cada job pode rodar por até 6 horas, e até 20 jobs rodam ao mesmo
tempo ([Actions limits](https://docs.github.com/en/actions/reference/limits)); daí o tempo disponível
por candidato, a amostragem de modelos muito lentos (o Bonsai de 27B precisa de dezenas de minutos por chamada)
e os jobs em paralelo. Instalar o Ollama ou o llama.cpp no runner é uso comum do runner; os pesos dos
modelos são baixados das fontes oficiais no momento da execução.

## Como acrescentar um candidato

Acrescente uma entrada em [`candidates.json`](candidates.json):

```json
{"label": "my-model:4b", "backend": "ollama", "model": "my-model:4b", "options": {"think": false}}
{"label": "Some GGUF", "backend": "llamacpp", "model": "some-gguf", "hf_repo": "org/repo-GGUF", "hf_file": "model-Q4_K_M.gguf"}
```

`"experiment": true` mede um candidato sem torná-lo elegível (ex.: uma versão antiga do prompt via
`"prompt_ref"`). Para grupos de comparação, `title_pt`, `note_pt` e `unrunnable_pt` dão o texto deste
LEIAME. Rode *Actions → Model benchmark → Run workflow*, opcionalmente com `only`.

## Licenças

Código: MIT. Os modelos são baixados no momento da execução das suas fontes oficiais e não são
redistribuídos; cada um mantém sua própria licença. Ollama e llama.cpp são MIT; os modelos Bonsai são
Apache-2.0.

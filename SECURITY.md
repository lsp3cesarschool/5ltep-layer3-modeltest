# Security policy · Política de segurança

[English](#english) · [Português](#português)

## English

This benchmark downloads and runs models from outside sources, and its result
([`results/recommendation.json`](results/recommendation.json)) decides which model the Layer 3
instances use. So it treats as **untrusted** the models (their weights and every word they write),
the model catalogues and file hosts, and the inputs of manual runs. The toolkit's full threat model is
in [5ltep-layer3/SECURITY.md](https://github.com/lsp3cesarschool/5ltep-layer3/blob/main/SECURITY.md).

### Reporting a vulnerability

Use **Security → Report a vulnerability** on GitHub (private), or write to `lsp3@cesar.school`.

### What the benchmark does

| Threat | Mitigation |
|---|---|
| A model that **executes code** through a crafted file | The jobs that run models have a read-only token and no stored credentials, and hand over only their own result file. The scoring job, which never runs a model, accepts from each job only the file named after that candidate, checks its structure and bounds its text (`bench/accept_runs.py`); a job cannot change another candidate's result. |
| A **malicious or tampered model** reaching production | Discovery only looks at the official Ollama library (curated by Ollama), with strict name and tag patterns; GGUF files come only from the curated list and are checked against their SHA-256. A switch is adopted automatically only for an Ollama model whose exact build has been **in observation for 30 days** (`selection.min_age_days_to_adopt`); otherwise the leaderboard shows it, but production keeps the current model. The recommendation carries the build's **digest**, and the instances refuse a model whose digest differs. |
| A model **tuned to the public gold set** | Cannot be ruled out by a public benchmark. The waiting period, the official-source restriction and the containment in the instances (labels are data, data-quality labels go to a person) bound the harm; a hidden hold-out set is a possible next step (not implemented). |
| **Script injection** (crafted model name, file name or input) | Candidate names are validated (`bench/plan.py`) and reach the shell only through environment variables (a test fails otherwise). |
| **Software supply chain** | Ollama from a pinned release checked against its SHA-256; llama.cpp from a pinned release checked against its SHA-256; the PrismML fork built from a pinned commit; Python dependencies pinned to exact versions. |

### Residual risks

The benchmark trusts GitHub, the GitHub-hosted runners, the official Ollama library and the pinned
releases. Pinned versions must be updated deliberately, with their checksums.

## Português

Este benchmark baixa e executa modelos de fontes externas, e o seu resultado
([`results/recommendation.json`](results/recommendation.json)) decide qual modelo as instâncias da
Camada 3 usam. Por isso trata como **não confiáveis** os modelos (seus pesos e cada palavra que
escrevem), os catálogos e hospedagens de modelos, e as entradas das execuções manuais. O modelo de
ameaças completo do kit está em
[5ltep-layer3/SECURITY.md](https://github.com/lsp3cesarschool/5ltep-layer3/blob/main/SECURITY.md).

### Como relatar uma vulnerabilidade

Use **Security → Report a vulnerability** no GitHub (privado), ou escreva para `lsp3@cesar.school`.

### O que o benchmark faz

| Ameaça | Mitigação |
|---|---|
| Um modelo que **executa código** por meio de um arquivo forjado | Os jobs que rodam modelos têm token somente leitura, sem credenciais guardadas, e entregam só o próprio arquivo de resultado. O job de pontuação, que nunca roda modelo, aceita de cada job só o arquivo com o nome daquele candidato, confere a estrutura e limita o texto (`bench/accept_runs.py`); um job não consegue alterar o resultado de outro candidato. |
| Um **modelo malicioso ou adulterado** chegando à produção | A descoberta só olha a biblioteca oficial do Ollama (curada pelo Ollama), com padrões estritos de nome e tag; arquivos GGUF vêm só da lista curada e são conferidos pelo SHA-256. Uma troca só é adotada automaticamente para um modelo do Ollama cuja build exata esteja **em observação há 30 dias** (`selection.min_age_days_to_adopt`); senão a classificação o mostra, mas a produção mantém o modelo atual. A recomendação traz o **digest** da build, e as instâncias recusam um modelo com digest diferente. |
| Um modelo **ajustado ao gabarito público** | Não pode ser descartado por um benchmark público. O período de espera, a restrição a fontes oficiais e a contenção nas instâncias (rótulos são dados, rótulos de qualidade de dados vão para uma pessoa) limitam o dano; um conjunto de teste oculto é um próximo passo possível (não implementado). |
| **Injeção de script** (nome de modelo, nome de arquivo ou entrada forjados) | Os nomes dos candidatos são validados (`bench/plan.py`) e chegam ao shell só por variáveis de ambiente (um teste falha se não for assim). |
| **Cadeia de suprimentos de software** | Ollama de uma release fixada e conferida pelo SHA-256; llama.cpp de uma release fixada e conferida pelo SHA-256; fork PrismML compilado de um commit fixado; dependências Python com versões exatas. |

### Riscos residuais

O benchmark confia no GitHub, nos runners hospedados pelo GitHub, na biblioteca oficial do Ollama e nas
releases fixadas. As versões fixadas precisam ser atualizadas de forma deliberada, com seus checksums.

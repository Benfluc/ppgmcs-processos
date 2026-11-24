# Processos Acadêmicos do PPGMCS/Unimontes

Documentação dos principais processos do **Mestrado Profissional em Modelagem Computacional e Sistemas (PPGMCS)** da Universidade Estadual de Montes Claros. Cada processo tem um PDF próprio com:

- público-alvo;
- responsáveis e atribuições;
- base normativa;
- requisitos;
- fluxograma;
- passo a passo;
- prazos;
- documentos;
- pendências de validação.

> **Versão 1.0 (minuta), novembro de 2026.** Documento informativo. Em caso de divergência, prevalecem as normas oficiais do PPGMCS e da Unimontes. Cada PDF traz, ao final, os pontos que ainda dependem de validação pela Coordenação.

## Processos

| # | Processo | Público-alvo principal | PDF | Fluxograma |
|---|----------|------------------------|-----|------------|
| 01 | Ingresso no Mestrado | Candidatos(as) | [PDF](pdf/01-ingresso.pdf) | [SVG](fluxogramas/01-ingresso.svg) |
| 02 | Requisitos para Obtenção do Título | Discentes e orientadores | [PDF](pdf/02-requisitos-titulo.pdf) | [SVG](fluxogramas/02-requisitos-titulo.svg) |
| 03 | Agendamento do Exame de Qualificação | Discentes e orientadores | [PDF](pdf/03-agendamento-qualificacao.pdf) | [SVG](fluxogramas/03-agendamento-qualificacao.svg) |
| 04 | Agendamento da Defesa de Dissertação | Discentes e orientadores | [PDF](pdf/04-agendamento-defesa.pdf) | [SVG](fluxogramas/04-agendamento-defesa.svg) |
| 05 | Atividade Acadêmica de Créditos Especiais | Discentes e orientadores | [PDF](pdf/05-creditos-especiais.pdf) | [SVG](fluxogramas/05-creditos-especiais.svg) |
| 06 | Disciplinas de Estudos Dirigidos | Discentes e docentes | [PDF](pdf/06-estudos-dirigidos.pdf) | [SVG](fluxogramas/06-estudos-dirigidos.svg) |
| 07 | Trancamento Parcial e Total | Discentes e orientadores | [PDF](pdf/07-trancamento.pdf) | [SVG](fluxogramas/07-trancamento.svg) |
| 08 | Aproveitamento de Disciplinas de Outro PPG | Discentes | [PDF](pdf/08-aproveitamento-disciplinas.pdf) | [SVG](fluxogramas/08-aproveitamento-disciplinas.svg) |

## Resumo rápido

- **Créditos para o título:** 38 no total (Res. 001/2024).
  - 28 em disciplinas: Seminários (4), mais 2 obrigatórias entre Introdução à Modelagem Computacional, Visualização Científica e Estatística e Probabilidade (8), Créditos Especiais A (4) e optativas (12).
  - 4 no Exame de Qualificação.
  - 6 na Dissertação.
- **Prazo máximo do curso:** 24 meses, prorrogáveis por até 6.
  - Qualificação concluída até o **14º mês**.
  - Depósito da dissertação até o **23º mês**.
- **Banca de defesa:** mínimo de 3 doutores: orientador(a) (presidente), 1 docente credenciado(a) no PPGMCS e 1 membro externo.

## Estrutura do repositório

```
processos/     Fonte de cada processo em YAML (edite aqui)
templates/     Modelo HTML/CSS dos PDFs
scripts/       build.py: gera fluxogramas e PDFs
fluxogramas/   Fluxogramas gerados (.svg e fonte .dot)
pdf/           PDFs gerados
normas/        Normas consultadas (regulamentos, resoluções, edital)
formularios/   Requerimentos oficiais de qualificação e defesa
```

## Como atualizar

1. Edite o arquivo YAML do processo em `processos/`.
   - Os passos do fluxograma ficam em `etapas`.
   - Cada etapa tem `ator`, `texto` e o destino em `para`.
   - Decisões usam `tipo: decisao` e destinos rotulados, por exemplo `{"Sim": e5, "Não": e6}`.
2. Gere os arquivos novamente:

```bash
pip install -r requirements.txt   # PyYAML e Jinja2
# Requer também Graphviz (dot) e Google Chrome ou Chromium no PATH
python scripts/build.py            # todos os processos
python scripts/build.py 04         # apenas o processo 04
```

Os atores disponíveis e suas cores estão definidos em `ATORES`, no início de `scripts/build.py`.

## Normas consultadas

- Regulamento do PPGMCS, aprovado pelo Colegiado em 15/03/2024 (`normas/regulamento-ppgmcs-2024.pdf`)
- Resolução PPGMCS nº 001/2024: estrutura curricular, créditos e créditos especiais
- Resolução PPGMCS nº 004/2019: exame de qualificação e defesa
- Edital de Seleção 2027-1 (retificado)
- Regulamento de 2022 e Resolução nº 003/2019, mantidos apenas como referência histórica

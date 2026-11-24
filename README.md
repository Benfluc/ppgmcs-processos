# Processos Acadêmicos do PPGMCS/Unimontes

Documentação dos principais processos acadêmicos do **Mestrado Profissional em Modelagem Computacional e Sistemas (PPGMCS)** da Universidade Estadual de Montes Claros. Cada processo tem um arquivo em Markdown com:

- público-alvo;
- responsáveis e atribuições;
- base normativa;
- requisitos;
- fluxograma;
- passo a passo;
- prazos;
- documentos.


## Processos

| # | Processo | Público-alvo principal | Documento | PDF |
|---|----------|------------------------|-----------|-----|
| 01 | Ingresso no Mestrado | Candidatos(as) | [Abrir](processos/01-ingresso.md) | [PDF](pdf/01-ingresso.pdf) |
| 02 | Requisitos para Obtenção do Título | Discentes e orientadores | [Abrir](processos/02-requisitos-titulo.md) | [PDF](pdf/02-requisitos-titulo.pdf) |
| 03 | Agendamento do Exame de Qualificação | Discentes e orientadores | [Abrir](processos/03-agendamento-qualificacao.md) | [PDF](pdf/03-agendamento-qualificacao.pdf) |
| 04 | Agendamento da Defesa de Dissertação | Discentes e orientadores | [Abrir](processos/04-agendamento-defesa.md) | [PDF](pdf/04-agendamento-defesa.pdf) |
| 05 | Atividade Acadêmica de Créditos Especiais | Discentes e orientadores | [Abrir](processos/05-creditos-especiais.md) | [PDF](pdf/05-creditos-especiais.pdf) |
| 06 | Disciplinas de Estudos Dirigidos | Discentes e docentes | [Abrir](processos/06-estudos-dirigidos.md) | [PDF](pdf/06-estudos-dirigidos.pdf) |
| 07 | Trancamento Parcial e Total | Discentes e orientadores | [Abrir](processos/07-trancamento.md) | [PDF](pdf/07-trancamento.pdf) |
| 08 | Aproveitamento de Disciplinas de Outro Programa | Discentes | [Abrir](processos/08-aproveitamento-disciplinas.md) | [PDF](pdf/08-aproveitamento-disciplinas.pdf) |

## Estrutura

```
processos/      Documentos dos processos em Markdown (edite aqui)
pdf/            PDFs gerados a partir dos .md
normas/         Normas de referência (regulamentos, resoluções, edital)
formularios/    Modelos de requerimento
scripts/        Script e estilo para gerar os PDFs
PENDENCIAS.md   Pontos em aberto para validação com a Coordenação
```

## Como editar

1. Abra o arquivo do processo em `processos/` e edite o texto. No GitHub, use o ícone de lápis.
2. Os **fluxogramas** são escritos em [Mermaid](https://mermaid.js.org/syntax/flowchart.html), dentro do bloco ` ```mermaid `. O GitHub desenha o diagrama automaticamente.
   - Cada etapa é uma linha, como `e1["Texto da etapa<br/>(Responsável)"]:::discente --> e2`.
   - Decisões usam chaves e setas rotuladas: `d1{"Pergunta?"}` e `d1 -->|Sim| e2`.
   - As cores por responsável são as classes definidas no fim de cada bloco: `discente`, `orientador`, `secretaria`, `colegiado`, `banca` e `terminal`.
3. Mantenha os documentos **genéricos**. Datas, vagas e nomes de uma edição específica ficam no edital ou na comunicação da Secretaria, não aqui.
4. Depois de editar, gere os PDFs de novo (abaixo) e faça o commit dos `.md` e dos `.pdf`.

## Como gerar os PDFs

Requisitos: Python 3.9+, [Pandoc](https://pandoc.org), Node.js/npm e Google Chrome ou Chromium.

```bash
npm install                        # instala o Mermaid (uma única vez)
python3 scripts/gerar_pdfs.py      # gera todos os PDFs
python3 scripts/gerar_pdfs.py 04   # gera só o processo 04
```

## Normas de referência

- Regulamento do PPGMCS, aprovado pelo Colegiado em 15/03/2024
- Resolução PPGMCS nº 001/2024: estrutura curricular, créditos e créditos especiais
- Resolução PPGMCS nº 004/2019: exame de qualificação e defesa
- Resolução CEPEx nº 024/2021: reserva de vagas
- Regulamento de 2022 e Resolução nº 003/2019, mantidos apenas como histórico
Documentos disponíveis no atual [site do programa](https://ppgmcs.com.br)

> Documentação informativa em construção. Em caso de divergência, prevalecem as normas oficiais do PPGMCS e da Unimontes.

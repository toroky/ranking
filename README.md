# Sistema de Ranking de Jogadores de Games

Este projeto é um sistema web para gerenciamento de rankings de jogadores de jogos online, desenvolvido em Python com Flask, utilizando SQLite como banco de dados e Bootstrap com tema Bootswatch para a interface.

---

## Funcionalidades

- Importação de arquivos CSV contendo informações de jogadores (nome, nível e pontuação).
- Validação dos dados do CSV, com registro de linhas inválidas em um arquivo `erros.log`.
- Armazenamento persistente dos dados em banco SQLite.
- Suporte a múltiplas listas de rankings (histórico).
- Visualização interativa das listas disponíveis.
- Destaque visual para os 3 primeiros colocados usando Bootstrap.
- Interface responsiva e moderna com tema Cosmo do Bootswatch.

---

## Tecnologias utilizadas

- Python 3
- Flask
- SQLite
- Bootstrap 5
- Bootswatch (tema Cosmo)

---

## Como usar

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto

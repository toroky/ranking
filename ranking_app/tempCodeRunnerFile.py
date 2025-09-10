from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

DB_PATH = 'ranking.db'
TEMP_CSV = 'temp.csv'
LOG_PATH = 'erros.log'

# ========== Banco de Dados ==========
def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jogadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nivel INTEGER,
                pontuacao REAL,
                lista TEXT
            )
        ''')
        conn.commit()

def inserir_jogadores(jogadores):
    with conectar() as conn:
        cursor = conn.cursor()
        for j in jogadores:
            cursor.execute('''
                INSERT INTO jogadores (nome, nivel, pontuacao, lista)
                VALUES (?, ?, ?, ?)
            ''', (j['nome'], j['nivel'], j['pontuacao'], j['lista']))
        conn.commit()

def obter_listas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT lista FROM jogadores ORDER BY lista DESC")
        return [row[0] for row in cursor.fetchall()]

def obter_ranking(lista):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nome, nivel, pontuacao FROM jogadores
            WHERE lista = ?
            ORDER BY pontuacao DESC
        ''', (lista,))
        return cursor.fetchall()

# ========== Leitura do CSV ==========
def registrar_erro(linha, erro):
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] Erro: {erro} | Linha: {linha}\n")

def ler_csv(caminho, nome_lista):
    jogadores = []
    with open(caminho, encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            try:
                # Adaptado para aceitar chaves com maiúsculas/minúsculas
                # e garantir stripping e valores
                nome = linha.get('nome') or linha.get('Nome')
                nivel_str = linha.get('nivel') or linha.get('Nivel')
                pontuacao_str = linha.get('pontuacao') or linha.get('Pontuacao')

                if nome is None or nivel_str is None or pontuacao_str is None:
                    raise ValueError("Campos 'nome', 'nivel' ou 'pontuacao' ausentes no CSV.")

                nome = nome.strip()
                nivel_str = nivel_str.strip()
                pontuacao_str = pontuacao_str.strip()

                if not nome or not nivel_str or not pontuacao_str:
                    raise ValueError("Campo vazio encontrado.")

                nivel = int(nivel_str)
                pontuacao = float(pontuacao_str)

                jogadores.append({
                    'nome': nome,
                    'nivel': nivel,
                    'pontuacao': pontuacao,
                    'lista': nome_lista
                })
            except Exception as e:
                registrar_erro(linha, str(e))
    return jogadores

# ========== Rotas ==========
@app.route('/')
def index():
    listas = obter_listas()
    return render_template('ranking.html', listas=listas, jogadores=[], selecionada=None)

@app.route('/upload', methods=['POST'])
def upload():
    nome_lista = request.form.get('nome_lista')
    arquivo = request.files.get('arquivo')

    if not nome_lista or not arquivo:
        flash("Nome da lista e arquivo são obrigatórios.")
        return redirect(url_for('index'))

    if not arquivo.filename.endswith('.csv'):
        flash("Por favor, envie um arquivo CSV.")
        return redirect(url_for('index'))

    arquivo.save(TEMP_CSV)
    jogadores = ler_csv(TEMP_CSV, nome_lista)

    if jogadores:
        inserir_jogadores(jogadores)
        flash(f"{len(jogadores)} jogadores inseridos com sucesso na lista '{nome_lista}'.")
    else:
        flash("Nenhum jogador válido encontrado no arquivo.")

    os.remove(TEMP_CSV)
    return redirect(url_for('index'))

@app.route('/ranking/<lista>')
def ranking(lista):
    listas = obter_listas()
    jogadores = obter_ranking(lista)
    return render_template('ranking.html', listas=listas, jogadores=jogadores, selecionada=lista)

# ========== Inicialização ==========
if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)

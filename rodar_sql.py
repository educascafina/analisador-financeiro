import sqlite3

# 1. Conecta ao banco de dados
conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

# 2. Abre e lê o arquivo SQL automaticamente 
with open('sql/03_consultas.sql', 'r', encoding='utf-8') as arquivo:
    comando_sql = arquivo.read()

# 3. Executa o comando lido do arquivo
cursor.executescript(comando_sql)
conn.commit()
conn.close()

print("Arquivo SQL executado com sucesso!")
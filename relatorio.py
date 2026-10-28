import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

print("=" * 40)
print("       RELATÓRIO FINANCEIRO PESSOAL     ")
print("=" * 40)

# 1. Buscar todas as transações cadastradas
cursor.execute("SELECT * FROM transacoes;")
transacoes = cursor.fetchall()

print(f"\n1. LISTA DE TRANSAÇÕES ({len(transacoes)} registros):")
for transacao in transacoes:
    print(f"ID: {transacao[0]}, Data: {transacao[1]}, Descrição: {transacao[2]}, Categoria: {transacao[3]}, Tipo: {transacao[4]}, Valor: R$ {transacao[5]:,.2f}")

# 2. Total de Entradas vs Saídas
cursor.execute("SELECT tipo, SUM(valor) AS total_por_tipo FROM transacoes GROUP BY tipo;")
total_por_tipo = cursor.fetchall()

print("\n2. RESUMO DE ENTRADAS E SAÍDAS:")
for tipo, total in total_por_tipo:
    print(f"   - {tipo}: R$ {total:,.2f}")

# 3. Calcula o saldo atual (Entradas - Saídas)
dados = dict(total_por_tipo)
saldo = dados.get('Entrada', 0) - dados.get('Saída', 0)

print(f"\n3. SALDO ATUAL: R$ {saldo:,.2f}")

# 4.Gastos por categoria
cursor.execute("SELECT categoria, SUM(valor) AS total_gastos FROM transacoes WHERE tipo = 'Saída' GROUP BY categoria;")
gastos = cursor.fetchall()

print(f"\n4. GASTOS POR CATEGORIA:")
for categoria, total in gastos:
    print(f"- {categoria} : R$ {total:,.2f}")

# 5. Maior despesa
cursor.execute("SELECT  categoria, valor FROM transacoes  WHERE tipo = 'Saída' ORDER BY valor DESC LIMIT 1;")
maior_despensa= cursor.fetchone()

print(f"\n5. Maior despensa:")
print(f"- Categoria: {maior_despensa [0]}")
print(f"- Valor: R$ {maior_despensa [1]:,.2f}")

# 6. Gastos por mês
cursor.execute("SELECT strftime('%Y-%m', data) AS mes, SUM(valor) AS total from transacoes WHERE tipo = 'Saída' GROUP BY  mes;")
gastos_mes= cursor.fetchall()

print(f"\n6. Gastos Por Mes: ")
for mes, total in gastos_mes:
    print(f"- {mes}: R$ {total:,.2f}")

# 07. Evolução do saldo
cursor.execute("SELECT data, descricao, SUM(CASE WHEN tipo = 'Entrada' THEN valor WHEN tipo = 'Saída' THEN -valor END ) OVER (ORDER BY data, id) AS saldo FROM transacoes;")
resultado = cursor.fetchall()

print(f"\n7.Evolução do saldo: ")
print(f"="*100)
for data, descricao, saldo in resultado:
    print(f"data:{data:<12} descrição: {descricao:<25} saldo: R$ {saldo:>15,.2f} ")
conn.close()
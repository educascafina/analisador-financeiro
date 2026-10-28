-- 01 Buscar todas as transações cadastradas
SELECT * FROM transacoes;

-- 02 Somar o controle de entradas e saídas
SELECT tipo, SUM(valor) AS total_por_tipo FROM transacoes 
GROUP BY tipo;

-- 03 Calcular o saldo atual (Entradas -Saídas)
SELECT 
    SUM(CASE WHEN tipo = 'Entrada' THEN valor ELSE 0 END) -
    SUM(CASE WHEN tipo = 'Saída' THEN valor ELSE 0 END) AS saldo_atual
FROM transacoes;

-- 04 Gastos por categoria
SELECT categoria, Sum(valor) 
AS total_gastos FROM transacoes
WHERE tipo = 'Saída'
GROUP BY categoria;

-- 05 Maior despesa
SELECT  categoria, valor FROM transacoes
WHERE tipo = 'Saída'
ORDER BY valor DESC LIMIT 1; 

-- 06 Gastos por mês
SELECT strftime('%Y-%m', data) AS mes,
SUM(valor) AS total from transacoes
WHERE tipo = 'Saída'
GROUP BY  mes; 

-- 07 Evolução do saldo
SELECT data, descricao, 
SUM(
    CASE 
      WHEN tipo = 'Entrada' THEN valor 
      WHEN tipo = 'Saída' THEN - valor 
    END  
) OVER (ORDER BY data, id) AS saldo
FROM transacoes;
--1. Qual a média de gasto de cada pessoa?

SELECT avg(order_total) AS Avg_Ticket
FROM client_order
GROUP BY fk_client
HAVING fk_restaurant = 1;

--2. Qual a maior compra (em valor) feita no restaurante?

SELECT order_total
FROM client_order
GROUP BY order_total
HAVING fk_restaurant = 1
ORDER BY order_total DESC
LIMIT 1;

--3. Qual o maior pedido (em quantidade de itens) feita no restaurante?

SELECT fk_product, sum(quantity)
FROM client_order
GROUP BY order_total
HAVING fk_restaurant = 1
ORDER BY order_total DESC
LIMIT 1;

--4. Liste a maior e a menos comissão paga pelo restaurante.

--5. Qual o item mais pedido?

SELECT fk_product, sum(quantity)
FROM client_order
GROUP BY fk_product
HAVING fk_restaurant = 1
ORDER BY fk_product DESC
LIMIT 1;

--6. Quantos pedidos em cada status? Liste todos os status, mesmo que não haja pedido.

SELECT status,
       count(*) AS qntd_status
FROM client_order
GROUP BY status
HAVING fk_restaurant= 1;

--7. Calcule a quantidade média de pedidos por cada dia da semana. Pivote o resultado.
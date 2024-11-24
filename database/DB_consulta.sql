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

--4. Liste a maior e a menor comissão paga pelo restaurante.

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

--ADMIN---------------------------------------------------

--1. Quantidade de restaurantes e clientes cadastrados.

SELECT count(r.id)
FROM restaurant r;

SELECT count(c.id)
FROM client c;

--2. Quantidade de clientes únicos que já fizeram um pedido em cada restaurante.

SELECT co.fk_restaurant, COUNT(DISTINCT co.fk_client) AS unique_client_count
FROM client_order co
GROUP BY co.fk_restaurant;

--3. Ticket médio por restaurante (valor médio de cada pedido).

SELECT fk_restaurant, avg(co.order_total)
FROM client_order co
GROUP BY fk_restaurant;
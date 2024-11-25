--1. Qual a média de gasto de cada pessoa?

SELECT fk_client, avg(order_total) AS Avg_Ticket
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

SELECT client_order.order_id, fk_product, sum(quantity)
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
       COUNT(DISTINCT order_id) AS qntd_status
FROM client_order
WHERE fk_restaurant = 1
GROUP BY status;

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

-----INSERTS------

INSERT INTO restaurant (name_restaurant, commission, email, password) VALUES
('Restaurante 1', 10, 'restaurante1@gmail.com', 'Senha1'),
('Restaurante 2', 15, 'restaurante2@gmail.com', 'Senha2'),
('Restaurante 3', 5, 'restaurante3@gmail.com', 'Senha3'),
('Restaurante 4', 20, 'restaurante4@gmail.com', 'Senha4'),
('Restaurante 5', 25, 'restaurante5@gmail.com', 'Senha5'),
('Restaurante 6', 18, 'restaurante6@gmail.com', 'Senha6'),
('Restaurante 7', 12, 'restaurante7@gmail.com', 'Senha7'),
('Restaurante 8', 10, 'restaurante8@gmail.com', 'Senha8'),
('Restaurante 9', 22, 'restaurante9@gmail.com', 'Senha9'),
('Restaurante 10', 30, 'restaurante10@gmail.com', 'Senha10'),
('Restaurante 11', 8, 'restaurante11@gmail.com', 'Senha11'),
('Restaurante 12', 14, 'restaurante12@gmail.com', 'Senha12'),
('Restaurante 13', 9, 'restaurante13@gmail.com', 'Senha13'),
('Restaurante 14', 16, 'restaurante14@gmail.com', 'Senha14'),
('Restaurante 15', 5, 'restaurante15@gmail.com', 'Senha15');

INSERT INTO product (name_product, price, fk_id_restaurant) VALUES
('Produto A', 1500, 1),
('Produto B', 2000, 1),
('Produto C', 1200, 2),
('Produto D', 2500, 2),
('Produto E', 1000, 3),
('Produto F', 1800, 3),
('Produto G', 2200, 4),
('Produto H', 1700, 4),
('Produto I', 3000, 1),
('Produto J', 1300, 1),
('Produto K', 1600, 2),
('Produto L', 2400, 2),
('Produto M', 1400, 3),
('Produto N', 2000, 3),
('Produto O', 1000, 4);

INSERT INTO client (name_client, email, password) VALUES
('Ana Costa', 'cliente1@gmail.com', 'Senha1'),
('Carlos Silva', 'cliente2@gmail.com', 'Senha2'),
('Maria Oliveira', 'cliente3@gmail.com', 'Senha3'),
('João Pereira', 'cliente4@gmail.com', 'Senha4'),
('Fernanda Souza', 'cliente5@gmail.com', 'Senha5'),
('Lucas Almeida', 'cliente6@gmail.com', 'Senha6'),
('Beatriz Santos', 'cliente7@gmail.com', 'Senha7'),
('Ricardo Lima', 'cliente8@gmail.com', 'Senha8'),
('Patrícia Rocha', 'cliente9@gmail.com', 'Senha9'),
('Eduardo Martins', 'cliente10@gmail.com', 'Senha10'),
('Gabriela Ferreira', 'cliente11@gmail.com', 'Senha11'),
('Marcos Costa', 'cliente12@gmail.com', 'Senha12'),
('Juliana Mendes', 'cliente13@gmail.com', 'Senha13'),
('Felipe Barbosa', 'cliente14@gmail.com', 'Senha14'),
('Isabela Pereira', 'cliente15@gmail.com', 'Senha15');

INSERT INTO client_order (order_id, fk_client, fk_product, quantity, date_order, fk_restaurant, order_total, status) VALUES
('f47ac10b-58cc-4372-a567-0e02b2c3d479', 1, 1, 2, '23-11-2024 20:39:19', 1, 15000, 0),
('2c6ee24b-52d8-4c92-9f74-d98f8c7b2b91', 2, 2, 3, '23-11-2024 20:40:45', 2, 20000, 0),
('0c9b2d11-9f65-47e5-b5c8-c7cb4596b2b8', 3, 3, 1, '23-11-2024 20:42:12', 3, 12000, 0),
('ee6db7b7-d859-4edb-9539-5f842dfb5c3b', 4, 4, 4, '23-11-2024 20:43:30', 4, 10000, 0),
('b624be61-2a50-4d71-8b3c-bc01758ad237', 5, 5, 2, '23-11-2024 20:45:00', 1, 25000, 0),
('b351ff97-cc71-46b1-bfbb-6a44a473b3a3', 6, 6, 3, '23-11-2024 20:46:25', 2, 27000, 0),
('1950e4a0-9287-4131-87a1-228b672b9c6f', 7, 7, 1, '23-11-2024 20:47:50', 3, 22000, 0),
('3bb0a1f8-5b9c-42f1-935b-56073d538982', 1, 1, 5, '23-11-2024 20:49:15', 4, 85000, 0),
('0e61e777-d110-411f-92a7-b63a8f443c9c', 2, 2, 2, '23-11-2024 20:50:40', 1, 60000, 0),
('e7d6991d-b241-4bc3-9e88-d90c933c7c77', 3, 3, 3, '23-11-2024 20:52:05', 2, 39000, 0),
('2e83d73f-79f2-49a7-84a3-d272a5cf8b25', 4, 4, 4, '23-11-2024 20:53:30', 3, 64000, 0),
('7d1cd743-3a0d-40c3-b3d3-0ff1f3b0bdfb', 5, 5, 3, '23-11-2024 20:54:55', 4, 72000, 0),
('465493e5-02de-4536-b6b0-f1cd6a9c78cf', 6, 6, 2, '23-11-2024 20:56:20', 1, 28000, 0),
('abf8f62f-c7c7-42fa-b5b5-299660d9c848', 7, 7, 1, '23-11-2024 20:57:45', 2, 20000, 0),
('d20a80be-63d1-4d57-9c2c-e7f0a9304fd5', 1, 1, 5, '23-11-2024 20:59:10', 3, 50000, 0);

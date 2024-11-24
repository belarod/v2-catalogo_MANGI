# v2-catalogo_MANGI

flask --app appFlask.py run
flask --app appFlask.py --debug run

SELECT DISTINCT avg(order_total) AS Avg_Ticket
FROM client_order
GROUP BY fk_client
HAVING fk_restaurant = 1;


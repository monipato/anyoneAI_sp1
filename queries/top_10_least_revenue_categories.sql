-- TODO: 
-- This query will return a table with the top 10 least revenue categories 
-- in English, the number of orders and their total revenue. 
-- It will have different columns: 
--      Category, that will contain the top 10 least revenue categories; 
--      Num_order, with the total amount of orders of each category; 
--      Revenue, with the total revenue of each category.

-- HINT: 
-- All orders should have a delivered status and the Category and actual delivery date should be not null.
-- For simplicity, if there are orders with multiple product categories, consider the full order's payment_value in the summation of revenue of each category
SELECT
    c.product_category_name_english AS category,
    COUNT(DISTINCT o.order_id) AS num_order,
    SUM(op.payment_value) AS revenue
    --SUM(oi.price) AS revenue
FROM olist_orders o
JOIN olist_order_items oi 
	ON o.order_id = oi.order_id
JOIN olist_products p 
	ON oi.product_id = p.product_id
JOIN product_category_name_translation c 
	ON p.product_category_name = c.product_category_name
JOIN olist_order_payments op 
	ON o.order_id = op.order_id
WHERE
    o.order_status = 'delivered'
    AND p.product_category_name IS NOT NULL
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY
    c.product_category_name_english
ORDER BY
    revenue ASC
LIMIT 10;
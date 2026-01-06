/*
A. SQL & DATA EXTRACTION (CONCEPTUAL OR VIA SQLITE)
------------------------------------------------------------------
------------------------------------------------------------------
*/

-- Customers table 
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(50),
    total_orders FLOAT,
    total_spent FLOAT,
    last_order VARCHAR(50),  -- Convert to DATETIME later
    days_since_last_order FLOAT,
    churn_flag INT,
    city FLOAT  -- Encoded city names as FLOAT
);

-- Products table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    category_english VARCHAR(100),
    product_name_lenght FLOAT,
    product_description_lenght FLOAT,
    product_photos_qty FLOAT
);

-- Sales table 
CREATE TABLE sales (
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    category_english VARCHAR(100),
    price FLOAT,
    freight_value FLOAT,
    payment_type VARCHAR(50),
    payment_value FLOAT,
    order_purchase_timestamp DATETIME,  
    order_delivered_customer_date VARCHAR(50),  
    total_price FLOAT
);

-- Marketing table
CREATE TABLE marketing (
    campaign_id VARCHAR(50),
    customer_id VARCHAR(50),
    channel VARCHAR(50),
    start_date DATETIME,  
    spend INT,
    conversions INT,
    response_rate FLOAT
);

-- Reviews table
CREATE TABLE reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    review_score INT,
    review_comment_message TEXT
);

-- Load CSVs files (datasets)


-- BASIC SQL OPERATIONS (having the output as well in comment)
--************************************************************
-- 1. Retrieve Top 10 Customers by Total Spend:

SELECT customer_id, total_spent
FROM customers
ORDER BY total_spent DESC
LIMIT 10;

/*
|		customer_id				 | total_spent |
|--------------------------------|-------------|
|1617b1357756262bfa56ab541c47bc16|	13664.08	|
|9af2372a1e49340278e7c1ef8d749f34|	13281.71	|
|de832e8dbb1f588a47013e53feaa67cc|	11111.4		|
|63b964e79dee32a3587651701a2b8dbf|	10553.28	|
|6f241d5bbb142b6f764387c8c270645a|	10055.22	|
|926b6a6fb8b6081e00b335edaf578d35|	 8389.52	|
|eb7a157e8da9c488cd4ddc48711f1097|	 8068.88	|
|f959b7bc834045511217e6410985963f|	 8030.46	|
|d1ea705f2fdd8f98eff86c2691652e60|	 7413.7	 	|
|ec5b2ba62e574342386871631fafd3fc|	 7274.88	|

*/

-- 2. Identify Top 5 Product Categories by Revenue:

SELECT category_english, SUM(total_price) AS revenue
FROM sales
GROUP BY category_english
ORDER BY revenue DESC
LIMIT 5;

/*
| category_english 		| 	revenue  |
|-----------------------|------------|
|health_beauty	   		| 1549751.22 |
|watches_gifts	   		| 1430999.55 |
|bed_bath_table	   		| 1370217.74 |
|sports_leisure	   		| 1238470.4  |
|computers_accessories	| 1134101.36 |

*/

-- 3. Average Order Value per City/State:

SELECT c.customer_city AS city, AVG(s.total_price) AS avg_order_value
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_city
ORDER BY avg_order_value DESC
LIMIT 10;  

/*
| city 						| avy_order_value | customer_state|
|---------------------------|-----------------|---------------|
| salto grande				|	6743.4		  |		SP		  |
| pianco					|	2324.99		  |		PB		  |
| nova esperanca do piria	|	2252.66		  |		PA		  |
| engenheiro navarro		|	2106.55		  |		MG		  |
| agrestina					|	2066.34		  |		PE		  |
| triunfo					|	1985.7		  |		PB		  |	
| itaparica					|	1883.6		  |		BA		  |
| mariental					|	1867.85 	  |		PR		  |
................. SO ON
*/

-- 4. Determine the percentage of customers who have churned (churn_flag = 1)

SELECT (SUM(CASE WHEN churn_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS churn_percentage
FROM customers;

/*
80.4135115294496
*/

-- 5. Join sales and marketing tables to find conversion rate by channel

SELECT m.channel, (SUM(m.conversions) * 1.0 / COUNT(DISTINCT m.customer_id)) AS conversion_rate
FROM marketing m
LEFT JOIN sales s ON m.customer_id = s.customer_id
GROUP BY m.channel;

/*
| channel      | 	avg_conversion |
|--------------|-------------------|
| Affiliate	   | 0.387096774193548 |
| Email		   | 0.347826086956522 |
| SMS		   | 0.362903225806452 |
| Social Media | 0.416058394160584 |

*/

-- DETECT INVALID/MISSING VALUES WITH SQL QUERIES :
--*************************************************

-- Check nulls in key columns
SELECT COUNT(*) FROM customers 
WHERE days_since_last_order IS NULL;  -- ~5724 nulls
SELECT COUNT(*) FROM sales 
WHERE category_english IS NULL;  -- ~1723 nulls
SELECT COUNT(*) FROM sales 
WHERE payment_type IS NULL;  -- 3 nulls
SELECT COUNT(*) FROM products 
WHERE category_english IS NULL;  -- 618 nulls

-- Check for invalid values (e.g., negative prices)
SELECT COUNT(*) 
FROM sales WHERE price < 0;  -- Should be 0
SELECT COUNT(*) 
FROM sales WHERE total_price < 0;  -- Should be 0

-- Referential integrity: Check unmatched IDs

SELECT COUNT(DISTINCT s.customer_id) 
FROM sales s LEFT JOIN customers c 
ON s.customer_id = c.customer_id 
WHERE c.customer_id IS NULL;  -- Should be 0

SELECT COUNT(DISTINCT s.product_id) 
FROM sales s LEFT JOIN products p 
ON s.product_id = p.product_id 
WHERE p.product_id IS NULL;  -- Minor mismatches

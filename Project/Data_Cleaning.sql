-- Create database 
CREATE DATABASE IF NOT EXISTS retailsmart;
USE retailsmart;

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

-- Load data from CSVs (use Table Data Import Wizard )

-- Retrieve Top 10 Customers by Total Spend:

SELECT customer_id, total_spent
FROM customers
ORDER BY total_spent DESC
LIMIT 10;

-- Identify Top 5 Product Categories by Revenue:

SELECT category_english, SUM(total_price) AS revenue
FROM sales
GROUP BY category_english
ORDER BY revenue DESC
LIMIT 5;

-- Average Order Value per City/State:

SELECT c.customer_city AS city, AVG(s.total_price) AS avg_order_value
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_city
ORDER BY avg_order_value DESC
LIMIT 10;  -- Top 10 for brevity

-- Percentage of Customers Who Have Churned:

SELECT (SUM(churn_flag) / COUNT(*)) * 100 AS churn_percentage
FROM customers;

-- Join Sales and Marketing for Conversion Rate by Channel:

SELECT m.channel, AVG(m.response_rate) AS avg_conversion
FROM marketing m
JOIN sales s ON m.customer_id = s.customer_id
GROUP BY m.channel;

-- Detect Invalid/Missing Values with SQL Queries:

-- Check nulls in key columns
SELECT COUNT(*) FROM customers 
WHERE days_since_last_order IS NULL;  -- ~5775 nulls
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


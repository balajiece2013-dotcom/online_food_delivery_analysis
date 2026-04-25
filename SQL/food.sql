CREATE DATABASE food_delivery_db;

USE food_delivery_db;

SELECT COUNT(*) FROM engineered_food_delivery;

SELECT * FROM  engineered_food_delivery;

#------------------------------
#1.0 TOP 5 CITIES BY REVENUE
#------------------------------
SELECT city, SUM(order_value) AS revenue
FROM engineered_food_delivery
GROUP BY city
ORDER BY revenue DESC
LIMIT 5;
#---------------------------------
#2.0 TOP RESTAURANTS (RANK FUNCTION 🔥)
#---------------------------------
SELECT 
    restaurant_name,
    SUM(order_value) AS revenue
FROM engineered_food_delivery
GROUP BY restaurant_name
ORDER BY revenue DESC
LIMIT 10;

#---------------------------------
#3.0 CANCELLATION RATE BY CITY
#---------------------------------
SELECT 
    city,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),2) AS cancel_rate
FROM engineered_food_delivery
GROUP BY city
ORDER BY cancel_rate DESC;
#---------------------------------
#4.0 REVENUE BY CUISINE (WITH % CONTRIBUTION 🔥)
#---------------------------------
SELECT 
    cuisine_type,
    SUM(order_value) AS revenue,
    ROUND(SUM(order_value) * 100.0 / SUM(SUM(order_value)) OVER (),2) AS contribution_percent
FROM engineered_food_delivery
GROUP BY cuisine_type;
#---------------------------------
#5.0 PEAK HOUR PERFORMANCE
#---------------------------------
SELECT 
    peak_hour,
    COUNT(*) AS orders,
    AVG(order_value) AS avg_order_value
FROM engineered_food_delivery
GROUP BY peak_hour;
#---------------------------------
#6.0 DELIVERY PERFORMANCE ANALYSIS
#---------------------------------
SELECT 
    delivery_performance,
    COUNT(*) AS total_orders,
    AVG(delivery_time_min) AS avg_time
FROM engineered_food_delivery
GROUP BY delivery_performance;
#---------------------------------
#️7.0 MONTHLY REVENUE TREND
#---------------------------------
SELECT 
    order_month,
    SUM(order_value) AS revenue
FROM cleaned_data
GROUP BY order_month
ORDER BY order_month;
#---------------------------------
#8.0 CUSTOMER SEGMENT ANALYSIS
#---------------------------------
SELECT 
    customer_age_group,
    COUNT(*) AS total_orders,
    AVG(order_value) AS avg_spend
FROM engineered_food_delivery
GROUP BY customer_age_group;
#---------------------------------
#9.0 TOP 3 RESTAURANTS PER CITY (ADVANCED 🔥🔥)
#---------------------------------
SELECT *
FROM (
    SELECT 
        city,
        restaurant_name,
        SUM(order_value) AS revenue,
        RANK() OVER (PARTITION BY city ORDER BY SUM(order_value) DESC) AS rnk
    FROM engineered_food_delivery
    GROUP BY city, restaurant_name
) t
WHERE rnk <= 3;
#---------------------------------
#10.0 DISTANCE VS DELIVERY TIME RELATION
#---------------------------------
SELECT 
    ROUND(distance_km,0) AS distance_bucket,
    AVG(delivery_time_min) AS avg_time
FROM engineered_food_delivery
GROUP BY distance_bucket
ORDER BY distance_bucket;
#---------------------------------






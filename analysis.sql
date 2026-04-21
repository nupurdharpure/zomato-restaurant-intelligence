
-- Query 1: Top cities by restaurant count
SELECT City, COUNT(*) AS total_restaurants, ROUND(AVG(`Aggregate rating`), 2) AS avg_rating
FROM restaurants
GROUP BY City
ORDER BY total_restaurants DESC
LIMIT 10;

-- Query 2: Most popular cuisines in Delhi
SELECT `Primary Cuisine`, COUNT(*) AS total_restaurants,
ROUND(AVG(`Aggregate rating`), 2) AS avg_rating,
ROUND(AVG(`Average Cost for two`), 0) AS avg_cost
FROM restaurants
WHERE City = 'New Delhi'
GROUP BY `Primary Cuisine`
ORDER BY total_restaurants DESC
LIMIT 10;

-- Query 3: Price range vs rating
SELECT `Price range`, COUNT(*) AS total_restaurants,
ROUND(AVG(`Aggregate rating`), 2) AS avg_rating,
ROUND(AVG(`Average Cost for two`), 0) AS avg_cost
FROM restaurants
GROUP BY `Price range`
ORDER BY `Price range` ASC;

-- Query 4: Online delivery analysis
SELECT `Has Online delivery`, COUNT(*) AS total_restaurants,
ROUND(AVG(`Aggregate rating`), 2) AS avg_rating,
ROUND(AVG(`Average Cost for two`), 0) AS avg_cost
FROM restaurants
GROUP BY `Has Online delivery`;

-- Query 5: Overrated restaurants in Delhi
SELECT `Restaurant Name`, City, `Primary Cuisine`,
`Aggregate rating`, Votes, `Average Cost for two`
FROM restaurants
WHERE Votes > 500 AND `Aggregate rating` < 3.5 AND City = 'New Delhi'
ORDER BY Votes DESC
LIMIT 10;

SELECT id, name, min_temp FROM items ORDER BY name;

SELECT id, name FROM categories ORDER BY name;

SELECT name, min_temp FROM items WHERE min_temp <= 0;

SELECT * FROM categories WHERE name LIKE '%обувь%';

SELECT items.name AS item_name, categories.name AS category_name
FROM items
JOIN categories ON items.category_id = categories.id;

SELECT items.name, categories.name AS category, seasons.name AS season
FROM items
JOIN categories ON items.category_id = categories.id
JOIN seasons ON items.season_id = seasons.id;

SELECT COUNT(*) AS total_items FROM items;

SELECT AVG(min_temp) AS avg_temp FROM items;

SELECT categories.name AS category_name, COUNT(items.id) AS items_count
FROM categories
LEFT JOIN items ON categories.id = items.category_id
GROUP BY categories.id, categories.name
ORDER BY items_count DESC;

SELECT categories.name AS category_name, COUNT(items.id) AS items_count
FROM categories
JOIN items ON categories.id = items.category_id
GROUP BY categories.id, categories.name
HAVING COUNT(items.id) > 1;
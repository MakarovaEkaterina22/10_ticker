CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    demand INTEGER NOT NULL,
    date DATE NOT NULL
);

INSERT INTO products (category, product_name, demand, date) VALUES
('Electronics', 'Smartphone X', 150, '2023-01-01'),
('Electronics', 'Laptop Pro', 80, '2023-01-01'),
('Clothing', 'T-Shirt', 200, '2023-01-01'),
('Clothing', 'Jeans', 120, '2023-01-01'),
('Electronics', 'Smartphone X', 180, '2023-02-01'),
('Electronics', 'Laptop Pro', 95, '2023-02-01'),
('Clothing', 'T-Shirt', 220, '2023-02-01'),
('Clothing', 'Jeans', 110, '2023-02-01');
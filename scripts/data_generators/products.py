import random

class ProductGenerator:
    def generate(self):
        products = [
            # Smartphones
            ('iPhone 14', 'Electronics', 'Smartphones', 'Apple', 79999),
            ('iPhone 15', 'Electronics', 'Smartphones', 'Apple', 89999),
            ('Samsung Galaxy S23', 'Electronics', 'Smartphones', 'Samsung', 74999),
            ('Samsung Galaxy A54', 'Electronics', 'Smartphones', 'Samsung', 38999),
            ('Nothing Phone 1', 'Electronics', 'Smartphones', 'Nothing', 27999),
            ('OnePlus 11', 'Electronics', 'Smartphones', 'OnePlus', 56999),
            ('Redmi Note 13', 'Electronics', 'Smartphones', 'Xiaomi', 18999),

            # Laptops
            ('Macbook M1 Air', 'Electronics', 'Laptops', 'Apple', 65999),
            ('Macbook M2 Pro', 'Electronics', 'Laptops', 'Apple', 149999),
            ('Dell XPS 13', 'Electronics', 'Laptops', 'Dell', 99999),
            ('HP Pavilion 15', 'Electronics', 'Laptops', 'HP', 59999),
            ('Lenovo ThinkPad X1', 'Electronics', 'Laptops', 'Lenovo', 129999),
            ('Asus ROG Strix', 'Electronics', 'Laptops', 'Asus', 119999),

            # Televisions
            ('Samsung 55" 4K TV', 'Electronics', 'Televisions', 'Samsung', 55000),
            ('LG OLED C3', 'Electronics', 'Televisions', 'LG', 145000),
            ('Sony Bravia 50"', 'Electronics', 'Televisions', 'Sony', 78000),
            ('Mi Smart TV 43"', 'Electronics', 'Televisions', 'Xiaomi', 28999),

            # Footwear
            ('Nike Air Max', 'Clothing', 'Footwear', 'Nike', 8999),
            ('Nike Revolution 6', 'Clothing', 'Footwear', 'Nike', 4999),
            ('Adidas Ultraboost', 'Clothing', 'Footwear', 'Adidas', 12999),
            ('Adidas RunFalcon', 'Clothing', 'Footwear', 'Adidas', 5999),
            ('Puma RS-X', 'Clothing', 'Footwear', 'Puma', 7999),

            # Clothing
            ('Levi\'s Jeans', 'Clothing', 'Apparel', 'Levis', 2999),
            ('H&M T-Shirt', 'Clothing', 'Apparel', 'H&M', 999),
            ('Zara Jacket', 'Clothing', 'Apparel', 'Zara', 4999),
            ('Uniqlo Hoodie', 'Clothing', 'Apparel', 'Uniqlo', 2499),

            # Accessories
            ('Apple AirPods Pro', 'Electronics', 'Accessories', 'Apple', 24999),
            ('Boat Rockerz 450', 'Electronics', 'Accessories', 'Boat', 1999),
            ('Sony WH-1000XM5', 'Electronics', 'Accessories', 'Sony', 29999),
            ('Logitech MX Master 3', 'Electronics', 'Accessories', 'Logitech', 8999),

            # Home Appliances
            ('Dyson V11 Vacuum', 'Home', 'Appliances', 'Dyson', 45000),
            ('Philips Air Fryer', 'Home', 'Appliances', 'Philips', 12999),
            ('LG Washing Machine', 'Home', 'Appliances', 'LG', 39999),
            ('Samsung Refrigerator', 'Home', 'Appliances', 'Samsung', 55999),

            # Gaming
            ('PlayStation 5', 'Electronics', 'Gaming', 'Sony', 54990),
            ('Xbox Series X', 'Electronics', 'Gaming', 'Microsoft', 54990),
            ('Nintendo Switch', 'Electronics', 'Gaming', 'Nintendo', 29999),
            ('Asus Gaming Monitor', 'Electronics', 'Gaming', 'Asus', 25999),
        ]
        p = random.choice(products)
        return {
            'name': p[0],
            'category': p[1],
            'sub_category': p[2],
            'brand': p[3],
            'unit_price': p[4]
        }
    def generate_batch(self, count):
        return [self.generate() for _ in range(count)]
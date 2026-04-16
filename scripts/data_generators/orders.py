import random

class OrderGenerator:
    def __init__(self):
        pass
    
    def generate(self, customer_id, date_id, product_id, location_id, unit_price):
        qty = random.randint(1, 5)
        discount = random.choice([0, 5, 10, 15, 20])
        total_amount = unit_price * qty * (1 - discount / 100)

        return {
            'customer_id': customer_id,
            'date_id': date_id,
            'product_id': product_id,
            'location_id': location_id,
            'unit_price': unit_price,
            'qty': qty,
            'discount': discount,
            'total_amount': total_amount,
            'status': random.choice(['Delivered', 'Returned', 'Pending'])
        }
    def generate_batch(self, count, customer_ids, date_ids, product_ids_with_prices, location_ids):
        orders = []
        for _ in range(count):
            pid = random.choice(list(product_ids_with_prices.keys()))
            order = self.generate(
                customer_id=random.choice(customer_ids),
                date_id=random.choice(date_ids),
                product_id=pid,
                location_id=random.choice(location_ids),
                unit_price=product_ids_with_prices[pid]
            )
            orders.append(order)
        return orders

import pandas as pd
import numpy as np
import random

def generate_laptop_data(num_samples=1000):
    np.random.seed(42)
    random.seed(42)
    
    brands = ['Apple', 'HP', 'Dell', 'Lenovo', 'Asus', 'Acer', 'MSI']
    processors = ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9', 
                  'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9', 'Apple M1', 'Apple M2']
    rams = [4, 8, 16, 32, 64]
    storages = [256, 512, 1024, 2048]
    gpus = ['Intel Iris Xe', 'Intel UHD', 'AMD Radeon', 'NVIDIA GTX 1650', 
            'NVIDIA RTX 3050', 'NVIDIA RTX 3060', 'NVIDIA RTX 4060', 'NVIDIA RTX 4070', 'Apple GPU']
    
    data = []
    for _ in range(num_samples):
        brand = random.choice(brands)
        
        if brand == 'Apple':
            processor = random.choice(['Apple M1', 'Apple M2'])
            gpu = 'Apple GPU'
        else:
            processor = random.choice([p for p in processors if 'Apple' not in p])
            gpu = random.choice([g for g in gpus if 'Apple' not in g])
            
        ram = random.choice(rams)
        storage = random.choice(storages)
        
        base_price = 300
        
        if brand == 'Apple': base_price += 500
        elif brand in ['MSI', 'Asus']: base_price += 200
        
        if 'i5' in processor or 'Ryzen 5' in processor: base_price += 150
        elif 'i7' in processor or 'Ryzen 7' in processor: base_price += 300
        elif 'i9' in processor or 'Ryzen 9' in processor: base_price += 500
        elif 'M1' in processor: base_price += 300
        elif 'M2' in processor: base_price += 500
        
        base_price += (ram - 4) * 15
        
        base_price += (storage - 256) * 0.2
        
        if 'GTX 1650' in gpu: base_price += 150
        elif 'RTX 3050' in gpu: base_price += 250
        elif 'RTX 3060' in gpu: base_price += 400
        elif 'RTX 4060' in gpu: base_price += 500
        elif 'RTX 4070' in gpu: base_price += 800
        
        price = base_price + np.random.normal(0, 100)
        price = max(200, round(price, 2))
        price_pkr = int(round(price * 278))
        
        data.append({
            'Brand': brand,
            'Processor': processor,
            'RAM_GB': ram,
            'Storage_GB': storage,
            'GPU': gpu,
            'Price_PKR': price_pkr
        })
        
    df = pd.DataFrame(data)
    df.to_csv('laptop_data.csv', index=False)
    print(f"Generated laptop_data.csv with {num_samples} samples.")

if __name__ == "__main__":
    generate_laptop_data()

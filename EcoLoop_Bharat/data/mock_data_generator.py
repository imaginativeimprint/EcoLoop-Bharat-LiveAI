"""
Generate realistic mock data for the MVP demo
Creates streams that demonstrate Pathway's real-time capabilities
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import hashlib
import os

class MockDataGenerator:
    """
    Generate realistic Indian waste management data
    """
    def __init__(self):
        np.random.seed(42)
        random.seed(42)
        
        # Indian manufacturer data
        self.manufacturers = [
            {"id": "M001", "name": "Tata Steel", "city": "Jamshedpur", "state": "Jharkhand"},
            {"id": "M002", "name": "Relacy Plastics", "city": "Mumbai", "state": "Maharashtra"},
            {"id": "M003", "name": "Dixit E-Waste", "city": "Delhi", "state": "Delhi"},
            {"id": "M004", "name": "Kumar Paper Mills", "city": "Chennai", "state": "Tamil Nadu"},
            {"id": "M005", "name": "GreenGlass India", "city": "Bengaluru", "state": "Karnataka"},
            {"id": "M006", "name": "Amul Dairy", "city": "Anand", "state": "Gujarat"},
            {"id": "M007", "name": "Apple India", "city": "Bengaluru", "state": "Karnataka"},
            {"id": "M008", "name": "Samsung India", "city": "Noida", "state": "UP"},
        ]
        
        # Recovery centers across India
        self.recovery_centers = [
            {"id": "R001", "name": "Delhi Recycling Hub", "city": "Delhi", "capacity": 10000},
            {"id": "R002", "name": "Mumbai Waste Warriors", "city": "Mumbai", "capacity": 15000},
            {"id": "R003", "name": "Bengaluru E-Parisara", "city": "Bengaluru", "capacity": 8000},
            {"id": "R004", "name": "Chennai Green Center", "city": "Chennai", "capacity": 7000},
            {"id": "R005", "name": "Kolkata Recovery", "city": "Kolkata", "capacity": 6000},
            {"id": "R006", "name": "Pune Recycling", "city": "Pune", "capacity": 5000},
            {"id": "R007", "name": "Ahmedabad Waste", "city": "Ahmedabad", "capacity": 4500},
            {"id": "R008", "name": "Hyderabad Green", "city": "Hyderabad", "capacity": 5500},
        ]
        
        # Material types with recycling percentages
        self.materials = [
            {"type": "PET Plastic", "category": "plastic", "recyclable": 0.85, "carbon_per_kg": 2.5},
            {"type": "HDPE Plastic", "category": "plastic", "recyclable": 0.90, "carbon_per_kg": 2.3},
            {"type": "Aluminum", "category": "metal", "recyclable": 0.95, "carbon_per_kg": 8.0},
            {"type": "Steel", "category": "metal", "recyclable": 0.88, "carbon_per_kg": 1.8},
            {"type": "Copper", "category": "metal", "recyclable": 0.92, "carbon_per_kg": 3.5},
            {"type": "Glass", "category": "glass", "recyclable": 0.80, "carbon_per_kg": 0.8},
            {"type": "Paper/Cardboard", "category": "paper", "recyclable": 0.75, "carbon_per_kg": 0.5},
            {"type": "E-Waste PCB", "category": "e_waste", "recyclable": 0.70, "carbon_per_kg": 15.0},
            {"type": "Lithium Battery", "category": "e_waste", "recyclable": 0.60, "carbon_per_kg": 25.0},
            {"type": "Organic Waste", "category": "organic", "recyclable": 0.95, "carbon_per_kg": 0.2},
        ]
        
        # Create data directories
        os.makedirs("data/live", exist_ok=True)
        os.makedirs("data/archive", exist_ok=True)
    
    def generate_product_id(self, material_code, manufacturer_id):
        """Generate unique product ID with QR code"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = random.randint(1000, 9999)
        product_id = f"{material_code}{manufacturer_id}{timestamp}{random_part}"
        
        # Generate QR hash (simulated)
        qr_hash = hashlib.sha256(product_id.encode()).hexdigest()[:16]
        
        return product_id, qr_hash
    
    def generate_factory_output(self, num_records=1000):
        """
        Generate manufacturing output stream
        """
        records = []
        
        # Start from 30 days ago to create history
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(num_records):
            # Random manufacturer
            mfg = random.choice(self.manufacturers)
            
            # Random material
            material = random.choice(self.materials)
            
            # Generate product ID
            material_code = material['type'][:3].upper()
            product_id, qr_hash = self.generate_product_id(material_code, mfg['id'])
            
            # Random timestamp in last 30 days (weighted towards recent)
            days_ago = random.expovariate(0.2)  # Exponential to favor recent
            timestamp = start_date + timedelta(days=min(days_ago, 30))
            
            # Weight in kg
            weight = random.uniform(0.5, 50.0)
            
            # Carbon footprint calculation
            carbon = weight * material['carbon_per_kg']
            
            # GPS coordinates (rough Indian centers)
            gps_coords = {
                "Delhi": (28.6139, 77.2090),
                "Mumbai": (19.0760, 72.8777),
                "Bengaluru": (12.9716, 77.5946),
                "Chennai": (13.0827, 80.2707),
                "Kolkata": (22.5726, 88.3639),
                "Pune": (18.5204, 73.8567),
                "Ahmedabad": (23.0225, 72.5714),
                "Hyderabad": (17.3850, 78.4867),
                "Jamshedpur": (22.8046, 86.2029),
                "Noida": (28.5355, 77.3910),
                "Anand": (22.5645, 72.9289)
            }
            
            lat, lon = gps_coords.get(mfg['city'], (20.5937, 78.9629))
            
            record = {
                'product_id': product_id,
                'batch_number': f"BATCH-{timestamp.strftime('%Y%m')}-{random.randint(1,999):03d}",
                'manufacturer_id': mfg['id'],
                'manufacturer_name': mfg['name'],
                'material_type': material['type'],
                'material_category': material['category'],
                'weight_kg': round(weight, 2),
                'carbon_footprint': round(carbon, 2),
                'recyclable_percentage': material['recyclable'],
                'gst_hsn_code': f"39{random.randint(10,99)}{random.randint(100,999)}",
                'manufacturing_date': timestamp.timestamp(),
                'expiry_date': (timestamp + timedelta(days=random.randint(30, 365))).timestamp() 
                              if material['category'] in ['organic', 'paper'] else None,
                'qr_code_hash': qr_hash,
                'gps_lat': lat + random.uniform(-0.1, 0.1),
                'gps_lon': lon + random.uniform(-0.1, 0.1),
                'source': 'manufacturing'
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        df = df.sort_values('manufacturing_date')
        
        # Save to CSV
        df.to_csv('data/factory_output.csv', index=False)
        print(f"✅ Generated {num_records} factory output records")
        
        # Also create streaming version (continuous updates)
        self.create_streaming_updates(df)
        
        return df
    
    def generate_return_logs(self, production_df, recovery_rate=0.65):
        """
        Generate recovery logs based on production data
        """
        records = []
        
        # For each product, randomly decide if recovered
        for _, product in production_df.iterrows():
            # Decide if recovered (with some bias)
            if random.random() < recovery_rate:
                # Choose random recovery center
                center = random.choice(self.recovery_centers)
                
                # Recovery date (between manufacturing and now)
                mfg_date = datetime.fromtimestamp(product['manufacturing_date'])
                max_delay = min(30, (datetime.now() - mfg_date).days)
                delay_days = random.randint(1, max(1, max_delay))
                recovery_date = mfg_date + timedelta(days=delay_days)
                
                # Recovery weight (usually less due to losses)
                recovery_weight = product['weight_kg'] * random.uniform(0.7, 0.98)
                
                # Circular credit calculation (₹ per kg recovered)
                credit_rates = {
                    'plastic': 15,
                    'e_waste': 45,
                    'metal': 35,
                    'paper': 8,
                    'glass': 5,
                    'organic': 3
                }
                credit_rate = credit_rates.get(product['material_category'], 10)
                circular_credit = recovery_weight * credit_rate
                
                # Condition assessment
                conditions = ['excellent', 'good', 'damaged', 'end_of_life']
                weights = [0.2, 0.4, 0.3, 0.1]
                condition = random.choices(conditions, weights=weights)[0]
                
                record = {
                    'recovery_id': f"REC-{recovery_date.strftime('%Y%m%d')}-{random.randint(10000,99999)}",
                    'product_id': product['product_id'],
                    'recovery_center_id': center['id'],
                    'recovery_center_name': center['name'],
                    'recovery_date': recovery_date.timestamp(),
                    'material_type': product['material_type'],
                    'weight_recovered': round(recovery_weight, 2),
                    'condition': condition,
                    'recycling_method': random.choice(['mechanical', 'chemical', 'pyrolysis', 'composting']),
                    'recovered_by': f"Collector-{random.randint(1,100)}",
                    'circular_credit_amount': round(circular_credit, 2),
                    'gps_lat': 12.9716 + random.uniform(-0.5, 0.5),  # Rough Bengaluru area
                    'gps_lon': 77.5946 + random.uniform(-0.5, 0.5),
                    'verification_hash': hashlib.sha256(f"{product['product_id']}{recovery_date}".encode()).hexdigest()[:16]
                }
                records.append(record)
        
        df = pd.DataFrame(records)
        df = df.sort_values('recovery_date')
        
        # Save to CSV
        df.to_csv('data/return_logs.csv', index=False)
        print(f"✅ Generated {len(records)} recovery records ({(len(records)/len(production_df))*100:.1f}% recovery rate)")
        
        return df
    
    def create_streaming_updates(self, production_df):
        """
        Create streaming updates for live demo
        """
        # Take last 100 records as "new" streaming data
        streaming_df = production_df.tail(100).copy()
        
        # Update timestamps to be recent
        base_time = datetime.now() - timedelta(hours=24)
        for i, (idx, row) in enumerate(streaming_df.iterrows()):
            streaming_df.at[idx, 'manufacturing_date'] = (
                base_time + timedelta(minutes=i*10)
            ).timestamp()
        
        streaming_df.to_csv('data/live/new_products.csv', index=False)
        
        # Create Kafka-style JSONL stream
        with open('data/live/stream.jsonl', 'w') as f:
            for _, row in streaming_df.iterrows():
                f.write(json.dumps(row.to_dict()) + '\n')
        
        print("✅ Created streaming updates in data/live/")
    
    def generate_complete_dataset(self):
        """
        Generate complete mock dataset
        """
        print("📊 Generating EcoLoop Bharat mock data...")
        
        # Generate production data
        production_df = self.generate_factory_output(5000)
        
        # Generate recovery data with 65% recovery rate
        recovery_df = self.generate_return_logs(production_df, recovery_rate=0.65)
        
        # Create leakage hotspots (areas with poor recovery)
        hotspots = [
            {"city": "Delhi", "recovery_rate": 0.45, "alert": "Critical leakage in North Delhi"},
            {"city": "Mumbai", "recovery_rate": 0.58, "alert": "Moderate leakage in Dharavi"},
            {"city": "Bengaluru", "recovery_rate": 0.72, "alert": "Good recovery in Whitefield"},
        ]
        
        with open('data/hotspots.json', 'w') as f:
            json.dump(hotspots, f, indent=2)
        
        print("\n✅ Mock data generation complete!")
        print(f"📈 Production records: {len(production_df)}")
        print(f"♻️ Recovery records: {len(recovery_df)}")
        print(f"📊 Overall recovery rate: {(len(recovery_df)/len(production_df))*100:.1f}%")
        
        return production_df, recovery_df

if __name__ == "__main__":
    generator = MockDataGenerator()
    prod_df, rec_df = generator.generate_complete_dataset()
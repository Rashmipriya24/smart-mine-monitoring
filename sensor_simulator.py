import random
import time
import sqlite3
import datetime

print("🚀 Starting Sensor Simulator...")
print("=" * 40)

# Create database
conn = sqlite3.connect('rockfall.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY,
    sensor_id TEXT,
    timestamp TEXT,
    vibration REAL,
    displacement REAL,
    risk_score REAL
)
''')

print("✅ Database connected")

# Generate fake readings
try:
    for i in range(5):  # Sirf 5 readings
        sensor_id = f"sensor_{i+1}"
        vibration = random.uniform(0.1, 0.8)
        displacement = random.uniform(0.5, 5.0)
        risk_score = vibration * 0.7 + displacement * 0.03
        
        cursor.execute('''
            INSERT INTO readings 
            VALUES (NULL, ?, ?, ?, ?, ?)
        ''', (sensor_id, datetime.datetime.now().isoformat(), 
              vibration, displacement, risk_score))
        
        print(f"📊 Reading {i+1}: Sensor={sensor_id}, Vib={vibration:.2f}, Risk={risk_score:.2f}")
        time.sleep(1)
    
    conn.commit()
    print("✅ 5 readings saved to database")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()
    print("👋 Done!")
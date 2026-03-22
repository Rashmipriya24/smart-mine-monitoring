from fastapi import FastAPI
import sqlite3
import uvicorn

app = FastAPI(title="Rockfall Prediction API")

@app.get("/")
def home():
    return {
        "message": "Rockfall Prediction API",
        "endpoints": [
            "/sensors",
            "/readings",
            "/alerts",
            "/stats"
        ]
    }

@app.get("/sensors")
def get_sensors():
    """Get all sensors"""
    conn = sqlite3.connect('rockfall.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT sensor_id FROM readings")
    sensors = cursor.fetchall()
    conn.close()
    return {"sensors": [s[0] for s in sensors]}

@app.get("/readings")
def get_readings(limit: int = 10):
    """Get recent readings"""
    conn = sqlite3.connect('rockfall.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sensor_id, timestamp, vibration, displacement, risk_score 
        FROM readings 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (limit,))
    readings = cursor.fetchall()
    conn.close()
    
    return {
        "readings": [
            {
                "sensor_id": r[0],
                "timestamp": r[1],
                "vibration": r[2],
                "displacement": r[3],
                "risk_score": r[4]
            }
            for r in readings
        ]
    }

@app.get("/alerts")
def get_alerts(threshold: float = 0.5):
    """Get high risk readings"""
    conn = sqlite3.connect('rockfall.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sensor_id, timestamp, vibration, displacement, risk_score 
        FROM readings 
        WHERE risk_score > ?
        ORDER BY risk_score DESC
    """, (threshold,))
    alerts = cursor.fetchall()
    conn.close()
    
    return {
        "alerts": [
            {
                "sensor_id": a[0],
                "timestamp": a[1],
                "vibration": a[2],
                "displacement": a[3],
                "risk_score": a[4]
            }
            for a in alerts
        ]
    }

@app.get("/stats")
def get_stats():
    """Get database statistics"""
    conn = sqlite3.connect('rockfall.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM readings")
    total_readings = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(risk_score) FROM readings")
    avg_risk = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM readings WHERE risk_score > 0.5")
    high_risk = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_readings": total_readings,
        "average_risk": round(avg_risk, 3),
        "high_risk_alerts": high_risk,
        "timestamp": str(datetime.datetime.now())
    }

if __name__ == "__main__":
    print("🚀 Starting API server...")
    print("📡 http://localhost:8000")
    print("📚 http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()

# 1. CORS Setup (Crucial for Phase 5)
# This allows your future React dashboard to talk to this API without security errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Host the images! 
# This makes it so going to http://localhost:8000/evidence/violation_123.jpg shows the image
app.mount("/evidence", StaticFiles(directory="evidence"), name="evidence")

# 3. Create the Database Endpoint
@app.get("/api/incidents")
def get_incidents():
    # Connect to the database
    conn = sqlite3.connect('safesite.db')
    conn.row_factory = sqlite3.Row # This formats the data nicely into key/value pairs
    cursor = conn.cursor()
    
    # Fetch all records, putting the newest ones at the top
    cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # Return the data as a list of dictionaries (JSON)
    return [dict(row) for row in rows]
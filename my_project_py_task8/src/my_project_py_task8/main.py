from fastapi import FastAPI, HTTPException
from .models import CustomerRequest
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Customer Requests Service")

DATA_FILE = Path("customers.json")

@app.post("/customer/")
async def create_customer(request: CustomerRequest):
    try:
        record = request.dict()
        #record["created_at"] = datetime.utcnow().isoformat()
        record["birth_date"] = record["birth_date"].isoformat()

        if DATA_FILE.exists():
            with DATA_FILE.open("r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(record)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with DATA_FILE.open("w", encoding="utf-8") as f:
                json.dump([record], f, ensure_ascii=False, indent=4)

        return {"status": "success", "data": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
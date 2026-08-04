from motor.motor_asyncio import AsyncIOMotorClient
import yaml

# Load configuration
with open("app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# MongoDB connection settings
DATABASE_URI = config["database"]["uri"]
DATABASE_NAME = config["database"]["name"]

# Initialize MongoDB client
client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]

# Dependency for FastAPI
async def get_db():
    """Dependency to provide database access."""
    return db

# Example utility function for YOLO-specific queries
async def get_prediction_history(user_id: str):
    """Fetch all predictions made by a specific user."""
    predictions = await db["predictions"].find({"user_id": user_id}).to_list(100)
    return predictions
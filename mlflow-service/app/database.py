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

# Example utility function for MLFlow-specific logs
async def log_experiment_data(experiment_data: dict):
    """Log experiment data to the metrics_logs collection."""
    result = await db["metrics_logs"].insert_one(experiment_data)
    return str(result.inserted_id)

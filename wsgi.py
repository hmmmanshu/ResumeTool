import logging
from app import app, db

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting application...")
    
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully!")
    
    logger.info("Running Flask application...")
    app.run(debug=True)

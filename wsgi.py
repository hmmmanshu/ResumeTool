from app import app, db, logger

if __name__ == "__main__":
    logger.info("Starting application...")

    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully!")

    logger.info("Running Flask application...")
    app.run(debug=False)

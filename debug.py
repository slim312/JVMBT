from service import app

if __name__ == '__main__':
    app.run(debug=True)
    app.logger.info("Starting server (Debug=True)...")

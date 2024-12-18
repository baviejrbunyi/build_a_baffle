from backend import create_app  # Import the create_app function from the backend package

# Create an instance of the Flask app
app = create_app()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)  # Starts the Flask development server

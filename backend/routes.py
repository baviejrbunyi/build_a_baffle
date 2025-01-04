from flask import Flask, render_template, request, session #Make sure to import 'request'
import backend.baffle as Baffle
import json

# Define the routes and handling for POST requests
def init_routes(app):

    # Function to initialize the baffles in session
    def init_baffles_in_session():
        if 'baffles' not in session:
            session['baffles'] = []  # Initialize the session with an empty baffles list
    
    @app.route('/get_baffles', methods=['GET'])
    def get_baffles():
        # Get the list of baffles from the session
        baffles = session.get('baffles', [])
        return {"baffles": baffles}, 200

    @app.route('/', methods=['GET', 'POST'])
    def home():

        return render_template('LoginPage.html')  # Pass baffles to template
    
    @app.route('/signup')
    def signup():
        return render_template('SignupPage.html')
    
    @app.route('/login')
    def login():
        return render_template('LoginPage.html')
    
    @app.route('/profile')
    def profile():
        return render_template('ProfilePage.html')
    
    @app.route('/questions')
    def questions():
        return render_template('QuestionsPage.html')
    
    @app.route('/cards', methods=['GET', 'POST'])
    def cards():
        init_baffles_in_session()  # Initialize the session with an empty baffles list
        baffles = session.get('baffles', [])
        
        if request.method == 'POST':
            # Get the questions and answers as a JSON string
            questions_and_answers_json = request.form.get('questions_and_answers')
            
            # Print the raw JSON string to inspect its structure
            print("Raw received JSON:", questions_and_answers_json)
            
            # Parse the JSON string into a Python object (list of dictionaries)
            try:
                questions_and_answers = json.loads(questions_and_answers_json)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                return "There was an error processing your submission.", 400
            
            # Print the parsed questions and answers to confirm structure
            print("Parsed questions and answers:")
            for qa in questions_and_answers:
                print(f"Question: {qa.get('question')}, Answer: {qa.get('answer')}")
            
            # Example usage: Combine all answers to form a topic or use for processing
            topic = " ".join([qa['answer'] for qa in questions_and_answers if qa.get('answer')])
            print(f"Generated topic: {topic}")
            
            # Example: Use the answers to generate baffles
            baffles = Baffle.create_baffles(questions_and_answers_json, 6)
            
            # Store generated baffles in session
            session['baffles'] = [b.__dict__ for b in baffles]
            return render_template('CardPage.html', baffles=baffles)
        
        return render_template('CardPage.html', baffles=baffles)

    @app.route('/regenerate_baffle', methods=['POST'])
    def regenerate_baffle():
        field = request.json.get('field')  # Get the field of the current baffle
        card_number = request.json.get('card_number')  # Get the card number
        
        if not field or not card_number:
            return {"error": "Field and card number are required to regenerate baffle"}, 400
        
        # Convert card_number to an integer
        try:
            card_number = int(card_number)
        except ValueError:
            return {"error": "Invalid card number"}, 400
        
        # Generate a new baffle based on the field
        new_baffle = Baffle.create_baffle_with_field(field)
        if new_baffle:
            # Update the list of baffles in the session
            baffles = session.get('baffles', [])
            
            # Check if the card_number is valid (1-based index)
            if 1 <= card_number <= len(baffles):
                # Replace the old baffle with the new one at the given index (card_number - 1 for 0-based index)
                baffles[card_number - 1] = new_baffle.__dict__
                session['baffles'] = baffles  # Update the session with the modified list of baffles
                
                # Return the new baffle details
                return {
                    "title": new_baffle.title,
                    "field": new_baffle.field,
                    "gaps": new_baffle.gaps,
                    "recommendations": new_baffle.recommendations,
                    "updated_baffles": baffles  # Return the updated list of baffles
                }, 200
            else:
                return {"error": "Invalid card number"}, 400
        else:
            return {"error": "Failed to generate baffle"}, 500

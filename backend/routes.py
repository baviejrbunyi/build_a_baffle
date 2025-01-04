from flask import Flask, render_template, request  # Make sure to import 'request'
import backend.baffle as Baffle
import json

# Define the routes and handling for POST requests
def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        baffles = None
        if request.method == 'POST':
            topic = request.form.get('topic')
            output_num = request.form.get('output_num')
            if topic:
                # Generate baffles based on the input topic
                baffles = Baffle.create_baffles(topic, output_num)
        return render_template('LoginPage.html')
    
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

            return render_template('CardPage.html', baffles=baffles)
        
        return render_template('CardPage.html', baffles=[])

    @app.route('/regenerate_baffle', methods=['POST'])
    def regenerate_baffle():
        field = request.json.get('field')  # Get the field of the current baffle
        if not field:
            return {"error": "Field is required to regenerate baffle"}, 400

        # Generate a new baffle based on the field
        new_baffle = Baffle.create_baffle_with_field(field)
        if new_baffle:
            return {
                "title": new_baffle.title,
                "field": new_baffle.field,
                "gaps": new_baffle.gaps,
                "recommendations": new_baffle.recommendations
            }, 200
        else:
            return {"error": "Failed to generate baffle"}, 500
from flask import Flask, render_template, request  # Make sure to import 'request'
import backend.baffle as Baffle

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
            answer1 = request.form.get('answer1')
            answer2 = request.form.get('answer2')
            answer3 = request.form.get('answer3')
            
            # Combine or process answers as needed
            answers = [answer1, answer2, answer3]
            print("Received answers:", answers)
            
            # Example: Use the answers to generate baffles
            topic = " ".join(answers)  # Combine answers as a topic (example usage)
            baffles = Baffle.create_baffles(topic, 6)
            return render_template('CardPage.html', baffles=baffles)
        
        return render_template('CardPage.html', baffles=[])

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
        return render_template('index.html', baffles=baffles)
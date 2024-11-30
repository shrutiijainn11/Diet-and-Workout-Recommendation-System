from flask import Flask, render_template, request
import os
import google.generativeai as genai

# Set your API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyB6MS35tfH3t_tqhkOs5leWsfQyOqETBXE"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

app = Flask(__name__)

# Initialize model
model = genai.GenerativeModel('models/gemini-pro')


# Custom function
def generate_recommendation(dietary_preferences, fitness_goals, lifestyle_factors, dietary_restrictions, health_conditions, user_query, age, weight, height, goalWeight, dietPreference):
    prompt = f"""Can you suggest a comprehensive plan that includes diet and workout options for better fitness for this user:
            dietary preferences: {dietary_preferences},
            fitness goals: {fitness_goals},
            lifestyle factors: {lifestyle_factors},
            dietary restrictions: {dietary_restrictions},
            health conditions: {health_conditions},
            user query: {user_query},
            age: {age},
            weight: {weight},
            height: {height},
            goalWeight: {goalWeight},
            dietPreference: {dietPreference},

            Based on the above user's dietary_preferences, fitness_goals, lifestyle_factors, dietary_restrictions, health_conditions, user_query, age, weight, height, goalWeight, dietPreference

            Diet recommendations: RETURN LIST
            5 specific diet types suited to their preferences and goals
            Workout options: RETURN LIST
            5 workout options that align with their fitness level and goals
            Meal suggestions: RETURN LIST
            5 breakfast ideas
            5 lunch ideas
            5 dinner options

            Additional recommendation: RETURN LIST
            Any useful tips, snacks, supplements or hydration tips tailored to their profile.
             """
    results = model.generate_content(prompt).text
    return results


@app.route("/")
def index():
    # Provide an empty `recommendations` to avoid Jinja errors
    return render_template('index.html', recommendations=None)


@app.route("/recommendations", methods=['POST'])
def recommendations():
    if request.method == 'POST':
        # Collect data from form
        dietary_preferences = request.form['dietary_preferences']
        fitness_goals = request.form['fitness_goals']
        lifestyle_factors = request.form['lifestyle_factors']
        dietary_restrictions = request.form['dietary_restrictions']
        health_conditions = request.form['health_conditions']
        user_query = request.form['user_query']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        goalWeight = request.form['goalWeight']
        dietPreference = request.form['dietPreference']

        # Generate recommendations
        recommendations_text = generate_recommendation(
            dietary_preferences, fitness_goals, lifestyle_factors,
            dietary_restrictions, health_conditions, user_query,
            age, weight, height, goalWeight, dietPreference
        )

        recommendations = {
            "diet_types": [],
            "workout": [],
            "meal": [],
            "additional": []
        }

        # Split and map responses
        current_section = None
        for line in recommendations_text.splitlines():
            if "Diet Recommendations" in line:
                current_section = 'diet_types'
            elif "Workout Options" in line:
                current_section = 'workout'
            elif "Meal Suggestions" in line:
                current_section = 'meal'
            elif "Additional Recommendations" in line:
                current_section = 'additional'
            elif line.strip() and current_section:
                recommendations[current_section].append(line.strip())

        return render_template('index.html', recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)

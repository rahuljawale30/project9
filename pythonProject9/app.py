from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager,create_access_token, get_jwt_identity, jwt_required
from flask_pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)



client = MongoClient("mongodb://localhost:27017/")
db = client['ashwini']
historical_collection = db['historials']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submission', methods=['GET','POST'])
def submission():
    if request.method == 'POST':
        task_name = request.form['task_name']
        complexity = request.form['complexity']
        size = request.form['size']
        task_type = request.form['task_type']
        estimated_effort_hours = int(request.form['estimated_effort_hours'])
        confidence_level = request.form['confidence_level']
        estimated_range_hours = request.form['estimated_range_hours']

        new_data = {
            "task_name": task_name,
            "complexity": complexity,
            "size": size,
            "task_type": task_type,
            "estimated_effort_hours": estimated_effort_hours,
            "confidence_level": confidence_level,
            "estimated_range_hours": estimated_range_hours
        }

        historical_collection.insert_one(new_data)
        return redirect(url_for('view_historical_data'))

    return render_template('create.html')


@app.route('/view_historical_data')
def view_historical_data():
    users = list(historical_collection.find())
    return render_template('view_data.html', users=users)

@app.route('/update_historical_data/<int:task_id>', methods=['POST'])
@jwt_required
def update_historical_data(task_id):
    # Extract updated data from the request
    updated_data = request.json

    # Update the record in the database
    result = historical_collection.update_one(
        {"task_id": task_id},
        {"$set": updated_data}
    )

    if result.modified_count > 0:
        message = "Record updated successfully"
    else:
        message = "No record updated"

    return jsonify({"message": message})
print("hello")


if __name__ == '__main__':
    app.run(debug=True, port=5020)
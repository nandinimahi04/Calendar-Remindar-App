from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import calendar
from flask_migrate import Migrate
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Flask app
app = Flask(__name__)
CORS(app) 
user_email = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SECRET_KEY'] = 'mahi0405'  # Replace with a secure key in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Reminder Model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Reminder {self.title} on {self.date}>"

# Helper Functions
def get_current_month_data():
    """Helper function to get current month's calendar and metadata."""
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_month_name = today.strftime('%B')
    month_cal = calendar.monthcalendar(current_year, current_month)
    return current_year, current_month, current_month_name, month_cal

# Routes
@app.route('/')
def index():
    """Homepage displaying the calendar and reminders."""
    current_year, current_month, current_month_name, month_cal = get_current_month_data()
    reminders = Reminder.query.all()
    reminder_dates = [reminder.date for reminder in reminders]

    return render_template(
        'calendar.html',
        calendar=month_cal,
        reminders=reminders,
        reminder_dates=reminder_dates,
        current_year=current_year,
        current_month=current_month,
        current_month_name=current_month_name
    )

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    """Route to add a new reminder."""
    date = request.form.get('date')
    title = request.form.get('title')
    description = request.form.get('description')

    if not date or not title:
        flash("Date and title are required.", "error")
        return redirect(url_for('index'))

    try:
        new_reminder = Reminder(date=date, title=title, description=description)
        db.session.add(new_reminder)
        db.session.commit()
        flash("Reminder added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    """Route to fetch reminders as JSON."""
    reminders = Reminder.query.all()  # Fetch all reminders from the database
    reminders_list = []
    for reminder in reminders:
        reminders_list.append({
            "id": reminder.id,
            "date": reminder.date,
            "title": reminder.title,
            "description": reminder.description
        })
    return jsonify({"reminders": reminders_list})  # Return reminders as JSON

@app.route('/delete_reminder/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    """Route to delete a reminder."""
    reminder = Reminder.query.get(id)
    if reminder:
        try:
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({"success": True, "message": "Reminder deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"success": False, "message": "Reminder not found"}), 404
    


# Email sending function
def send_email(to_email, subject, body):
    from_email = "nandinimahi0404@gmail.com" 
    from_password = "M@hi0404"  
    smtp_server = "smtp.example.com"  
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, 587)  # For Gmail, the port is 587
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    reminder_date = request.form['date']
    reminder_title = request.form['title']
    reminder_description = request.form['description']

    # After setting the reminder in your database, send an email
    subject = f"Reminder for {reminder_title}"
    body = f"Don't forget your reminder for {reminder_title} on {reminder_date}. Description: {reminder_description}"

    send_email(user_email, subject, body)  # Send the email to the logged-in user

    return jsonify({"message": "Reminder set and email sent!"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(debug=True)

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired
import pickle
import numpy as np
from sklearn 

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

# Load the pickle file with error handling
try:
    with open('EDA_wine_pkl_file', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: Pickle file not found!")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class PredictionForm(FlaskForm):
    # Replace with your actual features
    alcohol = IntegerField('alcohol', validators=[DataRequired()])
    pH = FloatField('pH Level', validators=[DataRequired(), NumberRange(min=2.0, max=4.5)])
    sulphates = FloatField('Sulphates', validators=[DataRequired(), NumberRange(min=0.0, max=2.0)])
    # pH = FloatField('pH level', validators=[DataRequired()])
    # sulphates = FloatField('sulphates', validators=[DataRequired()])
    submit = SubmitField('Predict Price')
 

# Route to pages 
@app.route("/")
def index():
    return render_template("home.html")

# Works -- about the author page
@app.route("/about")
def about():
    return render_template("about.html")

# Works -- view profile 
@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = PredictionForm()
    prediction = None
    
    if upload_model is None:
        prediction = "Error: Model could not be loaded. Check server logs."
    elif form.validate_on_submit():
        try:
            # Create input array with correct shape: (1, 3)
            input_features = np.array([[ 
                float(form.alcohol.data),
                float(form.pH.data),
                float(form.sulphates.data)
            ]])

            # Make prediction
            raw_prediction = model.predict(input_features)[0]
            
            # Most wine quality models predict quality (integer 3–8) or class (0/1)
            if raw_prediction.is_integer():
                quality = float(raw_prediction)
                prediction = f"Predicted Wine Quality: <strong>{quality}/10</strong> ⭐"
                if quality >= 7:
                    prediction += " — Excellent wine!"
                elif quality >= 6:
                    prediction += " — Good wine."
                else:
                    prediction += " — Average or below."
            else:
                # If it's probability (e.g., Logistic Regression)
                prob = raw_prediction
                quality_class = "Good" if prob > 0.5 else "Average/Poor"
                confidence = prob if prob > 0.5 else 1 - prob
                prediction = f"{quality_class} Wine (confidence: {confidence:.1%})"

        except Exception as e:
            prediction = f"Prediction error: {str(e)}"
    
    return render_template("predict.html", form=form, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

#-----------------------------------------------
# Uncomment 
# from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# import pickle
# import numpy


# app = Flask(__name__)

# # load your picke file here 
# app.config["SECRET_KEY"] = "your_secret_key"
# upload_model = pickle.load(open('EDA_churn_pkl_file','rb'))


# # Route to pages 
# @app.route("/")
# def index():
#     return render_template("home.html")

##---------------------------------------------





# @app.route("/member", methods=["GET", "POST"])
# def member():
#     name = False
#     email = False
#     form = MemberInfo()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         form.name.data = ""
#     return render_template("member.html", name=name, email=email, form=form)


# @app.route("/member/<name>")
# def member(name):
#     return render_template("member.html", name=name)

## Uncomment 
## -----------------------------------------------
# # Works -- about the auther page
# @app.route("/about")
# def about():
#     return render_template("about.html")


# # Works -- view profile 
# @app.route("/profile")
# def profile():
#     return render_template("profile.html")

## --------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

# def main():
#     print("Hello from basic!")


# if __name__ == "__main__":
#     main(debug=True)




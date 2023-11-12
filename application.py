from flask import Flask, request, render_template

from mlengine.models.predict import Prediction, CustomData

application = Flask(__name__)

app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template(('prediction.html'))
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=int(request.form.get('reading_score')),
            writing_score=int(request.form.get('writing_score')),
        )

        pred_df = data.get_data_as_data_frame()
        prediction = Prediction()
        results = prediction.predict(pred_df)

        return render_template('prediction.html', results=results[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0")

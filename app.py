from flask import Flask, request
from flasgger import Swagger
import joblib
import pickle

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/', methods=['POST'])
def predict():
    """
    Make a prediction
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                msg:
                    type: string
                    example: This is an example msg.
    responses:
      200:
        description: Some result
    """
    # get the message to be classified from the request body
    review = request.get_json().get('msg')
    # load the model
    classifier = joblib.load('c2_Classifier_Sentiment_Model')
    cv = pickle.load(open('c1_BoW_Sentiment_Model.pkl', "rb"))
    # preprocess the input
    processed_input = cv.transform([review]).toarray()[0]
    # make a prediction
    sentiment = classifier.predict([processed_input])[0]
    prediction_map = {
        0: "negative",
        1: "positive"
    }
    return {
        "review": review,
        "prediction": f"{prediction_map[sentiment]}"
    }


app.run(host="0.0.0.0", port=8080, debug=True)

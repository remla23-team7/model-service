FROM ghcr.io/remla23-team7/model-training:0.0.1 AS model-training

# Start with a base Python image
FROM python:3.8-slim
WORKDIR /root

# Copy the trained models from the model-training Docker image
COPY --from=model-training /root/c2_Classifier_Sentiment_Model /root/
COPY --from=model-training /root/c1_BoW_Sentiment_Model.pkl /root/

COPY requirements.txt /root/
RUN pip install -r requirements.txt

COPY app.py /root/

ENTRYPOINT ["python"]
CMD ["app.py"]
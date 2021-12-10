from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers_api.model import Model, get_model
import time

# API View here
class AnalysisAPI(APIView):
    def get(self, request):
        return Response({"status": "success",
                         "data": "Success Request"},
                        status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        request_data = request.data
        analyze_text = request_data['text']

        t1= time.time()

        model = Model()
        sentiment, confidence, probabilities = model.predict(analyze_text)

        print(sentiment,confidence,probabilities)
        t2=time.time()
        print(t2-t1)
        return Response({"status": "success",
                         "given_text": analyze_text,
                         "prediction": {
                             "sentiment": sentiment,
                             "confidence": confidence,
                             "probabilities": probabilities
                         }},
                        status=status.HTTP_200_OK)

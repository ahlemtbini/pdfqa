
from django.shortcuts import render, HttpResponse
from .utils import pdf_to_chunks
from .vector_store import VectorStore
from django.views.decorators.csrf import csrf_exempt
import json


vector_store = VectorStore()
@csrf_exempt
def train(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pdfs')
        for file in files:
            chunks = pdf_to_chunks(file)
            vector_store.add_chunks(chunks)
        return HttpResponse("Training completed")
    return HttpResponse("Send PDF files")
@csrf_exempt
def question(request):
    if request.method == 'POST':
        query = request.POST.get("question")
        response = vector_store.retrieve(query)
        # Convert response to JSON
        response_json = json.dumps(response)
        return HttpResponse(response_json, content_type='application/json')
    return HttpResponse("Send a question")

# qa/vector_store.py

from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import numpy as np
from .models import DocumentVector

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        # Vectors and texts now stored in database
        self.nn = None

    def add_chunks(self, chunks):
        if not chunks:
            return

        vectors = self.model.encode(chunks)

        # Store vectors and texts in the database
        for text, vector in zip(chunks, vectors):
            DocumentVector.objects.create(text=text, vector=vector.tolist())

        # Initialize NearestNeighbors model after adding vectors
        all_vectors = np.array([doc.vector for doc in DocumentVector.objects.all()])
        if len(all_vectors) > 0:
            self.nn = NearestNeighbors(n_neighbors=5).fit(all_vectors)

    def retrieve(self, query):
        if not self.nn:
            return [("No trained model available", 0)]

        q_vector = self.model.encode([query])[0]
        all_docs = DocumentVector.objects.all()
        print(f"documentss: {all_docs}")

        all_vectors = np.array([doc.vector for doc in all_docs])
        all_texts = [doc.text for doc in all_docs]

        # Re-initialize NearestNeighbors with all_vectors
        self.nn = NearestNeighbors(n_neighbors=5).fit(all_vectors)
        distances, indices = self.nn.kneighbors([q_vector])
        print(f"indices: {indices}")
        print(f"distances: {distances}")
        # Retrieve relevant texts
        results = []
        print(f"text: {all_texts[indices[0][0]]}")
        for i in indices[0]:
            if i < len(all_texts):
                print(f"nb: {i}")
                results.append((all_texts[i]))
            else:
                print(f"Index {i} is out of bounds")
        return results

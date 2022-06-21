import json
import threading

from flask import Flask, request

from my_data_store.main import InsertRecord
from my_data_store.settings import Settings

sem = threading.Semaphore()

app = Flask(__name__)


@app.route('/query-example')
def query_example():
    return 'Query String Example'


@app.route('/form-example')
def form_example():
    return 'Form Data Example'


@app.route('/insert', methods=['POST'])
def insert_data():
    request_data = request.get_json()
    # data = CustomDataStructure(**request_data)

    sem.acquire()
    storage = InsertRecord(data=request_data, file_format=Settings.FORMAT, destination=Settings.DESTINATION)
    storage.save()
    sem.release()

    return 'data insertion was successful'


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

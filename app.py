from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

##connect to Mongodb
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbmypetdiary
# client = MongoClient('mongodb:address', 27017)

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})


##save post
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    contents_receive = request.form['contents_give']

    file = request.files['file_give']
    # to remove extention
    extention = file.filename.split('.')[-1]
    today = datetime.now()
    # convert datetime to string
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}'
    date = today.strftime('%Y. %m. %d')

    save_to = f'static/{filename}.{extention}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'contents': contents_receive,
        'file': f'{filename}.{extention}',
        'date': f'{date}'
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': 'Save completed'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
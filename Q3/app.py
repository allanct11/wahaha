from flask import Flask, redirect, request
import os
import logging
import uuid
import json
import re
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from sqlalchemy_utils import create_database, database_exists

schema = {
    'type': 'object',
    'properties': {
        'url': {'type': 'string'}
    },
    'required': ['url']
}
schema_id = {
    'type': 'object',
    'properties': {
        'url': {'type': 'string'}
    },
    'required': ['url']
}

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(
                    convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


app = Flask(__name__)
logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# url = f'postgresql+psycopg2://appseed:appseed@10.1.100.220:5432/Redirect'
url = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
    'root', 'mypass', 'db', '3306', 'Redirect')
if not database_exists(url):
    create_database(url)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Url(db.Model):
    __tablename__ = "Url"
    id = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(80), nullable=False)

    def __init__(self, id, url):
        self.id = id
        self.url = url

    @property
    def json(self):
        return to_json(self, self.__class__)


db.create_all()
db.session.commit()


@app.route('/newurl', methods=['POST'])
@expects_json(schema)
def new():
    content = request.json
    temp = content.keys()
    expected_f = {'url'}
    list_extra_f = [ele for ele in temp if ele not in expected_f]
    if len(list_extra_f) != 0:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    try:
        content = request.json
        url_uuid = uuid.uuid4().hex[:9]
        content['shortenUrl'] = "https://shortenurl.org/"+url_uuid
        db.session.add(Url(url_uuid, content['url']))
        db.session.commit()
        return content, 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}


@ app.route('/<uri>', methods=['GET'])
def response(uri):
    x = re.findall("[a-zA-Z0-9]{9}", uri)
    if len(x)!= 1:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    if x[0]!=uri:
        return json.dumps({'status': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    try:
        exists = db.session.query(db.session.query(Url).filter_by(id=uri).exists()).scalar()
        logger.info(exists)
        if exists:
            u_url = db.session.query(Url).filter_by(id=uri).one()
            return redirect(u_url.url, code=304)
        else:
            return json.dumps({'status': 'Not Found'}), 404, {'ContentType': 'application/json'}
    except:
        return json.dumps({'status': 'Not Found'}), 404, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

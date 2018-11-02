import sys
from io import BytesIO
from flask import Flask,request,render_template,jsonify
import pymysql
import json
from flask_bootstrap import Bootstrap
from flask_cors import CORS

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = pymysql.connect("localhost","webcourse","M10709311","web" )

cursor = db.cursor()
col_name = []
cmd = 'SHOW COLUMNS FROM book'
cursor.execute(cmd)
result = cursor.fetchall()
i = 0
for col in result:
    col_name.append(col[0])
    i += 1
@app.route('/')
def index():
    ret = render_template('search.html')
    return ret
@app.route('/api/books/', methods=['GET'])
@app.route('/api/books',methods=['GET'])
def showBooks():
    # parse all books in database
    # and return results to front end
    cmd = 'SELECT * FROM book'
    cursor.execute(cmd)
    ret = cursor.fetchall()
    _json = []    
    data = []
    _json.append({"error":"false"})
    _json.append({"message":"M10709311"})
    for row in ret:
        content = {}
        for i in range(6):
            content.update({'{}'.format(col_name[i]) : '{}'.format(row[i])})
        data.append(content)
    _json.append({"data":data})
    #print(_json)
    return json.dumps(_json)    
@app.route('/api/books/<int:id>', methods=['GET'])
def showBook(id):
    # SELECT ID $id FROM books
    # return the result to front end
    cmd = "SELECT * FROM book where id = '" + str(id) + "'"
    cursor.execute(cmd)
    ret = cursor.fetchone()
    print(ret)
    _json = []
    content = {}
    if ret is None :
        _json.append({"error":"true"})
        _json.append({"message":"M10709311"})
        _json.append({"data":[""]})

    else:
        for i in range(6):
            content.update({'{}'.format(col_name[i]) : '{}'.format(ret[i])})
        _json.append({"error":"false"})
        _json.append({"message":"M10709311"})
        _json.append({"data":content})
    print(_json)
    return json.dumps(_json)

@app.route('/robots.txt')
def robots():
    robots_file = render_template('robots.txt')
    return robots_file
# listening 0.0.0.0
# in local port 8080

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)




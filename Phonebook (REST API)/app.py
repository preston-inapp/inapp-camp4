import pyodbc
from flask import jsonify, Flask, request

app = Flask(__name__)

pb = []

connString = 'Driver={SQL Server};Server=DESKTOP-DH4N9T0\SQLEXPRESS01;Database=inapp;Trusted_Connection=yes;'
conn = pyodbc.connect(connString)

def init():
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM phonebook")
    for contact in cursor:
        _contact = dict()
        _contact.update({"name":contact[0]})
        _contact.update({"phno":contact[1]})
        pb.append(_contact)
    conn.close()

def commit():
    conn = pyodbc.connect(connString)
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE phonebook")

    for i in pb:
        cursor.execute("INSERT INTO {} (name, phno) VALUES ('{}', '{}')".format("phonebook", i['name'], i['phno']))
    print("Committed edits")
    conn.commit()
    conn.close()

@app.route('/contacts', methods=["GET"])
def listContacts():
    return jsonify(pb)


@app.route('/contacts/name/<name>', methods=['GET'])
def searchByName(name):
    for i in pb:
        if i['name'] == name:
            return jsonify({"name":i['name'],"phno":i['phno']}), 200


@app.route('/contacts/name/<phno>', methods=[ 'GET'])
def searchByNumber(phno):
    for i in pb:
        if i['phno'] == phno:
            return jsonify({"name":i['name'],"phno":i['phno']}), 200


@app.route('/contacts', methods=['POST'])
def addContact():
    name = request.json['name']
    phno = request.json['phno']
    pb.append({"name":name,"phno":phno})
    commit()
    return jsonify({"name":name,"phno":phno}), 200


@app.route('/contacts', methods=['PATCH'])
def updateContact():
    name = request.json['name']
    for i in pb:
        if i['name'] == name:
            i['phno'] = request.json['phno']
            commit()
            return jsonify({"name":i['name'],"phno":i['phno']}), 200



@app.route('/contacts', methods=['DELETE'])
def deleteContact():
    name = request.json['name']
    for i in pb:
        if i['name'] == name:
            pb.remove(i)
            commit()
            return jsonify({"name":i['name'],"phno":i['phno']}), 200

if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", debug=True) 

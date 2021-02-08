from flask import Flask, request, jsonify 
from datetime import datetime

app = Flask(__name__)

User = {}


counter = 0
Temp = []

@app.route('/profile')
def profile_get():
    global User
    Success = {
        "success" :True,
        "data" : User
    }
    return jsonify(Success)

@app.route('/profile', methods = ['POST'])
def profile_post():

     now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
   
    UData = request.json
    #do the validation 
    if len(UData) > 0:
        global User
        User = UData

        UData["last_updated"] = dt
        Success = {
            "successs":True,
            "data": UData
        }
        return jsonify(Success)


@app.route('/profile', methods = ["PATCH"])
def profile_patch():
    global User 

     now = datetime.now()code
    dt = now.strftime("%d/%m/%Y %H:%M:%S")

    UData = request.json   

    if len(User) > 0:
        User = UData
     
        UData["last_updated"] = dt
        Success = {
        "successs":True,
        "data": UData
        }            
        return jsonify(Success)

 
@app.route("/data")
def data_get():
    return jsonify(Temp)

@app.route("/data", methods = ["POST"])
def data_post():
    global counter
    Tnk = request.json
    counter+=1
    Tnk["id"] = str(counter)
    Temp.append(Tnk)
    return jsonify(Tnk)

@app.route('/data/<int:id>', methods = ["PATCH"])
def data_patch(id):
    patch = request.json
    found = False
    for SystemDataFiles in Temp:
        if SystemDataFiles["id"] == str(id):
            found = True 
            SystemDataFiles["location"] = patch["location"]
            SystemDataFiles["lat"] = patch["lat"]
            SystemDataFiles["long"] = patch["long"]
            SystemDataFiles["percentage_full"] = patch["percentage_full"]
       
            break 
    if found == False:
        
        return redirect(url_for("data_get"))
    return jsonify(Temp[id-1])

@app.route('/data/<int:id>', methods = ["DELETE"])
def data_delete(id):
    Temp.remove(Temp[id-1])
    Success = { "success":True,}
    return jsonify(Success)


if __name__ == '__main__':
    app.run(debug=True, port = 3000)
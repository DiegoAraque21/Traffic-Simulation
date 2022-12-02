from flask import Flask, request, jsonify
from model import RandomModel
from agents.Car import Car
from agents.Traffic_Light import Traffic_Light

# Size of the board:
randomModel = None
currentStep = 0
app = Flask("Traffic Simulation")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel

    if request.method == 'POST':
        currentStep = 0

        # Create model
        randomModel = RandomModel()

        return jsonify({"message": "Parameters recieved, model initiated."})

@app.route('/getCars', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = []
        for (w, x, z) in randomModel.grid.coord_iter():
            for agent in w:
                if isinstance(agent, Car):
                    agentPositions.append({
                        "id": str(agent.unique_id), 
                        "x": x,
                        "y":0, 
                        "z":z, 
                        "arrived": agent.arrived
                    })
        
        return jsonify({'positions':agentPositions, "activeCars": randomModel.active_cars})

@app.route('/getTrafficLights', methods=['GET'])
def getTrafficLights():
    global randomModel

    if request.method == 'GET':
        agentPositions = []
        for (w, x, z) in randomModel.grid.coord_iter():
            for agent in w:
                if isinstance(agent, Traffic_Light):
                    agentPositions.append({
                        "id": str(agent.unique_id), 
                        "x": x, 
                        "y": 0, 
                        "z":z, 
                        "green": agent.state, 
                        "direction": agent.direction
                    })

        return jsonify({'positions': agentPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
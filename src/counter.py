from flask import Flask

from src import status

app = Flask(__name__)

COUNTERS = {}


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    # 1. Create a route for method PUT on endpoint /counters/<name>.
    app.logger.info(f"Request to update counter: {name}")
    # 2. Create a function to implement that route.
    global COUNTERS
    if name in COUNTERS:
        # 3. Increment the counter by 1.
        COUNTERS[name] += 1
        # 4. Return the new counter and a 200_OK return code.
        return {name: COUNTERS[name]}, status.HTTP_200_OK
    return {"Message": f"Counter {name} does not exists"}, status.HTTP_404_NOT_FOUND


@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    app.logger.info(f"Request to read counter: {name}")
    global COUNTERS
    # return the count and 200_OK return code
    if name in COUNTERS:
        return {name: COUNTERS[name]}, status.HTTP_200_OK
    return {"Message": f"Counter {name} does not exists"}, status.HTTP_404_NOT_FOUND


@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS
    # Delete the count and 204_NO_CONTENT
    if name in COUNTERS:
        del COUNTERS[name]
        return {"Message": f"Counter {name} has been deleted"},  status.HTTP_204_NO_CONTENT

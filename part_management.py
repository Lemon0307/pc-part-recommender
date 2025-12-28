from flask import request, jsonify, Blueprint
from db import get_driver
import uuid

part_management = Blueprint('part_management', __name__)

valid_parts = {"cpu", "gpu", "ram", "motherboard", "storage", "power supply", "cpu cooler", "chassis", "accessories", "monitors"}
comptatibility = {
    "cpu": ["socket", ]
}

@part_management.route('/add_part', methods=['POST'])
def add_part():
    driver = get_driver()

    #get data from request
    data = request.json
    part_type = next(iter(data))
    part_id = str(uuid.uuid4())

    # checks if part type is valid
    if part_type.lower() not in valid_parts:
        return jsonify({"error": "Invalid part type"}), 400
    
    properties = data[part_type]
    properties['part_id'] = part_id
        
    #builds and executes query
    query = f"CREATE (p:{part_type} $props)"
    driver.execute_query(query, props=properties)

    return jsonify({"message": f"{part_type} added successfully"}), 201

@part_management.route('/create_empty_order', methods=['POST'])
def create_empty_order():
    driver = get_driver()
    order_id = str(uuid.uuid4())

    query = "CREATE (o:Order {status: 'pending', created_at: datetime(), order_id: $order_id}) RETURN $order_id AS order_id"
    result = driver.execute_query(query, order_id=order_id)

    return jsonify({"order_id": result.records[0]["order_id"]}), 201

@part_management.route('/add_part_to_order', methods=['POST'])
def add_part_to_order():
    driver = get_driver()
    
    #get data from request
    data = request.json
    part_id = data.get("part_id")
    order_id = data.get("order_id")
    quantity = data.get("quantity")
    
    # checks if parts and order exist
    check_part_exists = "MATCH (p {part_id: $part_id}) RETURN p"
    part_result = driver.execute_query(check_part_exists, part_id=part_id)
    check_order_exists = "MATCH (o:Order {order_id: $order_id}) RETURN o"
    order_result = driver.execute_query(check_order_exists, order_id=order_id)  

    if not order_result.records[0] and not part_result.records[0]:
        return jsonify({"error": "Part or order does not exist"}), 404
    
    # checks if part is already in order
    check_if_already_in_order = driver.execute_query("""
    MATCH (o:Order {order_id: $order_id})-[r:CONTAINS]->(p {part_id: $part_id})
    RETURN r 
    """, order_id=order_id, part_id=part_id)

    if check_if_already_in_order.records[0]:
        return jsonify({"error": "Part already in order"}), 400

    #builds and executes query
    query = """
    MATCH (p {part_id: $part_id}), (o:Order {order_id: $order_id})
    CREATE (o)-[:CONTAINS {quantity: $quantity}]->(p)
    """

    driver.execute_query(query, part_id=part_id, order_id=order_id, quantity=quantity)
    return jsonify({"message": "Part added to order successfully"}), 200

# @part_management.route('/testing', methods=['POST'])
# def testing():
#     driver = get_driver()
#     data = request.json
#     part_type = next(iter(data))
#     properties = data[part_type]

#     #check if other parts have some of the same properties as this one

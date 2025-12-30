from flask import request, jsonify, Blueprint
from db import get_driver
import uuid

part_management = Blueprint('part_management', __name__)

valid_parts = ["CPU", "GPU", "RAM", "MOTHERBOARD", "STORAGE", "POWER SUPPLY", "CPU COOLER", "CHASSIS", "ACCESSORIES", "MONITORS"]
compatibility = {
    "CPU": ["socket"],
    "MOTHERBOARD": ["socket", "memory_type", "form_factor", "chipset"],
    "GPU": ["length"],
    "RAM": ["memory_type", "capacity"],
    "POWER SUPPLY": ["wattage", "form_factor"],
    "CHASSIS": ["form_factor", "max_gpu_length", "max_cpu_cooler_height"]
}

@part_management.route('/add_part', methods=['POST'])
def add_part():
    driver = get_driver()

    #get data from request
    data = request.json
    part_type = next(iter(data))
    properties = data[part_type]
    part_type = part_type.upper()
    part_id = str(uuid.uuid4())

    # checks if part type is valid
    if part_type not in valid_parts:
        return jsonify({"error": "Invalid part type"}), 400
    
    properties['part_id'] = part_id
        
    #builds and executes query
    query = f"CREATE (p:{part_type} $props)"
    driver.execute_query(query, props=properties)

    # check for compatibility with other parts
    conditions_to_check_for_compatibility = ""
    for condition in compatibility[part_type]:
        conditions_to_check_for_compatibility += f"p.{condition} = n.{condition} OR "

    conditions_to_check_for_compatibility = conditions_to_check_for_compatibility.rstrip(" OR ")
    check_if_compatible_with_others = f"MATCH (p:{part_type} {{part_id: $part_id}}), (n) WHERE NOT (n:Build) AND NOT (n:{part_type}) AND p <> n AND ({conditions_to_check_for_compatibility}) MERGE (p)-[:COMPATIBLE]-(n);"
    driver.execute_query(check_if_compatible_with_others, part_id=part_id)

    return jsonify({"message": f"{part_type} added successfully"}), 201

@part_management.route('/create_empty_build', methods=['POST'])
def create_empty_build():
    driver = get_driver()
    build_id = str(uuid.uuid4())

    query = "CREATE (o:Build {status: 'pending', created_at: datetime(), total_wattage: 0, max_wattage: 0, total_cost: 0, budget: 0, build_id: $build_id}) RETURN $build_id AS build_id"
    result = driver.execute_query(query, build_id=build_id)

    return jsonify({"build_id": result.records[0]["build_id"]}), 201

@part_management.route('/add_part_to_build', methods=['POST'])
def add_part_to_build():
    driver = get_driver()
    
    #get data from request
    data = request.json
    part_id = data.get("part_id")
    build_id = data.get("build_id")
    quantity = data.get("quantity")
    
    # checks if parts and build exist
    check_part_exists = f"MATCH (p {{part_id: $part_id}}) RETURN p"
    part_result = driver.execute_query(check_part_exists, part_id=part_id)
    check_build_exists = "MATCH (o:Build {build_id: $build_id}) RETURN o"
    build_result = driver.execute_query(check_build_exists, build_id=build_id)  

    if not build_result.records and not part_result.records:
        return jsonify({"error": "Part or build does not exist"}), 404
    
    # checks if part is already in build
    check_if_already_in_build = driver.execute_query("""
    MATCH (o:Build {build_id: $build_id})-[r:CONTAINS]->(p {part_id: $part_id})
    RETURN r 
    """, build_id=build_id, part_id=part_id)

    if check_if_already_in_build.records:
        return jsonify({"error": "Part already in build"}), 400

    #builds and executes query
    query = """
    MATCH (p {part_id: $part_id}), (o:Build {build_id: $build_id})
    CREATE (o)-[:CONTAINS {quantity: $quantity}]->(p)
    """

    driver.execute_query(query, part_id=part_id, build_id=build_id, quantity=quantity)
    return jsonify({"message": "Part added to build successfully"}), 200

# @part_management.route('/testing', methods=['POST'])
# def testing():
#     driver = get_driver()
#     data = request.json
#     part_type = next(iter(data))
#     properties = data[part_type]

#     #check if other parts have some of the same properties as this one
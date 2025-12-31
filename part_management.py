from flask import request, jsonify, Blueprint
from flask_restful import Resource
from neo4j.time import DateTime
from db import get_driver
from user_management import decode_token
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

# controller for parts (modify later with flask-restful if needed)

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
    conditions_to_check_for_compatibility = []
    for condition in compatibility[part_type]:
        conditions_to_check_for_compatibility.append(f'CASE WHEN p.{condition} = n.{condition} THEN "{condition}" END')

    case_block = ", ".join(conditions_to_check_for_compatibility)

    check_if_compatible_with_others = f"""
    MATCH (p:{part_type} {{part_id: $part_id}}), (n)
    WHERE
    NOT n:Build
    AND NOT n:{part_type}
    AND p <> n
    WITH
    p, n,
    [{case_block}] AS conditions
    WITH
    p, n,
    [c IN conditions WHERE c IS NOT NULL] AS matching_conditions
    WHERE size(matching_conditions) > 0
    MERGE (p)-[c:COMPATIBLE]-(n)
    SET c.compatible_on = matching_conditions
    """

    record = driver.execute_query(check_if_compatible_with_others, part_id=part_id)

    return jsonify({"message": f"{part_type} added successfully"}), 201

@part_management.route('/parts/<part_type>', methods=['GET'])
def get_parts(part_type):
    driver = get_driver()
    query = f"MATCH (p:{part_type}) RETURN p"
    query_result = driver.execute_query(query)
    
    parts = []
    for record in query_result.records:
        node = record['p']
        part = dict(node)
        part["part_type"] = list(part.labels)[0]
        parts.append(part)

    return jsonify({"parts": parts}), 200

@part_management.route('/parts/<part_type>/<part_id>', methods=['GET'])
def get_part_by_id(part_type, part_id):
    driver = get_driver()
    part_type = part_type.upper()

    # checks if part type is valid
    if part_type not in valid_parts:
        return jsonify({"error": "Invalid part type"}), 400

    query = f"MATCH (p:{part_type} {{part_id: $part_id}}) RETURN p"
    result = driver.execute_query(query, part_id=part_id)

    parts = []
    for record in result.records:
        node = record["p"]
        part_dict = dict(node)          
        part_dict["part_type"] = list(node.labels)[0]
        parts.append(part_dict)

    if not parts:
        return jsonify({"error": "Part not found"}), 404

    return jsonify({"part": parts[0]}), 200

# controller for builds (modify later with flask-restful if needed)

@part_management.route('/create_empty_build', methods=['POST'])
def create_empty_build():
    driver = get_driver()

    # copy for all routes that need authentication

    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    decoded_token = decode_token(token)

    if decoded_token in ["expired", "invalid"]:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # copy for all routes that need authentication
    
    build_id = str(uuid.uuid4())

    query = """CREATE (o:Build {
        status: 'pending', 
        created_at: datetime(), 
        total_wattage: 0, 
        max_wattage: 0,
        max_ram_capacity: 0, 
        total_cost: 0, 
        budget: 0, 
        build_id: $build_id});"""
    
    create_relation_query = """
        MATCH (u:User {username: $username}), (o:Build {build_id: $build_id})
        CREATE (u)-[:OWNS]->(o)
        """
    driver.execute_query(query, build_id=build_id)
    driver.execute_query(create_relation_query, build_id=build_id, username=decoded_token["username"])
    return jsonify({"message": "Successfully created new build"}), 201

@part_management.route('/add_part_to_build', methods=['POST'])
def add_part_to_build():
    driver = get_driver()

    # copy for all routes that need authentication

    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    decoded_token = decode_token(token)

    if decoded_token in ["expired", "invalid"]:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # copy for all routes that need authentication
    
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
    MATCH (u:User)-[:OWNS]->(o)
    WHERE u.username = $username
    RETURN r 
    """, build_id=build_id, part_id=part_id, username=decoded_token["username"])

    if check_if_already_in_build.records:
        return jsonify({"error": "Part already in build"}), 400

    #builds and executes query
    query = """
    MATCH (p {part_id: $part_id}), (o:Build {build_id: $build_id})
    CREATE (o)-[:CONTAINS {quantity: $quantity}]->(p)
    """

    driver.execute_query(query, part_id=part_id, build_id=build_id, quantity=quantity)
    return jsonify({"message": "Part added to build successfully"}), 200

@part_management.route('/get_build/<build_id>', methods=['GET'])
def get_build(build_id):
    driver = get_driver()

    # copy for all routes that need authentication

    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    decoded_token = decode_token(token)

    if decoded_token in ["expired", "invalid"]:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # copy for all routes that need authentication

    query = """
    MATCH (u:User)-[:OWNS]->(o:Build {build_id: $build_id})
    WHERE u.username = $username
    OPTIONAL MATCH (o)-[r:CONTAINS]->(p)
    RETURN o, collect({part: p, quantity: r.quantity}) AS parts
    """

    result = driver.execute_query(query, build_id=build_id, username=decoded_token["username"])

    if not result.records:
        return jsonify({"error": "Build not found"}), 404

    record = result.records[0]

    build_node = record["o"]
    parts_info = record["parts"]

    build_dict = dict(build_node)

    for k, v in build_dict.items():
        if isinstance(v, DateTime):
            build_dict[k] = v.iso_format()
    parts_list = []

    for item in parts_info:
        part_node = item["part"]
        if part_node is not None:
            part_dict = dict(part_node)
            part_dict["part_type"] = list(part_node.labels)[0]
            parts_list.append({
                "part": part_dict,
                "quantity": item["quantity"]
            })

    build_dict["parts"] = parts_list

    return jsonify({"build": build_dict}), 200
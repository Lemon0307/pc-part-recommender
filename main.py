from flask import Flask
from part_management import part_management
from db import driver

app = Flask(__name__)
app.register_blueprint(part_management)

if __name__ == '__main__':
    driver.verify_connectivity()
    print("Connected to the database successfully.")
    app.run(debug=True)
from flask import Flask, escape, request,send_file
from flask import render_template
from flask_swagger_ui import get_swaggerui_blueprint
from controllers.ApiController import Api_Controller
from controllers.ApartmentEquipment import Apartment_Equipment
from controllers.ElectionInformation import Election_Information
from controllers.NotificationInformation import Notification_Information
from controllers.GuestInformation import Guest_Information
from controllers.EmployeeInformation import Employee_Information
from controllers.EventInformation import Event_Information
from controllers.BankInformation import Bank_Information
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
#@app.route('/api/swagger.json')
#def swagger_json():
    # Read before use: http://flask.pocoo.org/docs/0.12/api/#flask.send_file
#    return send_file('/tmp/patch_it_framework/controllers/swagger.yml') 
app.register_blueprint(Api_Controller)
app.register_blueprint(Apartment_Equipment)
app.register_blueprint(Election_Information)
app.register_blueprint(Notification_Information)
app.register_blueprint(Guest_Information)
app.register_blueprint(Employee_Information)
app.register_blueprint(Event_Information)
app.register_blueprint(Bank_Information)
app.secret_key="automation"
    
# Create the application instance


# Read the swagger.yml file to configure the endpoints
#SWAGGER_URL = '/api'
#app.add_api('swagger.yml')
#API_URL=('/api/swagger.json')
# Call factory function to create our blueprint
#SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
#API_URL,
#config={ # Swagger UI config overrides
#'app_name': "Test application"
#},
# oauth_config={ # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
# 'clientId': "your-client-id",
# 'clientSecret': "your-client-secret-if-required",
# 'realm': "your-realms",
# 'appName': "your-app-name",
# 'scopeSeparator': " ",
# 'additionalQueryStringParams': {'test': "hello"}
# }
#)
#app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('static/home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

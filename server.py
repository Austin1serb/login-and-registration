from flask_app import app
from flask_app.controllers import controller



# from flask_Bycrypt import Bcrypt        
# bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument




# step one:
#     pip3 install pipenv

# step two:
#     pipenv install flask

# step three:
#     pipenv install PyMySQL flask-bcrypt
#     or
#     pipenv install flask-bcrypt
# step four:

    # pipenv shell

    
if __name__=="__main__":
    app.run(debug=True, port=5004)
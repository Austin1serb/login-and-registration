from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
# from flask_app.models

bycrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db='users_schema'
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_one_email(cls,data):
        
        query = "SELECT * FROM users "
        query +="WHERE email = %(email)s;"

        result = connectToMySQL("users_schema").query_db(query,data)
        if len(result) < 1:
            return False
        
        return cls(result[0])



    @classmethod
    def create_user(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);"""
        return connectToMySQL("users_schema").query_db(query, data)


    @classmethod
    def get_one_id(cls,data):
        query = """
         SELECT * 
         FROM users
         WHERE id = %(id)s
        """
        result=connectToMySQL('users_schema').query_db(query,data)
        if len(result)<=1:
            return False
        return cls(result[0])




    


    # EMAIL VALIDATION
    @staticmethod
    def validate_email(email):
        is_valid = True

        if User.get_one_email(email):
            flash("Email already taken.",'email_error')
            is_valid=False
        elif not EMAIL_REGEX.match(email['email']):
            flash("Invalid Email!!!",'email_error')
            is_valid=False
        return is_valid
    
    @staticmethod
    def validate_user(data):
            errors=False
            if len(data['first_name']) < 2:
                flash('First name must be at least two characters', "first_name")
                errors=True
            if len(data['last_name'])<2:
                flash('Last Name must be at least two characters', 'last_name')
                errors=True
            if len(data['password'])<6:
                flash('Password must be at least six characters long',"password")      
    # Check if the password contains at least one number and one uppercase letter
            if not re.search(r'\d', 'password') or not re.search(r'[A-Z]', 'password'):
                flash('Password must contain at least one number and one uppercase letter.','password')
                errors=True
            elif not data['password'] == data['password_confirm']:
                flash('Passwords do NOT match, please try again', 'password_error')
                errors=True

            return True

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re  

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z]')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def create(cls, data): 
        query = "INSERT INTO users (first_name , last_name , email, password) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return []

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            user = cls(results[0])
            return user
        return []

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['first_name']) < 2 :
            flash('First name must contain at least 2 characters.', 'err_users_first_name')
            is_valid = False
        if not NAME_REGEX.match(data['first_name']) and len(data['first_name']) >= 1:
            flash('First name can only contain letters', 'err_users_first_name')

        if len(data['last_name']) < 2:
            flash('Last name must contain at least 2 characters.', 'err_users_last_name')
            is_valid = False
        if not NAME_REGEX.match(data['last_name']) and len(data['last_name']) >= 1:
            flash('Last name can only contain letters.', 'err_users_last_name')

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address format.", 'err_users_email')
            is_valid = False
        else:
            existing_user = User.get_one_by_email(data)
            if existing_user:
                flash ("Email already in use. Please try another.", 'err_users_email')
                is_valid = False

        if not PASSWORD_REGEX.match(data['password']):
            flash("Password must be at least 8 characters in length and contain at least one uppcase letter, one lowercase letter, one number, and one special character.", 'err_users_password')
            is_valid = False
        elif (data['password']) != (data['confirm_password']):
            flash("Passwords do not match. Please try again.", 'err_users_password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address format.", 'err_users_email_login')
            is_valid = False
        else:
            user = User.get_one_by_email(data)
            if not bcrypt.check_password_hash(user.password, data['password']):
                flash("Invalid credentials. Please try again.", 'err_users_password_login')
                is_valid = False
            else:
                session['user_id'] = user.id
        return is_valid
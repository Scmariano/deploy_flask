from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    schema = 'belt_exam'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def save_user(cls, data):
        query = "INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results)< 1:
            return False
        row = results[0]
        users = cls(row)
        return users

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results)< 1:
            return False
        row = results[0]
        users = cls(row)
        return users
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users "
        results = connectToMySQL(cls.schema).query_db(query)
        email = []
        for row in results:
            email.append( cls(row) )
        return email

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s,  last_name = %(last_name)s,  email = %(email)s, WHERE users.id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query,data)
        
    @staticmethod
    def validate_register(user):
        is_valid = True
        user_email_in_db = User.get_email(user)
        if user_email_in_db:
            flash("Email is already been taken", "register")
            is_valid =  False
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 3 characters","register")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters", "register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters", "register")
        if user['password'] != user['confirm']:
            flash("Password must match!", "register")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        user_email_in_db = User.get_email(user)
        if not user_email_in_db:
            flash("Email not registered!", "login")
            is_valid = False
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must not be at least 8 characters.", "login")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "login")
            is_valid = False
        return is_valid

    @staticmethod
    def update_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 3 characters","register")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters", "register")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        return is_valid
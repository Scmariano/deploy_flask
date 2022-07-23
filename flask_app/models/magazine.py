from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Magazine:
    schema = 'belt_exam'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.users_who_subscribed = []
        self.user_id_who_subscribed = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines JOIN users AS creators on creators.id = magazines.user_id LEFT JOIN subscriptions ON magazines.id = subscriptions.magazine_id LEFT JOIN users AS users_who_subscribed ON users_who_subscribed.id = subscriptions.user_id"
        results = connectToMySQL(cls.schema).query_db(query)
        magazines = []
        for row in results:
            new_magazine = True
            user_who_subscribed_data = {
                'id': row['users_who_subscribed.id'],
                'first_name': row['users_who_subscribed.first_name'],
                'last_name': row['users_who_subscribed.last_name'],
                'email': row['users_who_subscribed.email'],
                'password': row['users_who_subscribed.password'],
                'created_at': row['users_who_subscribed.created_at'],
                'updated_at': row['users_who_subscribed.updated_at']
            }

            number_of_magazines = len(magazines)
            if number_of_magazines > 0:
                last_magazine = magazines[number_of_magazines-1]
                if last_magazine.id == row['id']:
                    last_magazine.user_id_who_subscribed.append(row['users_who_subscribed.id'])
                    last_magazine.users_who_subscribed.append(User(user_who_subscribed_data))
                    new_magazine = False
            if new_magazine:
                magazine = cls(row)
                user_data = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at']
                }
                user = User(user_data)
                magazine.user = user
                if row['users_who_subscribed.id']:
                    magazine.user_id_who_subscribed.append(row['users_who_subscribed.id'])
                    magazine.users_who_subscribed.append(User(user_who_subscribed_data))
                magazines.append(magazine)
        return magazines

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM magazines JOIN users AS creators on creators.id = magazines.user_id LEFT JOIN subscriptions ON magazines.id = subscriptions.magazine_id LEFT JOIN users AS users_who_subscribed ON users_who_subscribed.id = subscriptions.user_id WHERE magazines.id = %(id)s"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) < 1:
            return False
        new_magazine = True
        for row in results:
            if new_magazine:
                magazine = cls(row)
                user_data = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at']
                }
                creator = User(user_data)
                magazine.user = creator
                new_magazine = False
            if row['users_who_subscribed.id']:
                user_who_subscribed_data = {
                    'id': row['users_who_subscribed.id'],
                    'first_name': row['users_who_subscribed.first_name'],
                    'last_name': row['users_who_subscribed.last_name'],
                    'email': row['users_who_subscribed.email'],
                    'password': row['users_who_subscribed.password'],
                    'created_at': row['users_who_subscribed.created_at'],
                    'updated_at': row['users_who_subscribed.updated_at']
                }
                user_who_subscribed = User(user_who_subscribed_data)
                magazine.users_who_subscribed.append(user_who_subscribed)
                magazine.user_id_who_subscribed.append(row['users_who_subscribed.id'])
        return magazine

    @classmethod
    def create(cls, data):
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s) "
        results = connectToMySQL(cls.schema).query_db(query,data)
        return results

    @classmethod
    def edit(cls, data):
        query = "UPDATE magazines SET title = %(title)s,  description = %(description)s, WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query,data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def subscribed(cls, data):
        query='INSERT INTO subscriptions (user_id, magazine_id) VALUES(%(user_id)s, %(id)s);'
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def unsubscribed(cls, data):
        query='DELETE FROM subscriptions WHERE user_id=%(user_id)s AND magazine_id=%(id)s;'
        return connectToMySQL(cls.schema).query_db(query, data)


    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine["title"]) < 2:
            is_valid = False
            flash("Title must be atleast 2 characters long!")
        if len(magazine["description"]) < 10:
            is_valid = False
            flash("Description must be 10 characters long!")
        return is_valid
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
from flask_app.models import model_user, model_trail


class Review:
    def __init__( self , data ):
        self.id = data['id']
        self.hiked_at = data['hiked_at']
        self.description = data['description']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.trail_id = data['trail_id']
        self.user = {}
        self.trail = {}

    @classmethod
    def get_all_with_user(cls, data):
        query = "SELECT * FROM reviews JOIN users ON users.id = reviews.user_id WHERE trail_id = %(trail_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            all_reviews = []
            for row in results:
                review = cls(row)
                user = {
                    'id' : row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at'],
                }
                review.user = model_user.User(user)
                all_reviews.append(review)
            return all_reviews
        return []

    @classmethod
    def get_one_with_trail(cls, data):
        query = "SELECT * FROM reviews JOIN trails ON trails.id = reviews.trail_id WHERE reviews.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            review = cls(results[0])
            for row in results:
                trail = {
                    'id': row['trails.id'],
                    'name': row['name'],
                    'location': row['location'],
                    'longitude': row['latitude'],
                    'latitude': row['latitude'],
                    'type': row['type'],
                    'length': row['length'],
                    'elevation_gain': row['elevation_gain'],
                    'dog_friendly': row['dog_friendly'],
                    'created_at': row['trails.created_at'],
                    'updated_at': row['trails.updated_at'],
                    'user_id' : row['user_id']
                }
                review.trail = model_trail.Trail(trail)
            return review
        return []

    @classmethod 
    def create(cls, data): 
        query = "INSERT INTO reviews (hiked_at, description, rating, user_id, trail_id) VALUES ( %(hiked_at)s, %(description)s, %(rating)s, %(user_id)s, %(trail_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data)

    @classmethod 
    def update_one(cls, data):
        query = "UPDATE reviews SET hiked_at = %(hiked_at)s, description = %(description)s, rating = %(rating)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
        
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

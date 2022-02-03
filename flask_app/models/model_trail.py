from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session

class Trail:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.type = data['type']
        self.length = data['length']
        self.elevation_gain = data['elevation_gain']
        self.dog_friendly = data['dog_friendly']
        # self.average_rating = data['average_rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod 
    def create(cls, data): 
        query = "INSERT INTO trails (name, location, longitude, latitude, type, length, elevation_gain, dog_friendly, user_id) VALUES ( %(name)s, %(location)s, %(longitude)s, %(latitude)s, %(type)s, %(length)s, %(elevation_gain)s, %(dog_friendly)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trails;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_trails = []
            for trail in results:
                all_trails.append(cls(trail))
            return all_trails
        return []

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trails WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return []

    @classmethod
    def update_one(cls, data):
        query = "UPDATE trails SET name = %(name)s, location = %(location)s, type = %(type)s, length = %(length)s, elevation_gain = %(elevation_gain)s, dog_friendly = %(dog_friendly)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM trails WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # @staticmethod
    # def validate_trail(data):
    #     is_valid = True
    #     return is_valid

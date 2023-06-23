from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import sqlite3
import pandas as pd


app = Flask(__name__)
CORS(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Booking(Resource):
    def post(self):

        data = request.get_json()

        conn = sqlite3.connect('schedule.db')

        cursor = conn.cursor()

        table_name = 'schedule'

        room_id = data['room_id']
        slot = data['slot']
        booking_date = data['booking_date']

        # Check if a row with the same room_id, date, and slot already exists
        query = f"SELECT COUNT(*) FROM {table_name} WHERE room_id=? AND slot=? AND booking_date=?"
        cursor.execute(query, (room_id,slot,booking_date))
        count = cursor.fetchone()[0]

        # If a row already exists, return a message saying the slot is occupied
        if count > 0:
            print("Slot is occupied. Cannot insert the values.")
            return {"Error Message": "Slot is occupied."}
        else:
            # Create the INSERT query
            insert_query = f"INSERT INTO {table_name} (room_id, slot, booking_date) VALUES (?, ?, ?)"

            # Execute the query and insert the values
            cursor.execute(insert_query, (room_id, slot, booking_date))

            # Commit the transaction
            conn.commit()
            print("Values inserted successfully.")
            return {"Info Message": "Slot has been booked!"}

class Check(Resource):
    def get(self):

        args = request.args

        booking_date = args['booking_date']

        print(booking_date)

        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()
        table_name = 'schedule'

        query = f"SELECT * FROM {table_name} WHERE booking_date=?"
        cursor.execute(query,(booking_date,))
        res = cursor.fetchall()

        print(res)

        _id = []
        _room_id = []
        _slot = []
        _booking_date = []

        for each in res:
            _id.append(each[0])
            _room_id.append(each[1])
            _slot.append(each[2])
            _booking_date.append(each[3])

        df = pd.DataFrame({'room_id' : _room_id , 'slot' : _slot, 'booking_date' : _booking_date})
        print(df)

        return {'data' : df.to_dict(orient='record')}
        


api.add_resource(HelloWorld, '/')
api.add_resource(Booking, '/book')
api.add_resource(Check, '/check')

if __name__ == '__main__':
    app.run(debug=True)
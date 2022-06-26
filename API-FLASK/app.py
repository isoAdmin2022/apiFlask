from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


@app.route("/")
def getListPost():
    register = []
    
    try: 
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='1234',
            database='iso'
        )
        
        print('conexion exitosa')
        cursor = connection.cursor()
        cursor.execute("select * from postBlog")
        rows = cursor.fetchall()
        count = 0

        
        for element in rows:
            
            newRegister = {
                    'id': element[0],
                    'title': element[1],
                    'body': element[2]
                }
            register.append(newRegister)
        print(register)
        
    except Exception as ex:
        print(ex)
        
    finally: 
        connection.close()
        print('Conexion finalizada')
    
    return jsonify({'data': register})

@app.route("/create", methods=['POST'])
def createPost():
    title = request.json['title']
    body = request.json['body']
    propt = (title, body)
    
    try: 
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='1234',
            database='iso'
        )
        
        print('conexion exitosa')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO postblog(idpost, title, body) VALUES ((select count(*) from postblog), %s,  %s)""", propt)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")
        
        register = 'OK'
    except Exception as ex:
        register = 'Error'
        print(ex)
        
    finally: 
        connection.close()
        print('Conexion finalizada')
    
    return jsonify({'data': register})



if __name__ == '__main__':
    app.run(debug = False, port = 4000)
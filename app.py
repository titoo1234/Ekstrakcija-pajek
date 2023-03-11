from flask import Flask
from flask import jsonify
from flask_httpauth import HTTPBasicAuth


import threading
import psycopg2
app = Flask(__name__)

lock = threading.Lock()

def reset_db_values():
    conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
    conn.autocommit = True
    
    cur = conn.cursor()
    cur.execute("UPDATE showcase.counters SET value = 0")
    
    cur.close()
    conn.close()
    
def print_db_values():
    conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
    conn.autocommit = True

    retVal = []
    print("\nValues in the database:")
    cur = conn.cursor()
    cur.execute("SELECT counter_id, value FROM showcase.counters ORDER BY counter_id")
    for counter_id, value in cur.fetchall():
        print(f"\tCounter id: {counter_id}, value: {value}")
        retVal.append({counter_id: value})
    cur.close()
    conn.close()
    return retVal

def increase_db_values(counter_id):
    conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
    conn.autocommit = True
    
    cur = conn.cursor()
    cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
                (counter_id,))
    value = cur.fetchone()[0]
    cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
                (value+1, counter_id))
    cur.close()
    conn.close()
    
def increase_db_values_locking(counter_id):
    conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
    conn.autocommit = True

    with lock:
        cur = conn.cursor()
        cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
                    (counter_id,))
        value = cur.fetchone()[0]
        cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
                    (value+1, counter_id))
        cur.close()
    conn.close()

# basic_auth = HTTPBasicAuth()

# @basic_auth.verify_password
# def verify_password(username, password):
#     if password == "BestNonencryptedPasswordEver!!!":
#         return username
#     else:
#         return None

# @basic_auth.error_handler
# def basic_auth_error(status):
#     return jsonify({"success": False, "message": "Wrong credentials!"}), status

# @app.errorhandler(404)
# def not_found_error(error):
#     return jsonify({"success": False, "message": "Object not found!"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     # rollback db if using transactions
#     return jsonify({"success": False, "message": "Server error!"}), 500


@app.route('/db/reset', methods=['POST'])
#@basic_auth.login_required
def fl_restart():
    reset_db_values()
    return jsonify({"success": True})

@app.route('/db/get_values', methods=['GET'])
#@basic_auth.login_required
def fl_get_values():
    retVal = print_db_values()
    return jsonify(retVal)
    
@app.route('/db/increase/<int:id>', methods=['POST'])
#@basic_auth.login_required
def fl_inc_vals(id):
    increase_db_values(id)
    return jsonify({"success": True})

@app.route('/db/increase_locking/<int:id>', methods=['POST'])
#@basic_auth.login_required
def fl_inc_vals_lock(id):
    increase_db_values_locking(id)
    return jsonify({"success": True})


if __name__ == "__main__":
    #app.run(ssl_context='adhoc')
    app.run()

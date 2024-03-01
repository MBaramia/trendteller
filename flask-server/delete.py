from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from server import UserData

app = Flask(__name__)
app.secret_key = "ddf4354fhdsuh4534534"

login_manager = LoginManager()
login_manager.init_app(app)


#mock database
users = {
    "username@email.com": "password123",
}


#mock user table
class User(UserMixin):
    pass


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        #Replace with actual user table
        user = UserData()
        user.id = username

        login_user(user)
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login unsuccessful"}), 401


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})

@app.route("/checkLoggedIn")
@login_required
def protected():
    return jsonify({"message": "Is logged in"})

# Members API route - delete
@app.route("/members")
def members():
    return {"members": ["member1", "member2", "member3"]}

if __name__ == "__main__":
    app.run(debug=True)
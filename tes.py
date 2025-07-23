from werkzeug.security import generate_password_hash

hash = generate_password_hash("Pajak@123")
print(hash)
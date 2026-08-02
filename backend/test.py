from werkzeug.security import generate_password_hash

pin = "100097"
hashed = generate_password_hash(pin, method="pbkdf2:sha256")
print(hashed)

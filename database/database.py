# init database
def init_db():
    return {
        "user_template": {
            "form": {"name": None, "age": None, "sex": None, "phone_number": None}
        },
        "users": dict(),
    }

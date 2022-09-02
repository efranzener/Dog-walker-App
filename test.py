#print("hello")
import json

class SignupRequest(dict):
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

newSignup = SignupRequest("Ety", "ety@gmail.com", 12)

print("name: ", newSignup.name)
newSignupJson = json.dumps(newSignup.__dict__)
print("newSignupJson: ", newSignupJson)

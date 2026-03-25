# This is the schemas define the shape of the data coming IN and going out of our API it's not the databse models , they are validation layer's

from pydantic import BaseModel , EmailStr , field_validator

# What we expect when a user REGISTER'S into the system. 
class UserRegister(BaseModel):
    username : str
    email : EmailStr  # EmailStr is the one that validates the email address , it would reject the email if it's not in the correct format "ashutosh@gmail.com"
    password : str

    @field_validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 72:
            raise ValueError("Password cannot be longer than 72 characters")
        return v

# What we expect when a user LOG'S into the syetem. 
class UserLogin(BaseModel):
    email:EmailStr
    password:str

# What we send BACK after user's successful login. 
class TokenResponse(BaseModel):
    access_token:str  # this is the actual JWT string. That `header.payload.signature`
    token_type:str   # the client "hey, this is a Bearer token, send it in the Authorization header like this:"(like  the label on the box that tells the delivery system how to handle it.)
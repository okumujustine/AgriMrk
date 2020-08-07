from app import db, ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('country', 'region', 'district', 'phone', 'name', 'email', 'password', 'status')

user_schema = UserSchema()
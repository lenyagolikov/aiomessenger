class UserSettings:
    user_id = None
    timezone = None

    def __init__(self, user_id, timezone=0):
        self.user_id = user_id
        self.timezone = timezone

    def __repr__(self):
        return f"{{timezone: {self.timezone}}}"


user1 = UserSettings("allison", 1)
user2 = UserSettings("lenyagolikov", 2)
user3 = UserSettings("rachik", 3)

users = [user1, user2, user3]

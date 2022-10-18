
users = [
    (0,"user1", "pass1"),
    (1,"user2", "pass2"),
    (2,"user3", "pass3"),
]
#users is list
#users[0] is tupble
print(type(users),type(users[0]))


usermapping = {user[1]:user for user in users}
#usermapping is dict

print(type(usermapping) , usermapping)


print(usermapping["user2"])

_, username, password = usermapping["user2"]
print(username, password)

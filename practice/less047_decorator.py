import functools

user = { "username":"robin", "access_level": "guest" }


# def secue_func(func):
    
#     # functools.wraps(func)
#     # dùng để khi gọi get_admin_password_withAt.__name__ 
#     # sẽ trả về đúng tên func truyền vào 
#     # tức là khi đặt @secue_func vào func nào thì gọi __name__ sẽ trả về name đúng của func đó
#     # nếu không có nó sẽ trả về __name__ của secue_get_admin_pass
#     # đại khái là nó báo cho python là trả về info của func nào 
#     @functools.wraps(func)
#     def secue_get_admin_pass(*args, **kwargs): #pass parameter 
#         if user['access_level'] == 'admin':
#             return func(*args, **kwargs)
    
#     return secue_get_admin_pass # return none if is not admin

def secue_func(access_level):
    
    def decorator(func):
        # functools.wraps(func)
        # dùng để khi gọi get_admin_password_withAt.__name__ 
        # sẽ trả về đúng tên func truyền vào 
        # tức là khi đặt @secue_func vào func nào thì gọi __name__ sẽ trả về name đúng của func đó
        # nếu không có nó sẽ trả về __name__ của secue_get_admin_pass
        # đại khái là nó báo cho python là trả về info của func nào 
        @functools.wraps(func)
        def secue_get_admin_pass(*args, **kwargs): #pass parameter 
            if user['access_level'] == access_level:
                return func(*args, **kwargs)
            else:
                return f"No {access_level} permission for {user['username']}"
        
        return secue_get_admin_pass # return none if is not admin
    
    return decorator

# -----------------------
# def get_admin_password():
#     return "ahihi"

# get_admin_password = secue_func(get_admin_password)
# print(get_admin_password())
# #########################

#with @ decorator
@secue_func("admin")
def get_admin_password_withAt():
    return "hello admin"

@secue_func("guest")
def get_password():
    return "hello guest"

@secue_func("admin") # like annotation [Authorize("admin")] .net
def get_admin_pass_with_pram( param ):
    return f"password nay {param}"

print(get_admin_password_withAt.__name__)

print(get_password())
print(get_admin_pass_with_pram("ahihi"))
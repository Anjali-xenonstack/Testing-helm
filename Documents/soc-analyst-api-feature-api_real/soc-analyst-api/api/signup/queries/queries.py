signup_query = """
INSERT INTO public."users" (email, password,name) VALUES (%s, %s, %s);

"""
Check_user_query = """
select * from public."users" where email =  %s
"""
Logout_query = """
UPDATE public.sessionlog
SET isactive = 'false'
WHERE token =%s;

"""
Check_token_query = """
SELECT token FROM public.sessionlog WHERE token = %s and isactive = 'false';
"""
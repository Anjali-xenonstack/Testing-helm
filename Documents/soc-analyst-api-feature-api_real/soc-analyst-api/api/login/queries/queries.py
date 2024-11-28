# Login_query = """
# INSERT INTO public."users"(createdat,  updatedat, email, name )
# VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,  %s,%s);
# """


# user_table_updatedby = """
# UPDATE public."users" SET  createdby = %s ,updatedat = CURRENT_TIMESTAMP  ,updatedby = %s
# WHERE id = %s;
# """


# Login_query_check_new_user_todo = """
# INSERT INTO public."user"(createdat,  updatedat, emailid, username , rolename, userurl, emailid, workingzone)
# VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP,  %s);

# """

Login_query_check_userid = """
SELECT id, password FROM public."users" WHERE email = %s;

"""


# Enter_into_Session_log_query = """
# INSERT INTO public."sessionlog"
#     (createdat, createdby, updatedat, updatedby, isactive, loggedinat, token)
# VALUES
#     (CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP, %s, true, CURRENT_TIMESTAMP, %s );
# """

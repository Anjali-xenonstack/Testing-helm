import os

db_params = os.getenv("db_reader")

if db_params is None:
    db_params = {
        #         'host': '20.115.57.131',
        # 'database': 'soc_real_database',
        # 'user': 'postgres',
        # 'password': 'Jg0pHVcFmy',
        # 'port': 31588
        # 'host': 'postgres-xenonstack.postgres.database.azure.com',
        # 'database': 'soc_real_database',
        # 'user': 'postgres',
        # 'password': 'xenonstack@123',
        # 'port': 5432
        "host": "172.16.200.201",
        "port": 31326,
        "database": "soc_real_database",
        "user": "postgres",
        "password": "Q53NKxdwL3",
        }
    
postgres_config = os.getenv("postgres_config")
if postgres_config is None:
    postgres_config = {
        # "host": "localhost",
        # "port": 5432,
        # "database": "Data_analyst",
        # "username": "postgres",
        # "password": "Shubham1203",
        # "table": "case_logs_firewall",
    # }
    # postgres_config = {
    #       'host': '20.115.57.131',
    #     'database': 'soc_real_database',
    #     'username': 'postgres',
    #     'password': 'Jg0pHVcFmy',
    #     'port': 31588,
    # "host": "postgres-xenonstack.postgres.database.azure.com",
    # "port": 5432,
    # "database": "soc_real_database",
    # "username": "postgres",
    # "password": "xenonstack%40123",
    # "table": "case_logs_firewall",
            "host": "172.16.200.201",
            "port": 31326,
            "database": "soc_real_database",
            "username": "postgres",
            "password": "Q53NKxdwL3",
            "table": "case_logs_firewall",
}

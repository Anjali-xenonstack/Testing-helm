get_progress_count = """
    SELECT COUNT(*)
    FROM public.case_logs_firewall
    WHERE ended_at IS NULL;
"""


# case_list_query_by_id = """
# SELECT 
#     id, 
#     alert_type, 
#     CASE 
#         WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
#         ELSE '{}'::jsonb 
#     END AS logs, 
#     REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
#     REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
#     REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
#     REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
#     TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
#     TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
# FROM 
#     public.case_logs_firewall 
# WHERE 
#     id = %s;
# """


# case_list_query = """
# SELECT 
#     id, 
#     alert_type, 
#     CASE 
#         WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
#         ELSE '{}'::jsonb 
#     END AS logs, 
#     REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
#     REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
#     REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
#     REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
#     TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
#     TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
# FROM 
#     public.case_logs_firewall 
# WHERE 
#     LOWER(type::text) = LOWER(%s);
# """



# case_list_query_with_alert = """
# SELECT 
#     id, 
#     alert_type, 
#     CASE 
#         WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
#         ELSE '{}'::jsonb 
#     END AS logs, 
#     REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
#     REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
#     REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
#     REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
#     TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
#     TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
# FROM 
#     public.case_logs_firewall 
# WHERE 
#     LOWER(type::text) = LOWER(%s) AND LOWER(alert_type::text) ILIKE LOWER(%s);
# """

# case_list_query = """
# SELECT 
#     id, 
#     alert_type, 
#     CASE 
#         WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
#         ELSE '{}'::jsonb 
#     END AS logs, 
#     REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
#     REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
#     REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
#     REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
#     TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
#     TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
# FROM 
#     public.case_logs_firewall 
# WHERE 
#     LOWER(type::text) = LOWER(%s) AND LOWER(alert_type::text) ILIKE '%' ||LOWER(%s)|| '%';
# """

# case_list_query = """
# SELECT 
#     id, 
#     alert_type, 
#     CASE 
#         WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
#         ELSE '{}'::jsonb 
#     END AS logs, 
#     criticality::xml as criticality,
#     analysis::xml as analysis,
#     report::xml as report ,
#     recommendation::xml as recommendation, 
#     TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
#     TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
# FROM 
#     public.case_logs_firewall 
# WHERE 
#     LOWER(type::text) = LOWER(%s);

# """
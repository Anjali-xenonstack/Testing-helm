case_list_query = """
SELECT 
    id, 
    alert_type, 
    CASE 
        WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
        ELSE '{}'::jsonb 
    END AS logs, 
    REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
    REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
    REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
    REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
    TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
FROM 
    public.case_logs_firewall 
WHERE 
    LOWER(type::text) = LOWER(%s)
ORDER BY created_at DESC;
"""

# LIMIT 5 OFFSET %s;
# sort according to time latest to oldest
# pagination 5 per page and total count 
# get data by type firewall etc
# in progress count for all 
# http://127.0.0.1:5000/cases_list?type=FIREWALL&page=1 if none send all 


case_list_query_pagination = """
SELECT 
    id, 
    alert_type, 
    CASE 
        WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
        ELSE '{}'::jsonb 
    END AS logs, 
    REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
    REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
    REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
    REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
    TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
FROM 
    public.case_logs_firewall 
WHERE 
    LOWER(type::text) = LOWER(%s)
ORDER BY ended_at DESC
LIMIT 5 OFFSET %s;
"""


case_list_query_with_alert = """
SELECT 
    id, 
    alert_type, 
    CASE 
        WHEN logs::text IS NOT NULL AND logs::text <> '' AND logs::text::jsonb IS NOT NULL THEN logs::jsonb 
        ELSE '{}'::jsonb 
    END AS logs, 
    REPLACE(REPLACE(REPLACE(criticality, '', '')   , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ') As criticality, 
    REPLACE(REPLACE(REPLACE(analysis, '', '')      , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS analysis,
    REPLACE(REPLACE(REPLACE(report, '', '')        , '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS report,
    REPLACE(REPLACE(REPLACE(recommendation, '', ''), '•', ' \n'), '**Conclusion:**',' **Conclusion:** ')  AS recommendation, 
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at,
    TO_CHAR(ended_at, 'YYYY-MM-DD HH24:MI:SS') AS ended_at 
FROM 
    public.case_logs_firewall 
WHERE 
    LOWER(type::text) = LOWER(%s) AND LOWER(alert_type::text) ILIKE LOWER(%s);
"""
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
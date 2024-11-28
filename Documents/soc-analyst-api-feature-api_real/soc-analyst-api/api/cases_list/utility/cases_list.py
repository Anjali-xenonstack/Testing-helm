import logging
import os
import sys
from utils import  decode_andfetch_user_id
from cases_list.queries import queries

def cases_list(conn,input_type,alert_type):
    try:
        #outlet_report
        cursor = conn.cursor()
        print("*********",input_type,alert_type)
        # query = queries.case_list_query.rstrip("\n")
        
        if alert_type == None:
            query = queries.case_list_query.rstrip("\n")
            query_params = (input_type)
            cursor.execute(query,(input_type,))
        else:
        # query_params = (input_type, alert_type,)
            query = queries.case_list_query_with_alert.rstrip("\n")
            query_params = (input_type, '%' + alert_type + '%')
            cursor.execute(query,query_params)

        results = cursor.fetchall()

        if not results:
            return {"message": "Data Not Found", "error": True}, 404
        
        if isinstance(results, tuple):
            results = [results]

        print("*********************")
        column_names = [desc[0] for desc in cursor.description]

        cases_list = []

        for result in results:
            row_dict = dict(zip(column_names, result))
            cases_list_dict = {
                "id": row_dict["id"],
                "alert_type": row_dict["alert_type"],
                "logs": row_dict["logs"],
                "criticality": row_dict["criticality"],
                "analysis": row_dict["analysis"],
                "report": row_dict["report"],
                "recommendation": row_dict["recommendation"],
                "created_at": row_dict["created_at"],
                "ended_at": row_dict["ended_at"]
            }
            cases_list.append(cases_list_dict)
        return cases_list, 200
    
    except Exception as e:
        logging.info("Error in report Function", exc_info=True)
        return {'message': 'Internal server error', 'error': True}, 500


def cases_list_pagination(conn,case_type,alert_type,page):
    try:
        #outlet_report
        cursor = conn.cursor()
        print("*********",case_type,alert_type,type(page))
        query = queries.case_list_query_pagination.rstrip("\n")

        offset = (int(page) - 1) * 5
        cursor.execute(query, (case_type, offset))

        count_query = """
        SELECT COUNT(*)
        FROM public.case_logs_firewall
        WHERE LOWER(TRIM(type::text)) LIKE LOWER(TRIM(%s));
        """

        print(f"case_type: {case_type}")
        
        cursor.execute(count_query, (case_type,))
        # cursor.execute(count_query)
        total_count = cursor.fetchone()[0]
        
        print(total_count,"total===================================================================") 
    
        # if alert_type == None:
        #     query = queries.case_list_query.rstrip("\n")
        #     query_params = (case_type)
        #     cursor.execute(query,(case_type,))
        # else:
        # # query_params = (input_type, alert_type,)
        #     query = queries.case_list_query_with_alert.rstrip("\n")
        #     query_params = (case_type, '%' + alert_type + '%')
        #     cursor.execute(query,query_params)

        cursor.execute(query, (case_type, offset))
        results = cursor.fetchall()

        # print("results=------------------------------------------",results)

        if not results:
            return {"message": "Data Not Found", "error": True}, 404
        
        if isinstance(results, tuple):
            results = [results]

        print("*********************")
        column_names = [desc[0] for desc in cursor.description]

        cases_list = []

        for result in results:
            row_dict = dict(zip(column_names, result))
            cases_list_dict = {
                "id": row_dict["id"],
                "alert_type": row_dict["alert_type"],
                "logs": row_dict["logs"],
                "criticality": row_dict["criticality"],
                "analysis": row_dict["analysis"],
                "report": row_dict["report"],
                "recommendation": row_dict["recommendation"],
                "created_at": row_dict["created_at"],
                "ended_at": row_dict["ended_at"]
            }
            cases_list.append(cases_list_dict)
        return cases_list,total_count, 200
    
    except Exception as e:
        logging.info("Error in report Function", exc_info=True)
        return {'message': 'Internal server error', 'error': True}, 500
    


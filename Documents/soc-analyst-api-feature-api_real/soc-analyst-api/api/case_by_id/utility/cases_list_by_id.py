import logging
import os
import sys
from utils import  decode_andfetch_user_id
from case_by_id.queries import queries


def cases_list_by_id(conn,caseID):
    try:
        #outlet_report
        cursor = conn.cursor()
        print("*********",caseID)
        # query = queries.case_list_query.rstrip("\n")
        
        # if alert_type == None:
        #     query = queries.case_list_query.rstrip("\n")
        #     query_params = (input_type)
        #     cursor.execute(query,(input_type,))
        # else:
        # # query_params = (input_type, alert_type,)
        #     query = queries.case_list_query_with_alert.rstrip("\n")
        #     query_params = (input_type, '%' + alert_type + '%')
        #     cursor.execute(query,query_params)

        # results = cursor.fetchall()
        
        print(caseID, "caseID")
        print(type(caseID), "caseID type")

        query = queries.case_list_query_by_id.rstrip("\n")
        query_params = (caseID,)
        cursor.execute(query, query_params)

        results = cursor.fetchall()
        
        print(results,"this is results---------------------------------------------------------------======================")

        if not results:
            return {"message": "Data Not Found", "error": True}, 404
        
        if isinstance(results, tuple):
            results = [results]

        print("*********************")
        column_names = [desc[0] for desc in cursor.description]

        cases_list = {}

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
            # cases_list.append(cases_list_dict)
            # cases_list[row_dict["id"]] = cases_list_dict
        return cases_list_dict, 200
    
    except Exception as e:
        logging.info("Error in report Function", exc_info=True)
        return {'message': 'Internal server error', 'error': True}, 500
    

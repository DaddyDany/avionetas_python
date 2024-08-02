import json
import pymysql
from common.db_connection import get_db_connection

def lambda_handler(event, context):
    """ This function retrieves all avionetas

    Returns:
        dict: A dictionary containing the list of avionetas
    """
    try:
        # Obtener los datos de la base de datos
        avionetas = get_all_avionetas()

        response = {
            'statusCode': 200,
            'body': json.dumps(avionetas),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            }
        }

    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}"),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            }
        }

    return response
#JUST BECAUSE
def get_all_avionetas():
    connection = get_db_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM avioneta"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

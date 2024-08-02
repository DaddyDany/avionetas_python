import json
from common.db_connection import get_db_connection

def lambda_handler(event, context):
    """ This function deletes an avioneta by its ID

    Returns:
        dict: A dictionary that contains the result of the operation
    """
    try:
        # Obtener el ID del evento
        body = json.loads(event.get('body', '{}'))
        avioneta_id = body.get('id')

        # Verificar que el ID esté presente
        if not avioneta_id:
            response = {
                'statusCode': 400,
                'body': json.dumps("ID is required"),
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,DELETE'
                }
            }
            return response

        # Eliminar la avioneta de la base de datos
        delete_avioneta(avioneta_id)

        response = {
            'statusCode': 200,
            'body': json.dumps({"message": "Avioneta deleted successfully"}),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,DELETE'
            }
        }

    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}"),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,DELETE'
            }
        }

    return response

def delete_avioneta(avioneta_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM avioneta WHERE id = %s"
            cursor.execute(sql, (avioneta_id,))
            connection.commit()
    finally:
        connection.close()

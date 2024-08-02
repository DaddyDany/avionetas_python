import json
from common.db_connection import get_db_connection

def lambda_handler(event, context):
    """ This function registers an avioneta

    Returns:
        dict: A dictionary that contains the result of the operation
    """
    try:
        # Obtener los datos de la avioneta del evento
        body = json.loads(event.get('body', '{}'))
        modelo = body.get('modelo')
        tipo = body.get('tipo')
        profundidad_maxima = body.get('profundidadMaxima')
        velocidad = body.get('velocidad')

        # Verificar que todos los datos estén presentes
        if not modelo or not tipo or not profundidad_maxima or not velocidad:
            response = {
                'statusCode': 400,
                'body': json.dumps("All fields (modelo, tipo, profundidadMaxima, velocidad) are required"),
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT'
                }
            }


            return response

        # Registrar la avioneta en la base de datos
        avioneta_id = register_avioneta(modelo, tipo, profundidad_maxima, velocidad)

        response = {
            'statusCode': 201,
            'body': json.dumps({"message": "Avioneta registered successfully", "id": avioneta_id}),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT'
            }
        }



    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}"),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,PUT'
            }
        }

    return response

def register_avioneta(modelo, tipo, profundidad_maxima, velocidad):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO avioneta (modelo, tipo, profundidadMaxima, velocidad) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (modelo, tipo, profundidad_maxima, velocidad))
            connection.commit()
            avioneta_id = cursor.lastrowid
            return avioneta_id
    finally:
        connection.close()

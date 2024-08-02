import json
from common.db_connection import get_db_connection

def lambda_handler(event, context):
    """ This function updates an avioneta

    Returns:
        dict: A dictionary that contains the result of the operation
    """
    try:
        # Obtener los datos de la avioneta del evento
        body = json.loads(event.get('body', '{}'))
        avioneta_id = body.get('id')
        modelo = body.get('modelo')
        tipo = body.get('tipo')
        profundidad_maxima = body.get('profundidadMaxima')
        velocidad = body.get('velocidad')

        # Verificar que el ID y al menos uno de los datos estén presentes
        if not avioneta_id:
            response = {
                'statusCode': 400,
                'body': json.dumps("ID is required"),
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,PUT'
                }
            }

            return response

        if not modelo and not tipo and not profundidad_maxima and not velocidad:
            response = {
                'statusCode': 400,
                'body': json.dumps("At least one field (modelo, tipo, profundidadMaxima, velocidad) is required to update"),
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,PUT'
                }
            }

            return response

        # Actualizar la avioneta en la base de datos
        update_avioneta(avioneta_id, modelo, tipo, profundidad_maxima, velocidad)

        response = {
            'statusCode': 200,
            'body': json.dumps({"message": "Avioneta updated successfully"}),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,PUT'
            }
        }


    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}"),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,PUT'
            }
        }

    return response

def update_avioneta(avioneta_id, modelo=None, tipo=None, profundidad_maxima=None, velocidad=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE avioneta SET "
            updates = []
            params = []

            if modelo:
                updates.append("modelo = %s")
                params.append(modelo)
            if tipo:
                updates.append("tipo = %s")
                params.append(tipo)
            if profundidad_maxima:
                updates.append("profundidadMaxima = %s")
                params.append(profundidad_maxima)
            if velocidad:
                updates.append("velocidad = %s")
                params.append(velocidad)

            if not updates:
                raise ValueError("No fields provided to update")

            sql += ", ".join(updates) + " WHERE id = %s"
            params.append(avioneta_id)

            cursor.execute(sql, params)
            connection.commit()

    finally:
        connection.close()

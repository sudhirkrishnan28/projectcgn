import logging
import json
from DB_manager import DB_manager

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    try:
        # Connect to the database
        conn = DB_manager.get_db_connection()

        try:
            # Parse the incoming event body for phone details
            phone_details = json.loads(event['body'])

            # Log the received phone details for debugging
            logger.info("Phone details: %s", phone_details)



            

            # Insert query to add phone data to the database
            insert_phone_query = '''
                INSERT INTO PH (phName, phModel)
                VALUES (%s, %s)
            '''

            # Prepare the data to insert into the table
            phone_data = [
                phone_details['phName'],
                phone_details['phModel']
            ]

            # Execute the insert query
            with conn.cursor() as cur:
                cur.execute(insert_phone_query, phone_data)

                # Log the inserted phone ID
                logger.info("Inserted phone with ID: %s", cur.lastrowid)

                # Commit the changes to the database
                conn.commit()

                # Return a successful response
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    "body": json.dumps({
                        "statusCode": 200,
                        "responseMessage": "SUCCESS",
                        "response": phone_details
                    }, default=str)
                }

        except Exception as ex:
            # Log any error during the request processing
            logger.error("Error processing request: %s", str(ex))
            return {
                "statusCode": 502,
                "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                },
                "body": json.dumps({
                    "statusCode": 502,
                    "responseMessage": "FAILURE",
                    "response": str(ex)
                }, default=str)
            }

        finally:
            # Ensure the database connection is closed
            if conn:
                conn.close()

    except Exception as ex:
        # Log any database connection error
        logger.error("Database connection error: %s", str(ex))
        return {
            "statusCode": 502,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            "body": json.dumps({
                "statusCode": 502,
                "responseMessage": "FAILURE",
                "response": str(ex)
            }, default=str)
        }

# Testing the Lambda function
if __name__ == "__main__":
    event = {
        "body": json.dumps({
            "phName": "iPhone 14",
            "phModel": "Pro Max"
        })
    }
    response = lambda_handler(event, None)
    print(response)

"""
    This program listens for messages sent from the smart_smoker.py. 
    Messages received will include temperatures for a smoker and two foods inside.
    While listening, it will raise alerts if the smoker or food temperatures reach predetermined fluctuations.

    Author: Matt Goeckel
    Date: 11 February 2023

"""

import pika
import sys
import time

# define a callback function to be called when a message is received
def callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received {body.decode()}")

    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str = "localhost", q1: str = "smoker", q2: str = "food1", q3: str = "food2"):
    """ Continuously listen for task messages on a named queue."""

    try:
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        channel.queue_declare(queue=q1, durable=True)

        # Set the prefetch count to one to limit the number of messages being consumed and processed concurrently.
        # prefetch_count = Per consumer limit of unaknowledged messages      
    ####    channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=q1, on_message_callback=callback)

        # print a message to the console for the user
        print(" [*] Ready to receive temps. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", "smoker", "food1", "food2")

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt
import sys
import threading
import time
from uuid import uuid4
import json

# Parse arguments
import command_line_utils;
cmdUtils = command_line_utils.CommandLineUtils("PubSub - Send and recieve messages through an MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", type=str, default="private.pem.key")
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", type=str, default="certificate.pem.crt")
cmdUtils.register_command("endpoint", "<path>", "Endpoint address.", type=str, default="a13tm7plfyuhhu-ats.iot.us-east-1.amazonaws.com")
cmdUtils.register_command("port", "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
cmdUtils.register_command("client_id", "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
cmdUtils.register_command("count", "<int>", "The number of messages to send (optional, default='100').", default=100, type=int)
cmdUtils.get_args()


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))
    


if __name__ == '__main__':
    
    mqtt_connection = cmdUtils.build_mqtt_connection(None, None)
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    ####################
    
    # Publish (example)
    pub_topic_name = "ncsu/team_0/test_pub" #TODO: change the topic name
    pub_message = "Hi, we are "
    message_json = json.dumps(pub_message)
    print("Publishing message '{}' to topic {}".format(pub_message, pub_topic_name))
    mqtt_connection.publish(topic=pub_topic_name, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE)
    
    ####################
            
    # Subscribe (example)
    sub_topic_name = "ncsu/team_0/test_sub"    
    subscribe_future, packet_id = mqtt_connection.subscribe(topic=sub_topic_name, qos=mqtt.QoS.AT_LEAST_ONCE, callback=on_message_received)
    print("Subscribed to topic '{}'...".format(sub_topic_name))
    subscribe_result = subscribe_future.result()
    
    
    ####################
    
    # Publish
    while (True):
        blinking_rate = input("Please enter the LED blinking rate (in ms): ")
        print("Publishing LED blinking rate '{}' to topic {}".format("TODO", "TODO"))
        #TODO: Publish the LED blinking rate

        

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")

import json
import random
import math
# Set the number of devices and gateways

# Set the latitude and longitude of UNIPA
unipa_lat = 38.10391610180684
unipa_lon = 13.345738017336016
username="<username here>"
password="<passowrd here>"
mqtt_broker_hostname="<mqtt broker hostname>" #"lab.tti.unipa.it"
network_server_addr = "<network server addr>"
mqtt_broker_port=8883
mongodb_database_hostname = "<mongodb database hostname>" #"10.8.9.27"
mongodb_port = 27017
api_token = "<API token Here>"
# Set the radius (in kilometers) within which to distribute the gateways
blueprint_id=0

from geopy.distance import geodesic
import random
import math

def generate_random_coordinates(lat, lon, radius):
    # Generate random angle and distance
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius)

    # Calculate new latitude and longitude
    new_coordinates = geodesic(kilometers=distance).destination((lat, lon), angle * 180 / math.pi)

    return new_coordinates.latitude, new_coordinates.longitude

for radius in [1,6]:
    for nDevices in [10,100]:
        for nGateways in [1,10]:
            for rand_id in range(0,1):
                print(f"[{blueprint_id}] nDevices={nDevices} nGateways={nGateways}")
                # Create the JSON object
                mqtt_config={
                    "mqtt": {
                        "broker": mqtt_broker_hostname,#"lab.tti.unipa.it",
                        "port": mqtt_broker_port,
                        "client_id": "mqtt-db-logger",
                        "username": username,
                        "password": password,
                        "topics": [
                            "application/+/device/+/event/#"
                            ]
                        },
                    "mongodb": {
                        "host": mongodb_database_hostname, 
                        "port": mongodb_port,
                        "database": "Chirpstack-Supernova"
                    },
                }
                
                
                config = {
                    "type": "configuration",
                    "version": "1.0",
                    
                    "mqtt": {
                        "broker": mqtt_broker_hostname,#"lab.tti.unipa.it",
                        "port": mqtt_broker_port,
                        "client_id": "mqtt-db-logger",
                        "username": username,
                        "password": password,
                        "topics": [
                            "application/+/device/+/event/#"
                            ]
                        },
                    "mongodb": {
                        "host": mongodb_database_hostname, 
                        "port": mongodb_port,
                        "database": "Chirpstack-Supernova"
                    },
                    
                    "network": {
                        "id": "lorawan-network",
                        "name": "LoRaWAN Network",
                        "network_server": {
                            "id": "network-server-1",
                            "name": "ChirpStack Network Server",
                            "address": network_server_addr,
                            "api_token": api_token
                        },
                        "coverage":{
                            "radius":radius
                        },
                        "gateways": [],
                        "devices": []
                    }
                }

                # Generate the gateways
                for i in range(1, nGateways + 1):
                    lat, lon = generate_random_coordinates(unipa_lat,unipa_lon,radius)

                    # Add the gateway to the JSON object
                    config["network"]["gateways"].append({
                        "id": f"gateway-{i}",
                        "name": f"LoRa Gateway {i}",
                        "address": f"192.168.1.{100 + i}",
                        "latitude": lat,
                        "longitude": lon,
                        "frequency_band": "EU868",
                        "model": f"gateway-model-{i}"
                    })

                # Generate the devices
                for i in range(1, nDevices + 1):
                    lat, lon = generate_random_coordinates(unipa_lat,unipa_lon,radius)

                    # Generate random dev_eui value as EUI64
                    dev_eui = format(random.randint(0, 2**64 - 1), "016X")

                    # Set app_eui value to all zeros
                    app_eui = "0000000000000000"

                    # Set app_key value to a random 128-bit hexadecimal value
                    app_key = format(random.randint(0, 2**128 - 1), "032X")
                    sf = 7 #ALL DEVICES WITH SAME SF, TODO: add ADR or SF Planning
                    # Add the device to the JSON object
                    config["network"]["devices"].append({
                        "id": f"device-{i}",
                        "name": f"LoRa Device {i}",
                        "DR":sf,
                        "dev_eui": dev_eui,
                        "app_eui": app_eui,
                        "app_key": app_key,
                        "profile": "sensor-profile-xyz",
                        "latitude": lat,
                        "longitude": lon
                    })
                # Write the JSON object to a file
                id = format(blueprint_id, "04d")
                with open(f"simulation/ns3/lorawan/blueprint/ns3_blueprint_example-nDevices-{nDevices}-nGateways-{nGateways}-radius-{radius}.json", "w") as f:
                    
                    
                        
                    json.dump(config, f, indent=2)
                blueprint_id+=1


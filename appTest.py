#!venv/bin/python3
from flask import Flask, jsonify, request
from kubernetes import client, config
import json
from json import dumps
import re
from flask_pymongo import PyMongo

app = Flask(__name__)
'''
app.config['MONGO_DBNAME'] = 'ml'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ml'
mongo = PyMongo(app)
'''


@app.route('/kube-api/graph', methods=['GET']) # http://localhost:5000/kube-api/graph
def get_graph():
    aToken =  "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWs5NzdyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI2YzRlMmQ2MS02ZDE2LTExZTktOTkwYi0wMDUwNTY5OTFkNGYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.VGvaz_JvrINzDXuDEUCYLK0PVWrgNq-iNpZLUuMoq5YiJSgcMsWfhZwzt0dqrdbrEzj53yMMy0SsSGc9aGRoYTxfdtUnCYYdpvoFsd14NiqBIBVbvglxjL6MhCFAX2nn-wUJH7PLyD5xdB0I2_ieg8Xl9hJe3lKHdeXypRsvi7X3H4j4lGs_ibPVYahHMvoJ4GOAw06HRt6zVhd8OVGXflmVkt0rgC_PsUrCCPMP38J4QSk1hcPt29TUJ7CsNIoE2r6uDShKI6IIq9MbkZy8_UuJvzTA39PWlj9rf_0iIZpkJlyT7kK_NBVQm6I9Ef7XCCJmqtlWDKsgGFUDzuZvAQ"

    aConfiguration = client.Configuration()

    aConfiguration.host = "https://130.65.159.69"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}


    aApiClient = client.ApiClient(aConfiguration)

    v1 = client.CoreV1Api(aApiClient)

    print("Listing pods with their IPs:")
    ret = v1.list_node(watch=False)
    print(ret)

    with open('data.json') as f:
        data = json.load(f)

        for i in ret.items:
            for j in data['nodes']:
                if i.metadata.name in j['id']:
                    j['memory'] = i.status.capacity['memory']
                    j['condition_NetworkUnavailable'] = i.status.conditions[0].status
                    j['condition_MemoryPressure'] = i.status.conditions[1].status
                    j['condition_DiskPressure'] = i.status.conditions[2].status
                    j['condition_PIDPressure'] = i.status.conditions[3].status
                    j['condition_Ready'] = i.status.conditions[4].status
                    j["status"] = j["condition_Ready"]
                    break


            temp ={}

            temp['id'] = i.metadata.name
            temp['IP'] = i.status.addresses[0].address
            temp['memoryUsage'] = i.status.capacity['memory']
            temp['architecture'] = i.status.node_info.architecture
            temp['machineID'] = i.status.node_info.machine_id
            temp['kernel_version'] = i.status.node_info.kernel_version
            temp['operating_system'] = i.status.node_info.operating_system
            temp['os_image'] = i.status.node_info.os_image
            temp['creation_timestamp'] = i.metadata.creation_timestamp
            temp['condition_NetworkUnavailable'] = i.status.conditions[0].status
            temp['condition_MemoryPressure'] = i.status.conditions[1].status
            temp['condition_DiskPressure'] = i.status.conditions[2].status
            temp['condition_PIDPressure'] = i.status.conditions[3].status
            temp['condition_Ready'] = i.status.conditions[4].status
            temp["status"] = temp["condition_Ready"]
            if i.metadata.name == "kubernetes-sdn-master":
                temp["parent"] = "null"
            else:
                temp["parent"] = "OpenVSwitch"
            data['nodes'].append(temp)

    count = 0
    for node in data["nodes"]:
        if count>1:
            edge_from_master = {
                "source": 1,
                "target": count
            }
            edge_from_switch = {
                "source": 0,
                "target": count
            }

            data['edges'].append(edge_from_switch)
        count = count+1

    return jsonify({'graph': data})

@app.route('/fetch_output_data', methods=['GET']) # http://localhost:5000/fetch_output_data
def get_output():
    app.config['MONGO_DBNAME'] = 'ml'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/ml'
    mongo = PyMongo(app)
    print(request.args.get('node'))
    result =[]
    output = mongo.db.output
    for x in output.find({'node':request.args.get('node')},{'_id':False}):
        result.append(x)

    attack_result =[]
    attack = mongo.db.attack
    for x in attack.find({'node':request.args.get('node')},{'_id':False}):
        attack_result.append(x)

    openv_result =[]
    openv = mongo.db.openv
    for x in openv.find({},{'_id':False}).limit(1).sort('_id',-1):
        openv_result.append(x)

    return jsonify({'output':result, 'attack':attack_result, 'openv_result': openv_result})

@app.route('/kube-api/pods', methods=['GET']) # http://localhost:5000/kube-api/graph
def get_pods():
    aToken =  "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWs5NzdyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI2YzRlMmQ2MS02ZDE2LTExZTktOTkwYi0wMDUwNTY5OTFkNGYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.VGvaz_JvrINzDXuDEUCYLK0PVWrgNq-iNpZLUuMoq5YiJSgcMsWfhZwzt0dqrdbrEzj53yMMy0SsSGc9aGRoYTxfdtUnCYYdpvoFsd14NiqBIBVbvglxjL6MhCFAX2nn-wUJH7PLyD5xdB0I2_ieg8Xl9hJe3lKHdeXypRsvi7X3H4j4lGs_ibPVYahHMvoJ4GOAw06HRt6zVhd8OVGXflmVkt0rgC_PsUrCCPMP38J4QSk1hcPt29TUJ7CsNIoE2r6uDShKI6IIq9MbkZy8_UuJvzTA39PWlj9rf_0iIZpkJlyT7kK_NBVQm6I9Ef7XCCJmqtlWDKsgGFUDzuZvAQ"

    aConfiguration = client.Configuration()

    aConfiguration.host = "https://130.65.159.69"
    aConfiguration.verify_ssl = False
    aConfiguration.api_key = {"authorization": "Bearer " + aToken}

    aApiClient = client.ApiClient(aConfiguration)

    v1 = client.CoreV1Api(aApiClient)
    ret = v1.list_pod_for_all_namespaces(watch=False)

    result = []
    for i in ret.items:
        temp ={}

        temp['name'] = i.metadata.name
        temp['namespace'] = i.metadata.namespace
        temp['timestamp'] = i.metadata.creation_timestamp
        temp['container_name'] = i.spec.containers[0].name
        temp['image_name'] = i.spec.containers[0].image
        temp['node'] = i.spec.node_name
        temp['host_ip'] = i.status.host_ip
        temp['pod_ip'] = i.status.pod_ip
        if i.spec.containers[0].ports is not None:
            temp['container_port'] = i.spec.containers[0].ports[0].container_port
            temp['protocol'] = i.spec.containers[0].ports[0].protocol
        else:
            temp['container_port'] = None
            temp['protocol'] = None

        if i.status.container_statuses is not None:
           if i.status.container_statuses[0] is not None:
               temp['start_time'] = i.status.container_statuses[0].state.running.started_at
               temp['terminated'] = i.status.container_statuses[0].state.terminated
               temp['waiting'] = i.status.container_statuses[0].state.waiting

        else:
            temp['start_time'] = None
            temp['terminated'] = None
            temp['waiting'] = None

        result.append(temp)
    print(result)
    return jsonify({'pods': result})

if __name__ == '__main__':
    app.run(debug=True)
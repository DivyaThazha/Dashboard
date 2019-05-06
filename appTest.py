#!venv/bin/python3
from flask import Flask, jsonify
from kubernetes import client, config
import json
import re

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
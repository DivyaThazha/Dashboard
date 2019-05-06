const express = require('express');
var cors = require('cors')
var bodyParser = require('body-parser')

const app = express();
app.use(cors());
app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true }));
const port = 5000;
obj={
    "graph": {
        "comment": "Network Graph",
        "edges": [
            {
                "source": 1,
                "target": 0
            },
            {
                "source": 1,
                "target": 2
            },
            {
                "source": 1,
                "target": 2
            },
            {
                "source": 1,
                "target": 3
            },
            {
                "source": 1,
                "target": 3
            },
            {
                "source": 1,
                "target": 4
            },
            {
                "source": 1,
                "target": 4
            }
        ],
        "nodes": [
            {
                "IP": "192.168.0.20",
                "id": "OpenVSwitch",
                "memoryUsage": 50,
                "role": "router",
                "root": true,
                "status": "True",
                "update": "up"
            },
            {
                "IP": "130.65.159.69",
                "architecture": "amd64",
                "condition_DiskPressure": "False",
                "condition_MemoryPressure": "False",
                "condition_NetworkUnavailable": "False",
                "condition_PIDPressure": "False",
                "condition_Ready": "True",
                "creation_timestamp": "Thu, 02 May 2019 00:08:27 GMT",
                "id": "kubernetes-sdn-master",
                "kernel_version": "4.10.0-42-generic",
                "machineID": "5f5999e547a74e8ba126e84fafdf4645",
                "memoryUsage": "32945828Ki",
                "operating_system": "linux",
                "os_image": "Ubuntu 16.04.5 LTS",
                "status": "True"
            },
            {
                "IP": "130.65.152.191",
                "architecture": "arm",
                "condition_DiskPressure": "False",
                "condition_MemoryPressure": "False",
                "condition_NetworkUnavailable": "False",
                "condition_PIDPressure": "False",
                "condition_Ready": "True",
                "creation_timestamp": "Thu, 02 May 2019 00:15:25 GMT",
                "id": "slave01",
                "kernel_version": "4.14.98-v7+",
                "machineID": "6dcf523fed9f461884cd0c2f810acb02",
                "memoryUsage": "949444Ki",
                "operating_system": "linux",
                "os_image": "Raspbian GNU/Linux 9 (stretch)",
                "status": "True"
            },
            {
                "IP": "130.65.156.248",
                "architecture": "arm",
                "condition_DiskPressure": "False",
                "condition_MemoryPressure": "False",
                "condition_NetworkUnavailable": "False",
                "condition_PIDPressure": "False",
                "condition_Ready": "True",
                "creation_timestamp": "Thu, 02 May 2019 00:11:39 GMT",
                "id": "slave02",
                "kernel_version": "4.14.98-v7+",
                "machineID": "3f555497ae274258b1bf411a0bc946c1",
                "memoryUsage": "949444Ki",
                "operating_system": "linux",
                "os_image": "Raspbian GNU/Linux 9 (stretch)",
                "status": "True"
            },
            {
                "IP": "130.65.152.218",
                "architecture": "arm",
                "condition_DiskPressure": "False",
                "condition_MemoryPressure": "False",
                "condition_NetworkUnavailable": "False",
                "condition_PIDPressure": "False",
                "condition_Ready": "True",
                "creation_timestamp": "Thu, 02 May 2019 00:18:37 GMT",
                "id": "slave03",
                "kernel_version": "4.14.98-v7+",
                "machineID": "cf7d2f0462ac4f3f9d384fab4bdd7948",
                "memoryUsage": "949444Ki",
                "operating_system": "linux",
                "os_image": "Raspbian GNU/Linux 9 (stretch)",
                "status": "True"
            }
        ]
    }
};







app.get('/kube-api/graph', (req, res) => {
    console.log("Get request /kube-api/graph");
    res.send(obj);
});

obj1 = {
    "name": "flare",
    "children": [
        {
            "name": "analytics",
            "children": [
                {
                    "name": "cluster",
                    "children": [
                        {"name": "AgglomerativeCluster", "size": 3938},
                        {"name": "CommunityStructure", "size": 3812},
                        {"name": "HierarchicalCluster", "size": 6714},
                        {"name": "MergeEdge", "size": 743}
                    ]
                },
                {
                    "name": "graph",
                    "children": [
                        {"name": "BetweennessCentrality", "size": 3534},
                        {"name": "LinkDistance", "size": 5731},
                        {"name": "MaxFlowMinCut", "size": 7840},
                        {"name": "ShortestPaths", "size": 5914},
                        {"name": "SpanningTree", "size": 3416}
                    ]
                },
                {
                    "name": "optimization",
                    "children": [
                        {"name": "AspectRatioBanker", "size": 7074}
                    ]
                }
            ]
        }
    ]
};
app.get('/kube-api/graph1', (req, res) => {
    console.log("Get request /kube-api/graph1");
    res.send(obj1);
});


app.listen(port, () => console.log(`Example app listening on port ${port}!`));


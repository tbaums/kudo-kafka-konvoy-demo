# Kudo Kafka on Konvoy Demo

_NB: This is a work in progress. PRs and issues are most welcome._

## Background

This demo is designed to show a simple container running in Konvoy writing to Kudo Kafka. Another container reads from the Kudo Kafka stream and outputs the Kafka messages to logs, which you can follow to demonstrate.


## Prereqs 

- Konvoy Kubernetes Cluster 1.13 or above
- Installed and configured kubectl with version 1.13 or later


## Step 1 - Install Kudo on Konvoy

```
./kudo-prereqs.sh
```

## Step 2 - Install Kudo CLI

```
brew tap kudobuilder/tap
brew install kudo-cli
```

## Step 3 - Launch Kafka Instance

```
kubectl kudo install kafka --all-dependencies
```

This will install both ZooKeeper and Kafka over the course of a few minutes.

## Step 4 - Find Kafka endpoint

```
kubectl describe service kafka-svc
```


Your output should look like the below:

```
» k describe service kafka-svc                                                
Name:              kafka-svc
Namespace:         default
Labels:            app=kafka
                   heritage=kudo
                   instance=kafka
                   phase=deploy-kafka
                   plan=deploy
                   planexecution=kafka-deploy-819232397
                   step=deploy
                   version=0.1.0
Annotations:       <none>
Selector:          app=kafka,heritage=kudo,instance=kafka,phase=deploy-kafka,plan=deploy,planexecution=kafka-deploy-819232397,step=deploy,version=0.1.0
Type:              ClusterIP
IP:                None
Port:              server  9093/TCP
TargetPort:        9093/TCP
Endpoints:         192.168.15.11:9093
Session Affinity:  None
Events:            <none>
```


## Step 5 - Edit `kafka-demo-generator-kudo.yaml`

Edit the `kafka-demo-generator-kudo.yaml` file to point to the endpoint you found in Step 4.

## Step 6 - Edit `kafka-demo-consumer-kudo.yaml`

Edite the `kafka-demo-consumer-kudo` file to point to the endpoint you found in Step 4.

## Step 7 - Deploy Generator and Consumer

```
kubectl apply -f kafka-demo-generator-kudo.yaml
kubectl apply -f kafka-demo-consumer-kudo.yaml
```

## Step 8 - Observe Kafka message read/write


Run `kubectl get pods` to find the pod ID of the pods for the generator and consumer service.

```
k get pods

NAME                                    READY   STATUS    RESTARTS   AGE
kafka-kafka-0                           1/1     Running   1          5h10m
kudo-kafka-consumer-77cdd9559f-h8rcs    1/1     Running   0          119s
kudo-kafka-generator-5c8f4784dc-vgxh9   1/1     Running   0          116s
zk-zk-0                                 1/1     Running   0          5h10m
zk-zk-1                                 1/1     Running   0          5h10m
zk-zk-2                                 1/1     Running   0          5h10m
```

Then, follow the logs for the consumer or generator pods to show reading/writing to Kafka.

```
k logs kudo-kafka-consumer-77cdd9559f-h8rcs --follow

Message: b'2019-06-21T16:18:20Z;5;0;3072'
Message: b'2019-06-21T16:18:29Z;2;4;9296'
Message: b'2019-06-21T16:18:30Z;6;3;6477'
Message: b'2019-06-21T16:18:31Z;2;0;4452'
Message: b'2019-06-21T16:18:32Z;4;1;7288'
Message: b'2019-06-21T16:18:37Z;9;1;7198'
Message: b'2019-06-21T16:18:39Z;2;0;9703'
Message: b'2019-06-21T16:18:46Z;1;2;1323'
Message: b'2019-06-21T16:18:48Z;3;6;5534'
Message: b'2019-06-21T16:18:55Z;3;4;1143'
Message: b'2019-06-21T16:18:58Z;7;9;217'
Message: b'2019-06-21T16:18:59Z;3;0;2691'
Message: b'2019-06-21T16:19:03Z;2;5;8785'
Message: b'2019-06-21T16:19:04Z;3;5;4883'
Message: b'2019-06-21T16:19:06Z;9;0;9543'
Message: b'2019-06-21T16:19:07Z;1;3;7573'
Message: b'2019-06-21T16:19:08Z;1;0;4322'
Message: b'2019-06-21T16:19:10Z;6;4;6676'
Message: b'2019-06-21T16:19:13Z;3;9;6500'
Message: b'2019-06-21T16:19:14Z;7;3;9239'
Message: b'2019-06-21T16:19:19Z;3;2;4910'
Message: b'2019-06-21T16:19:22Z;5;7;4644'
Message: b'2019-06-21T16:19:27Z;7;9;1764'
Message: b'2019-06-21T16:19:35Z;7;5;5065'
Message: b'2019-06-21T16:19:37Z;0;6;3450'
Message: b'2019-06-21T16:19:39Z;1;0;1103'
Message: b'2019-06-21T16:19:41Z;9;5;2869'
Message: b'2019-06-21T16:19:44Z;0;6;5505'
Message: b'2019-06-21T16:19:56Z;9;0;8393'
Message: b'2019-06-21T16:20:00Z;7;1;7710'
Message: b'2019-06-21T16:20:05Z;8;2;2603'
Message: b'2019-06-21T16:20:09Z;0;1;9885'

```
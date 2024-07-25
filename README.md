# House of quests 

A scalable platform for setting up hackatons, team events and coding competitions. The platform's primitives are strongly coupled with the corresponding Kubernetes primitives e.g.

- Team workspace <-> K8S workspace
- Task solution <-> K8S pod


## Repo strucuture

* _hoa-control-app_ Helm chart for the hoa controlling app
* _tasks_ folder with helm charts for single hoa tasks

## HOA structure

Teams operate in their own worskpaces which are represented by a corresponsing K8S workspace. All for the current team intended quests are being deployed as helm charts in the target workspace.

## How to start

### Prerequisite

1. **Install the necessary tooling.**
   * install docker desktop, enable kubernetes support 
     * https://www.docker.com/products/docker-desktop/
     * https://docs.docker.com/desktop/kubernetes/
   * install helm, add it to PATH
     * https://helm.sh/docs/intro/install/
   * install kubectl, add it to PATH
     * https://kubernetes.io/de/docs/tasks/tools/install-kubectl/
   * install kind, add it to PATH
     * https://kind.sigs.k8s.io/docs/user/quick-start/#installation

2. **Create a cluster using kind with the config below**
    ```sh
     kind create cluster --config cluster_config.yaml
    ```
   _Hint:_ using port 80 requires administrator rights, so you might want to choose a number with 4 digits.
### Control app

Run the following command from the _hoa-control-app_ folder.
If the target workspace not exists.

```sh
helm install control -n {TEAM_NAME} --create-namespace .
```

If the workspace already exists
```sh
helm install control -n {TEAM_NAME} .
```


### How to deploy a task

Wheather there is no dedicated k8s workspace, run the following command from the according helm task subfolder. The parameter task.impl.image.repo is required 
```sh
helm install {TASK_NAME} . -n {TEAM_NAME} --create-namespace --set task.impl.image.repo=dockerRepository
```

If the workspace already exists
```sh
helm install {TASK_NAME} -n {TEAM_NAME} --set task.impl.image.repo=dockerRepository .
```


### Metrics

The hoa control app exposes measurements e.g. amount of solved task etc. This metrics can be monitored, aggregated and visualized by monitoring systems like prometheus, influxdb etc. pp. 
The for prometheus required labels are already added to the hoa pod so that the metrics can already be scrapped by prometheus. To install the prometheus community version run the following command 

```sh
helm install prometheus prometheus-community/prometheus
```

### KIND
#### nginx ingress controller

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

#### Kind example configuration

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
```

## Example startup script

**To run the setup for 2 teams, run the following commands:**

```sh
kubectl create namespace team1 
kubectl create namespace team2

# start the control app per team
helm install control hoa_helm/hoa-control-app -n team1
helm install control hoa_helm/hoa-control-app -n team2

# start every task for each team
helm install task1 hoa_helm/tasks/filecheck -n team1 --set task.impl.image.repo=dockerRepository
helm install task1 hoa_helm/tasks/filecheck -n team2 --set task.impl.image.repo=dockerRepository

helm install task2 hoa_helm/tasks/echo_server1 -n team1 --set task.impl.image.repo=dockerRepository
helm install task2 hoa_helm/tasks/echo_server1 -n team2 --set task.impl.image.repo=dockerRepository

helm install task3 hoa_helm/tasks/echo_server2 -n team1 --set task.impl.image.repo=dockerRepository
helm install task3 hoa_helm/tasks/echo_server2 -n team2 --set task.impl.image.repo=dockerRepository


 
```

**After this, your deployment should look like this:**
```text
> helm list -A
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
control team1           1               2024-07-25 13:21:27.104043 +0200 CEST   deployed        hoa_helm-0.1.0                  1.16.0
control team2           1               2024-07-25 13:21:27.6455303 +0200 CEST  deployed        hoa_helm-0.1.0                  1.16.0
task1   team1           1               2024-07-25 13:27:33.4222118 +0200 CEST  deployed        filecheck-0.1.0                 1.16.0
task1   team2           1               2024-07-25 13:27:35.039713 +0200 CEST   deployed        filecheck-0.1.0                 1.16.0
task2   team1           1               2024-07-25 13:27:40.3268046 +0200 CEST  deployed        echo-server-0.1.0               1.16.0
task2   team2           1               2024-07-25 13:27:40.9290248 +0200 CEST  deployed        echo-server-0.1.0               1.16.0
task3   team1           1               2024-07-25 13:27:41.4515664 +0200 CEST  deployed        echo-server-advanced-0.1.0      1.16.0
task3   team2           1               2024-07-25 13:27:41.9799056 +0200 CEST  deployed        echo-server-advanced-0.1.0      1.16.0
```
**And the pods for each namespace look like this:**
```text
> kubectl get pods -n team1
NAME                                                READY   STATUS                  RESTARTS   AGE
hoa-control-app-8d47565ff-xfszx                     1/1     Running                 0          7m30s
hoa-control-app-landingpage-846c45c885-585jp        1/1     Running                 0          7m30s
task1-filecheck-check-28698448-rdbvd                0/1     Init:ImagePullBackOff   0          57s
task1-filecheck-descr-78d985944d-qvmf7              1/1     Running                 0          84s
task2-echo-server-check-28698448-p2mjs              0/3     Error                   0          57s
task2-echo-server-descr-56d55fc7d9-gkbvx            1/1     Running                 0          77s
task2-echo-server-impl-9cc859467-xg7gt              0/1     ContainerCreating       0          4s
task2-echo-server-reaper-28698448-lnxkv             0/1     Completed               0          57s
task3-echo-server-advanced-check-28698448-kwftb     0/5     Error                   0          57s
task3-echo-server-advanced-descr-66dbcbdd69-wpcdn   1/1     Running                 0          76s
task3-echo-server-advanced-impl-58bd84c684-cslqm    0/1     ContainerCreating       0          3s
task3-echo-server-advanced-reaper-28698448-v57b5    0/1     Completed               0          57s
```

### clean up
To remove the namespaces, run a delete per name 
```sh
kubectl delete namespace team1 
kubectl delete namespace team2

```
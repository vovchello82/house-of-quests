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
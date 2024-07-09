# House of quests 

A scalable platform for setting up hackatons, team events and coding competitions.

## Repo strucuture

* _hoa-control-app_ Helm chart for the hoa controlling app
* _tasks_ folder with helm charts for single hoa tasks

## HOA structure

Team operate in their own worskpaces which are represented by a corresponsing K8S workspace. All for the current team intended quests are being deployed as helm charts in the target workspace.

Team workspace <-> K8S workspace


### How to deploy a task

Wheather there is no dedicated k8s workspace, run the following command from the according helm task subfolder
`helm install {TASK_NAME} . -n {TEAM_NAME} --create-namespace`
If the workspace exists
`helm install {TASK_NAME} . -n {TEAM_NAME}`

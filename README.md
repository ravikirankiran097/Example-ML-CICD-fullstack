## ML Example App
### An Example of how to deploy ML model and scale with kubernetes

## Requirements: Docker & Kubernetes
Ensure that your kubectl is connected to a kubernetes cluster
This can be done by modifying your kubectl config
with a system path pointing to KUBECONFIG
### Private Docker Registry
You must have a docker registry for the docker images to be sent to.
indicate the host to your docker registry in the file `docker-registry-address`

## Local kubernetes setup
If you dont have a kubernetes cluster, try microk8s
And then install kubectl separately:
#### Configure your kubectl with
`cat microk8s.config >> ~/.kube/config`
Then add `export KUBECONFIG=~/.kube/config`
into your bashrc
#### Installing Docker Registry
On microk8s, enable docker registry with 
`microk8s.enable registry`

## Allowing docker to push to private docker registry
Add the address of the docker private registry into your insecure-registries
E.g http://localhost:32000
For Mac/Windows:

```open the settings, goto the daemon tab and then pop in your registry’s URL in the “Insecure registries”``` 
Restart docker

#### For Ubuntu:
 
vim `/etc/docker/daemon.json`
```
{
    "insecure-registries" : ["localhost:32000"]
}
```
Restart your docker service with systemctl restart docker

## Installation instructions
Just run the included install.sh file

`sh install.sh`

## Removal
Just run the included uninstall.sh file

`sh uninstall.sh`

# Features
1. Frontend --> UI built with ReactJS to request predictions
2. Backend --> Backend built with Python Flask for 
            
            sanitize inputs
            Track & record predictions
            REST API for model serving
            Requests Model Serving API
            REST API for past predictions
            
3. Mushroom Model --> ML Pipeline built with MLFlow
 
          Website for viewing model training / track models
          WorkFlow for Training and deploying model
          Model trained as a container
          Model deployed as an isolated container
          
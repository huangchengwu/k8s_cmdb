# k8s操作模块

from kubernetes import client, config


config.kube_config.load_kube_config(
    config_file="/root/.kube/config")


# 获取所有命名空间
def getnamespace():
    arry = []
    v1 = client.CoreV1Api()
    for ns in v1.list_namespace().items:
        arry.append(ns.metadata.name)
    return arry


# 获取pod
def getpod(n):
    arry = []
    v1 = client.CoreV1Api()
    pod = v1.list_namespaced_pod(namespace=n, watch=False)
    for i in pod.items:
        pod_info = {}
        pod_info["ip"] = i.status.pod_ip
        pod_info["namespace"] = i.metadata.namespace
        pod_info["metadata_name"] = i.metadata.name
        arry.append(pod_info)

    return arry


# 获取deployment


def getdeployment(n):
    arry = []
    v1 = client.AppsV1Api()
    deployment = v1.list_namespaced_deployment(namespace=n, watch=False)

    for i in deployment.items:
        dep_info = {}
        for a in i.status.conditions:

            dep_info["start_time"] = a.last_transition_time
            dep_info["update_time"] = a.last_update_time
            dep_info["status"] = a.status

        for b in i.spec.template.spec.containers:

            dep_info["image"] = b.image

        dep_info["replicas"] = i.status.updated_replicas
        dep_info["replicas_status"] = i.status.replicas
        dep_info["unavailable"] = i.status.unavailable_replicas
        dep_info["match_labels"] = i.spec.selector.match_labels

        arry.append(dep_info)

    return arry

# 获取服务


def getservice(n):
    arry = []
    v1 = client.CoreV1Api()
    service = v1.list_namespaced_service(namespace=n, watch=False)
    for i in service.items:
        svc_info = {}
        svc_info["service_name"] = i.metadata.name
        svc_info["start_time"] = i.metadata.creation_timestamp
        svc_info["cluster_ip"] = i.spec.cluster_ip
        svc_info["ports"] = i.spec.ports
        svc_info["selector"] = i.spec.selector
        svc_info["type"] = i.spec.type

        arry.append(svc_info)

    return arry

# 获取弹性伸缩


def gethpa():
    pass

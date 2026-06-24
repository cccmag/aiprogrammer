#!/usr/bin/env python3
"""Kubernetes Demo: Generate K8s YAML configurations"""

import yaml


def generate_deployment(name, image, replicas=2):
    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'labels': {'app': name}
        },
        'spec': {
            'replicas': replicas,
            'selector': {'matchLabels': {'app': name}},
            'template': {
                'metadata': {'labels': {'app': name}},
                'spec': {
                    'containers': [{
                        'name': name,
                        'image': image,
                        'ports': [{'containerPort': 80}],
                        'livenessProbe': {
                            'httpGet': {'path': '/health', 'port': 80},
                            'initialDelaySeconds': 3,
                            'periodSeconds': 3
                        },
                        'readinessProbe': {
                            'httpGet': {'path': '/health', 'port': 80},
                            'initialDelaySeconds': 5,
                            'periodSeconds': 5
                        },
                        'resources': {
                            'limits': {'memory': '256Mi', 'cpu': '500m'},
                            'requests': {'memory': '128Mi', 'cpu': '100m'}
                        }
                    }]
                }
            }
        }
    }
    return yaml.dump(deployment)


def generate_service(name, service_type='ClusterIP'):
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {'name': name},
        'spec': {
            'type': service_type,
            'selector': {'app': name},
            'ports': [{'protocol': 'TCP', 'port': 80, 'targetPort': 80}]
        }
    }
    return yaml.dump(service)


def generate_configmap(name, data):
    configmap = {
        'apiVersion': 'v1',
        'kind': 'ConfigMap',
        'metadata': {'name': name},
        'data': data
    }
    return yaml.dump(configmap)


def generate_ingress(name, host, service_name):
    ingress = {
        'apiVersion': 'networking.k8s.io/v1',
        'kind': 'Ingress',
        'metadata': {
            'name': name,
            'annotations': {'nginx.ingress.kubernetes.io/rewrite-target': '/'}
        },
        'spec': {
            'rules': [{
                'host': host,
                'http': {
                    'paths': [{
                        'path': '/',
                        'pathType': 'Prefix',
                        'backend': {
                            'service': {'name': service_name, 'port': {'number': 80}}
                        }
                    }]
                }
            }]
        }
    }
    return yaml.dump(ingress)


def demo():
    print("=== Kubernetes YAML Generator ===\n")
    print("Deployment:")
    print(generate_deployment('myapp', 'myregistry/myapp:latest'))
    print("\nService:")
    print(generate_service('myapp', 'LoadBalancer'))
    print("\nConfigMap:")
    print(generate_configmap('myapp-config', {'DATABASE_HOST': 'db-service', 'LOG_LEVEL': 'info'}))
    print("\nIngress:")
    print(generate_ingress('myapp-ingress', 'myapp.example.com', 'myapp'))


if __name__ == "__main__": demo()
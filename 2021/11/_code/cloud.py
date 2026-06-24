import time
import random
from typing import List, Dict, Optional


class Container:
    def __init__(self, name: str, image: str):
        self.name = name
        self.image = image
        self.status = "running"
        self.ports = []
        self.env = {}
        self.resources = {"cpu": "100m", "memory": "128Mi"}

    def __repr__(self):
        return f"Container({self.name}, {self.image}, {self.status})"


class Service:
    def __init__(self, name: str, selector: Dict[str, str]):
        self.name = name
        self.selector = selector
        self.containers: List[Container] = []
        self.port = 80

    def add_container(self, container: Container):
        if self._matches_selector(container):
            self.containers.append(container)

    def _matches_selector(self, container: Container) -> bool:
        return True

    def get_endpoints(self) -> List[str]:
        healthy = [c for c in self.containers if c.status == "running"]
        return [f"{self.name}-{i}" for i in range(len(healthy))]

    def __repr__(self):
        return f"Service({self.name}, {len(self.containers)} containers)"


class ServiceDiscovery:
    def __init__(self):
        self.services: Dict[str, Service] = {}

    def register(self, service: Service):
        self.services[service.name] = service
        print(f"Service registered: {service.name}")

    def discover(self, name: str) -> Optional[Service]:
        return self.services.get(name)

    def list_services(self) -> List[str]:
        return list(self.services.keys())


class LoadBalancer:
    def __init__(self):
        self.current_index = 0

    def distribute(self, endpoints: List[str]) -> str:
        if not endpoints:
            raise ValueError("No endpoints available")
        endpoint = endpoints[self.current_index]
        self.current_index = (self.current_index + 1) % len(endpoints)
        return endpoint


class Node:
    def __init__(self, name: str, capacity: int = 4):
        self.name = name
        self.capacity = capacity
        self.containers: List[Container] = []

    def can_schedule(self, container: Container) -> bool:
        return len(self.containers) < self.capacity

    def schedule(self, container: Container) -> bool:
        if self.can_schedule(container):
            self.containers.append(container)
            return True
        return False


class SimpleOrchestrator:
    def __init__(self):
        self.nodes: List[Node] = []
        self.containers: List[Container] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def schedule_container(self, container: Container) -> Optional[Node]:
        for node in self.nodes:
            if node.schedule(container):
                self.containers.append(container)
                return node
        return None

    def list_containers(self) -> List[Container]:
        return self.containers


def demo():
    print("=== Container Demo ===")
    container = Container("web-1", "myapp:latest")
    print(f"Created: {container}")

    print("\n=== Service Discovery Demo ===")
    sd = ServiceDiscovery()

    service = Service("myapp", {"app": "myapp"})
    service.add_container(container)
    sd.register(service)

    discovered = sd.discover("myapp")
    print(f"Discovered service: {discovered}")

    print("\n=== Load Balancer Demo ===")
    lb = LoadBalancer()
    endpoints = ["pod-1", "pod-2", "pod-3"]

    for i in range(6):
        endpoint = lb.distribute(endpoints)
        print(f"Request {i+1} -> {endpoint}")

    print("\n=== Orchestrator Demo ===")
    orch = SimpleOrchestrator()
    orch.add_node(Node("node-1"))
    orch.add_node(Node("node-2"))

    for i in range(3):
        c = Container(f"app-{i}", "myapp:v1")
        node = orch.schedule_container(c)
        print(f"Scheduled {c.name} on {node.name}")

    print(f"\nTotal containers: {len(orch.list_containers())}")

    print("\n=== Service Endpoints Demo ===")
    service = Service("api", {})
    for i in range(3):
        c = Container(f"api-{i}", "api:latest")
        service.add_container(c)

    endpoints = service.get_endpoints()
    print(f"Service endpoints: {endpoints}")

    print("\nDemo OK")


if __name__ == "__main__":
    demo()
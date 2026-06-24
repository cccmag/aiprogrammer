#!/usr/bin/env python3
"""2015 年度精選技術展示"""

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def demo_tensorflow():
    print_header("TensorFlow 模擬展示")

    class SimpleNN:
        def __init__(self):
            self.weights = [0.5, -0.5]
            self.bias = 0.1

        def predict(self, x):
            return sum(w * v for w, v in zip(self.weights, x)) + self.bias

        def train(self, X, y, epochs=10):
            for epoch in range(epochs):
                for x, target in zip(X, y):
                    pred = self.predict(x)
                    error = pred - target
                    print(f"Epoch {epoch+1}: Input {x}, Pred {pred:.4f}, Target {target}")

    X = [[1.0, 2.0], [2.0, 1.0], [0.5, 1.5]]
    y = [3.0, 3.0, 2.0]

    print("Training simple neural network...")
    nn = SimpleNN()
    nn.train(X, y, epochs=3)

def demo_react_components():
    print_header("React 元件模擬展示")

    class Component:
        def __init__(self, name):
            self.name = name
            self.props = {}
            self.state = {}

        def set_state(self, new_state):
            self.state.update(new_state)
            print(f"{self.name} state updated: {self.state}")

        def render(self):
            return f"<{self.name}>{self.props.get('children', '')}</{self.name}>"

    # 模擬 React 應用
    app = Component("App")
    app.props = {"children": "Hello from 2015!"}

    header = Component("Header")
    header.props = {"children": "AI 程式人雜誌"}

    content = Component("Content")
    content.set_state({"items": ["Web", "Mobile", "Cloud", "AI"]})

    print(f"\n{app.render()}")
    print(f"  {header.render()}")
    print(f"  {content.render()}")

def demo_docker_compose():
    print_header("Docker Compose 範例")

    compose_content = """
version: '3'
services:
  web:
    image: nginx:1.9
    ports:
      - "80:80"
    environment:
      - APP_ENV=production

  app:
    build: .
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://db:5432/app

  db:
    image: postgres:9.4
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
"""
    print(compose_content)

def demo_swift_syntax():
    print_header("Swift 語法展示")

    swift_code = """
import Foundation

// 結構體
struct User {
    let name: String
    let email: String
    var isActive: Bool = true
}

// 枚舉
enum Status {
    case active
    case inactive
    case pending
}

// 函數
func greet(_ user: User) -> String {
    return "Hello, \\(user.name)!"
}

// 使用
let user = User(name: "John", email: "john@example.com")
print(greet(user))
"""
    print(swift_code)

def demo_rust_syntax():
    print_header("Rust 語法展示")

    rust_code = """
fn main() {
    // 不可變變數
    let x = 5;

    // 可變變數
    let mut y = 10;
    y += x;

    // 所有權
    let s1 = String::from("hello");
    let s2 = s1;  // s1 被移動到 s2

    // 借用
    let len = calculate_length(&s2);
    println!("Length of '{}' is {}", s2, len);

    // 匹配
    match x {
        1 => println!("one"),
        2..=5 => println!("two to five"),
        _ => println!("other"),
    }
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
"""
    print(rust_code)

def demo_kubernetes():
    print_header("Kubernetes YAML 範例")

    k8s_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.9
        ports:
        - containerPort: 80
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
"""
    print(k8s_yaml)

def main():
    print("=" * 60)
    print("2015 年度精選技術展示")
    print("=" * 60)

    demo_tensorflow()
    demo_react_components()
    demo_docker_compose()
    demo_swift_syntax()
    demo_rust_syntax()
    demo_kubernetes()

    print("\n" + "=" * 60)
    print("2015 年度回顧完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
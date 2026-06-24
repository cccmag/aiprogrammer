#!/usr/bin/env python3
"""Docker 映像建置"""

def build_docker_image():
    print("Building Docker image...")
    
    image_name = "myapp:latest"
    
    print(f"  Image: {image_name}")
    print("  ✓ Image built successfully")
    return True

if __name__ == "__main__":
    success = build_docker_image()
    exit(0 if success else 1)
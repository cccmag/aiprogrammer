# Ansible 自動化設定

## 前言

Ansible 是簡單而強大的自動化工具，用於設定管理、應用部署與任務自動化。2016 年的 Ansible 2.0 帶來更多功能與穩定性。

## 安裝與基本設定

```bash
pip install ansible
ansible --version
```

## Inventory 檔案

```ini
# inventory/hosts
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=ubuntu
web2 ansible_host=192.168.1.11 ansible_user=ubuntu

[dbservers]
db1 ansible_host=192.168.1.20 ansible_user=ubuntu

[webservers:vars]
http_port=80
```

## Playbook 基本語法

```yaml
# site.yml
---
- hosts: webservers
  become: yes
  vars:
    app_version: "1.0.0"
  
  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Copy nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify:
        - Restart nginx
    
    - name: Deploy application
      git:
        repo: https://github.com/org/myapp.git
        dest: /var/www/myapp
        version: "{{ app_version }}"
    
    - name: Install npm dependencies
      npm:
        path: /var/www/myapp
      when: ansible_facts['os_family'] == "Debian"
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

## Jinja2 範本

```j2
# nginx.conf.j2
user www-data;
worker_processes {{ ansible_processor_vcpus }};

events {
    worker_connections 1024;
}

http {
    server {
        listen {{ http_port }};
        server_name {{ inventory_hostname }};
        
        location / {
            root {{ doc_root }};
            index index.html;
        }
        
        location /api {
            proxy_pass http://localhost:8000;
        }
    }
}
```

## 角色（Roles）

```bash
# 建立角色結構
ansible-galaxy init myrole
```

```yaml
# roles/myrole/tasks/main.yml
---
- name: Ensure required packages
  apt:
    name: "{{ packages }}"
    state: present
  vars:
    packages:
      - curl
      - git
```

```yaml
# playbook.yml
---
- hosts: webservers
  roles:
    - common
    - nginx
    - myapp
```

## 條件與迴圈

```yaml
- name: Install packages based on OS
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - git
    - curl
    - vim
  when: ansible_facts['os_family'] == "Debian"

- name: Create users
  user:
    name: "{{ item.name }}"
    state: "{{ item.state | default('present') }}"
  loop:
    - { name: 'user1', state: 'present' }
    - { name: 'user2', state: 'present' }
```

## 變數與 Vault

```bash
# 建立加密檔案
ansible-vault create vars/secrets.yml

# 編輯加密檔案
ansible-vault edit vars/secrets.yml

# 在 playbook 中使用
ansible-playbook site.yml --ask-vault-pass
```

```yaml
# vars/secrets.yml (加密)
db_password: "super_secret_password"
api_key: "your_api_key_here"
```

## Ansible Galaxy

```bash
# 搜尋角色
ansible-galaxy search nginx

# 安裝角色
ansible-galaxy install geerlingguy.nginx

# 使用角色
# roles/requirements.yml
- src: geerlingguy.nginx
  version: "3.1.0"
```

```bash
# 安裝所有角色
ansible-galaxy install -r roles/requirements.yml
```

## 延伸閱讀

- [Ansible 官方文檔](https://www.google.com/search?q=ansible+tutorial+2016)
- [Ansible Playbook 教學](https://www.google.com/search?q=ansible+playbook+tutorial+2016)
- [Ansible Roles 最佳實踐](https://www.google.com/search?q=ansible+roles+best+practices+2016)

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*
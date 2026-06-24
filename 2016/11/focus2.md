# Jenkins 2.0 與 Pipeline（2016）

## 前言

Jenkins 2.0 是十年來最大更新，引入了 Pipeline as Code，大幅提升 CI/CD 工作流的定義與維護性。

## Jenkins Pipeline 語法

### 基本結構

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DEPLOY_ENV = 'staging'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/**/*.xml'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                echo 'Deploying to production...'
                sh './deploy.sh production'
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#devops',
                      message: "Build #${env.BUILD_NUMBER} succeeded!"
        }
        failure {
            slackSend channel: '#devops',
                      message: "Build #${env.BUILD_NUMBER} failed!"
        }
    }
}
```

## 進階 Pipeline 功能

### 平行執行

```groovy
pipeline {
    stages {
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }
                stage('E2E Tests') {
                    steps {
                        sh 'npm run test:e2e'
                    }
                }
            }
        }
    }
}
```

### 條件執行

```groovy
pipeline {
    stages {
        stage('Deploy') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        sh './deploy.sh production'
                    } else if (env.BRANCH_NAME == 'develop') {
                        sh './deploy.sh staging'
                    } else {
                        echo 'Skipping deployment for feature branches'
                    }
                }
            }
        }
    }
}
```

### 參數化 Pipeline

```groovy
pipeline {
    parameters {
        choice(name: 'DEPLOY_ENV',
               choices: ['development', 'staging', 'production'],
               description: 'Select deployment environment')
        booleanParam(name: 'RUN_TESTS',
                     defaultValue: true,
                     description: 'Run tests before deployment')
        string(name: 'VERSION',
               defaultValue: '',
               description: 'Specific version to deploy (optional)')
    }
    
    stages {
        stage('Deploy') {
            steps {
                echo "Deploying to ${params.DEPLOY_ENV}"
                sh "./deploy.sh ${params.DEPLOY_ENV}"
            }
        }
    }
}
```

## Jenkins Pipeline 共享庫

### 定義共享庫

```groovy
// vars/deploy.groovy
def call(Map config) {
    pipeline {
        stages {
            stage("Deploy ${config.env}") {
                steps {
                    sh "./deploy.sh ${config.env}"
                }
            }
        }
    }
}
```

### 使用共享庫

```groovy
// Jenkinsfile
@Library('my-shared-library') _

pipeline {
    stages {
        stage('Deploy') {
            steps {
                deploy(env: 'production', version: '1.0.0')
            }
        }
    }
}
```

## 指令 Pipeline

對於簡單的 CI 流程，Jenkins 也支援指令式設定：

```groovy
node {
    stage('Source') {
        checkout scm
    }
    stage('Build') {
        sh 'npm install'
        sh 'npm run build'
    }
    stage('Test') {
        sh 'npm test'
    }
    stage('Deploy') {
        sh './deploy.sh'
    }
}
```

## Jenkins 設定即程式碼

```yaml
# configuration.yaml
jenkins:
  systemMessage: "Jenkins 2.0 - Pipeline as Code"
  numExecutors: 4
  mode: NORMAL
  
  security:
    remoting:
      enabled: true
    queueItemAuthenticator:
      enabled: true
      
  globalLibraries:
    - name: shared-library
      defaultVersion: "master"
      retriever:
        modernSCM:
          scm:
            git:
              remote: https://github.com/org/shared-library.git
```

## Docker 整合

```groovy
pipeline {
    agent {
        docker {
            image 'node:6-alpine'
            args '-v /workspace:/workspace'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/**/*.xml'
                }
            }
        }
    }
}
```

## 延伸閱讀

- [Jenkins Pipeline 文檔](https://www.google.com/search?q=jenkins+pipeline+tutorial+2016)
- [Jenkinsfile 範例](https://www.google.com/search?q=jenkinsfile+examples+2016)
- [Jenkins 2.0 新功能](https://www.google.com/search?q=jenkins+2.0+new+features+2016)

## 結語

Jenkins 2.0 的 Pipeline as Code 讓 CI/CD 流程的版本控制與協作變得簡單，是 DevOps 工程師必備技能。

---

*本篇文章為「AI 程式人雜誌 2016 年 11 月號」DevOps 系列之一。*
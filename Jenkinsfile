pipeline {
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    agent {
        label 'karrots'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                container('python') {
                    script {
                        sh """
                          pip install -r src/requirements.txt
                          pip install pylint
                        """
                    }
                }
            }
        }
        stage('Linting') {
            steps {
                container('python') {
                    script {
                        sh """
                          pylint **/*.py
                        """
                    }
                }
            }
        }
        stage('Unit Testing') {
            steps {
                container('python') {
                    script {
                        sh """
                          python -m unittest discover -s tests/unit
                        """
                    }
                }
            }
        }
        stage('Docker Build') {
            tools {
                dockerTool 'docker'
            }
            steps {
                container('python') {
                    script {
                        docker.withRegistry("https://${env.CONTAINER_REGISTRY}", "${env.CONTAINER_REGISTRY_CREDENTIAL_ID}") {
                            def dockerImage = docker.build("${env.CONTAINER_REGISTRY}:${env.BUILD_ID}")
                            dockerImage.push()
                        }
                    }
                }
            }
        }
    }
    post {
        failure {
            script {
                msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"
                //slackSend message: msg, channel: env.SLACK_CHANNEL
            }
        }
    }
}
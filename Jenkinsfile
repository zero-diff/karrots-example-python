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
            environment {
                PASSWORD = ""
            }
            steps {
                container('aws-cli') {
                    script {
                        withEnv(["PASSWORD=`aws ecr get-login-password --region us-west-1`"]) {
                            sh """#!/bin/bash
                            docker login --username AWS --password $env.PASSWORD 678685898948.dkr.ecr.us-west-1.amazonaws.com
                            docker build -t "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}" .
                            docker push "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}"
                            """
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
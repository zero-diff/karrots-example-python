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
            steps {
                container('python') {
                    script {
                        def dockerHome = tool 'docker'
                        sh """#!/bin/sh 
                          ${dockerHome}/bin/docker build . --no-cache --network=host -t zerodiff/karrots-example-python:${env.BUILD_ID}
                          ${dockerHome}/bin/docker push ${env.CONTAINER_REPO}
                        """
                    }
                }
            }
        }
    }
    post {
        failure {
            script {
                msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"

//        slackSend message: msg, channel: env.SLACK_CHANNEL
            }
        }
    }
}
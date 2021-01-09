pipeline {
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    agent {
        label 'karrots'
    }
    triggers {
        GenericTrigger(
                regexpFilterExpression: 'refs/tags/*',
                regexpFilterText: '$ref',
                genericVariables: [
                        [key: 'ref', value: '$.ref']
                ],
                causeString: 'Triggered on tag: $ref',
                token: '123456',
                tokenCredentialId: '',
                printContributedVariables: true,
                printPostContent: true,
                silentResponse: false,
        )
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
        stage('Docker Build and Push') {
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
                            try {
                                sh """#!/bin/bash
                                docker login --username AWS --password $env.PASSWORD ${env.CONTAINER_REGISTRY}
                                docker build --network=host -t "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}" .
                                docker push "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}"
    
                                if [ ! -z "$ref" ]
                                then
                                    IFS='/' read -r -a array <<< "${ref}"
                                    docker tag "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}" "${env.CONTAINER_REGISTRY}:${array[2]}"
                                    docker push "${env.CONTAINER_REGISTRY}:${array[2]}"
                                fi
                                """
                            }
                            catch(Exception e) {
                                println("Exception: ${e}")
                            }
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
def String[] refParsed = new String[3]

pipeline {
    parameters { string(name: 'ref', defaultValue: '', description: 'Used to automatically tag built docker images based on git tag. Leave blank for manual builds.') }
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
                        [key: 'ref', value: '$.ref', defaultValue: '']
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
                          cd src && pylint **/*.py
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
                          cd src && python -m unittest discover -s ../tests/unit
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
                                script {
                                    tag="\$(echo ${params.ref} | cut -d'/' -f3)"
                                }
                                sh """#!/bin/bash
                                docker login --username AWS --password $env.PASSWORD ${env.CONTAINER_REGISTRY}
                                docker build --network=host -t "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}" .
                                docker push "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}"

                                if [ ! -z "${params.ref}" ]
                                then
                                    docker tag "${env.CONTAINER_REGISTRY}:${env.BUILD_ID}" "${env.CONTAINER_REGISTRY}:${tag}"
                                    docker push "${env.CONTAINER_REGISTRY}:${tag}"
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

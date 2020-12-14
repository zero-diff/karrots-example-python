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
        script {
          sh """
          pip install -r src/requirements.txt
          pip install pylint
          """
        }
      }
    }
    stage('Linting') {
      steps {
        script {
          sh """
          pylint **/*.py
          """
        }
      }
    }
    stage('Unit Testing') {
      steps {
        script {
          sh """
          python -m unittest discover -s tests/unit
          """
        }
      }
    }
    stage('Docker Build') {
      agent none
      steps {
        script {
          def dockerHome = tool 'docker'
          sh """
          ${dockerHome}/bin/docker build . -t gadgetworks/karrots-example-python:0.1.0
          """
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
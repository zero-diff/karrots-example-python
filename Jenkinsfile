pipeline {
//  options {
//    buildDiscarder(logRotator(numToKeepStr: '10')) // Retain history on the last 10 builds
//    ansiColor('xterm') // Enable colors in terminal
//    timestamps() // Append timestamps to each line
//    timeout(time: 20, unit: 'MINUTES') // Set a timeout on the total execution time of the job
//  }
  agent {
    // Run this job within a Docker container built using Dockerfile.build
    // contained within your projects repository. This image should include
    // the core runtimes and dependencies required to run the job,
    // for example Python 3.x and NPM.
    docker { image 'python:3.9.1' }
  }
  stages {  // Define the individual processes, or stages, of your CI pipeline
    stage('Checkout') { // Checkout (git clone ...) the projects repository
      steps {
        checkout scm
      }
    }
    stage('Setup') { // Install any dependencies you need to perform testing
      steps {
        script {
          sh """
          pip install -r src/requirements.txt
          pip install pylint
          """
        }
      }
    }
    stage('Linting') { // Run pylint against your code
      steps {
        script {
          sh """
          pylint **/*.py
          """
        }
      }
    }
    stage('Unit Testing') { // Perform unit testing
      steps {
        script {
          sh """
          python -m unittest discover -s tests/unit
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
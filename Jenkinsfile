@Library('platform-shared-library@v1') _

pipeline {
    agent any
    environment {
        ECR_REGISTRY   = '267423569109.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = 'shopeasy-order-service'
        SERVICE_NAME   = 'order-service'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                checkoutPlatformDeps()
            }
        }
        stage('Secret Scan') { steps { secretScan() } }
        stage('Unit Tests') { steps { sh 'pip install -r requirements.txt pytest && pytest tests/ -v || true' } }
        stage('Build Once') {
            steps {
                script {
                    env.GIT_SHA = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "1.0.0-${env.GIT_SHA}"
                    env.LOCAL_IMAGE = "${ECR_REPOSITORY}:${env.IMAGE_TAG}"
                    dockerBuild imageName: env.LOCAL_IMAGE
                }
            }
        }
        stage('Trivy') { steps { trivyScan imageRef: env.LOCAL_IMAGE } }
        stage('Push') {
            steps {
                script {
                    generateSBOM imageRef: env.LOCAL_IMAGE
                    cosignSign imageRef: env.LOCAL_IMAGE
                    env.IMAGE_DIGEST = pushToEcr(imageRef: env.LOCAL_IMAGE, repository: env.ECR_REPOSITORY, tag: env.IMAGE_TAG)
                }
            }
        }
        stage('Deploy Dev') {
            steps {
                deployHelm release: env.SERVICE_NAME, namespace: 'shopeasy-dev',
                    valuesFile: 'helm-charts/values-dev.yaml',
                    imageRepository: "${ECR_REGISTRY}/${ECR_REPOSITORY}",
                    imageTag: env.IMAGE_TAG, imageDigest: env.IMAGE_DIGEST, servicePort: 5001
            }
        }
    }
    post { always { cleanWs() } failure { notifySlack color: 'danger', message: "Failed: ${SERVICE_NAME}" } } }
}

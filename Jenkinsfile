pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "krishna6666/study-with-ai"
        DOCKER_HUB_CREDENTIALS_ID = "gitops-dockerhub"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/krishnakumaragrawal/study-with-ai.git']])
            }
        }        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:v2")
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    docker.withRegistry('https://registry.hub.docker.com' , "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage('Update Deployment YAML with New Tag') {
            steps {
                script {
                    sh """
                    sed -i 's|image: krishnakumaragrawal/study-with-ai:.*|image: krishnakumaragrawal/study-with-ai:${IMAGE_TAG}|' manifests/deployment.yaml
                    """
                }
            }
        }

        stage('Commit Updated YAML') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        sh '''
                        git config user.name "Krishna Kumar Agrawal"
                        git config user.email "kumarkrishna11166@gmail.com"
                        git add manifests/deployment.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}" || echo "No changes to commit"
                        git push https://${GIT_USER}:${GIT_PASS}@github.com/krishnakumaragrawal/study-with-ai.git HEAD:main
                        '''
                    }
                }
            }
        }
    }
}   
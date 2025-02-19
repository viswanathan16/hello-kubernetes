pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = "058264079741"
        AWS_REGION = "ap-south-1"
        ECR_REGISTRY = "058264079741.dkr.ecr.ap-south-1.amazonaws.com"
        ECR_REPOSITORY = "fastapi-microservice"
        EKS_CLUSTER_NAME = "aivar-eks-cluster"
    }

    stages {
        stage('configure aws credentials') {
            steps {
                withCredentials([[
                $class: 'AmazonWebServicesCredentialsBinding',
                accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                secretKeyVariable: 'AWS_SECRET_ACCESS_KEY',
                credentialsId: 'aws-credentials']])

                script 
                    {
                        sh 'aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID'
                        sh 'aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY'
                     
                    }


}    
        stage('Checkout Code') {
            steps {
                script {
                    checkout scm
                    env.GIT_COMMIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                
                    sh """
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                    """
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def imageTag = "fastapi-micro:${env.GIT_COMMIT_HASH}"
                    sh """
                        docker build -t $imageTag .
                        docker tag $imageTag $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$imageTag
                        docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$imageTag
                    """
                    env.IMAGE_TAG = imageTag
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh """
                        aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME
                        kubectl set image deployment/fastapi-microservice fastapi-microservice=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG -n default
                        kubectl rollout status deployment/fastapi-microservice -n default
                    """
                }
            }
        }
    }
}


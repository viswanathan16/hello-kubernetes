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
        stage('Checkout Code') {
            steps {
                git branch: 'fastapi', url: 'https://github.com/viswanathan16/hello-kubernetes.git'
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                script {
                    sh """
                      
                      export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                      export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                      aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY                
                 """
              }
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    def imageTag = "fastapi-micro:${env.GIT_COMMIT.substring(0,7)}"
                    sh "docker build -t $imageTag ."
                    sh "docker tag $imageTag $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$imageTag"
                    sh "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$imageTag"
                    env.IMAGE_TAG = imageTag
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME"
                    sh "kubectl set image deployment/fastapi-microservice fastapi-microservice=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG -n default"
                    sh "kubectl rollout status deployment/fastapi-microservice -n default"
                }
            }
        }
    }
}


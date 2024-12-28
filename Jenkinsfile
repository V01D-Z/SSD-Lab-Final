pipeline {
    agent any

    stages {
        stage('Clone the Repo') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[ name: 'main' ]],
                    userRemoteConfigs: [[ url: 'https://github.com/V01D-Z/SSD-Lab-Final.git' ]]
                ])
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python --version
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Use python -m pytest instead of pytest
                bat 'python -m pytest tests --junitxml=test_results.xml'
            }
        }

        stage('Build Application') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                bat '''
                pip install build
                python -m build
                '''
            }
        }

        stage('Deploy Application') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                // Example: Just start the Flask app for demo purposes.
                // Not recommended for production usage on a Jenkins agent.
                bat '''
                @echo off
                :: Kill anything using port 5000 (optional)
                for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
                    taskkill /F /PID %%a
                ) || echo "No process on port 5000."
                
                start /B python app.py
                '''
            }
        }
    }

    post {
        always {
            junit 'test_results.xml'
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}

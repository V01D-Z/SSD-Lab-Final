pipeline {
    agent any  // or agent { label 'windows' } if you have a Windows label

    stages {

        // 1. Clone the Repo
        stage('Clone the Repo') {
            steps {
                // If your repo is private, set up Jenkins credentials
                checkout([
                    $class: 'GitSCM',
                    branches: [[ name: 'main' ]],
                    userRemoteConfigs: [[ url: 'https://github.com/V01D-Z/SSD-Lab-Final.git' ]]
                ])
            }
        }

        // 2. Install Dependencies
        stage('Install Dependencies') {
            steps {
                // Use 'bat' instead of 'sh' on Windows
                bat '''
                python --version
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // 3. Run Unit Tests
        stage('Run Unit Tests') {
            steps {
                // Run tests using bat
                // Ensure pytest is in your requirements.txt
                bat 'pytest tests --junitxml=test_results.xml'
            }
        }

        // 4. Build (Package) the Application
        stage('Build Application') {
            steps {
                // Example using Python's build library or setup.py
                bat '''
                pip install build
                python -m build
                '''
            }
        }

        // 5. Deploy the Application
        stage('Deploy Application') {
            steps {
                // Example 1: Run the Flask app locally in the background (demo only).
                // Kills any existing python app process, then restarts.
                bat '''
                for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
                    taskkill /F /PID %%a
                ) || echo "No existing Python app found."

                start /B python app.py
                '''
                
                // Example 2 (Commented Out):
                // Deploy to a remote server using xcopy/robocopy or SSH 
                // if you have an SSH client on Windows. Example:
                /*
                bat '''
                scp -i path\\to\\key dist\\YourProject-0.1.0-py3-none-any.whl user@remote.host:/home/user
                ssh -i path\\to\\key user@remote.host "pip install --upgrade /home/user/YourProject-0.1.0-py3-none-any.whl && nohup python -m your_flask_package &"
                '''
                */
            }
        }
    }

    post {
        always {
            // Look for JUnit XML test reports
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

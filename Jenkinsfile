pipeline {
    agent any

    stages {
        // 1. Clone the Repo
        stage('Clone the Repo') {
            steps {
                // If your repo is public, no credentials needed.
                // Otherwise, configure Jenkins credentials for private repos.
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']], 
                    userRemoteConfigs: [[url: 'https://github.com/V01D-Z/SSD-Lab-Final.git']]
                ])
            }
        }

        // 2. Install Dependencies
        stage('Install Dependencies') {
            steps {
                // Ensure Python is available on the Jenkins agent
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        // 3. Run Unit Tests
        stage('Run Unit Tests') {
            steps {
                // Example with pytest
                sh 'pytest tests --junitxml=test_results.xml'
            }
        }

        // 4. Build (Package) the Application
        //    Using standard Python packaging to create distribution artifacts:
        //    e.g. a wheel or source distribution.
        stage('Build Application') {
            steps {
                // If you have a setup.py:
                sh 'pip install build'
                // This command will create a 'dist/' folder containing .whl or .tar.gz
                sh 'python -m build'
            }
        }

        // 5. Deploy the Application
        //    There are several ways to do this without Docker:
        //    A) Run the app directly on the Jenkins agent (for demo).
        //    B) SCP the package to a remote server and install/run it.
        //    C) Use a Jenkins plugin like "Publish Over SSH" or "SSH Pipeline Steps".
        stage('Deploy Application') {
            steps {
                script {
                    // Example A: Run the Flask app locally in the background (not recommended for production)
                    // You might want to kill old processes or use something like screen/tmux.
                    // This is purely for demonstration.

                    // Stop any running Flask app (if you have a custom script, call it here)
                    sh 'pkill -f "python app.py" || true'

                    // Run your app in the background
                    // Note: This will hold the port 5000 open on the Jenkins node
                    sh 'nohup python app.py &> flask_app.log &'
                    
                    // Example B: Deploy to a remote server (pseudo-code):
                    /*
                    withCredentials([sshUserPrivateKey(credentialsId: 'SSH_CRED_ID', keyFileVariable: 'identity')]) {
                        sh """
                        scp -i $identity dist/YourProject-0.1.0-py3-none-any.whl user@remote.host:/home/user/
                        ssh -i $identity user@remote.host \\
                            'pip install --upgrade --force-reinstall /home/user/YourProject-0.1.0-py3-none-any.whl && \\
                             pkill -f "python app.py" || true && \\
                             nohup python -m your_flask_package &> app.log &'
                        """
                    }
                    */
                }
            }
        }
    }

    post {
        always {
            // Archive test results so Jenkins can show them in the job
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

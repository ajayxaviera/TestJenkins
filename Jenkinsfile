pipeline {
    agent any 

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ajayxaviera/TestJenkins.git'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python test.py'
            }
        }
    }
}

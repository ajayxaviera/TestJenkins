pipeline {
    agent any 

    stages {
        

        stage('Install requirements') {
            steps {
                sh 'pip install jenkinsapi'
            }
        }

        stage('Run Tests') {
            steps {
                sh "python test.py \"${params.pipeline}\" \"${params.stage}\" \"${params.status}\""
            }
        }
    }
}

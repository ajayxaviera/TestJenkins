pipeline {
    agent any 

    stages {
        

        stage('Install pip') {
            steps {
                sh 'pip install jenkinsapi'
            }
        }

        stage('Execute script') {
            steps {
                sh "python test.py \"${params.pipeline}\" \"${params.stage}\" \"${params.status}\""
            }
        }
    }
}

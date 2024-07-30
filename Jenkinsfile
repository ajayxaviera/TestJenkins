pipeline {
    agent any 

    stages {

        stage('Install pip') {
            steps {
                sh 'pip install jenkinsapi'
                sh 'pip install pyyaml'
            }
        }

        stage('Execute script') {
            steps {
                script {
                    if (params.pipeline == 'All') {
                        sh "python test.py \"${params.pipeline}\""
                    } else {
                        sh "python test.py \"${params.pipeline}\" \"${params.stage}\" \"${params.status}\""
                    }
                }
            }
        }
    }
}

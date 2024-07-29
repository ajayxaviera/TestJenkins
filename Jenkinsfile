pipeline {
    agent any 

    stages {
        // stage('Checkout') {
        //     steps {
        //         git branch: 'main', url: 'https://github.com/ajayxaviera/TestJenkins.git'
        //     }
        // }

        stage('Install requirements'){
            steps {
                sh 'pip install jenkinsapi'
            }
        }


        stage('Run Tests') {
            steps {
                sh '''
                    python test.py "${params.pipeline}" "${params.stage}" "${params.status}"
                '''
            }
        }
    }
}

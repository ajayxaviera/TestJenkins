pipeline {
    agent any 

    // parameters {
    //     string(name: 'pipeline', defaultValue: 'default_pipeline', description: 'Pipeline name')
    //     string(name: 'stage', defaultValue: 'default_stage', description: 'Stage name')
    //     string(name: 'status', defaultValue: 'default_status', description: 'Status')
    // }

    stages {
        // Uncomment the Checkout stage if needed
        // stage('Checkout') {
        //     steps {
        //         git branch: 'main', url: 'https://github.com/ajayxaviera/TestJenkins.git'
        //     }
        // }

        stage('Install requirements') {
            steps {
                sh 'pip install jenkinsapi'
            }
        }

        stage('Run Tests') {
            steps {
                // Correct way to pass parameters in shell script
                sh "python test.py \"${params.pipeline}\" \"${params.stage}\" \"${params.status}\""
            }
        }
    }
}

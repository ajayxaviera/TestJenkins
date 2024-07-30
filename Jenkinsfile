pipeline {
    agent any 

    stages {

        stage('PipelineChoice') {
            steps {
                script {
                    def yaml = new Yaml()
                    def yamlContent = readFile('pipelines.yaml')
                    def data = yaml.load(yamlContent)
                    def pipelines = data.pipelines

                    properties([
                        parameters([
                            choice(
                                name: 'pipeline',
                                choices: pipelines.join('\n'),
                                description: 'Select the pipeline'
                            ),
                            string(name: 'stage', defaultValue: '', description: 'Stage name'),
                            string(name: 'status', defaultValue: '', description: 'Status')
                        ])
                    ])
                }
            }
        }

        stage('Install pip') {
            steps {
                sh 'pip install jenkinsapi'
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

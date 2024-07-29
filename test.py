import sys
import requests
from requests.auth import HTTPBasicAuth
from jenkinsapi.jenkins import Jenkins

jenkins_url = 'http://localhost:8090'
username = 'ajayxavier'
token = '1137264fcd2aad9bc9b1ce66280021832c'
pipeline = ""
stage = ""
status = ""

# print(sys.argv[0])
try:
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])

    global pipeline, stage, status
    pipeline = sys.argv[1]
    stage = sys.argv[2]
    status = sys.argv[3]
except Exception as ee:
    print("No aruguments from commandline")



def get_input():
    global pipeline, stage, status

    print("List of Pipelines: \n")
    print("1: MyPipeline1")
    print("2: MyPipeline2")
    print("3: MyPipeline3")
    print("4: MyPipeline4 \n")

    pipelineOpt = int(input("Enter the option for pipeline: "))
    if(pipelineOpt == 1):
        pipeline = "MyPipeline1"
    elif(pipelineOpt == 2):
        pipeline = "MyPipeline2"
    elif(pipelineOpt == 3):
        pipeline = "MyPipeline3"
    elif(pipelineOpt == 4):
        pipeline = "MyPipeline4"
    else:
        print("Invalid option")

    print("List of Stages: \n")
    print("1: init")
    print("2: AT")
    print("3: middle")
    print("4: end \n")

    stageOpt = int(input("Enter your stage: "))
    if(stageOpt == 1):
        stage = "init"
    elif(stageOpt == 2):
        stage = "AT"
    elif(stageOpt == 3):
        stage = "middle"
    elif(stageOpt == 4):
        stage = "end"
    else:
        print("Invalid option")

    print("List of Status: \n")
    print("1: In Progress")
    print("2: Failure")
    print("3: Success \n")

    statusOpt = int(input("Enter the status of pipeline: "))
    if(statusOpt == 1):
        status = "IN_PROGRESS"
    elif(statusOpt == 2):
        status = "FAILURE"
    elif(statusOpt == 3):
        status = "SUCCESS"
    else:
        print("Invalid option")



def get_server_instance():
    server = Jenkins(jenkins_url, username=username, password=token)
    return server

def get_pipeline_stages(job_name, build_number):
    url = f"{jenkins_url}/job/{job_name}/{build_number}/wfapi/describe"
    response = requests.get(url, auth=HTTPBasicAuth(username, token))
    response.raise_for_status()
    return response.json()


def get_job_details(pipeline, stage, status):
    server = get_server_instance()
    
    try:
        job = server.get_job(pipeline)
    except Exception as e:
        print(f"Failed to get job {pipeline}: {e}")
        return
    
    print(f"Job details for {pipeline}: {job}")

    if job.is_running():
        try:
            builds = job.get_build_dict()
            i = 0
            for build_number, build_url in builds.items():
                build = job.get_build(build_number)
                buildno = build.get_number()

                stages = get_pipeline_stages(pipeline, buildno)
                for eachstage in stages.get('stages', []):
                    if eachstage['status'] == status and eachstage['name'] == stage:
                        print(f"Job name: {pipeline}, Build number: {buildno}, Running on stage: {eachstage['name']}")
                        i += 1
            
            if i == 0:
                print("No builds match the criteria.")
            else:
                print(f"{i} number of builds are currently running on stage {stage} in {pipeline}")
                
        except Exception as e:
            print(f"Error occurred while fetching builds or stages: {e}")

    else:
        print(f"Job {pipeline} is not currently running.")



def get_specific_job(jobname):
    jenkins = get_server_instance()

    job = jenkins.get_job(jobname)
    build = job.get_last_build()

    if build.is_running():
        buildnumber = build.get_number()
        stages = get_pipeline_stages(job,buildnumber)

        for stage in stages.get('stages', []):
            if stage['status'] == "IN_PROGRESS":
                print(f"Pipeline {build} is running on {stage['name']} stage")


# get_input()

get_job_details(pipeline, stage, status)

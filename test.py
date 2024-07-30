import sys
import requests
import yaml
from datetime import datetime , timedelta,timezone
from requests.auth import HTTPBasicAuth
from jenkinsapi.jenkins import Jenkins

jenkins_url = 'http://localhost:8080'
username = 'ajayxavier'
token = '11fe4e4682b27a41fa9d9db9545252816b'
pipeline = ""
stage = ""
status = ""

# print("length = ",len(sys.argv) - 1) 
# print(sys.argv[0])

arugumentsLen = len(sys.argv) -1
if(arugumentsLen == 1):
    pipeline = sys.argv[1]
else:
    try:
        print(sys.argv[1])
        print(sys.argv[2])
        print(sys.argv[3])

        # global pipeline, stage, status
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


def get_job_details(pipeline, stage=None, status=None):
    server = get_server_instance()
    
    job_names = []
    check_stage_status = True
    if pipeline.lower() == "all":
        with open('pipelines.yaml', 'r') as file:
            data = yaml.safe_load(file)

        job_names = data['pipelines']
        check_stage_status = False
    else:
        job_names.append(pipeline)
    
    for job_name in job_names:
        try:
            job = server.get_job(job_name)
        except Exception as e:
            print(f"Failed to get job {job_name}: {e}")
            continue

        # print(f"Job details for {job_name}: {job}")

        if job.is_running():
            try:
                builds = job.get_build_dict()
                i = 0
                for build_number, build_url in builds.items():
                    build = job.get_build(build_number)
                    buildno = build.get_number()
                    buildTime = build.get_timestamp()
                    currentTime = datetime.now(timezone.utc)
                    timeDiff = currentTime - buildTime
    
                    stages = get_pipeline_stages(job_name, buildno)
                    for eachstage in stages.get('stages', []):
                        if check_stage_status:
                            if eachstage['status'] == status and eachstage['name'] == stage:
                                if status == "FAILED":
                                    if timeDiff <= timedelta(hours=24):
                                        print(f"Job name: {job_name}, Build number: {buildno}, {status} on  {eachstage['name']}")
                                        i += 1
                                else:
                                    print(f"Job name: {job_name}, Build number: {buildno}, {status} on  {eachstage['name']}")
                                    i += 1
                        else:
                            if eachstage['status'] == "IN_PROGRESS" or eachstage['status'] == "FAILED":
                                print(f"Job name: {job_name}, Build number: {buildno}, Stage: {eachstage['name']}, Status: {eachstage['status']}")
                                i += 1
                
                if i == 0:
                    print(f"No builds match the criteria for job {job_name}.")
                else:
                    print(f"{i} number of builds {status} in {job_name}")
                    
            except Exception as e:
                print(f"Error occurred while fetching builds or stages for job {job_name}: {e}")

        else:
            print(f"Job {job_name} is not currently running.")



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

if(pipeline == "All"):
    get_job_details("All")
else:
    get_job_details(pipeline,stage,status)

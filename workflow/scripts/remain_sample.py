import time
import os
from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
# 
# - Comment : Run check remain sample
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

odate = "2023-03-17"
#ODATE=snakemake.config["odate"]

def main(): 
    #Run export remain sample list
    print('remain sample start!!')    

    config.load_kube_config()
    try:
        c = Configuration().get_default_copy()
    except AttributeError:
        c = Configuration()
        c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    shcommand = 'python3 mlops-de-sample.py'
    res = exec_commands('remainsample', '827884298122.dkr.ecr.us-west-2.amazonaws.com/lambda-py-dev:v2.0.3', shcommand, core_v1)
    print(res)

    #make result file
    directory = "/home/ubuntu/mlops-de-pipeline/" + odate
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

    f = open(directory + '/remain_sample.txt','w')
    f.write(str(res))
    f.close()

    print(snakemake.output[0])
    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()
    
def exec_commands(appname, image_name, commands, api_instance = None):
    namespace = 'default'
    if api_instance == None:
        config.load_incluster_config()
        api_instance = core_v1_api.CoreV1Api()
    
    name = appname + '-' + str(round(time.time() * 1000000))
    print(name)
    
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)
    
    if not resp:    
        print("Pod %s does not exist. Creating it..." % name)
        pod_manifest = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': name,
                'namespace': namespace
            },
            'spec': {
                'securityContext': {
                    'fsGroup': 1000
                },
                'ttlSecondsAfterFinished': 600,
                'containers': [{
                    'name': name,
                    'image': image_name,  #'j2lab/snakemake:v1.0.0'
                    'imagePullPolicy': 'IfNotPresent',
                    "args": [
                        "/bin/sh",
                        "-c",
                        "while true;do date;sleep 5; done"
                    ],
                    "env": [
                      {
                        "name": "dbhost",
                        "value": "minderamlops-dev-db-cluster.cluster-cqi4kxzksugm.us-west-2.rds.amazonaws.com"
                      },
                      {
                        "name": "dbport",
                        "value": "5432"
                      },
                      {
                        "name": "database",
                        "value": "postgres"
                      },
                      {
                        "name": "dbdatabase",
                        "value": "postgres"
                      },
                      {
                        "name": "dbhost_odm",
                        "value": "minderadbdev-cluster.cluster-crbuh5ce4q2a.us-east-1.rds.amazonaws.com"
                      },
                      {
                        "name": "dbport_odm",
                        "value": "54321"
                      },
                      {
                        "name": "dbname_odm",
                        "value": "minderadbdev"
                      },
                      {
                        "name": "dbschema",
                        "value": "public"
                      },
                      {
                        "name": "dbuser",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "dbuser",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "dbpasswd",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "dbpasswd",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "aws_access_key_id",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "aws_access_key_id",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "aws_secret_access_key",
                        "valueFrom": {
                          "secretKeyRef": {
                            "key": "aws_secret_access_key",
                            "name": "mlops-de"
                          }
                        }
                      },
                      {
                        "name": "s3bucktname_lims",
                        "value": "mlops-lims-dump"
                      },
                      {
                        "name": "s3bucktname_odm",
                        "value": "mlops-odm-dump"
                      },
                      {
                        "name": "s3bucktname_rnaseq",
                        "value": "dna-nexus-result-dev"
                      },
                      {
                        "name": "s3_region_name",
                        "value": "us-west-2"
                      },
                      {
                        "name": "s3_region_name_odm",
                        "value": "us-west-1"
                      },
                      {
                        "name": "s3_region_lims_name",
                        "value": "us-west-1"
                      },
                      {
                        "name": "access_bucket_snakemake_name",
                        "value": "mindera-mlops-dev-bucket"
                      },
                      {
                        "name": "SECRET_odm",
                        "value": "dev_cc_lambda_secrets"
                      },
                      {
                        "name": "SECRET_lims",
                        "value": "lims_app_secrets"
                      }

                    ],
                }],
            }
        }
        resp = api_instance.create_namespaced_pod(body=pod_manifest,
                                                  namespace=namespace)
        while True:
            resp = api_instance.read_namespaced_pod(name=name,
                                                    namespace=namespace)
            if resp.status.phase != 'Pending':
                break
            time.sleep(1)
        print("Pod %s done created." % name)
    else:
        print("Pod %s does exist. First delete it" % name)
    
    exec_command = [
        '/bin/sh',
        '-c',
        commands]
    restm = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    # return restm
    try:
        resdel = api_instance.delete_namespaced_pod(name=name,
                                                    namespace=namespace)
        print("Pod %s does delete." % name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    finally:
        return restm

if __name__ == '__main__':
    main()
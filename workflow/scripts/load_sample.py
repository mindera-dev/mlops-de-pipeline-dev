import k8s_exec
import s3_exec
import boto3
import os
# 
# - Comment : Get Remain sample list from s3
#             , Repeat load sample
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():
    #get environment variable
    os_aws_access_key_id = os.getenv("aws_access_key_id","")
    os_aws_secret_access_key = os.getenv("aws_secret_access_key","")
    os_s3_region_name = os.getenv("s3_region_name","us-west-2")
    os_bucket_name = os.getenv("access_bucket_snakemake_name", "mlops-pipeline-result")

    #set file name about get remain sample list txt
    file = 'not_exist_pipeline_2022-12-21.txt'

    
    bucket_file = "output_folders/" + file
    local_file = file

    #s3 connect
    try:        
        s3 = boto3.client(
            service_name = "s3",
            region_name = os_s3_region_name,
            aws_access_key_id = os_aws_access_key_id,
            aws_secret_access_key = os_aws_secret_access_key
        )
    except Exception as e:
        print(e)

    #get s3 list
    obj_list = s3.list_objects(Bucket=os_bucket_name)
    contents_list = obj_list['Contents']

    file_list=[]
    check_exist_file = False

    #check s3 list    
    for content in contents_list:
        #print("content : %s" % content)
        key = content['Key']
        if key == bucket_file:
            check_exist_file = True
            break
        else:
            check_exist_file = False

    #download reamin sample list file from s3 bucket
    if check_exist_file == True:
        print("file exist, file download!!")
        s3.download_file(os_bucket_name, bucket_file, local_file)
    
    #check remain sample list file
    f = open(local_file, 'r')    
    line = f.readline()
    print("line",line)
    
    f.close()    
    
    #Repeat load sample
    cnt = 0
    dict_line = eval(line)
    result = ""
    for i in dict_line:
        batch = i['batch']
        sample = i['sample']
        res = k8s_exec.exec_commands('loadsample', '779792627677.dkr.ecr.us-west-2.amazonaws.com/minderadatatransfer:V1.0.1', '/java/datatransfer.sh rnaseq ' + str(batch) + ' ' + str(sample))
        if "" == result:
            result = res
        else:
            result = result + res
        cnt = cnt + 1

    print(result)

    #make result file
    f = open('/dags/mlops-pipeline-result/load_sample.txt','w')
    f.write(snakemake.output[0] + "\n")
    f.write(str(result))    
    f.close()

    f = open(snakemake.output[0],'w')        
    f.write(str(result))
    f.close()
    s3.close()

if __name__ == '__main__':
    main()


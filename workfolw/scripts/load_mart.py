import k8s_exec
import s3_exec
# 
# - Comment : Run load mart
#             , make result file
# - History : 2023.01.10 V1.0 initial develop 
#

def main():
    #Run load mart
    res = k8s_exec.exec_commands('loadmart', '779792627677.dkr.ecr.us-west-2.amazonaws.com/minderadatatransfer:V1.0.1', '/java/datatransfer.sh mart all 2022-12-21')
    print(res)

    #make result file
    f = open('/dags/mlops-pipeline-result/load_mart.txt','w')
    f.write(snakemake.output[0] + "\n")
    f.write(str(res))    
    f.close()

    f = open(snakemake.output[0],'w')
    f.write(str(res))
    f.close()

if __name__ == '__main__':
    main()
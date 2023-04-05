
#get mart result txt
rule load_mart:
	input:
        FS_FILE
    output:
        MART_FILE
    script:
        "scripts/load_mart.py"	
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 


#get lims,odm(match-1),sample(rnaseq) result txt and load fs data and set fs result txt
rule load_fs:
    input:    
        LIMS_FILE
        MATCH1_FILE
        SAMPLE_FILE
    output:
        FS_FILE
    script:
        "scripts/load_fs.py" 
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline"       
        
#get export lims result txt and load lims data and set lims result txt
rule load_lims:
    input:
        EXPORT_LIMS_FILE
    output:
        LOAD_LIMS_FILE
    script:
        "scripts/load_lims.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

#export lims data and set export lims result txt
rule export_lims:
    output:
        EXPORT_LIMS_FILE
    script:
        "scripts/export_lims.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

#get export(sftp) odm(match-1) result txt and load odm(match-1) data and set odm(match-1) result txt
rule load_match_1:
    input:
        SFTP_MATCH1_FILE
    output:
        LOAD_MATCH1_FILE
    script:
        "scripts/load_match_1.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

#export(sftp) odm(match-1) data and set export(sftp) odm(match-1) result txt
rule sftp_odm:
    output:
        SFTP_MATCH1_FILE
    script:
       "scripts/sftp_odm.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

#get export sample(rnaseq) result txt and load sample(rnaseq) data and set sample(rnaseq) result txt
rule load_sample:
    input:
        EXPORT_SAMPLE_FILE
    output:
        LOAD_SAMPLE_FILE
    script:
        "scripts/load_sample.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

#export sample(rnaseq) data and set export sample(rnaseq) result txt
rule export_sample:
    output:
        EXPORT_SAMPLE_FILE
    script:
        "scripts/remain_sample.py"
	conda:
		f'{ENVS_DIR}/pipeline.yaml'
	params:		
		ODATE=ODATE # YYYYMMDD 
	group: "pipeline" 

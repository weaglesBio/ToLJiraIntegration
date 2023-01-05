#!/usr/bin/env python

from ToLJiraAuth import ToLJiraAuth
import JiraMethods as jm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s','--sample_id')
args = parser.parse_args()

# sample = "ilXanIcte2"

if args.sample_id:

    tja = ToLJiraAuth()
    jql_request = f"project in ('RC', 'GRIT') AND 'Sample ID' ~ {args.sample_id} ORDER BY updated DESC"
    results = tja.auth_jira.search_issues(jql_request)

    # Return most recently created entry if there are multiple with same name.
    issue = tja.auth_jira.issue(results[0])

    yaml_data = jm.get_yaml_attachment(issue)

    pri_fa = yaml_data["primary"]
    hap_fa = yaml_data["haplotigs"]
    pacbio_read_dir = yaml_data["pacbio_read_dir"]
    species_name = pacbio_read_dir.split("/")[8]

    print(f"{args.sample_id} - {species_name}")
    print(f"")
    print(f"")
    print(f"unset PERL5LIB")
    print(f"unset PYTHONPATH")
    print(f"export LD_LIBRARY_PATH=/software/python-3.7.4/lib/:${{LD_LIBRARY_PATH}}")
    print(f"export PYTHONPATH=/software/grit/lib/python3_lib:${{PYTHONPATH}}")
    print(f"export PERL5LIB=/software/grit/projects/vr-runner/modules:${{PERL5LIB}}")
    print(f"")
    print(f"cd /lustre/scratch123/tol/teams/grit/btk_runs/data")
    print(f"mkdir ${args.sample_id}_data")
    print(f"mkdir ${args.sample_id}Pri")
    print(f"mkdir ${args.sample_id}Hap")
    print(f"cd ${args.sample_id}_data")
    print(f"cp ${pacbio_read_dir}/fasta/*.fasta.gz .")
    print(f"cp ${pri_fa} ${args.sample_id}pri.fasta.gz")
    print(f"cp ${hap_fa} ${args.sample_id}hap.fasta.gz")
    print(f"")
    print(f"RENAME READS FILES")
    print(f"")
    print(f"/usr/bin/perl /nfs/team135/yy5/btk_config/run-btkconfig_2conf +loop 60 -b -s ${args.sample_id} -t '${species_name}' -o . -z config_done")
    print(f"")
    print(f"cd ../")
    print(f"cp ${args.sample_id}_data/config_pri.yaml ${args.sample_id}Pri/config.yaml")
    print(f"cp ${args.sample_id}_data/config_hap.yaml ${args.sample_id}Hap/config.yaml")
    print(f"")
    print(f"cd /lustre/scratch123/tol/teams/grit/btk_runs/data/${args.sample_id}Pri")
    print(f"ASSEMBLY=${args.sample_id}Pri TRANSFER=true bsub < /nfs/team135/yy5/btk_sig/run_pipeline.sh")
    print(f"cd /lustre/scratch123/tol/teams/grit/btk_runs/data/${args.sample_id}Hap")
    print(f"ASSEMBLY=${args.sample_id}Hap TRANSFER=true bsub < /nfs/team135/yy5/btk_sig/run_pipeline.sh")
    print(f"")
    print(f"cd /lustre/scratch123/tol/teams/grit/btk_runs/result/${args.sample_id}pri")
    print(f"tar -xvf ${args.sample_id}pri.tar")
    print(f"gunzip ${args.sample_id}pri/*")
    print(f"cp -r ${args.sample_id}pri /lustre/scratch123/tol/share/grit-btk-prod/blobplots/${args.sample_id}Pri")
    print(f"chmod -R g+w /lustre/scratch123/tol/share/grit-btk-prod/blobplots/${args.sample_id}Pri")
    print(f"gzip ${args.sample_id}pri/*")
    print(f"")
    print(f"cd /lustre/scratch123/tol/teams/grit/btk_runs/result/${args.sample_id}hap")
    print(f"tar -xvf ${args.sample_id}hap.tar")
    print(f"gunzip ${args.sample_id}hap/*")
    print(f"cp -r ${args.sample_id}hap /lustre/scratch123/tol/share/grit-btk-prod/blobplots/${args.sample_id}Hap")
    print(f"chmod -R g+w /lustre/scratch123/tol/share/grit-btk-prod/blobplots/${args.sample_id}Hap")
    print(f"gzip ${args.sample_id}hap/*")
    print(f"")
    print(f"BTK DONE")
    print(f"[Pri|https://grit-btk.tol.sanger.ac.uk/${args.sample_id}Pri/dataset/${args.sample_id}Pri/blob?plotShape=circle&zScale=scaleLog#Settings]")
    print(f"[Hap|https://grit-btk.tol.sanger.ac.uk/${args.sample_id}Hap/dataset/${args.sample_id}Hap/blob?plotShape=circle&zScale=scaleLog#Settings]")
    print(f"")
    print(f"curl -s 'https://grit-btk-api.tol.sanger.ac.uk/api/v1/search/reload/testkey%20npm%20start'")

else:
    print('No sample provided.')


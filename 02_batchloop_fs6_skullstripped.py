import pandas
import os.path as op
import os
import numpy as np
import shutil
import subprocess

camcan_dir = '/envau/work/meca/data/Various/camcan_data/cc700/mri/pipeline/release004/BIDSsep/anat'
root_dir = '/hpc/meca/data/Datasets/camcan'
genericbatch_path = op.join(root_dir,'scripts','01_preprocess_T1_mask_coreg_MNI_be4_fs_generic.m')

participants_path = op.join(camcan_dir,'participant_data.tsv')
df = pandas.read_csv(participants_path, sep='\t')

subject_df = df[(df['hand']>50) & (df['gender_text']=='MALE')]

subject_list = np.array(subject_df['Observations'])
#subject_list = [subject_list[3]]
subject_list = subject_list[4:60]

for subj in subject_list:
    print(subj)
    # add the prefix
    subject = 'sub-' + subj
    if subject == 'sub-CC221031':
        #t1_path = op.join(root_dir,'subjects',subject,'anat','mnicoreg_masked_sanlm_'+subject+'_T1w.nii.gz')
        #fs_subject = subject+'_mnicoreg_masked_sanlm'
        t1_path = op.join(root_dir,'subjects',subject,'anat','masked_msanlm_'+subject+'_T1w.nii')
        fs_subject = subject
        t2_path = op.join(camcan_dir,subject,'anat',subject+'_T2w.nii.gz')
        fs_cmd = "frioul_batch 'export FREESURFER_HOME=/hpc/soft/freesurfer/freesurfer_6.0.0; export SUBJECTS_DIR=/hpc/meca/data/FreesurferDatabases/FS6.0.0_camcan_sanlm_skullstripped/; . ${FREESURFER_HOME}/SetUpFreeSurfer.sh; recon-all -autorecon1 -noskullstrip -3T -s %s -i %s; cp ${SUBJECTS_DIR}/%s/mri/T1.mgz ${SUBJECTS_DIR}/%s/mri/brainmask.auto.mgz; ln -s  ${SUBJECTS_DIR}/%s/mri/brainmask.auto.mgz ${SUBJECTS_DIR}/%s/mri/brainmask.mgz; recon-all -autorecon2 -autorecon3 -3T -s %s -T2 %s -T2pial'" % (fs_subject, t1_path, fs_subject, fs_subject, fs_subject, fs_subject, fs_subject, t2_path)
        print(fs_cmd)
        subprocess.run(fs_cmd,shell=True)

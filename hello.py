import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import cytomine
from cytomine import Cytomine
from cytomine.models import Annotation, Job, ImageInstanceCollection, AnnotationCollection, Property,  AttachedFileCollection

from argparse import ArgumentParser
import sys
print(sys.argv[1:])

import os
base_path = os.getenv("HOME")

os.environ['TF_FORCE_GPU_ALLOW_GROWTH']='true'
import subprocess

from unet.params import parserer

def parsebool(x):
    return x in ['True','true','t','yes','y','yep','affirmative','yesplease','ya','oy','oui','ui','v','V','Vrai']

print(tf.test.is_gpu_available())
print(cv2.__version__)
print(os.listdir('/app/'))
print(os.listdir('/app/unet'))

with cytomine.CytomineJob.from_cli(sys.argv[1:]) as cj:

    cj.job.update(progress=0,statusComment="launched")

    params,_=parserer().parse_known_args(sys.argv[1:])
    
    idJob=params.cytomine_id_software

    stat=subprocess.run([str(x) for x in ['python3','/app/unet/utils/get_data.py',
        '--cytomine_host', params.cytomine_host,
        '--cytomine_public_key', params.cytomine_public_key,
        '--cytomine_private_key', params.cytomine_private_key,
        '--cytomine_id_project', params.cytomine_id_project,
        '--slice_term', str(params.slice_term),
        '--patch-size',str(params.crop_size),
        '--datadir',str(params.datadir),
        '--download_path', params.datadir]])

    cj.job.update(progress=30,statusComment="got data")


    if stat.returncode !=0 :
        cj.job.update(status=cj.job.FAILED)
        print(stat.returncode)
        raise Exception("return status not zero")

    stat=subprocess.run(['python3','/app/unet/main.py',*sys.argv[1:]])

    if stat.returncode !=0 :
        cj.job.update(status=cj.job.FAILED)
        raise Exception("return status not zero")

    cj.job.update(progress=60,statusComment="got masks")

    stat=subprocess.run(['python3','/app/unet/utils/postprocessing.py',
        '--cytomine_host', str(params.cytomine_host),
        '--cytomine_public_key', str(params.cytomine_public_key),
        '--cytomine_private_key', str(params.cytomine_private_key),
        '--cytomine_id_project', str(params.cytomine_id_project),
        '--slice_term', str(params.slice_term),
        '--imgs-test',*[str(x) for x in params.imgs_test],
        '--terms',*[str(x) for x in params.terms],
        '--model', params.checkpoint ])#,
        #'--upload','True'])

    if stat.returncode !=0 :
        cj.job.update(status=cj.job.FAILED)
        raise Exception("return status not zero")
    cj.job.update(progress=90,statusComment="got masks")


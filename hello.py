import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import cytomine
from cytomine import Cytomine

from argparse import ArgumentParser
import sys
print(sys.argv[1:])

import os
base_path = os.getenv("HOME")

import subprocess

def parsebool(x):
    return x in ['True','true','t','yes','y','yep','affirmative','yesplease','ya','oy','oui','ui','v','V','Vrai']

print(tf.test.is_gpu_available())
print(cv2.__version__)
print("yeay")
print(os.listdir('/app/'))
print(os.listdir('/app/ratseg-master'))
#sample option
#['--cytomine_host', 'http://localhost-core',
# '--cytomine_public_key', '9004d4c1-773a-40ac-90f1-9e2ef76ca96e',
#'--cytomine_private_key', 'd04f2eb5-4c4a-49fa-a840-d94b309d5eb5',
#'--cytomine_id_project', '155',
#'--cytomine_id_software', '228922',
# '--slice_term', '30289',
# '--model-name', 'vnet',
# '--model-type', 'vnet',
# '--residual', 'true']

with cytomine.CytomineJob.from_cli(sys.argv[1:]) as cj:


    parser = ArgumentParser(prog="ratseg_software")
    parser.add_argument('--cytomine_host', dest='host',
                        default='https://demo.cytomine.coop', help="The Cytomine host")
    parser.add_argument('--cytomine_public_key', dest='public_key',
                        default='5870ca8a-d1a6-4f8c-b51c-6cdb871cba5b',
                        help="The Cytomine public key")
    parser.add_argument('--cytomine_private_key', dest='private_key',
                        help="The Cytomine private key",
                        default='7d890db3-2537-4f7a-b313-2c36b208c22f')
    parser.add_argument('--cytomine_id_project', dest='id_project',
                        help="The project from which we want the images",
                        default=1012227)
    parser.add_argument('--download_path',
                        help="Where to store images",
                        default='/home/donovan/Downloads/')
    parser.add_argument('--slice_term',type=int,
                        help="id of the ROI delimiting annotation",
                        default=2469614)

    parser.add_argument('--cytomine_id_software',dest='id_software')

    parser.add_argument('-m','--model-name',default='vanilla')
    parser.add_argument('-t','--model-type',default='mnet')
    parser.add_argument('--residual',type=parsebool,default=True,
            help='add skip connections within blocks of convolution')

    cj.job.update(progress=0,statusComment="launched")

    params=parser.parse_args(sys.argv[1:])

    idJob=params.id_software



    subprocess.run(['mkdir','/tmp/imgs'])
    subprocess.run(['mkdir','tmp'])



    subprocess.run(['python3','ratseg-master/get_data.py',
        '--cytomine_host', params.host,
        '--cytomine_public_key', params.public_key,
        '--cytomine_private_key', params.private_key,
        '--cytomine_id_project', params.id_project,
        '--slice_term', str(params.slice_term),
        '--download_path', '/tmp/imgs'])

    cj.job.update(progress=30,statusComment="got data")
    imgs=[2319573,2319579,2319587,2319595]
    terms=[1012286,1012259,1012265,1012280]

    subprocess.run(['python3','ratseg-master/main.py',
        '--imgs-test',"%s %s %s %s" % tuple([str(x) for x in imgs]),
        '--terms',"%s %s %s %s" % tuple([str(x) for x in terms]),
        '--model-name',params.model_name,
        '--model_type',params.model_type,
        '--residual',params.residual,
        '--do-train', 'False',
        '--do-test', 'True'])

    cj.job.update(progress=60,statusComment="got masks")

    subprocess.run(['python3','ratseg-master/postprocessing.py',
        '--cytomine_host', params.host,
        '--cytomine_public_key', params.public_key,
        '--cytomine_private_key', params.private_key,
        '--cytomine_id_project', params.id_project,
        '--slice_term', str(params.slice_term),
        '--imgs-test',"%s %s %s %s" %tuple([str(x) for x in imgs]),
        '--terms',"%s %s %s %s" %tuple([str(x) for x in terms]),
        '--model-name',params.model_name ])

    cj.job.update(progress=90,statusComment="got masks")


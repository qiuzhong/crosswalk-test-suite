import sys, os
import itertools, shutil

if not os.path.isdir("/opt/usr/media/tct/opt/wrt-manifest-tizen-tests"):
   print "not /opt/usr/media/tct/opt/wrt-manifest-tizen-tests. Please pack.sh -> unzip .zip->inst.sh "
   sys.exit(1)
else:
   os.chdir("/opt/usr/media/tct/opt/wrt-manifest-tizen-tests/") 
   path = os.getcwd()
   print path
   path_tcs = path + "/tcs"
   path_result= path + "/result"
   path_resource = path + "/resource"
   seed_file = path + "/allpairs/input_seed.txt"
   seed_file_na = path + "/allpairs/input_seed_negative.txt"
   selfcomb_file = path + "/allpairs/selfcomb.txt"
   output_file = path + "/allpairs/output.txt"
   output_file_ne = path + "/allpairs/output_negative.txt"
   report_path = path + "/report"
   report_file = report_path + "/wrt-manifest-tizen-tests.xml"
   report_summary_file = report_path + "/summary.xml"
   allpairs_order = 2
   version="6.35.1.2"
   name="wrt-manifest-tizen-tests"

# Copyright (c) 2014 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this list
#   of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Fan, Yugang <yugang.fan@intel.com>

APP_TYPE_WEB = "WEB"
APP_TYPE_WGT = "WGT"

import Image
import string
import os
import md5
import time
import subprocess
import signal
DEFAULT_CMD_TIMEOUT = 60


class APP():

    def __init__(self, app_config=None, app_name=None, timeout=2):
        pass

    def quit(self):
        pass

    # standardize the image
    def make_regalur_image(self, img, size=(256, 256)):
        return img.resize(size).convert('RGB')

    def hist_similar(self, lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r))
                   for l, r in zip(lh, rh)) / len(lh)

    # Images similarity calculation
    def cal_images_similar(self, img1, img2):
        fimg1 = Image.open(img1)
        fimg2 = Image.open(img2)
        reg_img1 = self.make_regalur_image(fimg1)
        reg_img2 = self.make_regalur_image(fimg2)

        # calculate the similar
        ret = self.hist_similar(reg_img1.histogram(), reg_img2.histogram())
        return ret * 100

    def convert_pic(self, pic_name, ratio):
        im = Image.open(pic_name)
        smalling = im.resize(ratio, Image.ANTIALIAS)
        smalling.save(pic_name, "png")

    def crop_pic(self, page_pic, element_pic, box):
        im = Image.open(page_pic)
        regin = im.crop(box)
        regin.save(element_pic, "png")

    def check_pic_same(self, pic1, pic2, similarity):
        try:
            pic_similarity = self.cal_images_similar(pic1, pic2)
            if pic_similarity >= string.atoi(similarity):
                return True
            else:
                print "The similarity is: %s" % pic_similarity
                return False
        except Exception as e:
            print "Check similarity failed: %s" % e
            return False

    def check_pic_different(self, pic1, pic2, similarity):
        pic_similarity = self.cal_images_similar(pic1, pic2)
        if pic_similarity >= string.atoi(similarity):
            print "The similarity is: %s" % pic_similarity
            return False
        else:
            return True

    def get_string_md5(self, data_str):
        m = md5.new()
        m.update(data_str)
        return m.hexdigest()

    def devices(self):
        out = "\n".join(self.doCMD("adb devices")[1])
        match = "List of devices attached"
        index = out.find(match)
        if index < 0:
            print("adb is not working.")
        return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])


    def doCMD(self, cmd, time_out=DEFAULT_CMD_TIMEOUT):
        pre_time = time.time()
        output = []
        cmd_return_code = 1
        cmd_proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while True:
            output_line = cmd_proc.stdout.readline().strip("\r\n")
            cmd_return_code = cmd_proc.poll()
            elapsed_time = time.time() - pre_time
            if cmd_return_code is None:
                if elapsed_time >= time_out:
                    self.killProcesses(ppid=cmd_proc.pid)
                    return (None, None)
            elif output_line == '' and cmd_return_code is not None:
                break

            output.append(output_line)
        if cmd_return_code != 0:
            pass

        return (cmd_return_code, output)

    def install_app_by_cmd(self, device_id, app_path):
        action_status = False
        try:
            if not device_id:
                device_id = list(self.devices().keys())[0]
            cmd = "adb -s %s install %s" % (device_id, app_path)
            (return_code, output) = self.doCMD(cmd)
            if "Success" in output:
                action_status = True
            else:
                print("-->> Invalid apk path: %s " % app_path)
        except Exception as e:
            print("Failed to install %s: %s" % (app_path, e))
        return action_status

    def uninstall_app_by_cmd(self, device_id, package_name):
        action_status = False
        try:
            if not device_id:
                device_id = list(self.devices().keys())[0]
            cmd = "adb -s %s uninstall %s" % (device_id, package_name)
            (return_code, output) = self.doCMD(cmd)
            if "Success" in output:
                action_status = True
        except Exception as e:
            print("Failed to uninstall %s: %s" % (package_name, e))
        return action_status

    def killProcesses(self, ppid=None):
        ppid = str(ppid)
        pidgrp = []

        def GetChildPids(ppid):
            command = "ps -ef | awk '{if ($3 ==%s) print $2;}'" % str(ppid)
            pids = os.popen(command).read()
            pids = pids.split()
            return pids

        pidgrp.extend(GetChildPids(ppid))
        for pid in pidgrp:
            pidgrp.extend(GetChildPids(pid))

        pidgrp.insert(0, ppid)
        while len(pidgrp) > 0:
            pid = pidgrp.pop()
            try:
                os.kill(int(pid), signal.SIGKILL)
                return True
            except OSError:
                try:
                    os.popen("kill -9 %d" % int(pid))
                    return True
                except Exception:
                    return False

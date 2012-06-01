#!/usr/bin/python
import os
import sys
import time
import string
import commands
import thread

make_clean_flag=3
command_pos = 4
src_file_pos =2
dest_file_pos =3
path_temp_version_file="version.text"

command_pos_git_version=1

audio_playing = 1

tar_with_git_version_skip_pos = 0
tar_with_git_version_file_name = 1

someone_update = 0


#Template_changlog = build_templat_wiht_char("commint of %s auto build by kyomen"%(time.strftime("%Y/%m/%d", time.localtime()),'*',64)
write_chang_log = 0

def build_templat_wiht_char(data,char,length):
  if(len(data) > length):
    return data
  start_pos = (length - len(data))/2

  return start_pos*char+data+start_pos*char+"\n"

def write_log_to_changlog(project,fp,data):
  if(write_chang_log == 1):
    fp.writelines(build_templat_wiht_char("%s"%project,'*',64));
    fp.writelines(data+"\n");

def check_if_git_commit_from(time,unit):
  command_str = "git log --since=\'%s %s ago\'"%(time,unit)
  output = run_sys_command(command_str)
  return output

def run_sys_command(command):
  status,output_file = commands.getstatusoutput(command.strip())
  print "\"%s\" return: "%(command.strip()),"status: ", status,"output : ",output_file
  if(status != 0):
    print command.strip(),"return error!!! we only do to is exit"
    sys.exit()
  return output_file

#  if os.system(command) != 0:
#    print command.strip()+"  error !!!"
#    sys.exit()
#  else:
#    print command.strip()+"  success !!!"
#
def dete_path_and_create(path):
  if os.path.exists(path) == False:
    os.makedirs(path)

i = 0
temp_str=""
hash_file = ''
for path in sys.argv:
  i = 1+i
if i != 4:
  print "./auto_build.py rulefile fetch? clean?"
else:
  i = 0;
  output_file = open(path_temp_version_file,"w")
  py_work_path = "%s"%os.getcwd()

  for line in open(sys.argv[1]):
    data = line.split(",")
    data[dest_file_pos] = data[dest_file_pos].strip()
    dete_path_and_create(data[dest_file_pos])
    '''do git check out and complie
    '''
    os.chdir(data[0])
    #print "pwd path is: ",data[0]

    if(cmp(data[command_pos_git_version],"0") != 0):
      if(string.atoi(sys.argv[2],10) == 1):
        #run_sys_command("git fetch")#get newest version from origin git
        run_sys_command("git fetch")
       # status1,commands_output = commands.getstatusoutput("git fetch")
       # if(status1 != 0):
       #   print "fetch error!!! exit"
       #   sys.exit()
       # print "git fetch result is ",commands_output,"result length is ",len(commands_output)
       # if(len(commands_output) > 0):
       #   update = 1
     #time_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
     #print time_str
      run_sys_command("git reset --hard HEAD")
      run_sys_command("git checkout %s"%(data[1]))
      check_git_log_return = check_if_git_commit_from(23,'hour')
      if(len(check_git_log_return) != 0):
        someone_update = 1
        project_path = data[0].split("/")
        temp = 0
        for project_ele in project_path:
          temp = temp + 1
        if(len(project_ele) == 0):
          project_ele = project_path[temp - 2]#for paht "aa/aa/aa/aa/" if the last char is / will be get null string
        write_log_to_changlog(project_ele,Changelogfile_fp,check_git_log_return)
      commands_output = commands.getoutput("git rev-list --max-count=1 HEAD");
      commands_output = commands_output,data[0],"\n";
      output_file.writelines(commands_output)
      output_file.flush();
    temp_str = data[command_pos]
    if(temp_str.find("PATH") != -1):
      temp_str_data_path = temp_str.split("=")
      real_evn = os.getenv('PATH')
      temp_str_data_path[1]= temp_str_data_path[1].strip()+':'+real_evn
      os.putenv('PATH',temp_str_data_path[1])
      if(string.atoi(sys.argv[make_clean_flag],10) != 0):
        temp_str = temp_str_data_path[2]
        if(temp_str.find("make") != -1):
          temp_str = temp_str.replace("make","make clean")
          run_sys_command(temp_str)
      run_sys_command(temp_str_data_path[2].strip())
      os.putenv('PATH',real_evn)
    elif(temp_str.find("tar_with_git_version") != -1):
      print "get special command!!!!"
      commands_output = commands.getoutput("git rev-list HEAD")
      lines = commands_output.split("\n");
      tar_special_para = temp_str.split("=");
      lines_count = 0
      tar_str = ""
      tar_file_name = ""
      for elements in tar_special_para:
        if(lines_count == tar_with_git_version_skip_pos):
          lines_count = lines_count + 1
        elif(lines_count == tar_with_git_version_file_name):
          lines_count = lines_count + 1
          tar_file_name = elements
        else:
          tar_str = tar_str +" " + elements
      #print tar_str
      lines_count = 0
      for elements in lines:
        lines_count = lines_count+1
      command = "tar jcf %s%d.tar.bz2 "%(tar_file_name,lines_count)+tar_str
      print command
      run_sys_command(command)
    elif(temp_str.find("start_create") != -1):
      #check if update
      if(someone_update == 0):
        print "nothing update"
        break
      else:
        print "some one commit"
    elif(temp_str.find("ChangeLog") != -1):
      changlog_path = temp_str.split("=");
      Changelogfile_fp = open(changlog_path[1].strip(),"aw")
      Changelogfile_fp.write(3*"\n")
      Changelogfile_fp.write(build_templat_wiht_char("commint of %s auto build by kyomen"%(time.strftime("%Y/%m/%d-%H/%M/%S", time.localtime())),'*',64))
      write_chang_log = 1
    else:
      if(string.atoi(sys.argv[make_clean_flag],10) != 0):
        temp_str = data[command_pos]
        if(temp_str.find("make") != -1):
          temp_str = temp_str.replace("make","make clean")
          run_sys_command(temp_str)
      run_sys_command(data[command_pos])

    os.chdir(py_work_path)
    #print "py_work_path is: ",py_work_path
    if(cmp(data[src_file_pos],".") != 0):
      command = "cp -r %s %s"%(data[src_file_pos],data[dest_file_pos])
      run_sys_command(command)
  output_file.close()
  if(write_chang_log ==1):
    Changelogfile_fp.close();

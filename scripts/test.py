import shlex
import subprocess
import sys

f = open('/tmp/start.txt', 'w')
f.write(str(sys.argv[1]))
f.close()

command = 'docker swarm join --token '+str(sys.argv[1]+' 192.168.0.166:2377')


cmd = shlex.split(
    '''ssh -i /root/.ssh/id_rsa pi@192.168.0.103 ''' + command)
ssh = subprocess.Popen(
    cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    f = open('/tmp/error.txt', 'w')
    f.write(str(error))
    f.close()
ssh.terminate()

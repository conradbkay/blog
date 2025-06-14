# from https://superuser.com/a/1737216

# Create .ssh directory in home directory with proper permission
mkdir -m 700 ~/.ssh

# Get Windows user name
WINUSER=`cmd.exe /c 'echo %USERNAME%' | tr -d '\r'`

# Add a permanent mount entry for Windows user .ssh directory
cat << EOF | sudo tee -a /etc/fstab
C:\Users\\$WINUSER\.ssh\ /home/$USER/.ssh drvfs rw,noatime,uid=`id -u`,gid=`id -g`,case=off,umask=0077,fmask=0177 0 0
EOF

# Mount the .ssh
sudo mount /home/$USER/.ssh

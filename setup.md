# Setup

## Linux

- python3 -m venv .venv
- source .venv/bin/activate
- python -m pip install jupyter matplotlib plotly pandas python3 jupyter-cache

## Install Quarto

- (in ~)
- wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-linux-amd64.tar.gz
- mkdir ~/opt
- tar -C ~/opt -xvzf quarto-1.6.42-linux-amd64.tar.gz
- ln -s ~/opt/quarto-1.6.42/bin/quarto ~/.local/bin/quarto

## Hack for now

- ( echo ""; echo 'export PATH=$PATH:~/.local/bin\n' ; echo "" ) >> ~/.profile
  source ~/.profile

## Copy .ssh from windows

run copy-ssh.sh

## Cloudflare

change SSL to (full)

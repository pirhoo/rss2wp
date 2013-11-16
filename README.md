```
 , _                                   , _
/|/ \  ()  ()    _|_  _     (|  |  |_//|/ \
 |__/  /\  /\     |  / \_    |  |  |   |__/
 | \_//(_)/(_)    |_/\_/      \/ \/    |
```
This tool helps you to import an **RSS feed** to a **WordPress blog** using XMLRPC.

## Installation
### 1. Prerequisite
```bash
sudo apt-get install build-essential git-core python python-pip python-dev
sudo pip install virtualenv
```
### 2.  Download the project
```bash
git clone git@github.com:pirhoo/rss2wp.git
```
### 3. Install
```bash
make install
```
### 4. Configure
Create the following environement variables to configure you're client in command line:

* **WP_URL**: url of your Wordpress xmlrpc endpoint
* **WP_USER**: username to use to connect to Wordpress
* **WP_PWD**: password of this user

## Usage
### Command line
```bash
usage: parser.py [-h] [--force] target

positional arguments:
  target      Feed file path or URL (e.g: ./file.rss, http://exemple.org/rss)

optional arguments:
  -h, --help  show this help message and exit
  --force     Force the parser to create the posts (without checking duplicates).
```

## License
This software is under the [GNU GENERAL PUBLIC LICENSE v3](./LICENSE).

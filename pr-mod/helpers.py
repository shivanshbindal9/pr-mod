import string
import random
import socket
import json
import requests

from config import Config


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """ Generates a random string.
    :param size: Length of random string.
    :type size: Int
    :param chars: Charectors used for random string generation.
    :type chars: String
    :return: String, random string.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def find_free_port(num):
    """ Finds a free port on the server.
    :param num : Number of free ports required.
    :type num: Integer
    :return port : free port no.
    :rtype: Integer
    """
    ports = []
    for _ in range(0, num):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(('', 0))
        addr, port = tcp.getsockname()
        tcp.close()
        ports.append(port)
    return ports


def get_pull_request_info(oauth_token, repo):
    """ Gets pull request details.
    :param oauth_token: Authorization token for Owner.
    :type oauth_token: String
    :param repo: Name of the Github repository.
    :type repo: String
    :return tuple of remote url and git branch name.
    :rtype tuple object
    """
    response = requests.get(
        repo,
        auth=(Config.GITHUB_USER, oauth_token)
    )
    json_data = json.loads(response.text)
    return (
        json_data['head']['user']['login'],
        json_data['base']['repo']['owner']['login'],
        json_data['base']['repo']['name'],
        json_data['head']['ref']
    )


def execute_testfile(container, test_file_params):
    """ Setups environment inside `prmod\base-image` container.
    :param container: docker container for app-environment.
    :type container: Docker object
    :param test_file_params: Parsed Testfile cmd.
    :type test_file_params: UnorderDict Obj
    """
    print("logging: executing testfile cmds")
    # execute Testfile cmds in `prmod\base-image`
    for cmd in test_file_params['CMD']:
        print("logging: executing cmd: {}".format(cmd))
        container.exec_run(cmd, tty=True)

import socket


class MayaTalk:
    def __init__(self, host='localhost', port='6666'):
        self.host = host
        self.port = int(port)
        self.client = None

    @property
    def __get_address(self):
        return self.host, self.port

    def __enter__(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.__get_address)
            return self
        except socket.error, msg:
            raise RuntimeError('Couldn\'t connect with the socket-server : {} \n terminating program'.format(msg))

    def command(self, cmd):
        self.client.send(cmd)
        data = self.client.recv(20480)  # receive the result info
        return data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


if __name__ == '__main__':
    episode = 105
    shot = 14
    task = 'Animation'
    # pyCmd = 'import auto_publish;auto_publish.publish_shot_version({}, {}, "{}")'.format(episode, shot, task)
    pyCmd = 'print os.environ[\'USER\']'
    with MayaTalk(host='192.168.0.22', port='6666') as talk:
        print talk.command(cmd=pyCmd)

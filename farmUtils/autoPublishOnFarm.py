import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import farmConfig

from utils.maya_talk import MayaTalk


def publishOnFarm(episode, shot, task='Animation'):
    pyCmd = 'import auto_publish;auto_publish.publish_shot_version({}, {}, "{}")'.format(episode, shot, task)
    # pyCmd = 'os.environ[\'USER\']'
    result = None
    with MayaTalk(host=farmConfig.autoPublishMachine, port=farmConfig.mayaPort) as talk:
        result = talk.command(cmd=pyCmd)

    print [result.rstrip()], '<--------------'
    # do database entry here for the production to monitor.
    if 'ERROR:' in result:
        print 'Registering Failed Publish for the shot {}'.format('BDG{}_{}'.format(episode, shot))
    else:
        print 'Registering Successful Publish for the shot {}'.format('BDG{}_{}'.format(episode, shot))


if __name__ == '__main__':
    episode, shot, task = None, None, None
    if len(sys.argv) == 4:
        episode, shot, task = sys.argv[1], sys.argv[2], sys.argv[3]
    elif len(sys.argv) == 3:
        episode, shot, task = sys.argv[1], sys.argv[2], 'Animation'
    result = publishOnFarm(episode=episode, shot=shot, task=task)

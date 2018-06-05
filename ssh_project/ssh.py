import argparse
import paramiko
import os
from util import ssh_access as ssh


def main():

    parser = argparse.ArgumentParser(description="Tool to remotely access and manipulate other servers")
    subparser = parser.add_subparsers(title="actions",
                                      description="valid actions",
                                      help="use ssh.py {action} -h for help of specific action",
                                      dest="ssh")




    parser_connectSSH = subparser.add_parser('connection', help="Access remote server and run internal commands")
    parser_connectSSH.add_argument('-c','--config',
                                   dest="config",
                                   default=None,
                                   action="store",
                                   help="A configuration file to acess the credentials is needed. This must have username='<name>', server='<number_or_name>', password='<password>'",
                                   required=False)
    parser_connectSSH.add_argument('-k', '--command',
                                   dest="command",
                                   default=None,
                                   action="store",
                                   help="Write desired command to be run on the server between coats, for example > 'ls -la' ",
                                   required=False)




    parser_copy = subparser.add_parser('copy', help="Copy files trough servers")
    parser_copy.add_argument('-c', '--config',
                             dest="config",
                             default=None,
                             action="store",
                             help="A configuration file to acess the credentials is needed. This must have username='<name>', server='<number_or_name>', password='<password>'",
                             required=False)
    parser_copy.add_argument('-s', '--source',
                             dest="src",
                             default=None,
                             action="store",
                             help="Informe file's original path",
                             required=False)
    parser_copy.add_argument('-d','--destiny',
                             dest="dest",
                             default=None,
                             action="store",
                             help="Inform file's desired destiny path",
                             required=False)
    parser_copy.add_argument('-g', '--get',
                             dest="get",
                             action="store_true",
                             help="Get a copy file from remote server",
                             required=False)
    parser_copy.add_argument('-p', '--put',
                             dest="put",
                             action="store_true",
                             help="Put a copy file on the remote server",
                             required=False)


    args = parser.parse_args()

    if args.ssh == 'connection':
        credentials = ssh.get_credentials(args.config)
        client = ssh.connect_to_client(credentials)
        ssh.run_command(client, args.command)

    elif args.ssh == 'copy' and args.get is not False:
        credentials = ssh.get_credentials(args.config)
        sftp = ssh.connect_and_copy(credentials)
        ssh.get_file_from_server(sftp, args.src, args.dest)


    elif args.ssh == 'copy' and args.put is not False:
        credentials = ssh.get_credentials(args.config)
        sftp = ssh.connect_and_copy(credentials)
        ssh.copy_file_to_server(sftp, args.src, args.dest)





if __name__ == '__main__':
    main()

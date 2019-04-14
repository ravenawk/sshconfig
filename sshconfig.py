#!/usr/bin/env python3
"""Program to add hosts to ssh config file and create aliases."""

import argparse
import os


def sshconf(host, domain, user, port, diffieh, configfile):
    """Print an entry for .ssh config."""
    with open(configfile, 'a') as sshconf:
        sshconf.write("Host {}\n".format(host))
        sshconf.write("  Hostname {}.{}\n".format(host, domain))
        sshconf.write("  Port {}\n".format(port))
        sshconf.write("  User {}\n".format(user))
        if diffieh:
            sshconf.write("  KexAlgorithms +diffie-hellman-group1-sha1\n")
        sshconf.write("\n")
    return


def alias_entry(host, domain, telnet, aliasfile):
    """Print a line in .c-aliases file."""
    with open(aliasfile, 'a') as aliases:
        if telnet:
            aliases.write('alias {0}="telnet {0}.{1}"\n'.format(host, domain))
        else:
            aliases.write('alias {0}="ssh {0}"\n'.format(host))
    return


def entry_check(host, filename):
    """Check if host is in a file."""
    if not os.path.isfile(filename):
        return False
    with open(filename) as lines:
        for line in lines:
            if host in line:
                return True
    return False


def remove_entry(host, filename, filepath):
    """Remove an entry from ssh config and c-aliases."""
    deleteblock = False
    with open(filepath, 'r') as lines:
        memfile = lines.readlines()
    with open(filepath, 'w') as newfile:
        for line in memfile:
            if host in line:
                deleteblock = True
            elif (deleteblock and
                  filename == "sshconfig" and
                  ("Host " not in line)):
                pass
            else:
                newfile.write(line)
                deleteblock = False


def Main():
    """Run if run as a program."""
    aliasfile = os.path.expanduser("~/.c-aliases")
    sshconfig = os.path.expanduser("~/.ssh/config")

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", type=str, default="ne.pvhmc.org",
                        help='Domain name default=ne.pvhmc.org', metavar="")
    parser.add_argument("-D", "--diffie", action='store_true',
                        help='Set diffie-hellman flag (used in old ssh)')
    parser.add_argument("-n", "--hostname", required=True,
                        help='Hostname of device', metavar="")
    parser.add_argument("-p", "--port", default='22', type=int,
                        help='Port number', metavar="")
    parser.add_argument("-r", "--remove", action='store_true',
                        help="Remove entry")
    parser.add_argument("-t", "--telnet", action='store_true',
                        help='telnet instead of ssh')
    parser.add_argument("-u", "--user", type=str, default="admin",
                        help='user to connect with default=admin', metavar="")
    args = parser.parse_args()

    if entry_check(args.hostname, sshconfig):
        if args.remove:
            remove_entry(args.hostname, "sshconfig", sshconfig)
    elif not args.telnet:
        sshconf(args.hostname, args.domain, args.user, args.port,
                args.diffie, sshconfig)

    if entry_check(args.hostname, aliasfile):
        if args.remove:
            remove_entry(args.hostname, "c-aliases", aliasfile)
    else:
        alias_entry(args.hostname, args.domain, args.telnet, aliasfile)
    return


if __name__ == "__main__":
    Main()

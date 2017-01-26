from formatting import *

def process_send_msg(app, msg, user=None):
    '''Send and format a message, if a user / channel is defined PRIVMSG it'''
    if user:
        nmsg = "PRIVMSG {} :{}\r\n".format(user, msg)
        app.client.send(nmsg)
    else:
        app.client.send(msg + "\r\n")

def parse_message(s):
    """Breaks a message from an IRC server into its prefix, command, and arguments.
    """
    if len(s.split()) == 1:
        return
    prefix = ''
    trailing = []
    if not s:
       return
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
        prefix = prefix.split("!")[0]
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args


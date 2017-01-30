import socket, ssl, re
import Value
from setting import *
from Message import *
from Log import *

def send_msg(channel, txt):
    irc.send(bytes('PRIVMSG ' + channel + ' :' + txt + '\n', UTF8))

def pong():
    irc.send(bytes("PONG :pingpong\n", UTF8))

def join(channel, txt):
    irc.send(bytes("JOIN %s\r\n" %channel, UTF8))
    send_msg(channel, txt)

def part(channel, txt):
    send_msg(channel, txt)
    irc.send(bytes("PART %s\r\n" %channel, UTF8))

def quit(txt):
    send_msg(CHAN, txt)
    irc.send(bytes("QUIT\r\n", UTF8))

def react_part(msg):
    prtLog("part: "+msg.nick)
    part(msg.channel, "난 그럼 이만.")

def react_invite(msg):
    prtLog(msg)
    prtLog("invite"+msg.nick)
    irc.send(bytes("JOIN %s\r\n" %msg.channel, UTF8))
    send_msg(msg.channel, "안녕, 나는 미스틱의 리더 블랑쉬다.")

def react_mode(msg):
    if msg.msg == "+o " + NICK:
        send_msg(msg.channel, Value.randOPMsg(msg))
    elif msg.msg == "-o " + NICK:
        send_msg(msg.channel, Value.randDEOPMsg(msg))
    elif msg.msg.find(NICK) != -1:
        send_msg(msg.channel, Value.randCuriousMsg(msg))

def react_appraise(msg):
    prtLog("appraise: "+msg.nick)
    appraise = Value.randAppraise(msg)
    for line in appraise.split('\n'):
        send_msg(msg.channel, line)

def react_error(msg):
    prtLog("appraise error: "+msg.nick)
    send_msg(msg.channel, "!분석 [대상]과 같이 입력하여야 하네.")
    
def run():
    while 1:
        try:
            ircmsg_raw = irc.recv(8192).decode(UTF8)
        except KeyboardInterrupt:
            quit("난 그럼 이만.")
            prtLog("ctrl+c")
            return

        except UnicodeDecodeError as err:
            prtErr("Unicode Error!")
            prtLog(ircmsg_raw)
            prtErr(err)
            continue

        except:
            prtLog(ircmsg_raw)
            prtLog("?")
            continue

        ircmsg_raw = ircmsg_raw.strip("\n\r")
        
        if ircmsg_raw.find("PING :") != -1:
            pong()
            continue
        
        if ircmsg_raw[0] != ':':
            continue

        msg = Message(ircmsg_raw)
        
        if msg.msgType == "INVITE":
            react_invite(msg)
        elif msg.msgType == "MODE":
            react_mode(msg)
        elif msg.msgType == "PRIVMSG":
            if msg.msg[0:3] == '!분석':
                if msg.msg[3:].count('!') != 0 or len(msg.msg) < 4 or msg.msg[4] == ' ':
                    react_error(msg)
                else:
                    react_appraise(msg)

        else:
            prtLog(str(msg))
                
if __name__ == "__main__":
    irc_raw = socket.socket()
    irc_raw.connect((HOST, PORT))
    irc = ssl.wrap_socket(irc_raw)
    irc.send(bytes("NICK " + NICK + "\r\n", UTF8))
    irc.send(bytes("USER %s %s %s : %s\r\n" %(ID, ID, HOST, ID), UTF8))
    print("연결되었습니다.")
    join(CHAN, "안녕, 나는 미스틱의 리더 블랑쉬다.")
    run()

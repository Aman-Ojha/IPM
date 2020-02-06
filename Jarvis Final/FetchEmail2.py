from itertools import chain
import email
import imaplib
import sys
from datetime import datetime

params = {
    'imap_ssl_host':    'imap.yandex.ru',
    'imap_ssl_port':    993,
    'username':         'amanojha.sih@gmail.com',
    'password':         'jira2020',
    'criteria':         {
                            'FROM': 'jira@jarvissih2020.atlassian.net',
                            'SUBJECT': 'Undelivered Mail Returned to Sender'
                        },
    'uid_max':          0,
    'folder':           'Tracking',
    'start_date':       'SINCE 04-Jul-2019',
    'end_date':         'BEFORE 18-Jan-2020'
}

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
    return '(%s)' % ' '.join(chain(*c))

def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return bytes.decode(part.get_payload(decode=1))
    elif type == 'text':
        return bytes.decode(msg.get_payload(decode=1))

def get_email_address(msg):
    # need to be updated for other email search criteria
    index_start = msg.index('<')
    index_end = msg.index('>')
    str = msg[index_start+1:index_end]
    return str

def main(params):
    try:
        server = imaplib.IMAP4_SSL(params['imap_ssl_host'], params['imap_ssl_port'])
        server.login(params['username'], params['password'])
        server.select(params['folder'])
        if params['end_date'] == '':
            search_dates = '(' + params['start_date'] + ')'
        elif params['start_date'] == '':
            search_dates = '(' + params['end_date'] + ')'
        else:
            search_dates = '(' + params['start_date'] + ' ' + params['end_date'] + ')'

        result, data = server.uid('search', search_dates, search_string(params['uid_max'], params['criteria']))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return 1
    else:
        uids = [int(s) for s in data[0].split()]
        if not uids:
            print("Emails found by search criteria: 0")
            return 3
        print("Emails found by search criteria: ", len(uids))

        undelivered_email_list = list()
        for uid in uids:
            params['uid_max'] = max(uids)   # in case for while loop to search for new messages with sleep
            try:
                result, emailData = server.uid('fetch', str(uid), '(RFC822)')
                #result, emailData = server.fetch(str(uid), '(RFC822)')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return 2
            msg = email.message_from_string(emailData[0][1].decode("utf-8"))
            text = get_first_text_block(msg)
            undelivered_email_list.append(get_email_address(text))

        undelivered_email_set = set(undelivered_email_list)
        dlist = {}
        print('\nUndelivered emails:')
        for x in undelivered_email_set:
            dlist.update({x: undelivered_email_list.count(x)})
        sorted_dict = {r: dlist[r] for r in sorted(dlist, key=dlist.get, reverse=True)}
        for k, v in sorted_dict.items():
            print(k, ' : ', v)
    finally:
        if 'server' in locals():
            server.logout()
    return

if __name__ == '__main__':
    start_time = datetime.now()
    exitcode = main(params)
    end_time = datetime.now()
    print('\nDuration: {}'.format(end_time - start_time))
    exit(exitcode)
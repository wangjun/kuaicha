#coding=utf-8
from bottle import route, run, response, request
import sdict
import os
import string
import traceback 

alphabets='abcdefghijklmnopqrstuvwxyz'

def current_file_directory():
            import os, sys, inspect
            path = os.path.realpath(sys.path[0])        # interpreter starter's path
            if os.path.isfile(path):                    # starter is excutable file
                path = os.path.dirname(path)
                return os.path.abspath(path)            # return excutable file's directory
            else:                                       # starter is python script
                caller_file = inspect.stack()[1][1]     # function caller's filename
                return os.path.abspath(os.path.dirname(caller_file))# return function caller's file's directory

def edits1(W):
    N = len(W)
    splits = [(W[:i],W[i:]) for i in xrange(N)]
    deletes = [ x+y[1:] for x,y in splits if y]
    trans = [a + b[1] + b[0] +b[2:] for a,b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a,b in splits for c in alphabets if b]
    inserts =  [a + c + b for a,b in splits for c in alphabets]
    capts = [W.upper(),W.lower(),W.capitalize()]
    return set(deletes+trans+replaces+inserts+capts)
    
index = sdict.Dict()
_localDir=current_file_directory()

_curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
        
dic_name = os.path.join(_curpath,"endict.txt")

for line in open(dic_name,"rb"):
    #print line
    tup = line.rstrip().split('\t')
    en_word = tup[0]
    chn_word = tup[1:]
    chn_word = ' '.join(chn_word)
    index[en_word] = chn_word

@route('/')
def svr():
    response.set_header('content-type', 'text/html; charset=utf-8')
    word= request.query.word.encode('utf-8')
    rel_words = index.prefix(word)
    result='''
    <body onload="document.getElementById('word').focus();">
    <form action="/" method="GET"">
        <input type="text" name="word" id="word"  style="width: 216px;"/>
        <input type="submit" value="  查询  "/>
    </form>
    <br/>
    '''
    for w in rel_words:
        result+= (w+"&nbsp;&nbsp;"+index[w]+"<br/>")

    if len(rel_words)==0:
        cor_words = edits1(word)
        hit = False
        for w in cor_words:
            if w in index:
                hit = True
                result+= ('? '+"&nbsp;&nbsp;<a href='/?word="+w+"'>"+w+"</a><br/>")
    if len(word)>0:
                result += "<hr/>search <a href='http://dict.youdao.com/search?q="+word+"'>"+word+"</a> at youdao.com"
    result+="</body>"
    return result

run(host='127.0.0.1', port=8401)


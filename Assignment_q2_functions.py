#!usr/bin/python
def lcount():
        string=raw_input("Enter Your string")
        if string:
                letters={'upper':'isupper()', 'lower':'abcdefghijklmnopqrstuvwxyz', 'digits':'0123456789', 'space':' '}
                let={'uc':[],'lc':[],'spa':[],'di':[],'spe':[]}
                count={'u':0,'l':0,'sp':0,'sc':0,'d':0}
                for x in string:
                        if x in letters['upper']:
                                let['uc'].append(x)
                                count['u']=count['u']+1
                        elif x in letters['lower']:
                                let['lc'].append(x)
                                count['l']=count['l']+1
                        elif x in letters['space']:
                                let['spa'].append(x)
                                count['sp']=count['sp']+1
                        elif x in letters['digits']:
                                let['di'].append(x)
                                count['d']=count['d']+1
                        else:
                                let['spe'].append(x)
                                count['sc']=count['sc']+1
                if len(string)>=8 and count['u']>0 and count['l']>0 and count['sc']>0 and count['d']>0:
                        print "your password is correct"
                else:
                        print "Not a correct password"

        else:
                lcount()
lcount()
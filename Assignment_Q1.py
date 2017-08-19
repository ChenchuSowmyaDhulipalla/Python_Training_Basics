#!/usr/bin/python
string=raw_input("Enter your string :")
if len(string) == 0:
        print "please enter any string"
else:
        u=l=sc=sp=d=0
        for x in string:
                if x.isupper():
                        u=u+1
                elif x.islower():
                         l=l+1
                elif x in "`~!@#$%^&*()_-+=*/<>?/":
                        sc=sc+1
                elif x.isdigit():
                        sp=sp+1
                elif x in "0123456789":
                        d=d+1
        print "The UPPER case letter count is:",u,"\nThe lower case letter count is:",l,"\nThe special characters count is:",sc,"\nThe spaces count is:",sp,"\nThe digits count is:",d

#!/usr/bin/env python3
import requests
import os
import sys
import argparse



#ARGPARSER
parser = argparse.ArgumentParser(description='search for comments or specific keywords in source code')
parser.add_argument('-u', '--url', required=True, metavar='', help='target url')
parser.add_argument('-k', '--keyword', metavar='', nargs='+', help='search for specific keyword(s)')
parser.add_argument('-l', '--user_list', help='(/PATH) file with list of keywords')
args = parser.parse_args()




#FUNCTIONS:
def keyword_handler():
    default_keyword_list = []
    default_keyword_list.insert(0, "<!")

    #handle NO optional argument is set
    if args.keyword == None and args.user_list == None :     
        return default_keyword_list                         #use only default keyword ["<!"]
    

    #handle BOTH -k AND -l arguments  are set
    if args.keyword != None and args.user_list != None:     
        print("[#]", "-k or -l; it's not possible to use both arguments at the same time")
        print("[+]", "continue with default keyword <!")
        return default_keyword_list                         #use only default keyword
    

    #handle ONLY -k flag is set
    if args.keyword != None:                                
        for item in args.keyword:
            default_keyword_list.append(item)
        return default_keyword_list                         #append keywords -> to default_keyword_list /// ["<!", + items....]
    
    
    #handle ONLY -l flag is set
    if args.user_list != None:                              
        try:
            with open(args.user_list) as f:
                user_wordlist = f.read().split("\n")
                default_keyword_list = user_wordlist                
                return default_keyword_list                 #overwrites the default_keyword_list with user_wordlist
        except FileNotFoundError as e:
            print("[#]", "Error:", e)                      
            print("[+]", "continue with default keyword <!")        
        finally:
            return default_keyword_list                     #use only default keyword



def get_source(arg_url):
    if not arg_url.startswith("http://"):
        mod_url = "http://" + arg_url
    else:
        mod_url = arg_url

    request = requests.get(mod_url)
    source = request.text
    return source       



def search_keyword():               
    source = get_source(args.url)
    keyword_list = keyword_handler()
    print("[+] target:", args.url)
    print("[+] keywords in userlist:", keyword_list)
    
    split_source = source.split("\n")
    for index, value in enumerate(split_source):
        for keyword in keyword_list:
            if keyword in value:
                print("-----------------------------------------------------")
                print("[+] found keyword: [{}] in line number: {}".format(keyword, index+1))
                print("[+]", "context:  ", value)

    
    
if __name__ == "__main__":
    try:
        search_keyword()
    except requests.exceptions.ConnectionError:
        print("[#]", "no valid target, check -u argument")
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)




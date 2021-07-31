import hashlib,re,sys,requests,bs4,os
 
def stringToMD5(string):

    result = hashlib.new('md4',string.encode('utf-8')) #Create an MD5 hash object

    return result.hexdigest() #Return the required hexadecimal hash


def verifyMD4(md4):
    md4Regex = re.compile(r'^[0-9a-f]{32}$') #Create a regex object
    mo = md4Regex.search(md4.lower()) #Create a match object

    if mo == None:
        return False
    else:
        return True


def md4ToString(md4):

    if not verifyMD4(md4):
        print('error' + 'Invalid hash')
        sys.exit()
    else:
        url = 'https://md5decrypt.net/en/Md4/?md4=' + md4 #Create a url

        res = requests.get(url) #Query the url
        res.raise_for_status()
        
        source = res.content

        soup = bs4.BeautifulSoup(source, 'lxml') #Create a beautiful soup object

        css_path = 'html body div#page.p-1.p-3-lg div#container section#section article div#content p em.long-content.string'
        elem = soup.select(css_path) #Find the required element

        try:
            print('msg' + 'Cracked!' + '\n' +'success' + md4 + ':' + elem[0].text) #Print the cracked string
        except:
            print('msg' + 'Hash not found in databases')

def md5Brute(md4, wordlist):
    
    if os.path.exists(wordlist) and os.path.isfile(wordlist): #Check if the wordlist exists and if it is a file
        if not os.path.isabs(wordlist): #Check if it is an absolute path
            wordlist = os.path.abspath(wordlist)
    else:
        print('error' + 'Invalid path') #Exit program if invalid path
        sys.exit()

    if not verifyMD4(md4):  #Verify if hash is correct
        print('error' + 'Invalid hash')
        sys.exit()

    with open(wordlist, 'r', errors='replace') as w:
        words = w.readlines()   #Store all lines in a list

    for word in words:
        md5String = stringToMD5(word.rstrip())

        if md5String == md4:    #Check if hash matches
            print('msg' + 'Cracked!')
            print('success' + md4 + ":" + word)
            break
    else:
        print('msg' + "Not found")
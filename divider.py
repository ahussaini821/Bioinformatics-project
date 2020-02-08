string = "AATGCGTGTGTAAAAAGTGTGTAGATAGTAGATGTATGATGATGATAGTAGTAGTAGATGATGATGATAGTAGTATGATGATGATATGATGATGATGAAGA"

def divider(string):
    split_string = []
    x = []
    for index in range(0, len(string),10):
        split_string.append(string[index:index+10])
        count=1
    for i in range(0,len(split_string),4):
        curr=count*10
        try:
            
            x.append("         "+ str(curr) + "         " + str(curr+10) + "         "+ str(curr+20) + "         "+str(curr+30)+"\n" + " " + split_string[i]+ " " + split_string[i+1] + " " + split_string[i+2] + " " + split_string[i+3])
        except:
            continue
        count += 4
    y = ""
    for i in x:
        y += i + "\n"
    print(y)
    return(y)


divider(string)

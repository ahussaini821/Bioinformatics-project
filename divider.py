string = "AATGCGTGTGTAAAAAGTGTGTAGATAGTAGATGTATGATGATGATAGTAGTAGTAGATGATGATGATAGTAGTATGATGATGATATGATGATGATGAAGA"
split_string = []
def divider(string):
    for index in range(0, len(string),10):
        split_string.append(string[index:index+10])
    for i in range(0,len(split_string),4):
        try:
            print("         10         20         30         40\n",split_string[i],split_string[i+1], split_string[i+2], split_string[i+3])

        except:
            continue



divider(string)

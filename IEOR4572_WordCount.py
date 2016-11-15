# Shelby Jennings, ssj2124
# IEOR W4572, Professor Johar
# Assignment 2

# Problems 1 - 5

def word_distribution(text, proportion=0, word_list=None, case=0):
    word_count = {}
    words = text.split() 
    num_capital = 0 # This is used to track number of capital letter words for proportion count

    # CASE 1 - WANT TO CONSIDER ONLY WORDS STARTING WITH CAPITAL LETTER
    if case==1:     
        # LIST ARGUMENT    
        if word_list != None: # NON EMPTY WORD LIST - WANT TO CONSIDER ONLY WORDS IN GIVEN LIST
            for item in words: 
                if item in word_list or item[:-1] in word_list: # IF WORD MATCHES W/O PUNCTUATION
                    if 65 <= ord(item[0]) <= 90:
                        if 0 <= ord(item[-1]) < 65 or 90 < ord(item[-1]) < 97 or ord(item[-1]) > 122:
                            item = item[:-1] # REMOVE LAST CHARACTER IF NOT A LETTER
                        else: 
                            item = item
                    # PROPORTION
                    if proportion == 1: # PROPORTION IS 1
                        if word_count.get(item, None) == None:
                            word_count[item] = 1/len(word_list) # DIVIDE BY TOTAL IN LIST
                        else: 
                            word_count[item] = (word_count.get(item) + 1) / len(word_list) 
                    elif proportion == 0: # PROPORTION IS 0
                        if word_count.get(item, None) == None:
                            word_count[item] = 1
                        else: 
                            word_count[item] = word_count.get(item) + 1
        
        elif word_list == None: # EMPTY WORD LIST - CONSIDERING ALL WORDS INPUTTED IN FUNCTION WITH CAPITAL 1st LETTER
            for item in words:
            # Order range for upper case letters 97-122
                if 65 <= ord(item[0]) <= 90:
                    num_capital = num_capital + 1 # Keeping track of number of capital words for proportion
                    if 0 <= ord(item[-1]) < 65 or 90 < ord(item[-1]) < 97 or ord(item[-1]) > 122:
                        item = item[:-1] # REMOVE LAST CHARACTER IF NOT A LETTER
                    else: 
                        item = item 
                    # PROPORTION 
                    if proportion == 1: # PROPORTION IS 1 - WANT RATIO OF WORD TO TOTAL NOT JUST COUNT
                        if word_count.get(item, None) == None:
                            word_count[item] = 1 / num_capital # DIVIDE BY NUMBER OF CAPITAL 1st LETTERS
                        else: 
                            word_count[item] = (word_count.get(item) + 1) / num_capital
                    elif proportion == 0: # PROPORTION IS 0 - WANT RAW COUNT OF WORD
                        if word_count.get(item, None) == None:
                            word_count[item] = 1
                        else: 
                            word_count[item] = word_count.get(item) + 1
    
    # CASE 0 - CONSIDER ALL WORDS INPUTTED IN FUCTION REGARDLESS OF CASE OF 1st LETTER
    elif case==0:
        # LIST ARGUMENT 
        if word_list != None: # NON EMPTY WORD LIST - CONSIDER ALL WORDS GIVEN THEY'RE ALSO IN LIST
            for item in words:
                if item in word_list or item[:-1] in word_list:
                    item = item.lower()
                    #Order range for alphabet characters: 65-90 and 97-122
                    if 0 <= ord(item[-1]) < 65 or 90 < ord(item[-1]) < 97 or ord(item[-1]) > 122: 
                        item = item[:-1] # REMOVE LAST CHARACTER IF NOT A LETTER
                    else: 
                        item = item 
                    # PROPORTION
                    if proportion == 1: # PROPORTION IS 1 - WANT RATIO OF WORD TO TOTAL NOT JUST COUNT
                        if word_count.get(item, None) == None:
                            word_count[item] = 1 / len(word_list)
                        else: 
                            word_count[item] = (word_count.get(item) + 1) / len(word_list)
                    elif proportion == 0: # PROPORTION IS 0 - WANT RAW COUNT OF WORD
                        if word_count.get(item, None) == None:
                            word_count[item] = 1
                        else: 
                            word_count[item] = word_count.get(item) + 1
                            
        elif word_list == None: # EMPTY WORD LIST - CONSIDER ALL WORDS INPUTTED IN FUNCTION
            for item in words:
                item = item.lower()
                # Order range for alphabet characters: 65-90 and 97-122
                if 0 <= ord(item[-1]) < 65 or 90 < ord(item[-1]) < 97 or ord(item[-1]) > 122:
                    item = item[:-1] # REMOVE LAST CHARACTER IF NOT A LETTER
                else: 
                    item = item 
                
                # PROPORTION
                if proportion == 1: # PROPORTION IS 1 - WANT RATIO OF WORD TO TOTAL NOT JUST COUNT
                    if word_count.get(item, None) == None:
                        word_count[item] = 1 / len(words) # DIVIDE BY NUMBER OF WORDS IN INPUT
                    else: 
                        word_count[item] = (word_count.get(item) + 1) / len(words)
                elif proportion == 0: # PROPORTION IS 0 - WANT RAW COUNT OF WORD
                    if word_count.get(item, None) == None:
                        word_count[item] = 1
                    else: 
                        word_count[item] = word_count.get(item) + 1
    
    # SORTING VALUES IN WORD_COUNT BY VALUE (NOT KEY)
    from operator import itemgetter
    sorted_word_count = sorted(word_count.items(),key=itemgetter(1),reverse=True)
    return sorted_word_count

    

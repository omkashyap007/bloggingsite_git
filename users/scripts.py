def correctPassword(password) : 
    charset = "abcdefghijklmnopqrstuvwxyz"
    alpha = False
    numeric = False
    char = False 
    capalpha = False
    alpha_len =0
    numeric_len = 0
    char_len = 0 
    capalpha_len = 0
    for i in password :
        if i.isdigit(): 
            # print("The term {} is digit".format(i))
            numeric=  True
            numeric_len +=1
            
        elif i.lower() == i :
            if i in charset : 
                # print("The term {} is lower".format(i))
                alpha_len += 1
                alpha = True
        
        elif i.upper() == i :
            if i in charset.upper(): 
                # print("The term {} is upper".format(i))
                capalpha = True
                capalpha_len += 1
                
        if i not in charset.upper() and i not in charset and not i.isdigit() :
            # print("The term {} is character".format(i))
            ...
    
    # print(alpha_len+ numeric_len + capalpha_len)
    if alpha_len+ numeric_len + capalpha_len < len(password) : 
        char = True
    
    if char and alpha and numeric and capalpha : 
        return True
    return False

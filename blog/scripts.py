from blog.models import Hashtag 
def CreateHashtagList(text) :
    not_charlist = ["#" , "," , " "]
    hashtag_char = False
    length = len(text)-1
    l = []
    stack = []
    for j , i in enumerate(text) :
        if i == "#":
            hashtag_char = True

        if (i == " " or i == "," ) and hashtag_char :
            if "".join(stack) == "":
                stack = []
                hashtag_char = False
            else : 
                l.append( str("".join(stack)) )
                stack = []
                hashtag_char = False 
            
        if i not in not_charlist and hashtag_char:
            stack.append(i)
            
            if j == length :
                l.append( str("".join(stack)) )
                stack = []
                hashtag_char = False
    return l


def CreateOrAddHashtag(updated_hashtag_list  , post) :
    post_hashtag_list = list(post.hashtags.all())
    
    for i in post_hashtag_list :
        if i.title not in updated_hashtag_list : 
            post.hashtags.remove(i.id)
    
    for i in updated_hashtag_list :
        hashtag = Hashtag.objects.filter(title = i).first() 
        
        if hashtag not in post_hashtag_list :
            if hashtag :
                post.hashtags.add(hashtag.id)
            if not hashtag :
                hashtag =  Hashtag(title = i)
                hashtag.save()
                post.hashtags.add(hashtag.id)
    post.save()
    return list(post.hashtags.all())

def HashtagToList(theHashtags) : 
    return "#{} ".join(theHashtags)

def getErrorList(errors):
    l = []
    for i in errors:
        for j in errors[i]:
            l.append(j)
    return l

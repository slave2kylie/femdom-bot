mp={"0":"0"}

class KEYS:
    CMD_ROLE = 'cmd_role'
    EMBED_COLOR = 'embed_color'
    
def set(guild:str,key:str,value):
    global mp
    mp[guild+key]=value

def get(guild:str,key:str):
    global mp
    return mp.get(guild+key)


def MakeFileName( path, module, name ):
    idx = path.rfind('\\')
    idx2 = path.rfind('/')
    if idx2 > idx:
        idx = idx2
    suffix = path[idx+1:]
    
    return path + '\\'+ module + '\\' + name + suffix
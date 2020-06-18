import os


class Thing:
    def __init__(self, path):
        buf, name = '', ''
        for j in path[::-1]:
            if j == '\\' or j == '/':
                break
            else:
                buf += j
        for k in buf[::-1]:
            name += k
        if len(name) == 0:
            name = path[:-1]
        self.name = name
        self.path = self.name + "\\"
        if len(name) < 3:
            self.type = 'Локальний диск'
            self.size = ''
        elif os.path.isdir(path) == True:
            self.type = 'Папка'
            self.size = ''
        else:
            self.type = 'Файл'
            os.chdir(path[:-len(name)])
            buf = "%14d" % (os.path.getsize(name) / 2 ** 10)
            size = buf + ' КБ'
            self.size = size


def backend(path):
    if path != '':
        if len(path) == 1:
            path += ":\\"

        tree = os.walk(path)

        def findthings(te):
            try:
                if path == "C:\\" or path == "D:\\":
                    for tree in te:
                        for m in tree[1] + tree[2]:
                            if tree[0][-1] != '\\' or tree[0][-1] != '/':
                                dirs = Thing(str(tree[0] + '\\' + m))
                            else:
                                dirs = Thing(str(tree[0] + m))
                            listofthings.append(dirs)
                        break
                    return listofthings
                elif tuple(te)[0][0] == "D:":
                    tre = list(os.walk(str(tuple(te)[0][0])+"\\"))
                    for y in tre:
                        for m in y[1] + y[2]:
                            if y[0][-1] != '\\' or y[0][-1] != '/':
                                dirs = Thing(str(y[0] + '\\' + m))
                            else:
                                dirs = Thing(str(y[0] + m))
                            listofthings.append(dirs)
                        break
                    return listofthings
                else:
                    te = os.walk(path)
                    tree = tuple(te)[0]
                    for m in tree[1] + tree[2]:
                        if tree[0][-1] != '\\' or tree[0][-1] != '/':
                            dirs = Thing(str(tree[0] + '\\' + m))
                        else:
                            dirs = Thing(str(tree[0] + m))
                        listofthings.append(dirs)
                    return listofthings
            except:
                te = os.walk(path)
                tree = tuple(te)[0]
                for m in tree[1] + tree[2]:
                    if tree[0][-1] != '\\' or tree[0][-1] != '/':
                        dirs = Thing(str(tree[0] + '\\' + m))
                    else:
                        dirs = Thing(str(tree[0] + m))
                    listofthings.append(dirs)
                return listofthings

        listofthings = []
        l = findthings(tree)
        return l

    else:
        treec = os.walk('C:/')
        treed = os.walk('D:/')

        def localdisks(tree):
            for i in tree:
                disk = Thing(str(i[0])[:-1])
                listofdisks.append(disk)
                break

        listofdisks = []

        localdisks(treec)
        localdisks(treed)
        return listofdisks


def open_file(path, name):
    os.system("cd " + path)
    os.system("start " + name)

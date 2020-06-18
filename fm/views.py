from django.shortcuts import render
from .models import Data
from .backend import backend, open_file
from django.views.generic import View
import os
from shutil import rmtree, move, copytree, copyfile

class st:
    savetable1 = {}
    savetable2 = {}
    obj1 = ''
    obj2 = ''


def new_table(path=''):
    table = Data.objects.all()
    for h in range(len(table)):
        obj = Data.objects.get(path=table[h].path)
        obj.delete()
    if path!='':
        if path[-1]!='/' and path[-1]!='\\':
            listofthings = backend(path)
        elif path=="C:\\":
            listofthings = backend(path)
        else:
            listofthings = backend(path[:-1])
    else:
        listofthings = backend(path)
    for i in range(len(listofthings)):
        try:
            Data.objects.create(
                path=listofthings[i].path,
                name=listofthings[i].name,
                type=listofthings[i].type,
                size=listofthings[i].size)
        except: pass
    table = Data.objects.all()
    return table


def main_page(request):
    st.savetable1 = new_table()
    st.savetable2 = new_table()
    class Thi():
        def __init__(self):
            self.name = ""
            self.path = ""
            self.slug = 'obj'
        def __str__(self):
            return self.name
    st.obj1 = Thi()
    st.obj2 = Thi()
    return render(request, 'fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1, 'table2': st.savetable2})


class create_file(View):
    def post(self, request):
        p = request.POST.get('fullpath')
        buf, n = '', ''
        for j in p[::-1]:
            if j == '\\' or j == '/':
                break
            else:
                buf += j
        for k in buf[::-1]:
            n += k
        open(p, "a+")
        class Thin:
            def __init__(self):
                self.name = n
                self.path = p[:-(len(n)+1)]
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.savetable1 = new_table(p[:-(len(n)+1)])
        st.obj1 = Thin()
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})


class delete_thing(View):
    def post(self, request):
        p = request.POST.get('path')[:-(len(request.POST.get('name'))+1)]
        t = dict(request.POST)
        delete_list = t.get('file')
        for i in delete_list:
            try: os.remove(p+"\\"+i)
            except: rmtree(p+"\\"+i)
        buf = ''
        for i in p:
            if i != '/' and i != "\\":
                buf += i
            else:
                buf = ''
        class Thin:
            def __init__(self):
                if buf == "":
                    self.name = p[:2]
                else:
                    self.name = buf
                self.path = p
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.savetable1 = new_table(p)
        st.obj1 = Thin()
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})


class create_dir(View):
    def post(self, request):
        p = request.POST.get('fullpath')
        if not os.path.exists(p):
            os.makedirs(p)
        buf, n = '', ''
        for j in p[::-1]:
            if j == '\\' or j == '/':
                break
            else:
                buf += j
        for k in buf[::-1]:
            n += k
        class Thin:
            def __init__(self):
                self.name = n
                self.path = p
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.savetable1 = new_table(p)
        st.obj1 = Thin()
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})


class click_thing(View):
    def get(self, request, slug):
        if request.GET.get("check") == '0':
            if request.GET.get("numbtable") == '1':
                try:
                    if request.GET.get("slug")[0] == request.GET.get("path")[0].lower:
                        obj = Data.objects.get(name=request.GET.get("name"))
                    else:
                        raise SyntaxError
                except:
                    try:
                        st.savetable1 = new_table(request.GET.get("path")[:-len(request.GET.get("name"))])
                        obj = Data.objects.get(name=request.GET.get("name"))
                    except:
                        st.savetable1 = new_table()
                        obj = Data.objects.get(name=request.GET.get("name"))
                if obj.type == 'Файл':
                    open_file(obj.path, obj.name)
                    buf = ''
                    for u in request.GET.get("path")[:-(len(request.GET.get("name")) + 1)]:
                        if u != '/' and u != "\\":
                            buf += u
                        else:
                            buf = ''
                    class Thin:
                        def __init__(self):
                            self.name = buf
                            self.path = request.GET.get("path")[:-(len(request.GET.get("name"))+1)]
                            self.slug = 'obj1'
                        def __str__(self):
                            return self.name
                    st.obj1 = Thin()
                    st.savetable1 = new_table(obj.path[:-(len(obj.name)+1)])
                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2':st.obj2, 'table1': st.savetable1,
                                                              'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})
                if obj.type == 'Папка' or 'Локальний диск':
                    st.savetable1 = new_table(obj.path)
                    st.obj1 = obj
                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                              'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})
            elif request.GET.get("numbtable") == '2':
                try:
                    if request.GET.get("slug")[0] == request.GET.get("path")[0].lower:
                        obj = Data.objects.get(name=request.GET.get("name"))
                    else:
                        raise SyntaxError
                except:
                    try:
                        st.savetable2 = new_table(request.GET.get("path")[:-len(request.GET.get("name"))])
                        obj = Data.objects.get(name=request.GET.get("name"))
                    except:
                        st.savetable2 = new_table()
                        obj = Data.objects.get(name=request.GET.get("name"))
                if obj.type == 'Файл':
                    open_file(obj.path, obj.name)
                    buf = ''
                    for u in request.GET.get("path")[:-(len(request.GET.get("name")) + 1)]:
                        if u != '/' and u != "\\":
                            buf += u
                        else:
                            buf = ''
                    class Thin:
                        def __init__(self):
                            self.name = buf
                            self.path = request.GET.get("path")[:-(len(request.GET.get("name")) + 1)]
                            self.slug = 'obj2'
                        def __str__(self):
                            return self.name
                    st.obj2 = Thin()
                    st.savetable2 = new_table(obj.path[:-(len(obj.name) + 1)])
                    return render(request, 'return_fm.html',
                                  {'obj2': st.obj2, 'obj1': st.obj1, 'table1': st.savetable1, 'table2': st.savetable2,
                                   'numbtable': request.GET.get("numbtable")})
                if obj.type == 'Папка' or 'Локальний диск':
                    st.savetable2 = new_table(obj.path)
                    st.obj2 = obj
                    return render(request, 'return_fm.html',
                                  {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1, 'table2': st.savetable2,
                                   'numbtable': request.GET.get("numbtable")})
        else:
            iv = request.GET.get("path")[:-len(request.GET.get("name"))]
            if iv[1:] == ":\\\\":
                req_p = request.GET.get("path")[:2]
                req_n = ''
                mb = 0
            else:
                req_p = request.GET.get("path")
                req_n = request.GET.get("name")
                mb = 1
            if request.GET.get("numbtable") == '1':
                try:
                    if mb == 1:
                        st.savetable1 = new_table(req_p[:-(len(req_n) + mb)])
                    else:
                        st.savetable1 = new_table(req_p[0] + ':\\')
                except:
                    st.savetable1 = new_table(req_p[0]+':\\')
                try:
                    buf=''
                    for i in req_p[:-(len(req_n)+mb)]:
                        if i != '/' and i != "\\":
                            buf+=i
                        else:
                            buf = ''
                    class Thin:
                        def __init__(self):
                            if mb == 1:
                                self.name = buf
                                self.path = req_p[:-(len(req_n)+mb)]
                            else:
                                self.name = req_p+"\\"
                                self.path = req_p+"\\"
                            self.slug = 'obj1'
                        def __str__(self):
                            return self.name
                    st.obj1 = Thin()
                    for t in st.savetable2:
                        if t.name == "D:" or t.name == "E:" or t.name == "D:\\" or t.name == "E:\\":
                            for c in st.savetable1:
                                if c.name == "D:" or c.name == "E:" or c.name == "D:\\" or c.name == "E:\\":
                                    return render(request, 'fm.html', {'obj1': st.obj1, 'obj2':st.obj2, 'table1': st.savetable1, 'table2': st.savetable2})
                                else:
                                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                                              'table1': st.savetable1,
                                                                              'table2': st.savetable2,
                                                                              'numbtable': request.GET.get(
                                                                                  "numbtable")})
                        else:
                            return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                                      'table1': st.savetable1, 'table2': st.savetable2,
                                                                      'numbtable': request.GET.get("numbtable")})
                except:
                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                              'table1': st.savetable1, 'table2': st.savetable2,
                                                              'numbtable': request.GET.get("numbtable")})
            elif request.GET.get("numbtable") == '2':
                try:
                    if mb == 1:
                        st.savetable2 = new_table(req_p[:-(len(req_n) + mb)])
                    else:
                        st.savetable2 = new_table(req_p[0] + ':\\')
                except:
                    st.savetable2 = new_table(req_p[0]+':\\')
                try:
                    buf=''
                    for i in req_p[:-(len(req_n)+mb)]:
                        if i != '/' and i != "\\":
                            buf+=i
                        else:
                            buf = ''
                    class Thin:
                        def __init__(self):
                            if mb == 1:
                                self.name = buf
                                self.path = req_p[:-(len(req_n)+mb)]
                            else:
                                self.name = req_p+"\\"
                                self.path = req_p+"\\"
                            self.slug = 'obj2'
                        def __str__(self):
                            return self.name
                    st.obj2 = Thin()
                    for t in st.savetable2:
                        if t.name == "D:" or t.name == "E:" or t.name == "D:\\" or t.name == "E:\\":
                            for c in st.savetable1:
                                if c.name == "D:" or c.name == "E:" or c.name == "D:\\" or c.name == "E:\\":
                                    return render(request, 'fm.html', {'obj1': st.obj1, 'obj2':st.obj2,
                                                                       'table1': st.savetable1, 'table2': st.savetable2})
                                else:
                                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                                              'table1': st.savetable1,
                                                                              'table2': st.savetable2,
                                                                              'numbtable': request.GET.get(
                                                                                  "numbtable")})
                        else:
                            return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                                      'table1': st.savetable1, 'table2': st.savetable2,
                                                                      'numbtable': request.GET.get("numbtable")})
                except:
                    return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2,
                                                                      'table1': st.savetable1, 'table2': st.savetable2,
                                                                      'numbtable': request.GET.get("numbtable")})


class change_thing(View):
    def post(self, request):
        p = request.POST.get('path')[:-(len(request.POST.get('name'))+1)]
        t = dict(request.POST)
        old_list = t.get('name')
        new_list = t.get('newname')
        for n in range(len(new_list)):
            if new_list[n] != old_list[n]:
                os.rename(p+"\\"+old_list[n], p+"\\"+new_list[n])
        buf = ''
        for i in p:
            if i != '/' and i != "\\":
                buf += i
            else:
                buf = ''
        class Thin:
            def __init__(self):
                self.name = buf
                self.path = p
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.savetable1 = new_table(p)
        st.obj1 = Thin()
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})


class move_thing(View):
    def post(self, request):
        moveto = request.POST.get('path')
        path = request.POST.get('path1')
        t = dict(request.POST)
        files = t.get('file')
        try:
            for f in files:
                src = path+"\\"+f
                dst = moveto+"\\"+f
                move(src, dst)
        except:
            pass
        x = new_table(moveto)
        for r in x:
            pass
        st.savetable2 = x
        for rq in st.savetable2:
            pass
        buf = ''
        for i in path:
            if i != '/' and i != "\\":
                buf += i
            else:
                buf = ''
        class Thin:
            def __init__(self):
                self.name = buf
                self.path = path
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.obj1 = Thin()
        st.savetable1 = new_table(path)
        for rr in st.savetable1:
            pass
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})


class copy_thing(View):
    def post(self, request):
        moveto = request.POST.get('path')
        path = request.POST.get('path1')
        t = dict(request.POST)
        files = t.get('file')
        try:
            for f in files:
                src = path+"\\"+f
                dst = moveto+"\\"+f
                try:
                    copyfile(src, dst)
                except:
                    copytree(src, dst)
        except:
            pass
        buf = ''
        for i in moveto:
            if i != '/' and i != "\\":
                buf += i
            else:
                buf = ''
        class Thin:
            def __init__(self):
                self.name = buf
                self.path = moveto
                self.slug = 'obj'
            def __str__(self):
                return self.name
        st.obj2 = Thin()
        st.savetable2 = new_table(moveto)
        return render(request, 'return_fm.html', {'obj1': st.obj1, 'obj2': st.obj2, 'table1': st.savetable1,
                                                  'table2': st.savetable2, 'numbtable': request.GET.get("numbtable")})



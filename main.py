#!/usr/bin/python
# -*- coding: utf-8 -*-

# calculator.py
import wx
import wx.aui
from setting_UCF import UCF_LIB
import xml.etree.cElementTree as ET
from xml.dom.minidom import Document
import copy
from transducer import AIgroup
import inspect

class dict2xml(object):
    doc     = Document()

    def __init__(self, structure):

        rootName    = 'SC1'
        self.root   = self.doc.createElement(rootName)

        self.doc.appendChild(self.root)
        self.build(self.root, structure)

    '''
    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                #tag = self.doc.createElement(k)
                #father.appendChild(tag)
                self.build(self.root, structure[k])

        elif type(structure) == list:
            pass
                
        elif structure.__class__.__name__ == 'LabViewXml':
            father.appendChild(structure.root)
            
        else:
            data    = str(structure)
            tag     = self.doc.createTextNode(data)
            father.appendChild(tag)
            
    '''
    def build(self, father, structure):
        if type(structure) == dict:
            for k in structure:
                tag = self.doc.createElement(k)
                father.appendChild(tag)
                self.build(tag, structure[k])

        elif type(structure) == list:
            grandFather = father.parentNode
            tagName     = father.tagName
            grandFather.removeChild(father)
            tag = self.doc.createElement(tagName)
            
            for l in structure:    
                self.build(tag, l)
                grandFather.appendChild(tag)
                

        else:
            if isinstance(structure,AIgroup):
                if 'xmllist' in structure.__dict__:
                    nelem = 0
                    propdict = []
                    for key in structure.xmllist:
                        if key in structure.__dict__.keys():
                            if not hasattr(structure.__dict__[key], '__call__'):
                                nelem += 1
                                value = structure.__dict__[key]
                                temp = {'Name':key,'Val':value}
                                if type(value) == type(2.03) or type(value) == type(2): 
                                    propdict.append({'DBL':temp})
                                
                                elif type(value) == type(True):
                                    propdict.append( {'Boolean':{'Name':key,'Val':int(value)}})
                                
                                else:
                                    propdict.append( {'String':temp})
                                
                    propdict.insert(0,{'Name':''})
                    propdict.insert(1,{'NumElts':nelem})  
                    self.build(father,propdict)
                    
            else:

                data    = str(structure)
                tag     = self.doc.createTextNode(data)
                father.appendChild(tag)


    def display(self):
        print self.doc.toprettyxml(indent="  ")
    
    def GetXml(self):
        aa = self.doc.toprettyxml(indent="  ")
        return aa
        
class SelRadioButton(wx.RadioButton):
    def __init__(self,parent,skey=None):
        super(SelRadioButton, self).__init__(parent)
        self.key = skey


class SelCheckButton(wx.CheckBox):
    def __init__(self,parent,skey=None):
        super(SelCheckButton, self).__init__(parent, label=skey,style=wx.SHAPED)
        self.key = skey

class SelLabel(wx.StaticText):
    def __init__(self,parent,skey=None):
        super(SelLabel, self).__init__(parent, label=skey)
        self.key = skey
        
class SelTextCtrl(wx.TextCtrl):
    def __init__(self,parent,skey=None,size=(150,20),style=wx.DEFAULT):
        super(SelTextCtrl, self).__init__(parent,size=size,style=style)
        self.key = skey    

class SelChoice(wx.Choice):
    def __init__(self,parent,skey=None):
        super(SelChoice, self).__init__(parent)
        self.key = skey      

class SelButton(wx.Button):
    def __init__(self,parent,skey=None):
        super(SelButton, self).__init__(parent,label=skey)
        self.key = skey     


class ScxiFrame(wx.Frame):
    def __init__(self,parent,title='Setup'):
        size = (600,620)
        self.settings = {}        
        self.items = {}
        super(ScxiFrame, self).__init__(parent,size=size,title=title,style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.ModelNoteBookPanel = wx.Panel(self)
        
        bookStyle = wx.aui.AUI_NB_DEFAULT_STYLE 
        bookStyle &= ~(wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        bookStyle &= ~(wx.aui.AUI_NB_TAB_MOVE)
        self.ModelNoteBook = wx.aui.AuiNotebook(self.ModelNoteBookPanel,1,size=(500,500),style=bookStyle)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ModelNoteBook, 1, wx.EXPAND,border=5)
        
        
        hbox = wx.GridSizer(rows=1,cols=3,vgap=5,hgap=5)
        
        self.Btn_resetpage = SelButton(self.ModelNoteBookPanel,'ResetCurrentPage')
        self.Btn_resetall =  SelButton(self.ModelNoteBookPanel,'ResetALLPages')
        self.Btn_apply = SelButton(self.ModelNoteBookPanel,'OK')
        
        hbox.Add(self.Btn_resetpage, 0, wx.ALIGN_CENTER,border=5)
        hbox.Add(self.Btn_resetall, 0, wx.ALIGN_CENTER,border=5)
        hbox.Add(self.Btn_apply, 0, wx.ALIGN_CENTER,border=5)
        box.Add(hbox, 0, wx.ALIGN_RIGHT|wx.ALL,border=15)


        # create mod pages
        for i in range(1,5):
            self.AddModPage(i)

        self.ModelNoteBookPanel.SetSizer(box)
        self.ModelNoteBookPanel.Layout()        
        self.create_bind()
        self.Show()
    
    
    
    def create_bind(self):
        self.Btn_resetpage.Bind(wx.EVT_LEFT_DOWN,self.OnResetPage)
        self.Btn_resetall.Bind(wx.EVT_LEFT_DOWN,self.OnResetAll)
        self.Btn_apply.Bind(wx.EVT_LEFT_DOWN,self.OnApply)
        
    
    
    def OnApply(self,event):
        self.GetValue()
        self.export_xml()
    
    def GetValue(self):
        for key,item in self.items.items():
            self.settings[key] = item.GetValue()
        #print self.settings
        
    def OnResetPage(self,event):
        pagename = self.ModelNoteBook.GetPageText(self.ModelNoteBook.GetSelection())
        self.Reset(pagename)
    
    def OnResetAll(self,event):
        self.Resetall()
    
    def Reset(self,pagenamelist):
        self.items[pagenamelist].CleanUp()
        
    
    def Resetall(self):
        for key,pagepanel in self.items.items():
            self.Reset(key)
        
    
    def AddModPage(self,id):
        modname = 'mod'+str(id)
            
        self.items[modname] = {}
        self.settings[modname] = {}
        self.items[modname] = ModulePanel(self,id,self.settings[modname])
        self.ModelNoteBook.AddPage(self.items[modname], modname)        
        

    def cleanup_settings(self):
        settings_exp = {}
        
        for modkey,mod in self.settings.items():
            temp_mod = {}
            for channelkey,channel in mod.items():
                if channel['InUseChk']:
                    temp_mod[channelkey] = [{'String':{'Name':'Channel Name','Val':channel['Nameinput']}},
                                            {'String':{'Name':'Channel type','Val':channel['Transducerins']['item'].__class__.__name__}},
                                            {'String':{'Name':'Channel Physical Channel','Val':channel['PhysicalChannelName']}},
                                            {'String':{'Name':'Channel Transducer','Val':channel['Transducer']}},
                                            {'Cluster':channel['Transducerins']['item']}] #.GetPropDict(channel['PhysicalChannelName']}]
                #else:
                #    temp_mod[channelkey] = ''
            
            if len(temp_mod) > 0:
                settings_exp[modkey] = temp_mod
                
        return settings_exp
                    

    def export_xml(self):
        xml1 = dict2xml(self.cleanup_settings())
        
        f1 = open('xml_temp.xml','w')
        f1.write(xml1.GetXml())
        f1.close()
        #print self.settings
        
class ChannelSettings():
    ''' This is the AIgroup for internal voltage excitation'''
    
    def __init__(self, parent,box,name):
        self.items = {}
        self.settings = {'PhysicalChannelName':name,
                         'InUseChk':False,
                         'Nameinput':'',
                         'Transducer':'',
                         'Transducerins':None
                         }
        
        self.parent = parent
        self.items['PhysicalChannelName'] = SelLabel(parent,name)
        self.items['InUseChk'] = SelCheckButton(parent,'In Use?             ')
        
        self.items['Name'] = SelLabel(parent,'Physical Channel Name')
        self.items['Nameinput'] = SelTextCtrl(parent)

        self.items['Transducer1'] = SelLabel(parent,'Transducer Template')
        self.items['Transducerselect'] = SelChoice(parent) #SelButton(parent,'Select') 
        tlist = ['']
        tlist.extend(UCF_LIB.lib.keys())
        tlist.sort()
        self.items['Transducerselect'].AppendItems(tlist)
        
        
        self.items['Transducer2'] = SelLabel(parent,'Transducer Setting')
        self.items['Transducersetting'] = SelButton(parent,'Show')            
 
        
        self.itemkeylist = ['PhysicalChannelName','Name','Transducer1','Transducer2','InUseChk','Nameinput','Transducerselect','Transducersetting']
        
        sizer = wx.FlexGridSizer(rows=2, cols=4, hgap=15, vgap=15)
        # add component to size
        self.AddToSize(sizer,self.items,self.itemkeylist)
        
        # disable component as status
        self.EnableGroup(self.items,self.itemkeylist,False)
        self.EnableGroup(self.items,['InUseChk','PhysicalChannelName'],True)
        
        box.Add(sizer, 1, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.CreateBind()
        
    
    def CreateBind(self):
        self.parent.Bind(wx.EVT_CHECKBOX,self.OnUse,self.items['InUseChk'])
        self.items['Transducersetting'].Bind(wx.EVT_LEFT_DOWN,self.OnTransSet)
        self.items['Transducerselect'].Bind(wx.EVT_CHOICE, self.OnTransSelect)
    
    def OnTransSelect(self,event):
        self.settings['Transducer'] = self.items['Transducerselect'].GetStringSelection()
        if len(self.settings['Transducer']) > 0:
            self.settings['Transducerins'] = UCF_LIB.duplicate(self.settings['PhysicalChannelName'],self.settings['Transducer'])
        #print self.settings['Transducerins']
        
        
        
    def OnTransSet(self,event):
        if self.settings['Transducerins'] != None:
            g1 = TransducerDiag(self.parent,self.settings)
            g1.Show()
        else:
            errormessage = 'No transducer template selected, pick from the left dropdown list\n'
            a1 = wx.MessageDialog(self.parent, errormessage, caption='Error', style=wx.OK|wx.ICON_QUESTION)
            a1.ShowModal()              
        
    def OnUpdate(self,event):
        self.SetValue()
    
    def GetValue(self):
        self.settings['Nameinput'] = self.items['Nameinput'].GetValue()
        
        return self.settings
    
    def SetValue(self):
        self.items['InUseChk'].SetValue(self.settings['InUseChk'])
        self.items['Nameinput'].SetValue(self.settings['Nameinput'])
        self.items['Transducerselect'].SetStringSelection(self.settings['Transducer'])

        
    def CleanUp(self):
        self.settings['Nameinput'] = ''
        self.settings['Transducer'] = ''
        self.settings['InUseChk'] = False
        self.settings['Transducerins'] = None
        
        self.EnableGroup(self.items,self.itemkeylist,False)
        self.EnableGroup(self.items,['InUseChk','PhysicalChannelName'],True)
        self.OnUpdate(None)
            
    def OnUse(self,event):
        icheckbox = event.GetEventObject()
        if event.IsChecked():
            self.settings['InUseChk'] = True
            self.EnableGroup(self.items,self.itemkeylist,True)
            self.SetValue()
        else:
            # clean selection
            self.CleanUp()

    def OnClean(self,event):
        self.CleanUp()
    
    def EnableGroup(self,itemdict,itemkeylist,enable=True):
        for itemkey in itemkeylist:
            itemdict[itemkey].Enable(enable)      
        
    def AddToSize(self,sizer,itemdict,itemkeylist):
        for itemkey in itemkeylist:
            sizer.Add(itemdict[itemkey],0,0)


class ModulePanel(wx.Panel):
  
    def __init__(self, parent,id,settings):
        
        super(ModulePanel, self).__init__(parent)
        self.modid = id
        self.items = {}
        self.settings = {}
        box = wx.BoxSizer(wx.VERTICAL)
        self.channelname = []
        self.modname = 'mod'+str(self.modid)
        # initial channels
        for i in range(0,8):
            channelname = 'ai'+str(i)
            self.channelname.append(channelname)
            self.items[channelname] = ChannelSettings(self,box,'SC1'+self.modname+'/'+channelname)
            
        self.SetSizer(box)
        self.Layout()
        
    def SetValue(self):
        for channelname in self.channelname:
            self.items[channelname].SetValue(self.settings[channelname])
    
    def GetValue(self):
        for channelname in self.channelname:
            self.settings[channelname] = self.items[channelname].GetValue()
            
        return self.settings
    def CleanUp(self):
        for channelname in self.channelname:
            self.items[channelname].CleanUp()
            
    def OnCleanUp(self):
        self.CleanUp()

    def OnSubmit(self,event):
        print self.results
        self.Destroy()
        

class TransducerDiag(wx.Dialog):
    def __init__(self, parent,settings):
        super(TransducerDiag, self).__init__(parent) 
        #print settings
        self.settings = settings
        self.items = {}
        self.transducer = settings['Transducerins'] #UCF_LIB.lib[settings['Transducer']]

        self.InitUI()
        self.SetSize((500, 800))  # need to find a way to auto layout
        self.SetTitle("Transducer @ "+settings['PhysicalChannelName'])    
        #self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
         
    
    def InitUI(self):
        # setup the panel
        panelbox = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)#,style=wx.EXPAND|wx.ALL)
        panelbox.Add(self.panel,1,wx.EXPAND|wx.ALL)
        self.SetSizer(panelbox)

        
        # setup grid 
        box = wx.BoxSizer(wx.VERTICAL)
        
        self.add_image(box)
        
        self.add_info(box)
        
        self.add_property(box)
        
        self.add_buttongroup(box)
        
        self.panel.SetSizer(box)
        
    def add_buttongroup(self,box):
        hbox = wx.FlexGridSizer(rows=1,cols=2,vgap=15,hgap=15)
        self.btn_apply = wx.Button(self.panel,label='Apply')
        self.btn_default = wx.Button(self.panel,label='Default')
        
        hbox.Add(self.btn_default, 0, wx.ALL, border=5)
        hbox.Add(self.btn_apply, 0, wx.ALL, border=5)
        box.Add(hbox, 0, wx.ALIGN_RIGHT, border=5)
        
        self.btn_apply.Bind(wx.EVT_LEFT_DOWN,self.OnApply)
        self.btn_default.Bind(wx.EVT_LEFT_DOWN,self.OnDefault)
    
    
    def OnDefault(self,event):
        self.transducer = UCF_LIB.duplicate(self.settings['PhysicalChannelName'],self.settings['Transducer'])
        self.SetValue()
        
    def OnApply(self,event):
        
        self.GetValue()
    
    
    def add_info(self,box):
        hbox = wx.FlexGridSizer(rows=50,cols=4,vgap=15,hgap=15)
        
        for key,item in self.transducer.items():
            if not hasattr(item, '__call__'):
                if key !='description' and key != 'item' and key != 'image1':
                    t1 = SelLabel(self.panel,key)
                    s1 = SelTextCtrl(self.panel,skey=str(item),style=wx.TE_READONLY)
                    s1.SetValue(str(item))
                    hbox.Add(t1,wx.ALL|wx.EXPAND,5)
                    hbox.Add(s1,wx.ALL|wx.EXPAND,5)        
            
        
        sb = wx.StaticBox(self.panel, -1, self.settings['Transducer'])  
        sbox = wx.StaticBoxSizer(sb,wx.VERTICAL)
        
        
        s1 = SelTextCtrl(self.panel,skey=str(item),style=wx.TE_MULTILINE|wx.TE_READONLY,size=(200,60))
        s1.SetValue(str(self.transducer['description']))
        sbox.Add(s1,0, wx.ALL|wx.EXPAND, border=5)
        
        sbox.Add(hbox, 0, wx.ALL|wx.EXPAND, border=5)
        
        box.Add(sbox, 0, wx.ALL|wx.EXPAND, border=5)        
        
        
    def add_property(self,box):
        hbox = wx.FlexGridSizer(rows=50,cols=4,vgap=15,hgap=15)
        
         
        for key,item in self.transducer['item'].__dict__.items():
            if not hasattr(item, '__call__'):
                #print key,item
                self.items[key] = SelLabel(self.panel,key)
                self.items[key+'_input'] = SelTextCtrl(self.panel,skey=str(item))
                self.items[key+'_input'].SetValue(str(item))
                hbox.Add(self.items[key],wx.ALL|wx.EXPAND,5)
                hbox.Add(self.items[key+'_input'],wx.ALL|wx.EXPAND,5)        

        sb = wx.StaticBox(self.panel, -1, 'Instance Properties')  
        sbox = wx.StaticBoxSizer(sb,wx.VERTICAL)
        sbox.Add(hbox, 0, wx.ALL|wx.EXPAND, border=5)
        box.Add(sbox, 0, wx.ALL|wx.EXPAND, border=5)
        
    def add_image(self,box):
        # add images
        if len(self.transducer['image1']) == 0:
            imageFile = 'img/noavail.jpg'
        else:
            imageFile = self.transducer['image1']
            
        width = 200
        height = 200
        bitmap = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
    
        p1 = wx.StaticBitmap(self, -1, result, (10 + result.GetWidth(), 5), (result.GetWidth(), result.GetHeight()))

        sb = wx.StaticBox(self.panel, -1, 'Pictures')
        
        hbox = wx.StaticBoxSizer(sb,wx.VERTICAL)
        hbox.Add(p1, 0, wx.LEFT, border=5)
        
        box.Add(hbox, 0, wx.ALL|wx.EXPAND, border=5)  
        
    def SetValue(self):
        for key,item in self.transducer['item'].__dict__.items():
            if not hasattr(item, '__call__'):
                self.items[key+'_input'].SetValue(str(item))
        
    
    def GetValue(self):
        for key,item in self.transducer['item'].__dict__.items():
            if not hasattr(item, '__call__'):
                res = self.transducer['item'].SetValue(key,self.items[key+'_input'].GetValue())
                if res != 1:
                    errormessage = 'Type Error, can not convert "' + str(res[1][0]) + '" to "' + str(res[1][1]) +'" \n'
                    errormessage += 'Error at input for parameter "' + key +'"\n'
                    a1 = wx.MessageDialog(self.panel, errormessage, caption='Error', style=wx.OK|wx.ICON_QUESTION)
                    a1.ShowModal()  
 
if __name__ == '__main__':
  
    app = wx.App()
    ScxiFrame(None)
    app.MainLoop()
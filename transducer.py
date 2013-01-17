from xml.dom.minidom import Document, getDOMImplementation
import copy





class AIgroup(object):
    ''' This is the AIgroup for analog input'''
    
    def __init__(self,**kargs):
        self.max = 0.0
        self.min = 0.0
        self.lowpass = False
        self.lowpassfreq = 60
        self.factor_a = 1.0  # y=a*x+b
        self.factor_b = 0.0
        
        self.update_self(**kargs)
    
    
    def update_self(self,**kargs):
        for key,value in kargs.items():
            if key in self.__dict__.keys():
                self.__dict__[key] = value
    
    def SetValue(self,key,value):
        if key in self.__dict__.keys():
            if not hasattr(self.__dict__[key], '__call__'):
                if type(self.__dict__[key]) == type(value):
                    self.__dict__[key] = value
                    return 1
                else:
                    sourcetype = type(self.__dict__[key])
                    try:
                        results = sourcetype(value)
                        self.__dict__[key] = results
                        return 1
                    except:
                        return TypeError,(sourcetype,type(value))
    
    
    def GetPropDict(self,clustername):
        
        return LabViewXml(self,clustername)
        
class VolatgeInput(AIgroup):
    ''' Voltage input '''
    def __init__(self,**kargs):
        super(VolatgeInput, self).__init__(**kargs)
        self.update_self(**kargs)
        
class VoltageInputIntExc(VolatgeInput):
    ''' Voltage with internal excitation'''
    def __init__(self,**kargs):
        super(VoltageInputIntExc, self).__init__(**kargs)
        self.excitation = 0.0
        self.update_self(**kargs)
        self.xmllist = ['max','min','factor_a','factor_b','lowpass','lowpassfreq','excitation']

class VoltageInputExtExc(VolatgeInput):
    ''' Voltage with external excitation'''
    def __init__(self,**kargs):
        super(VoltageInputExtExc, self).__init__(**kargs)
        self.excitation = 0.0
        self.update_self(**kargs)
        self.xmllist = ['max','min','factor_a','factor_b','lowpass','lowpassfreq','excitation']

class StrainInput(AIgroup):
    def __init__(self,**kargs):
        super(StrainInput, self).__init__(**kargs)
        self.resistance = 0.0
        self.BridgeType = 'Quarter'
        self.GageFactor = 2.0
        self.excitation = 3.125
        
        self.update_self(**kargs)
        self.xmllist = ['max','min','factor_a','factor_b','lowpass','lowpassfreq','excitation','resistance','GageFactor','BridgeType']
        
        
class transcuderlib(object):
    def __init__(self):
        self.lib = {}
        
    def add(self,name,**kargs):
        ttype = kargs['type']
        
        if ttype == 'StrainInput':
            item = StrainInput(**kargs['prop'])
            
        elif ttype == 'VoltageInputIntExc':
            item = VoltageInputIntExc(**kargs['prop'])
            
        elif ttype == 'VoltageInputExtExc':
            item = VoltageInputExtExc(**kargs['prop'])
            
        self.lib[name] = {}
        self.lib[name]['item'] = item
        self.lib[name]['author'] = kargs['author']
        self.lib[name]['description'] = kargs['description']
        self.lib[name]['unit'] = kargs['unit']
        self.lib[name]['max'] = kargs['max']
        self.lib[name]['min'] = kargs['min']
        if 'image1' in kargs.keys():
            self.lib[name]['image1'] = kargs['image1']
        else:
            self.lib[name]['image1'] = ''
    
    def duplicate(self,tkey,skey):
        ''' duplicate the transducer instance with new key'''
        trans = self.lib[skey]
        self.lib[tkey] = trans.copy()
        newitem = trans['item'].__class__(**trans['item'].__dict__)
        
        #newitem.__dict__ = trans['item'].__dict__.copy()
        
        self.lib[tkey]['item'] = newitem
        
        return self.lib[tkey]
    
    
if __name__ == '__main__':
    c1 = VoltageInputIntExc()
    c2 = VoltageInputExtExc()
    c3 = StrainInput()
    print 1

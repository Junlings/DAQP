from transducer import transcuderlib


UCF_LIB = transcuderlib()

UTM_LOAD_0_200 = {
    'type':'VoltageInputExtExc',
    'unit':'kip',
    'max':200,
    'min':0,
    'author':'Jun Xia',
    'description':' UTM machine load signal',
    'image1':'img/UTM.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}


UTM_LOAD_0_100 = {
    'type':'VoltageInputExtExc',
    'unit':'kip',
    'max':100,
    'min':0,
    'author':'Jun Xia',
    'description':' UTM machine load signal',
    'image1':'img/UTM.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}

UTM_LOAD_0_20 = {
    'type':'VoltageInputExtExc',
    'unit':'kip',
    'max':20,
    'min':0,
    'author':'Jun Xia',
    'description':' UTM machine load signal',
    'image1':'img/UTM.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}

UTM_LOAD_0_10 = {
    'type':'VoltageInputExtExc',
    'unit':'kip',
    'max':10,
    'min':0,
    'author':'Jun Xia',
    'description':' UTM machine load signal',
    'image1':'img/UTM.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}


UTM_DISP_0_5 = {
    'type':'VoltageInputExtExc',
    'unit':'in.',
    'max':5,
    'min':0,
    'author':'Jun Xia',
    'description':' UTM machine disp signal',
    'image1':'img/UTM.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}



MTS_LOAD_0_100 = {
    'type':'VoltageInputExtExc',
    'unit':'kip',
    'max':100,
    'min':0,
    'author':'Jun Xia',
    'description':' MTS machine load signal',
    'image1':'img/MTS.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}

MTS_DISP_0_10 = {
    'type':'VoltageInputExtExc',
    'unit':'in.',
    'max':10,
    'min':0,
    'author':'Jun Xia',
    'description':' MTS machine disp signal',
    'image1':'img/MTS.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':0.4,
        }
}


STRAIN_120_quarter2 = {
    'type':'StrainInput',
    'unit':'microstrain',
    'max':3000,
    'min':-3000,
    'author':'Jun Xia',
    'description':' strain gauge signal',
    'image1':'img/strain.jpg',
    'prop':
        {
            'BridgeType':'Quarter Bridge II',
            'gageFactor': 2.0,
            'excitation': 3.125,
            'lowpass':True,
            'lowpassfreq':60,
            'max':0.01,
            'min':-0.01,
            'factor_a':1000000,
            'factor_b':0.0,
            'resistance':120,
            
        }
}

STRAIN_350_half = {
    'type':'StrainInput',
    'unit':'microstrain',
    'max':3000,
    'min':-3000,
    'author':'Jun Xia',
    'description':' strain gauge signal',
    'image1':'img/strain.jpg',
    'prop':
        {
            'BridgeType':'Half Bridge I',
            'gageFactor': 2.0,
            'excitation': 3.125,
            'lowpass':True,
            'lowpassfreq':60,
            'max':0.01,
            'min':-0.01,
            'factor_a':1000000,
            'factor_b':0.0,
            'resistance':350,
            
        }
}


EXTENSOMETER_5 = {
    'type':'VoltageInputIntExc',
    'unit':'in.',
    'max':5,
    'min':0,
    'author':'Jun Xia',
    'description':'extensometer',
    'image1':'img/ext.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':10,
        }
}

LVDT_5 = {
    'type':'VoltageInputIntExc',
    'unit':'in.',
    'max':5,
    'min':0,
    'author':'Jun Xia',
    'description':'extensometer',
    'image1':'img/lvdt.jpg',
    'prop':
        {
            'max':10,
            'min':-10,
            'factor_a':22.4,
            'factor_b':0.0,
            'lowpass':True,
            'lowpassfreq':60,
            'excitation':10,
        }
}


UCF_LIB.add('UTM_LOAD_0_200_kip',**UTM_LOAD_0_200)
UCF_LIB.add('UTM_LOAD_0_100_kip',**UTM_LOAD_0_100)
UCF_LIB.add('UTM_LOAD_0_20_kip',**UTM_LOAD_0_20)
UCF_LIB.add('UTM_LOAD_0_10_kip',**UTM_LOAD_0_10)
UCF_LIB.add('UTM_DISP_0_5_in',**UTM_DISP_0_5)
UCF_LIB.add('MTS_LOAD_0_100_kip',**MTS_LOAD_0_100)
UCF_LIB.add('MTS_DISP_0_10_in',**MTS_DISP_0_10)
UCF_LIB.add('STRAIN_120_quarter2',**STRAIN_120_quarter2)
UCF_LIB.add('STRAIN_350_half',**STRAIN_350_half)
UCF_LIB.add('LVDT_5',**LVDT_5)

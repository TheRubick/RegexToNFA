#0 for concat, 1 for oring, 2 for repeat
#((0|1)*+(01))
#((C)*+(01))
#(D+(01))
#(D+E)
#Z
table = {'Z':{"operation":1,'oprd1':'D', 'oprd2':'E' },
        'D':{'operation':2,'oprd1':'C', 'oprd2':-1 },
        'C':{'operation':1,'oprd1':'0', 'oprd2':'1' },
        'E':{'operation':0,'oprd1':'0', 'oprd2':'1' }}
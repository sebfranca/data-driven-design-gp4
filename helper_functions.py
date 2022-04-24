import sys

def LOG(msg):
    print >> sys.__stdout__, str(msg)
    
def parser_res(file='abaqus'):
    '''
    Function, that takes a name of result file (abaqus.rpt for default)
    and will give a tuple, which is:
    1) a dict with all maximum value per ply ----- for ALL iterations
    2) maximum value per ply                 ----- for LAST iteration
    output = ({1: max, 2: max, ... }, max)
    '''
    from odbAccess import openOdb
    
    res_file = file + '.odb'
    LOG('Starting processing file %s...'%(str(res_file)))
    try:
        odb = openOdb(res_file)
    except:
        LOG('Failed to open file %s...'%(str(res_file)))
        
    maxMises = -0.1
    maxElem = 0
    maxStep = "_None_"
    maxFrame = -1
    elemset = None
    Stress = 'S'
    isStressPresent = 0
    cur_step = 0
    for step in odb.steps.values():
        LOG('Processing Step: %s'%(str(step.name)))
        for frame in step.frames:
            cur_step += 1
            allFields = frame.fieldOutputs
            if (allFields.has_key(Stress)):
                isStressPresent = 1
                stressSet = allFields[Stress]
                if elemset:
                    stressSet = stressSet.getSubset(
                        region=elemset)      
                for stressValue in stressSet.values:                
                    if (stressValue.mises > maxMises):
                        maxMises = stressValue.mises
                        maxElem = stressValue.elementLabel
                        maxStep = step.name
                        maxFrame = frame.incrementNumber
    
    LOG('Finished processing results, display results : ')
    LOG('Max Von Mises stress : %.6f \nFound in element : %s \nAfter %i steps'%(maxMises, maxElem, cur_step))

#    return results, results[max(results.keys())]


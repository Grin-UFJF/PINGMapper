from main_readFiles import read_master_func
from funcs_common import *
import sys
sys.path.insert(0, 'src')

start_time = time.time()

#######################
# Start User Parameters
#######################

# Load default parameters from json file
paramsFile = os.path.join('pingmapper', 'default_params.json')
with open(paramsFile, 'r') as f:
    params = json.load(f)

# Change any default parameters here:
params.pop('inDir', None)  # Remove inDir if exists
params.pop('filter_table', None)  # Remove inDir if exists
params['project_mode'] = 1  # 0==NEW PROJECT; 1==OVERWRITE MODE
params['egn'] = False
params['egn_stretch'] = "Percent Clip"  # "Percent Clip", "Min-Max" or "None"
params['egn_stretch_factor'] = 0.5
params['wcp'] = True
params['wcm'] = False
params['wcr'] = False
params['rect_wcp'] = False
params['rect_wcr'] = False
params['sonogram_colorMap'] = 'copper'
params['son_colorMap'] = 'copper'
params['pred_sub'] = False

# EGN Stretch
egn_stretch = params['egn_stretch']
if egn_stretch == 'None':
    params['egn_stretch'] = 0
elif egn_stretch == 'Min-Max':
    params['egn_stretch'] = 1
elif egn_stretch == 'Percent Clip':
    params['egn_stretch'] = 2

# Depth detection
detectDep = params['detectDep']
if detectDep == 'Sensor':
    params['detectDep'] = 0
elif detectDep == 'Auto':
    params['detectDep'] = 1

# Shadow removal
remShadow = params['remShadow']
if remShadow == 'False':
    params['remShadow'] = 0
elif remShadow == 'Remove all shadows':
    params['remShadow'] = 1
elif remShadow == 'Remove only bank shadows':
    params['remShadow'] = 2

# Sonar mosaic
mosaic = params['mosaic']
if mosaic == 'False':
    params['mosaic'] = int(0)
elif mosaic == 'GTiff':
    params['mosaic'] = int(1)
elif mosaic == 'VRT':
    params['mosaic'] = int(2)

# Substrate mosaic
map_mosaic = params['map_mosaic']
if map_mosaic == 'False':
    params['map_mosaic'] = 0
elif map_mosaic == 'GTiff':
    params['map_mosaic'] = 1
elif map_mosaic == 'VRT':
    params['map_mosaic'] = 2

# Path to data/output
inFile = "/home/vini/PINGMapper/Sonar/Rec00005.DAT"
sonPath = inFile.split('.DAT')[0]
sonFiles = [os.path.join(sonPath, f) for f in sorted(
    os.listdir(sonPath)) if f.endswith('.SON')]
projDir = "/home/vini/PINGMapper/Sonar/outputs/test"
logfilename = 'log_'+time.strftime("%Y-%m-%d_%H%M")+'.txt'
logfilename = os.path.join(projDir, logfilename)
copied_script_name = os.path.basename(__file__).split(
    '.')[0]+'_'+time.strftime("%Y-%m-%d_%H%M")+'.py'
script = os.path.abspath(__file__)

# Add ofther params
params['sonFiles'] = sonFiles
params['logfilename'] = logfilename
params['script'] = [script, copied_script_name]
params['projDir'] = projDir
params['inFile'] = inFile

sys.stdout = Logger(logfilename)

print('\n\n', '***User Parameters***')
for k, v in params.items():
    print("| {:<20s} : {:<10s} |".format(k, str(v)))

try:
    # ==================================================
    print('\n===========================================')
    print('===========================================')
    print('***** READING *****')
    print("working on "+projDir)
    read_master_func(**params)

    gc.collect()
    print("\n\nTotal Processing Time: ", datetime.timedelta(
        seconds=round(time.time() - start_time, ndigits=0)))

    sys.stdout.log.close()

except Exception as Argument:
    unableToProcessError(logfilename)

import os
import sys
import xbmcaddon

sys.path.append (xbmc.translatePath( os.path.join( xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'lib' )))
from yogaglo import YogaGlo

yg = YogaGlo(sys.argv[0], int(sys.argv[1]), sys.argv[2])
yg.processParameters()

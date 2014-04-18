import os
# os.system("export VERSIONER_PYTHON_PREFER_32_BIT=yes")
from cocos.director import director
from trafficmap import TrafficMap
from cocos.scene import Scene


__author__ = 'danielqiu'

import cocos



def main():

    director.init(800, 800, do_not_scale=False)
    cocos.director.director.run(Scene(TrafficMap()))

if __name__ == "__main__":
    main()
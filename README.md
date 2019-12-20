# Synthetic Austin

This repository contains the rule files used to generate various versions of synthetic Austin. It also contains multiple different scenes of Austin with various street layouts, all based on the same rule files. It also has the scripts necessary for taking satellite images of the synthetic city.

### assets
This directory contains textures used to populate building roofs and facades.

### data
This directory contains the *camera.fbx* file used for scripting the image capturing with python.

### maps
This directory contains the OSM map data files. Not being used in any current versions of the city.

### rules
This directory contains the various rule files used to generate the cities. The current ones being used are

    austin_facades.cga
    austin_roofs.cga
    austin_rule.cga
    black.cga

### scenes
This directory contains the scenes used for the current versions of the city. To allow for rendering on personal machines, multiple smaller scenes were generated and had the same rule files applied then had photos taken. The scenes used are

- austin2.cej
- austin3.cej
- austin7.cej
- austin8.cej


The coordinates to use for shooting each scene are displayed in the table below. These parameters should be changed when the

    loop_capturer_dynamic_attributes()

function is called.

| Scene   |   start_axis  |    end_axis |
|---------|:-------------:|------------:|
| austin2 |   (-1600,0)   | (800, 1800) |
| austin3 | (-1600,-1700) |  (800,1500) |
| austin7 | (-1100,-1400) | (1300,1200) |
| austin8 | (-1800-1200)  | (1300,1200) |

### scripts
This includes the script necessary for taking images of the synthetic city, both in color and for the labels. It is called

    dynamic_shoot_syn_1_colorful_city.py

Before being used, the path the images are saved should be changed (lines 148, 155, 161). The relevant loop_capturer_dynamic_attributes() function should be called after updating the

    tag
    start_axis
    end_axis
    mode
    and other light/camera settings as necessary.

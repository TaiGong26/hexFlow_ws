from hex_flow_ros_template.template_archer_y6 import HexFlowTemplateArcherY6
from hex_flow_ros_template.template_e3_desktop import HexFlowTemplateE3Desktop


def main_archer_y6():
    template = HexFlowTemplateArcherY6()
    template.start()
    template.run()
    template.stop()


def main_e3_desktop():
    template = HexFlowTemplateE3Desktop()
    template.start()
    template.run()
    template.stop()

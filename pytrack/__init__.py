from meanshift import MeanShift
from opticalflow import OpticalFlow
from bidirectionaloptflow import BidirectionalOptFlow
from backgroundsubtract import BackgroundSubtract
from templatematching import TemplateMatch, BidirectionalTemplateMatch

#online = {"Mean Shift": MeanShift}
online = {
    "Optical Flow": OpticalFlow,
    "Background Subtraction":BackgroundSubtract,
    "Template": TemplateMatch,
}

bidirectional = {"Optical Flow": BidirectionalOptFlow, "Template": BidirectionalTemplateMatch}
multiobject = {}

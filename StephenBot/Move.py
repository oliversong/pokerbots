from Enums import *

class Move:
    def __init__(self, type, amt=None, myEV=None, leftEV=None, rightEV=None,
                 comment=None):
        self.type = type
        self.amount = amt
        self.myEV = myEV
        self.leftEV = leftEV
        self.rightEV = rightEV
        self.comment = comment

    def __repr__(self):
        ret = " "
        if self.myEV is not None:
            ret += "myEV=" + str(self.myEV)
        if self.leftEV is not None:
            ret += " leftEV:[%.1f %.1f]" % (self.leftEV[0],self.leftEV[1])
        if self.rightEV is not None:
            ret += " rightEV:[%.1f %.1f]" % (self.rightEV[0],self.rightEV[1])
        if self.comment is not None:
            ret += ", " + self.comment
        return ret

    def toString(self):
        ret = ACTION_TYPES[self.type]
        if self.amount is not None:
            ret += ":%d" % (int(round(self.amount)))
        return ret + "\n"

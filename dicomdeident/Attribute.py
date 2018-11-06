#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######


class Attribute(object):
    """DICOM Dataset attribute
    """

    def __init__(self, name, group, element, action=None, vr="", vm=""):
        """Default Constructor
        """
        self._name = name
        self._description = ""
        self._group = group
        self._element = element
        self._action = action

        # DICOM value representation (type)
        self._vr = vr
        # DICOM value multiplicity
        self._vm = vm

########  ########   #######  ########  ######## ########  ######## #### ########  ######
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##    ##
##     ## ##     ## ##     ## ##     ## ##       ##     ##    ##     ##  ##       ##
########  ########  ##     ## ########  ######   ########     ##     ##  ######    ######
##        ##   ##   ##     ## ##        ##       ##   ##      ##     ##  ##             ##
##        ##    ##  ##     ## ##        ##       ##    ##     ##     ##  ##       ##    ##
##        ##     ##  #######  ##        ######## ##     ##    ##    #### ########  ######

    @property
    def Name(self):
        """Name Getter
        """
        return self._name

    @property
    def Description(self):
        """Description Getter
        """
        return self._description

    @property
    def Group(self):
        """Group Getter
        """
        return self._group

    @property
    def Element(self):
        """Element Getter
        """
        return self._element

    @property
    def Action(self):
        """Action Getter
        """
        return self._action

    @Action.setter
    def Action(self, action):
        """Action Setter
        """
        # One-to-one association (bidirectional)
        self._action = action
        self._action.Attribute = self

##     ## ######## ######## ##     ##  #######  ########   ######
###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
#### #### ##          ##    ##     ## ##     ## ##     ## ##
## ### ## ######      ##    ######### ##     ## ##     ##  ######
##     ## ##          ##    ##     ## ##     ## ##     ##       ##
##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
##     ## ########    ##    ##     ##  #######  ########   ######

    def __str__(self):
        """String of tag value as (gggg, eeee)
        """
        return "(%s, %s)" % (self._group, self._element)

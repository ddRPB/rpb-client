#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Singleton
from utils.SingletonType import SingletonType

# Python 2 and 3
from six import with_metaclass


class ConfigDetails(with_metaclass(SingletonType)):
    """Application configuration details
    """

    def __init__(self):
        """Default Constructor
        """
        # Configuration file
        self.configFileName = "radplanbio-client.cfg"

        # Static burned in values
        self.name = "RadPlanBio - Desktop Client"
        self.identifier = "RPB-DESKTOP-CLIENT"
        self.version = "1.0.0.24"
        self.copyright = "2013-2018 German Cancer Consortium (DKTK)"
        self.logFilePath = ""
        self.keyFilePath = ""

        # Temp settings
        self.isUpgrading = None
        self.upgradeFinished = None

        # GUI settings - default
        self.width = 800
        self.height = 600

        # Data sanity testing/checks
        self.patientGenderMatch = True
        self.patientDobMatch = True

        # DICOM - defaults
        self.replacePatientNameWith = "pid"  # [pid, const]
        self.constPatientName = "XXX"
        self.replaceDateWith = "19000101"
        self.allowMultiplePatientIDs = False
        
        self.applicationConfidentialityProfile = True
        self.retainPatientCharacteristicsOption = True
        self.retainLongFullDatesOption = True
        self.retainDeviceIdentityOption = True
        self.cleanStructuredContentOption = True
        self.cleanDescriptorsOption = True

        self.retainStudyDate = True
        self.retainStudyTime = True
        self.retainSeriesTime = True
        self.retainSeriesDate = True

        self.retainStudySeriesDescriptions = False
        
        # DICOM RTStruct mapping
        self.autoRTStructMatch = True
        self.autoRTStructRef = False

        # DICOM download
        self.downloadDicomStudyFolderName = "oid"  # [oid, label]
        self.downloadDicomPatientFolderName = "ssid"  # [pid, ssid]

        # DICOM AE
        self.rpbAE = "RPBC"
        self.rpbAETsuffix = "no"  # [no, host, fqdn] host = hostname, fqdn = FullyQualifiedDomainName
        self.rpbAEport = 5681

        # Dicom remote AEs
        self.remoteAEs = []

        # Values read from config file
        self.rpbHost = ""
        self.rpbHostPort = ""
        self.rpbApplication = ""

        # Proxy
        self.proxyEnabled = ""
        self.proxyConfiguration = "manual" # [manual, auto] manual = user specified, auto = WPAD/PAC
        self.proxyHost = ""
        self.proxyPort = ""
        self.noProxy = ""

        # Proxy auth
        self.proxyAuthEnabled = ""
        self.proxyAuthLogin = ""
        self.proxyAuthPassword = ""

        # General
        self.startupUpdateCheck = True

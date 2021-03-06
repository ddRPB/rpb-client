#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######

# Logging
import logging
import logging.config

# PyQt - threading
from PyQt4 import QtCore

# String
from string import whitespace

# Services
from services.OCDataWsService import OCDataWsService
from services.OCEventWsService import OCEventWsService
from services.OCStudyEventDefinitionWsService import OCStudyEventDefinitionWsService
from services.OCStudySubjectWsService import OCStudySubjectWsService
from services.OCStudyWsService import OCStudyWsService

 ######   #######  ##    ##  ######  ########  ######  
##    ## ##     ## ###   ## ##    ##    ##    ##    ## 
##       ##     ## ####  ## ##          ##    ##       
##       ##     ## ## ## ##  ######     ##     ######  
##       ##     ## ##  ####       ##    ##          ## 
##    ## ##     ## ##   ### ##    ##    ##    ##    ## 
 ######   #######  ##    ##  ######     ##     ######

# WSDL locations for web services
STUDYURL = "ws/study/v1/studyWsdl.wsdl"
DATAURL = "ws/data/v1/dataWsdl.wsdl"
EVENTURL = "ws/event/v1/eventWsdl.wsdl"
STUDYSUBJECTURL = "ws/studySubject/v1/studySubjectWsdl.wsdl"
STUDYEVENTDEFURL = "ws/studyEventDefinition/v1/studyEventDefinitionWsdl.wsdl"

# OC result value after calling ws
STATUSSUCCCESS = "Success"
STATUSFAIL = "Fail"

 ######  ######## ########  ##     ## ####  ######  ########
##    ## ##       ##     ## ##     ##  ##  ##    ## ##
##       ##       ##     ## ##     ##  ##  ##       ##
 ######  ######   ########  ##     ##  ##  ##       ######
      ## ##       ##   ##    ##   ##   ##  ##       ##
##    ## ##       ##    ##    ## ##    ##  ##    ## ##
 ######  ######## ##     ##    ###    ####  ######  ########


class OCWebServices:
    """SOAP web services to OpenClinica

    Unify and simplify the access to OC web services methods
    """

    def __init__(self, ocConnectInfo, proxyHost="", proxyPort="", noProxy="", proxyUsr="", proxyPass="", trace=logging.INFO):
        """Constructor

        Param ocConnectInfo holds the basic OpenClinica connection information
        """
        self._logger = logging.getLogger(__name__)
        logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

        self.ocConnectInfo = ocConnectInfo

        proxyStr = None
        if noProxy != "" and noProxy is not whitespace and noProxy in self.ocConnectInfo.baseUrl:
            proxyStr = None
        else:
            if proxyHost != "" and proxyHost is not whitespace and proxyPort != "" and proxyPort is not whitespace:
                proxyStr = "%s:%s" % (proxyHost, proxyPort)

        if proxyStr:
            self._logger.info("OC SOAP web services are going to use: %s" % proxyStr)
        else:
            self._logger.info("OC SOAP web services are going to be used with environmental proxy (including no proxy).")

        self._logger.info("OC SOAP web services are going to be used with authentication: %s" % str(proxyUsr))

        # Define OC WS bindings
        self.studyBinding = OCStudyWsService(self.ocConnectInfo.baseUrl + STUDYURL, proxyStr, proxyUsr, proxyPass, trace)
        self.dataBinding = OCDataWsService(self.ocConnectInfo.baseUrl + DATAURL, proxyStr, proxyUsr, proxyPass, trace)
        self.studySubjectBinding = OCStudySubjectWsService(self.ocConnectInfo.baseUrl + STUDYSUBJECTURL, proxyStr, proxyUsr, proxyPass, trace)
        self.studyEventDefinitionBinding = OCStudyEventDefinitionWsService(self.ocConnectInfo.baseUrl + STUDYEVENTDEFURL, proxyStr, proxyUsr, proxyPass, trace)
        self.eventBinding = OCEventWsService(self.ocConnectInfo.baseUrl + DATAURL, proxyStr, proxyUsr, proxyPass, trace)

        # Define WSSE security
        self.studyBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.dataBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.studySubjectBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.studyEventDefinitionBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)
        self.eventBinding.wsse(self.ocConnectInfo.userName, self.ocConnectInfo.passwordHash)

 ######  ######## ##     ## ########  ##    ## 
##    ##    ##    ##     ## ##     ##  ##  ##  
##          ##    ##     ## ##     ##   ####   
 ######     ##    ##     ## ##     ##    ##    
      ##    ##    ##     ## ##     ##    ##    
##    ##    ##    ##     ## ##     ##    ##    
 ######     ##     #######  ########     ##   

    def getStudyMetadata(self, study, thread=None):
        """Get ODM metadata for study

        Param study specifies the study
        Returns XML ODM metadata of the study
        """
        successful = False
        result = ""
        data = None

        result, data =  self.studyBinding.getMetadata(study)

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), str(data))
            return None
        else:
            return successful, data


    def listAllStudies(self, data=None, thread=None):
        """Query studies available for the user

        Returns collection of study domain objects
        """
        self._logger.debug("listAllStudies")

        successful = False
        result = ""
        data = None

        result, data = self.studyBinding.listAll()

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), data)
            return None
        else:    
            return successful, data

 ######  ##     ## ########        ## ########  ######  ######## 
##    ## ##     ## ##     ##       ## ##       ##    ##    ##    
##       ##     ## ##     ##       ## ##       ##          ##    
 ######  ##     ## ########        ## ######   ##          ##    
      ## ##     ## ##     ## ##    ## ##       ##          ##    
##    ## ##     ## ##     ## ##    ## ##       ##    ##    ##    
 ######   #######  ########   ######  ########  ######     ## 

    def listAllStudySubjectsByStudy(self, data=None, thread=None):
        """Query all study subjects by study

        Returns collection of studySubject domain objects
        """
        if data:
            study = data[0]
            metadata = data[1]

        result = self.studySubjectBinding.listAllByStudy(study, metadata)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), result)
            return None
        else:
            return result


    def listAllStudySubjectsByStudySite(self, data=None, thread=None):
        """Query all study subjects by study site

        Returns collection of studySubject domain objects
        """
        if data:
            study = data[0]
            site = data[1]
            metadata = data[2]

        result = self.studySubjectBinding.listAllByStudySite(study, site, metadata)

        if thread:
            thread.emit(QtCore.SIGNAL("finished(QVariant)"), result)
            return None
        else:
            return result


    def createStudySubject(self, studySubject, study, studySite):
        """Create new StudySubject entity in OC
        """
        return self.studySubjectBinding.create(studySubject, study, studySite)


    def isStudySubject(self, studySubject, study, studySite):
        """Checks if the specified subject belongs to OC studySubjects
        """
        return self.studySubjectBinding.isStudySubject(studySubject)

######## ##     ## ######## ##    ## ######## 
##       ##     ## ##       ###   ##    ##    
##       ##     ## ##       ####  ##    ##    
######   ##     ## ######   ## ## ##    ##    
##        ##   ##  ##       ##  ####    ##    
##         ## ##   ##       ##   ###    ##    
########    ###    ######## ##    ##    ##

    def scheduleStudyEvent(self, study, site, studySubject, event):
        """Schedule study event for studySubject
        """
        successful = False

        result = ""
        result = self.eventBinding.schedule(study, site, studySubject, event)

        if result == STATUSSUCCCESS:
            successful = True
        elif result == STATUSFAIL:
            successful = False

        return successful


    def listAllStudyEventDefinitionsByStudy(self, study):
        """Query all study events by study

        Returns collection of studyEventDefinition domain objects
        """
        return self.studyEventDefinitionBinding.listAllByStudy(study)

########     ###    ########    ###    
##     ##   ## ##      ##      ## ##   
##     ##  ##   ##     ##     ##   ##  
##     ## ##     ##    ##    ##     ## 
##     ## #########    ##    ######### 
##     ## ##     ##    ##    ##     ## 
########  ##     ##    ##    ##     ## 

    def importODM(self, odm):
        """Import ODM structured data into OC

        Param odm is XML formatted data according to ODM and study metadata
        Returns result of the import
        """
        result = ""

        result = self.dataBinding.importData(odm)
        # try:
        #     result = self.dataBinding.importData(odm)
        #     self._logger.info(result)
        # except Exception, err:
        #     self._logger.error(err)

        return True if STATUSSUCCCESS in result else False

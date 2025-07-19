

import ctypes
from PyQt5.QtWidgets import QApplication
from fmpy.gui.MainWindow import MainWindow #has some troubles !! no gui
from fmpy import *
from fmpy.fmi2 import FMU2Slave
import shutil

class myFMU():
    def __init__(self,fmupath:str):
        """

        :param fmupath: path to FMU
        """
        # todo: separate fields according role (config, simul, etc
        self.__fmuP=fmupath
        self.__fmuInstance=None
        self.__model_description =  read_model_description(fmupath,validate=False)
        self.__vrs= {}
        self.__parameter=[]
        self.__input=[]
        self.__output=[]
        self.dicotype=dict()
        self.__initVals=dict()
        for variable in self.__model_description.modelVariables:
            self.__vrs[variable.name] = variable.valueReference
            if variable.causality == 'parameter':
               self.__parameter.append(variable.name)
            if variable.causality == 'output':
               self.__output.append(variable.name)
            if variable.causality == 'input':  # and print the names of all parameters
               self.__input.append(variable.name)
            self.dicotype[variable.name]=variable.type
            if variable.causality in ('parameter', 'input', 'output'):
                self.__initVals[variable.name]=variable.start

        self.__unzipdir=None
    def getInitVal(self,name):
        return self.__initVals[name]
    def getInitialization(self):
        return self.__initVals
    def getType(self,varname):
        """
        :param varname:  a string corresponding to a input,output or parameter
        :return: type of input,output or parameter (as str)
        """
        return self.dicotype[varname]
    def get_model_description(self):
        return self.__model_description
    def getInputList(self):
        return self.__input
    def getOutputList(self):
        return self.__output
    def getParameterList(self):
        return self.__parameter
    def info(self):
        dump(self.__fmuP)
        print("more info")
        self.moreinfo()
    def moreinfo(self):
        for variable in self.__model_description.modelVariables:  # iterate over the variables
            # if variable.causality == 'parameter':                    # and print the names of all parameters
            print('%-25s %s %s' % (variable.causality, variable.name, variable.start))
    def cosimInfo(self):
        print(self.__model_description.modelName)
        for variable in self.__model_description.modelVariables:  # iterate over the variables
            if variable.causality in ('parameter','input','output'):                    # and print the names of all parameters
                print('%-25s %s %s %s' % (variable.causality, variable.name, variable.start, variable.description))

    def gui(self):
        """ call fmpy gui
            has trouble on some platform / library version"""
        import os
        import platform
        if os.name == 'nt' and int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        cline = []
        app = QApplication(cline)
        window = MainWindow()
        window.show()
        window.load(self.__fmuP)
        sys.exit(app.exec_())

    def init(self, start_time,varvalues):
        """ extract fmu, and do useful steps to make fmu simulable
        Parameters
        ----------
        start_time : initial time double.
        varvalues : a list of couple VarNAme (string) and its value
        """
        # extract the FMU

        self.__unzipdir= extract(self.__fmuP)

        # see https://github.com/CATIA-Systems/FMPy/blob/3841175f6c08710b723d3628379eb2e3a20a5acf/fmpy/fmi2.py#L489
        fmu = FMU2Slave(guid=self.__model_description.guid,
                        unzipDirectory=self.__unzipdir,
                        modelIdentifier=self.__model_description.coSimulation.modelIdentifier,
                        instanceName='instance1')
        self.__fmuInstance=fmu

        # initialize
        fmu.instantiate()
        fmu.setupExperiment(startTime=start_time)
        if varvalues:
            for v in varvalues:
                var, val = v
                self.set(var, val)

        fmu.enterInitializationMode()
        fmu.exitInitializationMode()

    def _setVal(self,var,val):
        type =self.dicotype[var]
        if type=='String':
            self._setValStr(var,val)
        elif type=='Real':
            self._setValR(var,val)
        elif type=='Integer':
            self._setValI(var,val)
        else: #no check
            self._setValB(var,val)
    def _setValR(self, var, val):
        """
        set value to variable
        syntax: see below
        Parameters
        ----------
        var : a string
        val : a real value
        Returns
        -------
        None."""

        self.__fmuInstance.setReal([self.__vrs[var]], [val])

    def _setValB(self, var, val):
        """
        set value to variable
        syntax: see below
        Parameters
        ----------
        var : a string
        val : a real value
        Returns
        -------
        None."""

        self.__fmuInstance.setBoolean([self.__vrs[var]], [val])

    def _setValStr(self, var, val):
        """
        set value to variable
        syntax: see below
        Parameters
        ----------
        var : a string
        val : a real value
        Returns
        -------
        None."""

        self.__fmuInstance.setString([self.__vrs[var]], [val])

    def _setValI(self, var, val):
        """
        set value to variable
        syntax: see below
        Parameters
        ----------
        var : a string
        val : a real value
        Returns
        -------
        None."""

        self.__fmuInstance.setInteger([self.__vrs[var]], [val])

    def set(self, var, val):
        """
        set value(s) to variable(s)
        syntax:
            # setVal(['a','b','c'],(1,2,3))
            both are lists
            # setVal('a',1)
            both are simple values
            setVal(['a','b','c'],{ 'a':1, 'aprime':2, etc.})
            a list and a dictionnary
            setVal('a',{ 'a':1, 'aprime':2, etc.})
             a variable  and a dictionnary
        Parameters
        ----------
        variables : list of var string or a string
        val : dictionnary of varname (string) , value or a list of value OR a single value
        Returns
        -------
        None.
        """
        if isinstance(var,list) and isinstance(val,list):
            # setVal(['a','b','c'],(1,2,3))
            for v,value in zip(var,val):
                self._setVal(v,value)
        elif isinstance(var,list) and isinstance(val,dict):
            #  setVal(['a','b','c'],{ 'a':1, 'aprime':2, etc.})
            for v in var:
                self._setVal(v,val[v])
        elif isinstance(var,str) and isinstance(val,dict):
            # setVal(['a', 'b', 'c'], {'a': 1, 'aprime': 2, etc.})
            self._setVal(var,val[var])
        else:
            # setVal('a',1)
            #no check
            self._setVal(var,val)

    def get(self, var, dico=None):
        '''
        get a value or a list of values
        :param var  (str) or list of str: variable(s) name(s)
        :param dico (dict): if any the dict in which put values
        :return:
        values requested
        '''
        val=None
        if isinstance(var,str):
            #get('a')
            type = self.dicotype[var]
            if type == 'String':
                val = self.__fmuInstance.getString([self.__vrs[var]])[0]

            elif type == 'Real':
                val =self.__fmuInstance.getReal([self.__vrs[var]])[0]
            elif type == 'Integer':
                val = self.__fmuInstance.getInteger([self.__vrs[var]])[0]

            else:  # no check
                val = self.__fmuInstance.getBoolean([self.__vrs[var]])[0]
            if dico:
                dico[var]=val
            return val
        else:
            res=[]
            for v in var:
                value = self.get(v)
                if dico:
                    dico[v] = value
                res.append(value)
            return res

    def terminate(self):
        """
        clean files, etc.
        :return:
        """
        self.__fmuInstance.terminate()
        self.__fmuInstance.freeInstance() #unload the shared library (apparently) -> no need to call freeLibrary

        shutil.rmtree(self.__unzipdir, ignore_errors=True)

    def doStep(self, time, step_size):
        '''
        basic to call dostep
        need to be improved
        :param time:
        :param step_size:
        :return:
        '''
        self.__fmuInstance.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)


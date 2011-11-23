#!/usr/bin/env python

"""gui.py is a basic GUI to the Lascar Data Logger library wrapper created by Dxnx Ltd."""

import wx
from dataLogger import dataLoggerEL3
from dataHandlerEL3 import tcDataHandlerEL3
import time
from threading import Timer 

class MainPanel(wx.Panel):
    
    dl = dataLoggerEL3(verbose=0)
    dataHandler = None
    
    
    def __init__(self, parent, dataHandler=None):
        wx.Panel.__init__(self, parent)
        self.dl.addLogHandler(self.log)
        self.dataHandler = dataHandler
        
        b1= 150
        b2=60
        
        self.cmbStopAndDownload = wx.Button(self, label='Stop and Download', size=(b1,b2))
        self.cmbStartAndClear = wx.Button(self, label='Start and Clear',size=(b1,b2))
        #self.cmbStopPoll = wx.Button(self, label='Connect', size=(b1,b2))
        
        self.connectionStatus = wx.StaticText(self, -1, "Connection Status:")
        self.connectionStatusA = wx.StaticText(self, -1, "Not Connected")
        self.loggerName = wx.StaticText(self, -1, "Logger Name:")
        self.loggerNameA = wx.StaticText(self, -1, "N/A")
        self.loggingStatus = wx.StaticText(self, -1, "Currently Logging:")
        self.loggingStatusA = wx.StaticText(self, -1, "N/A")
        self.sampleCount = wx.StaticText(self, -1, "Sample Count:")
        self.sampleCountA = wx.StaticText(self, -1, "N/A")
        self.timeStarted = wx.StaticText(self, -1, "Logger Start Time:")
        self.timeStartedA = wx.StaticText(self, -1, "N/A")
        self.downloadedStatus = wx.StaticText(self, -1, "Data Downloaded:")
        self.downloadedStatusA = wx.StaticText(self, -1, "N/A")
        
        self.Bind(wx.EVT_BUTTON , self.onStopAndDownloadClick , self.cmbStopAndDownload)
        self.Bind(wx.EVT_BUTTON , self.onStartAndClearClick , self.cmbStartAndClear)
        #self.Bind(wx.EVT_BUTTON , self.stopPolling , self.cmbStopPoll)
        
        controlBox = wx.StaticBox(self, -1 , 'Operations:')
        controlSizer = wx.StaticBoxSizer(controlBox, wx.VERTICAL)
        
        controlSizer.Add(self.cmbStopAndDownload,0, wx.ALL, 2)
        controlSizer.Add(self.cmbStartAndClear,0, wx.ALL, 2)
        #controlSizer.Add(self.cmbStopPoll,0, wx.ALL, 2)
        
        statusBox = wx.StaticBox(self, -1, "Status:")
        statusSizer = wx.StaticBoxSizer(statusBox, wx.VERTICAL)
        
        statusSubSizer = wx.GridSizer(cols=2, hgap=5, vgap=5)
        statusSubSizer.Add(self.connectionStatus , 0, wx.ALL, 2)
        statusSubSizer.Add(self.connectionStatusA, 0, wx.ALL, 2)
        statusSubSizer.Add(self.loggerName, 0, wx.ALL, 2)
        statusSubSizer.Add(self.loggerNameA, 0, wx.ALL, 2)
        statusSubSizer.Add(self.loggingStatus, 0, wx.ALL, 2)
        statusSubSizer.Add(self.loggingStatusA, 0, wx.ALL, 2)
        statusSubSizer.Add(self.sampleCount, 0, wx.ALL, 2)
        statusSubSizer.Add(self.sampleCountA, 0, wx.ALL, 2)
        statusSubSizer.Add(self.timeStarted, 0, wx.ALL, 2)
        statusSubSizer.Add(self.timeStartedA, 0, wx.ALL, 2)
        statusSubSizer.Add(self.downloadedStatus, 0, wx.ALL, 2)
        statusSubSizer.Add(self.downloadedStatusA, 0, wx.ALL, 2)
        
        statusSizer.Add(statusSubSizer)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(controlSizer, 0, wx.ALL, 7)
        sizer.Add(statusSizer, 0, wx.ALL, 7)
        
        self.SetSizer(sizer)
        size = sizer.GetMinSize()
        self.Fit()
        parent.SetMinSize(size)
        parent.Fit()
        self.autoRefreshStatus()
        
    def log(self, message, priority, source):
        if not(self.dataHandler==None):
            self.dataHandler.logError(message, priority, source,self.dataHandler.dateStamp('', time=True, now=True))
    
    def onStopAndDownloadClick(self, event):
        self.dl.connect()
        self.updateStatus()
        self.dl.stopLogging()
        self.updateStatus()
        self.log("About to Download Data" , 0 , "gui.py:onStopAndDownloadClick")
        data = self.dl.getValidData()
        self.log("Downloaded: " +  str(len(data)) + " points" , 0 , "gui.py:onStopAndDownloadClick")
        times = self.dl.getStartTime()
        self.log("About to Backup Data" , 0 , "gui.py:onStopAndDownloadClick")
        self.dataHandler.dataBackup(data, times, int(self.dl.getSampleRate(),16))
        self.log("Data Backed Up" , 0 , "gui.py:onStopAndDownloadClick")
        self.updateStatus()
    
    def onStartAndClearClick(self, event):
        self.dl.connect()
        self.dl.startLogging()   
        self.updateStatus()
    
    def onRefreshClick(self, event):
        self.dl.connect()
        self.updateStatus()
    
    def onConnectClick(self, event):
        self.dl.connect()
        self.updateStatus()
    
    def onStopClick(self, event):
        self.dl.stopLogging()
        self.updateStatus()
    
    def onDownloadClick(self, event):
        self.log("About to Download Data" , 0 , "gui.py:onDownloadCLick")
        data = self.dl.getValidData()
        self.log("Downloaded: " +  str(len(data)) + " points" , 0 , "gui.py:onDownloadCLick")
        times = self.dl.getStartTime()
        self.log("About to Backup Data" , 0 , "gui.py:onDownloadCLick")
        self.dataHandler.dataBackup(data, times, int(self.dl.getSampleRate(),16))
        self.log("Data Backed Up" , 0 , "gui.py:onDownloadCLick")
        self.updateStatus()
    
    def onResetClick(self, event):
        self.dl.startLogging()   
        self.updateStatus()
        
    def stopPolling(self,event):
        loggerPoll.cancel()
    
    def autoRefreshStatus(self):
        try:
            status = self.dl.connect()
            self.updateStatus()
            if status == 0:
                Timer(5, self.autoRefreshStatus, ()).start()
        except:
            pass
        
    
    def updateStatus(self):
        dl = self.dl
        connectionStatus = dl.connected 
        unknown = "N/A"
        
        if connectionStatus == False:
            self.connectionStatusA.SetLabel( "Not Connected")
            self.loggerNameA.SetLabel(unknown)
            self.loggingStatusA.SetLabel(unknown)
            self.sampleCountA.SetLabel(unknown)
            self.timeStartedA.SetLabel(unknown)
            self.downloadedStatusA.SetLabel(unknown)
        else:
            self.connectionStatusA.SetLabel( "Connected")
            self.loggerNameA.SetLabel( dl.getName())
            self.loggingStatusA.SetLabel(dl.getLoggingStatus())
            self.sampleCountA.SetLabel( str(int(dl.getSampleCount(),16)) + ' / 32510')
            times = dl.getStartTime()
            timestr = str(times[0]) + ':' + str(times[1]) + ':' + str(times[2]) + ' ' + str(times[3]) + '/' + str(times[4]) + '/' + str(times[5])
            self.timeStartedA.SetLabel(timestr)
            self.downloadedStatusA.SetLabel(str(dl.getDownloadStatus()))

class Frame(wx.Frame):
    def __init__(self, parent, id, dh=None):
        wx.Frame.__init__(self, parent, id, title='Datalogger') 
        panel = MainPanel(self,dataHandler=dh)

class App(wx.App):
    
    dataStore = tcDataHandlerEL3()
    
    def OnInit(self):
        self.frame = Frame(parent=None, id=-1,dh=self.dataStore )
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = App(redirect=False)
    app.MainLoop()


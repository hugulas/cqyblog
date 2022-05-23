# 怎么得到所有的SNMP MIB的OIDs



有个问题，困扰了我很久，我需要通过SNMP收集一些硬件的性能计数和配置信息。

但是，我也不知道snmp都支持哪些OIDs？怎么办？

有人说，用snmpwalk，但是我遇到了报错，毕竟是snmpwalk已经是在收集数据了。

一番搜索，我找到了个靠谱的办法。

https://stackoverflow.com/questions/12507634/how-to-get-oids-from-a-mib-file/38375677#38375677

```bash
snmptranslate -Pu -Tz -M /usr/share/snmp/mibs/ -m IBM-OSA-MIB
```

通过这条命令，我就可以拿到目前机器上所有IBM网卡的snmp OID信息。

-M: mib文件所在目录

-m: 想要的mib列表

"ibm"                   "1.3.6.1.4.1.2"
"ibmProd"                       "1.3.6.1.4.1.2.6"
"ibmOSAMib"                     "1.3.6.1.4.1.2.6.188"
"ibmOSAExpNotif"                        "1.3.6.1.4.1.2.6.188.0"
"ibmOSAExpEthLANStateChange"                    "1.3.6.1.4.1.2.6.188.0.1"
"ibmOSAExpTRLANStateChange"                     "1.3.6.1.4.1.2.6.188.0.2"
"ibmOSAExp10GigEthLANStateChange"                       "1.3.6.1.4.1.2.6.188.0.3"
"ibmOSAExp3LANStateChange"                      "1.3.6.1.4.1.2.6.188.0.4"
"ibmOSAExp5SLANStateChange"                     "1.3.6.1.4.1.2.6.188.0.5"
"ibmOSAExp7LANStateChange"                      "1.3.6.1.4.1.2.6.188.0.7"
"ibmOSAMibObjects"                      "1.3.6.1.4.1.2.6.188.1"
"ibmOSAExpChannelTable"                 "1.3.6.1.4.1.2.6.188.1.1"
"ibmOSAExpChannelEntry"                 "1.3.6.1.4.1.2.6.188.1.1.1"
"ibmOSAExpChannelNumber"                        "1.3.6.1.4.1.2.6.188.1.1.1.1"
"ibmOSAExpChannelType"                  "1.3.6.1.4.1.2.6.188.1.1.1.2"
"ibmOSAExpChannelHdwLevel"                      "1.3.6.1.4.1.2.6.188.1.1.1.3"
"ibmOSAExpChannelSubType"                       "1.3.6.1.4.1.2.6.188.1.1.1.4"
"ibmOSAExpChannelShared"                        "1.3.6.1.4.1.2.6.188.1.1.1.5"
"ibmOSAExpChannelNodeDesc"                      "1.3.6.1.4.1.2.6.188.1.1.1.6"
"ibmOSAExpChannelProcCodeLevel"                 "1.3.6.1.4.1.2.6.188.1.1.1.8"
"ibmOSAExpChannelPCIBusUtil1Min"                        "1.3.6.1.4.1.2.6.188.1.1.1.9"
"ibmOSAExpChannelProcUtil1Min"                  "1.3.6.1.4.1.2.6.188.1.1.1.10"
"ibmOSAExpChannelPCIBusUtil5Min"                        "1.3.6.1.4.1.2.6.188.1.1.1.11"
"ibmOSAExpChannelProcUtil5Min"                  "1.3.6.1.4.1.2.6.188.1.1.1.12"
"ibmOSAExpChannelPCIBusUtilHour"                        "1.3.6.1.4.1.2.6.188.1.1.1.13"
"ibmOSAExpChannelProcUtilHour"                  "1.3.6.1.4.1.2.6.188.1.1.1.14"
"ibmOSAExpChannelCSS"                   "1.3.6.1.4.1.2.6.188.1.1.1.15"
"ibmOSAExpChannelMIF"                   "1.3.6.1.4.1.2.6.188.1.1.1.16"
"ibmOSAExpPerfTable"                    "1.3.6.1.4.1.2.6.188.1.2"
"ibmOSAExpPerfEntry"                    "1.3.6.1.4.1.2.6.188.1.2.1"
"ibmOSAExpPerfDataLP0"                  "1.3.6.1.4.1.2.6.188.1.2.1.1"
"ibmOSAExpPerfDataLP1"                  "1.3.6.1.4.1.2.6.188.1.2.1.2"
"ibmOSAExpPerfDataLP2"                  "1.3.6.1.4.1.2.6.188.1.2.1.3"
"ibmOSAExpPerfDataLP3"                  "1.3.6.1.4.1.2.6.188.1.2.1.4"
"ibmOSAExpPerfDataLP4"                  "1.3.6.1.4.1.2.6.188.1.2.1.5"
"ibmOSAExpPerfDataLP5"                  "1.3.6.1.4.1.2.6.188.1.2.1.6"
"ibmOSAExpPerfDataLP6"                  "1.3.6.1.4.1.2.6.188.1.2.1.7"
"ibmOSAExpPerfDataLP7"                  "1.3.6.1.4.1.2.6.188.1.2.1.8"
"ibmOSAExpPerfDataLP8"                  "1.3.6.1.4.1.2.6.188.1.2.1.9"
"ibmOSAExpPerfDataLP9"                  "1.3.6.1.4.1.2.6.188.1.2.1.10"
"ibmOSAExpPerfDataLP10"                 "1.3.6.1.4.1.2.6.188.1.2.1.11"
"ibmOSAExpPerfDataLP11"                 "1.3.6.1.4.1.2.6.188.1.2.1.12"
"ibmOSAExpPerfDataLP12"                 "1.3.6.1.4.1.2.6.188.1.2.1.13"
"ibmOSAExpPerfDataLP13"                 "1.3.6.1.4.1.2.6.188.1.2.1.14"
"ibmOSAExpPerfDataLP14"                 "1.3.6.1.4.1.2.6.188.1.2.1.15"
"ibmOSAExpPerfDataLP15"                 "1.3.6.1.4.1.2.6.188.1.2.1.16"
"ibmOSAExpPETable"                      "1.3.6.1.4.1.2.6.188.1.3"
"ibmOSAExpPEEntry"                      "1.3.6.1.4.1.2.6.188.1.3.1"
"ibmOSAExpPEMaxSizeArpCache"                    "1.3.6.1.4.1.2.6.188.1.3.1.1"
"ibmOSAExpPEArpPendingEntries"                  "1.3.6.1.4.1.2.6.188.1.3.1.2"
"ibmOSAExpPEArpActiveEntries"                   "1.3.6.1.4.1.2.6.188.1.3.1.3"
"ibmOSAExpPEIPEntries"                  "1.3.6.1.4.1.2.6.188.1.3.1.4"
"ibmOSAExpPEMulticastEntries"                   "1.3.6.1.4.1.2.6.188.1.3.1.5"
"ibmOSAExpPEMulticastData"                      "1.3.6.1.4.1.2.6.188.1.3.1.6"
"ibmOSAExpEthPortTable"                 "1.3.6.1.4.1.2.6.188.1.4"
"ibmOSAExpEthPortEntry"                 "1.3.6.1.4.1.2.6.188.1.4.1"
"ibmOsaExpEthPortNumber"                        "1.3.6.1.4.1.2.6.188.1.4.1.1"
"ibmOsaExpEthPortType"                  "1.3.6.1.4.1.2.6.188.1.4.1.2"
"ibmOsaExpEthLanTrafficState"                   "1.3.6.1.4.1.2.6.188.1.4.1.3"
"ibmOsaExpEthServiceMode"                       "1.3.6.1.4.1.2.6.188.1.4.1.4"
"ibmOsaExpEthDisabledStatus"                    "1.3.6.1.4.1.2.6.188.1.4.1.5"
"ibmOsaExpEthConfigName"                        "1.3.6.1.4.1.2.6.188.1.4.1.6"
"ibmOsaExpEthConfigSpeedMode"                   "1.3.6.1.4.1.2.6.188.1.4.1.7"
"ibmOsaExpEthActiveSpeedMode"                   "1.3.6.1.4.1.2.6.188.1.4.1.8"
"ibmOsaExpEthMacAddrActive"                     "1.3.6.1.4.1.2.6.188.1.4.1.9"
"ibmOsaExpEthMacAddrBurntIn"                    "1.3.6.1.4.1.2.6.188.1.4.1.10"
"ibmOsaExpEthUserData"                  "1.3.6.1.4.1.2.6.188.1.4.1.11"
"ibmOsaExpEthOutPackets"                        "1.3.6.1.4.1.2.6.188.1.4.1.12"
"ibmOsaExpEthInPackets"                 "1.3.6.1.4.1.2.6.188.1.4.1.13"
"ibmOsaExpEthInGroupFrames"                     "1.3.6.1.4.1.2.6.188.1.4.1.14"
"ibmOsaExpEthInBroadcastFrames"                 "1.3.6.1.4.1.2.6.188.1.4.1.15"
"ibmOsaExpEthPortName"                  "1.3.6.1.4.1.2.6.188.1.4.1.16"
"ibmOsaExpEthInUnknownIPFrames"                 "1.3.6.1.4.1.2.6.188.1.4.1.17"
"ibmOsaExpEthGroupAddrTable"                    "1.3.6.1.4.1.2.6.188.1.4.1.18"
"ibmOsaExpEthTrapControl"                       "1.3.6.1.4.1.2.6.188.1.4.1.19"
"ibmOSAExpTRPortTable"                  "1.3.6.1.4.1.2.6.188.1.5"
"ibmOSAExpTRPortEntry"                  "1.3.6.1.4.1.2.6.188.1.5.1"
"ibmOsaExpTRPortNumber"                 "1.3.6.1.4.1.2.6.188.1.5.1.1"
"ibmOsaExpTRPortType"                   "1.3.6.1.4.1.2.6.188.1.5.1.2"
"ibmOsaExpTRLanTrafficState"                    "1.3.6.1.4.1.2.6.188.1.5.1.3"
"ibmOsaExpTRServiceMode"                        "1.3.6.1.4.1.2.6.188.1.5.1.4"
"ibmOsaExpTRDisabledStatus"                     "1.3.6.1.4.1.2.6.188.1.5.1.5"
"ibmOsaExpTRConfigName"                 "1.3.6.1.4.1.2.6.188.1.5.1.6"
"ibmOsaExpTRMacAddrActive"                      "1.3.6.1.4.1.2.6.188.1.5.1.7"
"ibmOsaExpTRMacAddrBurntIn"                     "1.3.6.1.4.1.2.6.188.1.5.1.8"
"ibmOsaExpTRConfigSpeedMode"                    "1.3.6.1.4.1.2.6.188.1.5.1.9"
"ibmOsaExpTRActiveSpeedMode"                    "1.3.6.1.4.1.2.6.188.1.5.1.10"
"ibmOsaExpTRUserData"                   "1.3.6.1.4.1.2.6.188.1.5.1.11"
"ibmOsaExpTRPortName"                   "1.3.6.1.4.1.2.6.188.1.5.1.12"
"ibmOsaExpTRGroupAddrTable"                     "1.3.6.1.4.1.2.6.188.1.5.1.13"
"ibmOsaExpTRFunctionalAddr"                     "1.3.6.1.4.1.2.6.188.1.5.1.14"
"ibmOsaExpTRRingStatus"                 "1.3.6.1.4.1.2.6.188.1.5.1.15"
"ibmOsaExpTRAllowAccessPriority"                        "1.3.6.1.4.1.2.6.188.1.5.1.16"
"ibmOsaExpTREarlyTokenRelease"                  "1.3.6.1.4.1.2.6.188.1.5.1.17"
"ibmOsaExpTRBeaconingAddress"                   "1.3.6.1.4.1.2.6.188.1.5.1.18"
"ibmOsaExpTRUpstreamNeighbor"                   "1.3.6.1.4.1.2.6.188.1.5.1.19"
"ibmOsaExpTRRingState"                  "1.3.6.1.4.1.2.6.188.1.5.1.20"
"ibmOsaExpTRRingOpenStatus"                     "1.3.6.1.4.1.2.6.188.1.5.1.21"
"ibmOsaExpTRPacketsTransmitted"                 "1.3.6.1.4.1.2.6.188.1.5.1.22"
"ibmOsaExpTRPacketsReceived"                    "1.3.6.1.4.1.2.6.188.1.5.1.23"
"ibmOsaExpTRLineErrorCount"                     "1.3.6.1.4.1.2.6.188.1.5.1.24"
"ibmOsaExpTRBurstErrorCount"                    "1.3.6.1.4.1.2.6.188.1.5.1.25"
"ibmOsaExpTRACErrorCount"                       "1.3.6.1.4.1.2.6.188.1.5.1.26"
"ibmOsaExpTRAbortTransErrorCount"                       "1.3.6.1.4.1.2.6.188.1.5.1.27"
"ibmOsaExpTRInternalErrorCount"                 "1.3.6.1.4.1.2.6.188.1.5.1.28"
"ibmOsaExpTRLostFrameErrorCount"                        "1.3.6.1.4.1.2.6.188.1.5.1.29"
"ibmOsaExpTRRcvCongestionCount"                 "1.3.6.1.4.1.2.6.188.1.5.1.30"
"ibmOsaExpTRFrameCopyErrorCount"                        "1.3.6.1.4.1.2.6.188.1.5.1.31"
"ibmOsaExpTRTokenErrorCount"                    "1.3.6.1.4.1.2.6.188.1.5.1.32"
"ibmOsaExpTRFullDuplexErrorCount"                       "1.3.6.1.4.1.2.6.188.1.5.1.33"
"ibmOsaExpTRSoftErrorCount"                     "1.3.6.1.4.1.2.6.188.1.5.1.34"
"ibmOsaExpTRHardErrorCount"                     "1.3.6.1.4.1.2.6.188.1.5.1.35"
"ibmOsaExpTRSignalLossErrorCount"                       "1.3.6.1.4.1.2.6.188.1.5.1.36"
"ibmOsaExpTRTransmitBeaconCount"                        "1.3.6.1.4.1.2.6.188.1.5.1.37"
"ibmOsaExpTRRecoveryCounter"                    "1.3.6.1.4.1.2.6.188.1.5.1.38"
"ibmOsaExpTRLobeWireFaultCount"                 "1.3.6.1.4.1.2.6.188.1.5.1.39"
"ibmOsaExpTRRemoveReceivedCount"                        "1.3.6.1.4.1.2.6.188.1.5.1.40"
"ibmOsaExpTRSingleStationCount"                 "1.3.6.1.4.1.2.6.188.1.5.1.41"
"ibmOsaExpTRTrapControl"                        "1.3.6.1.4.1.2.6.188.1.5.1.42"
"ibmOSAExpATMPortTable"                 "1.3.6.1.4.1.2.6.188.1.7"
"ibmOSAExpATMPortEntry"                 "1.3.6.1.4.1.2.6.188.1.7.1"
"ibmOsaExpATMPortNumber"                        "1.3.6.1.4.1.2.6.188.1.7.1.1"
"ibmOsaExpATMPortType"                  "1.3.6.1.4.1.2.6.188.1.7.1.2"
"ibmOsaExpATMLanTrafficState"                   "1.3.6.1.4.1.2.6.188.1.7.1.3"
"ibmOsaExpATMServiceMode"                       "1.3.6.1.4.1.2.6.188.1.7.1.4"
"ibmOsaExpATMDisabledStatus"                    "1.3.6.1.4.1.2.6.188.1.7.1.5"
"ibmOsaExpATMConfigName"                        "1.3.6.1.4.1.2.6.188.1.7.1.6"
"ibmOsaExpATMMacAddrActive"                     "1.3.6.1.4.1.2.6.188.1.7.1.7"
"ibmOsaExpATMMacAddrBurntIn"                    "1.3.6.1.4.1.2.6.188.1.7.1.8"
"ibmOsaExpATMUserData"                  "1.3.6.1.4.1.2.6.188.1.7.1.9"
"ibmOsaExpATMPortName"                  "1.3.6.1.4.1.2.6.188.1.7.1.12"
"ibmOsaExpATMGroupMacAddrTable"                 "1.3.6.1.4.1.2.6.188.1.7.1.13"
"ibmOsaExpATMIBMEnhancedMode"                   "1.3.6.1.4.1.2.6.188.1.7.1.14"
"ibmOsaExpATMBestEffortPeakRate"                        "1.3.6.1.4.1.2.6.188.1.7.1.15"
"ibmOsaExpATMConfigMode"                        "1.3.6.1.4.1.2.6.188.1.7.1.16"
"ibmOsaExpATMConfigLanType"                     "1.3.6.1.4.1.2.6.188.1.7.1.17"
"ibmOsaExpATMActualLanType"                     "1.3.6.1.4.1.2.6.188.1.7.1.18"
"ibmOsaExpATMConfigMaxDataFrmSz"                        "1.3.6.1.4.1.2.6.188.1.7.1.19"
"ibmOsaExpATMActualMaxDataFrmSz"                        "1.3.6.1.4.1.2.6.188.1.7.1.20"
"ibmOsaExpATMConfigELANName"                    "1.3.6.1.4.1.2.6.188.1.7.1.21"
"ibmOsaExpATMActualELANName"                    "1.3.6.1.4.1.2.6.188.1.7.1.22"
"ibmOsaExpATMConfigLESATMAddress"                       "1.3.6.1.4.1.2.6.188.1.7.1.23"
"ibmOsaExpATMActualLESATMAddress"                       "1.3.6.1.4.1.2.6.188.1.7.1.24"
"ibmOsaExpATMControlTimeout"                    "1.3.6.1.4.1.2.6.188.1.7.1.25"
"ibmOsaExpATMMaxUnknownFrameCount"                      "1.3.6.1.4.1.2.6.188.1.7.1.26"
"ibmOsaExpATMMaxUnknownFrameTime"                       "1.3.6.1.4.1.2.6.188.1.7.1.27"
"ibmOsaExpATMVCCTimeoutPeriod"                  "1.3.6.1.4.1.2.6.188.1.7.1.28"
"ibmOsaExpATMMaxRetryCount"                     "1.3.6.1.4.1.2.6.188.1.7.1.29"
"ibmOsaExpATMAgingTime"                 "1.3.6.1.4.1.2.6.188.1.7.1.30"
"ibmOsaExpATMForwardDelayTime"                  "1.3.6.1.4.1.2.6.188.1.7.1.31"
"ibmOsaExpATMExpectedARPRespTime"                       "1.3.6.1.4.1.2.6.188.1.7.1.32"
"ibmOsaExpATMFlushTimeout"                      "1.3.6.1.4.1.2.6.188.1.7.1.33"
"ibmOsaExpATMPathSwitchingDelay"                        "1.3.6.1.4.1.2.6.188.1.7.1.34"
"ibmOsaExpATMLocalSegmentID"                    "1.3.6.1.4.1.2.6.188.1.7.1.35"
"ibmOsaExpATMMltcstSendVCCType"                 "1.3.6.1.4.1.2.6.188.1.7.1.36"
"ibmOsaExpATMMltcstSendVCCAvgRate"                      "1.3.6.1.4.1.2.6.188.1.7.1.37"
"ibmOsaExpATMMcastSendVCCPeakRate"                      "1.3.6.1.4.1.2.6.188.1.7.1.38"
"ibmOsaExpATMConnectCompleteTimer"                      "1.3.6.1.4.1.2.6.188.1.7.1.39"
"ibmOsaExpATMClientATMAddress"                  "1.3.6.1.4.1.2.6.188.1.7.1.40"
"ibmOsaExpATMClientIdentifier"                  "1.3.6.1.4.1.2.6.188.1.7.1.41"
"ibmOsaExpATMClientCurrentState"                        "1.3.6.1.4.1.2.6.188.1.7.1.42"
"ibmOsaExpATMLastFailureRespCode"                       "1.3.6.1.4.1.2.6.188.1.7.1.43"
"ibmOsaExpATMLastFailureState"                  "1.3.6.1.4.1.2.6.188.1.7.1.44"
"ibmOsaExpATMProtocol"                  "1.3.6.1.4.1.2.6.188.1.7.1.45"
"ibmOsaExpATMLeVersion"                 "1.3.6.1.4.1.2.6.188.1.7.1.46"
"ibmOsaExpATMTopologyChange"                    "1.3.6.1.4.1.2.6.188.1.7.1.47"
"ibmOsaExpATMConfigServerATMAddr"                       "1.3.6.1.4.1.2.6.188.1.7.1.48"
"ibmOsaExpATMConfigSource"                      "1.3.6.1.4.1.2.6.188.1.7.1.49"
"ibmOsaExpATMProxyClient"                       "1.3.6.1.4.1.2.6.188.1.7.1.50"
"ibmOsaExpATMLePDUOctetsInbound"                        "1.3.6.1.4.1.2.6.188.1.7.1.51"
"ibmOsaExpATMNonErrLePDUDiscIn"                 "1.3.6.1.4.1.2.6.188.1.7.1.52"
"ibmOsaExpATMErrLePDUDiscIn"                    "1.3.6.1.4.1.2.6.188.1.7.1.53"
"ibmOsaExpATMLePDUOctetsOutbound"                       "1.3.6.1.4.1.2.6.188.1.7.1.54"
"ibmOsaExpATMNonErrLePDUDiscOut"                        "1.3.6.1.4.1.2.6.188.1.7.1.55"
"ibmOsaExpATMErrLePDUDiscOut"                   "1.3.6.1.4.1.2.6.188.1.7.1.56"
"ibmOsaExpATMLeARPRequestsOut"                  "1.3.6.1.4.1.2.6.188.1.7.1.57"
"ibmOsaExpATMLeARPRequestsIn"                   "1.3.6.1.4.1.2.6.188.1.7.1.58"
"ibmOsaExpATMLeARPRepliesOut"                   "1.3.6.1.4.1.2.6.188.1.7.1.59"
"ibmOsaExpATMLeARPRepliesIn"                    "1.3.6.1.4.1.2.6.188.1.7.1.60"
"ibmOsaExpATMControlFramesOut"                  "1.3.6.1.4.1.2.6.188.1.7.1.61"
"ibmOsaExpATMControlFramesIn"                   "1.3.6.1.4.1.2.6.188.1.7.1.62"
"ibmOsaExpATMSVCFailures"                       "1.3.6.1.4.1.2.6.188.1.7.1.63"
"ibmOsaExpATMConfigDirectIntfc"                 "1.3.6.1.4.1.2.6.188.1.7.1.64"
"ibmOsaExpATMConfigDirectVPI"                   "1.3.6.1.4.1.2.6.188.1.7.1.65"
"ibmOsaExpATMConfigDirectVCI"                   "1.3.6.1.4.1.2.6.188.1.7.1.66"
"ibmOsaExpATMControlDirectIntfc"                        "1.3.6.1.4.1.2.6.188.1.7.1.67"
"ibmOsaExpATMControlDirectVPI"                  "1.3.6.1.4.1.2.6.188.1.7.1.68"
"ibmOsaExpATMControlDirectVCI"                  "1.3.6.1.4.1.2.6.188.1.7.1.69"
"ibmOsaExpATMControlDistIntfc"                  "1.3.6.1.4.1.2.6.188.1.7.1.70"
"ibmOsaExpATMControlDistributeVPI"                      "1.3.6.1.4.1.2.6.188.1.7.1.71"
"ibmOsaExpATMControlDistributeVCI"                      "1.3.6.1.4.1.2.6.188.1.7.1.72"
"ibmOsaExpATMMulticastSendIntfc"                        "1.3.6.1.4.1.2.6.188.1.7.1.73"
"ibmOsaExpATMMulticastSendVPI"                  "1.3.6.1.4.1.2.6.188.1.7.1.74"
"ibmOsaExpATMMulticastSendVCI"                  "1.3.6.1.4.1.2.6.188.1.7.1.75"
"ibmOsaExpATMMulticastFwdIntfc"                 "1.3.6.1.4.1.2.6.188.1.7.1.76"
"ibmOsaExpATMMulticastForwardVPI"                       "1.3.6.1.4.1.2.6.188.1.7.1.77"
"ibmOsaExpATMMulticastForwardVCI"                       "1.3.6.1.4.1.2.6.188.1.7.1.78"
"ibmOSAExpV2PerfTable"                  "1.3.6.1.4.1.2.6.188.1.8"
"ibmOSAExpV2PerfEntry"                  "1.3.6.1.4.1.2.6.188.1.8.1"
"ibmOSAExpV2PerfCSSId"                  "1.3.6.1.4.1.2.6.188.1.8.1.1"
"ibmOSAExpV2PerfImageId"                        "1.3.6.1.4.1.2.6.188.1.8.1.2"
"ibmOSAExpV2PerfProcUtil1Min"                   "1.3.6.1.4.1.2.6.188.1.8.1.3"
"ibmOSAExpV2PerfInKbytesRate1Min"                       "1.3.6.1.4.1.2.6.188.1.8.1.4"
"ibmOSAExpV2PerfOutKbytesRate1Min"                      "1.3.6.1.4.1.2.6.188.1.8.1.5"
"ibmOSAExpV2PerfProcUtil5Min"                   "1.3.6.1.4.1.2.6.188.1.8.1.6"
"ibmOSAExpV2PerfInKbytesRate5Min"                       "1.3.6.1.4.1.2.6.188.1.8.1.7"
"ibmOSAExpV2PerfOutKbytesRate5Min"                      "1.3.6.1.4.1.2.6.188.1.8.1.8"
"ibmOSAExpV2PerfProcUtilHour"                   "1.3.6.1.4.1.2.6.188.1.8.1.9"
"ibmOSAExpV2PerfInKbytesRateHour"                       "1.3.6.1.4.1.2.6.188.1.8.1.10"
"ibmOSAExpV2PerfOutKbytesRateHour"                      "1.3.6.1.4.1.2.6.188.1.8.1.11"
"ibmOSAExp10GigEthPortTable"                    "1.3.6.1.4.1.2.6.188.1.9"
"ibmOSAExp10GigEthPortEntry"                    "1.3.6.1.4.1.2.6.188.1.9.1"
"ibmOsaExp10GigEthPortNumber"                   "1.3.6.1.4.1.2.6.188.1.9.1.1"
"ibmOsaExp10GigEthPortType"                     "1.3.6.1.4.1.2.6.188.1.9.1.2"
"ibmOsaExp10GigEthLanTrafficState"                      "1.3.6.1.4.1.2.6.188.1.9.1.3"
"ibmOsaExp10GigEthServiceMode"                  "1.3.6.1.4.1.2.6.188.1.9.1.4"
"ibmOsaExp10GigEthDisabledStatus"                       "1.3.6.1.4.1.2.6.188.1.9.1.5"
"ibmOsaExp10GigEthActiveSpeedMode"                      "1.3.6.1.4.1.2.6.188.1.9.1.6"
"ibmOsaExp10GigEthMacAddrActive"                        "1.3.6.1.4.1.2.6.188.1.9.1.7"
"ibmOsaExp10GigEthMacAddrBurntIn"                       "1.3.6.1.4.1.2.6.188.1.9.1.8"
"ibmOsaExp10GigEthOutPackets"                   "1.3.6.1.4.1.2.6.188.1.9.1.9"
"ibmOsaExp10GigEthInPackets"                    "1.3.6.1.4.1.2.6.188.1.9.1.10"
"ibmOsaExp10GigEthGoodPackets"                  "1.3.6.1.4.1.2.6.188.1.9.1.11"
"ibmOsaExp10GigEthCRCRecErrors"                 "1.3.6.1.4.1.2.6.188.1.9.1.12"
"ibmOsaExp10GigEthPortName"                     "1.3.6.1.4.1.2.6.188.1.9.1.13"
"ibmOsaExp10GigEthMultiPacketsRcv"                      "1.3.6.1.4.1.2.6.188.1.9.1.14"
"ibmOsaExp10GigEthUniPacketsRcv"                        "1.3.6.1.4.1.2.6.188.1.9.1.15"
"ibmOsaExp10GigEthVLANPacketsRcv"                       "1.3.6.1.4.1.2.6.188.1.9.1.16"
"ibmOsaExp10GigEthJumboPacketsRcv"                      "1.3.6.1.4.1.2.6.188.1.9.1.17"
"ibmOsaExp10GigEthTotalOctetsRcv"                       "1.3.6.1.4.1.2.6.188.1.9.1.18"
"ibmOsaExp10GigEthRcvBroadCnt"                  "1.3.6.1.4.1.2.6.188.1.9.1.19"
"ibmOsaExp10GigEthRcvNoBufferCnt"                       "1.3.6.1.4.1.2.6.188.1.9.1.20"
"ibmOsaExp10GigEthRcvUndersizeCnt"                      "1.3.6.1.4.1.2.6.188.1.9.1.21"
"ibmOsaExp10GigEthRcvOversizeCnt"                       "1.3.6.1.4.1.2.6.188.1.9.1.22"
"ibmOsaExp10GigEthRcvLenErrorCnt"                       "1.3.6.1.4.1.2.6.188.1.9.1.23"
"ibmOsaExp10GigEthMissedPacketCnt"                      "1.3.6.1.4.1.2.6.188.1.9.1.24"
"ibmOsaExp10GigEthRcvJabberCnt"                 "1.3.6.1.4.1.2.6.188.1.9.1.25"
"ibmOsaExp10GigEthBroadPacketXmit"                      "1.3.6.1.4.1.2.6.188.1.9.1.26"
"ibmOsaExp10GigEthMultiPacketXmit"                      "1.3.6.1.4.1.2.6.188.1.9.1.27"
"ibmOsaExp10GigEthUniPacketXmit"                        "1.3.6.1.4.1.2.6.188.1.9.1.28"
"ibmOsaExp10GigEthVLANPacketXmit"                       "1.3.6.1.4.1.2.6.188.1.9.1.29"
"ibmOsaExp10GigEthJumboPacketXmit"                      "1.3.6.1.4.1.2.6.188.1.9.1.30"
"ibmOsaExp10GigEthTotalOctetsXmit"                      "1.3.6.1.4.1.2.6.188.1.9.1.31"
"ibmOsaExp10GigEthDeferCount"                   "1.3.6.1.4.1.2.6.188.1.9.1.32"
"ibmOsaExp10GigEthRemoteFaultCnt"                       "1.3.6.1.4.1.2.6.188.1.9.1.33"
"ibmOsaExp10GigEthLocalFaultCnt"                        "1.3.6.1.4.1.2.6.188.1.9.1.34"
"ibmOsaExp10GigEthPauseFrmRcvCnt"                       "1.3.6.1.4.1.2.6.188.1.9.1.35"
"ibmOsaExp10GigEthPauseFrmXmitCnt"                      "1.3.6.1.4.1.2.6.188.1.9.1.36"
"ibmOsaExp10GigEthXONRcvCount"                  "1.3.6.1.4.1.2.6.188.1.9.1.37"
"ibmOsaExp10GigEthXONXmtCount"                  "1.3.6.1.4.1.2.6.188.1.9.1.38"
"ibmOsaExp10GigEthXOFFRcvCount"                 "1.3.6.1.4.1.2.6.188.1.9.1.39"
"ibmOsaExp10GigEthXOFFXmtCount"                 "1.3.6.1.4.1.2.6.188.1.9.1.40"
"ibmOsaExp10GigEthTrapControl"                  "1.3.6.1.4.1.2.6.188.1.9.1.41"
"ibmOSAExp3PortTable"                   "1.3.6.1.4.1.2.6.188.1.10"
"ibmOSAExp3PortEntry"                   "1.3.6.1.4.1.2.6.188.1.10.1"
"ibmOsaExp3PortNumber"                  "1.3.6.1.4.1.2.6.188.1.10.1.1"
"ibmOsaExp3PortType"                    "1.3.6.1.4.1.2.6.188.1.10.1.2"
"ibmOsaExp3LanTrafficState"                     "1.3.6.1.4.1.2.6.188.1.10.1.3"
"ibmOsaExp3ServiceMode"                 "1.3.6.1.4.1.2.6.188.1.10.1.4"
"ibmOsaExp3DisabledStatus"                      "1.3.6.1.4.1.2.6.188.1.10.1.5"
"ibmOsaExp3ConfigName"                  "1.3.6.1.4.1.2.6.188.1.10.1.6"
"ibmOsaExp3ConfigSpeedMode"                     "1.3.6.1.4.1.2.6.188.1.10.1.7"
"ibmOsaExp3ActiveSpeedMode"                     "1.3.6.1.4.1.2.6.188.1.10.1.8"
"ibmOsaExp3MacAddrActive"                       "1.3.6.1.4.1.2.6.188.1.10.1.9"
"ibmOsaExp3MacAddrBurntIn"                      "1.3.6.1.4.1.2.6.188.1.10.1.10"
"ibmOsaExp3PortName"                    "1.3.6.1.4.1.2.6.188.1.10.1.11"
"ibmOsaExp3TotalPacketsXmit"                    "1.3.6.1.4.1.2.6.188.1.10.1.12"
"ibmOsaExp3TotalPacketsRecv"                    "1.3.6.1.4.1.2.6.188.1.10.1.13"
"ibmOsaExp3GoodPacketsXmit"                     "1.3.6.1.4.1.2.6.188.1.10.1.14"
"ibmOsaExp3GoodPacketsRecv"                     "1.3.6.1.4.1.2.6.188.1.10.1.15"
"ibmOsaExp3TotalOctetsXmit"                     "1.3.6.1.4.1.2.6.188.1.10.1.16"
"ibmOsaExp3TotalOctetsRecv"                     "1.3.6.1.4.1.2.6.188.1.10.1.17"
"ibmOsaExp3GoodOctetsXmit"                      "1.3.6.1.4.1.2.6.188.1.10.1.18"
"ibmOsaExp3GoodOctetsRecv"                      "1.3.6.1.4.1.2.6.188.1.10.1.19"
"ibmOsaExp3Packet64Xmit"                        "1.3.6.1.4.1.2.6.188.1.10.1.20"
"ibmOsaExp3Packet65to127Xmit"                   "1.3.6.1.4.1.2.6.188.1.10.1.21"
"ibmOsaExp3Packet128to255Xmit"                  "1.3.6.1.4.1.2.6.188.1.10.1.22"
"ibmOsaExp3Packet256to511Xmit"                  "1.3.6.1.4.1.2.6.188.1.10.1.23"
"ibmOsaExp3Packet512to1023Xmit"                 "1.3.6.1.4.1.2.6.188.1.10.1.24"
"ibmOsaExp3Packet1024toMaxXmit"                 "1.3.6.1.4.1.2.6.188.1.10.1.25"
"ibmOsaExp3Packet64Recv"                        "1.3.6.1.4.1.2.6.188.1.10.1.26"
"ibmOsaExp3Packet65to127Recv"                   "1.3.6.1.4.1.2.6.188.1.10.1.27"
"ibmOsaExp3Packet128to255Recv"                  "1.3.6.1.4.1.2.6.188.1.10.1.28"
"ibmOsaExp3Packet256to511Recv"                  "1.3.6.1.4.1.2.6.188.1.10.1.29"
"ibmOsaExp3Packet512to1023Recv"                 "1.3.6.1.4.1.2.6.188.1.10.1.30"
"ibmOsaExp3Packet1024toMaxRecv"                 "1.3.6.1.4.1.2.6.188.1.10.1.31"
"ibmOsaExp3BroadcastPacketsXmit"                        "1.3.6.1.4.1.2.6.188.1.10.1.32"
"ibmOsaExp3BroadcastPacketsRecv"                        "1.3.6.1.4.1.2.6.188.1.10.1.33"
"ibmOsaExp3MulticastPacketsXmit"                        "1.3.6.1.4.1.2.6.188.1.10.1.34"
"ibmOsaExp3MulticastPacketsRecv"                        "1.3.6.1.4.1.2.6.188.1.10.1.35"
"ibmOsaExp3AlignmentErrorCnt"                   "1.3.6.1.4.1.2.6.188.1.10.1.36"
"ibmOsaExp3CRCErrorcnt"                 "1.3.6.1.4.1.2.6.188.1.10.1.37"
"ibmOsaExp3MissedPacketCnt"                     "1.3.6.1.4.1.2.6.188.1.10.1.38"
"ibmOsaExp3SingleCollisionCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.39"
"ibmOsaExp3MultipleCollisionCnt"                        "1.3.6.1.4.1.2.6.188.1.10.1.40"
"ibmOsaExp3ExcessiveCollCnt"                    "1.3.6.1.4.1.2.6.188.1.10.1.41"
"ibmOsaExp3LateCollisionCnt"                    "1.3.6.1.4.1.2.6.188.1.10.1.42"
"ibmOsaExp3DeferCnt"                    "1.3.6.1.4.1.2.6.188.1.10.1.43"
"ibmOsaExp3SequenceErrorCnt"                    "1.3.6.1.4.1.2.6.188.1.10.1.44"
"ibmOsaExp3ReceiveNoBufferCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.45"
"ibmOsaExp3ReceiveLenErrorCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.46"
"ibmOsaExp3XONTransmittedCnt"                   "1.3.6.1.4.1.2.6.188.1.10.1.47"
"ibmOsaExp3XONReceiveCnt"                       "1.3.6.1.4.1.2.6.188.1.10.1.48"
"ibmOsaExp3XOFFTransmittedCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.49"
"ibmOsaExp3XOFFReceiveCnt"                      "1.3.6.1.4.1.2.6.188.1.10.1.50"
"ibmOsaExp3ReceiveJabberCnt"                    "1.3.6.1.4.1.2.6.188.1.10.1.51"
"ibmOsaExp3ReceiveUndersizeCnt"                 "1.3.6.1.4.1.2.6.188.1.10.1.52"
"ibmOsaExp3ReceiveOversizeCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.53"
"ibmOsaExp3ReceiveFragmentCnt"                  "1.3.6.1.4.1.2.6.188.1.10.1.54"
"ibmOsaExp3ExclusiveUseID"                      "1.3.6.1.4.1.2.6.188.1.10.1.55"
"ibmOsaExp3ExclusiveUseMAC"                     "1.3.6.1.4.1.2.6.188.1.10.1.56"
"ibmOsaExp3TrapControl"                 "1.3.6.1.4.1.2.6.188.1.10.1.57"
"ibmOsaExp3L3VMACipv4"                  "1.3.6.1.4.1.2.6.188.1.10.1.58"
"ibmOsaExp3L3VMACipv6"                  "1.3.6.1.4.1.2.6.188.1.10.1.59"
"ibmOSAExp5SPortTable"                  "1.3.6.1.4.1.2.6.188.1.11"
"ibmOSAExp5SPortEntry"                  "1.3.6.1.4.1.2.6.188.1.11.1"
"ibmOsaExp5SPortNumber"                 "1.3.6.1.4.1.2.6.188.1.11.1.1"
"ibmOsaExp5SPortType"                   "1.3.6.1.4.1.2.6.188.1.11.1.2"
"ibmOsaExp5SLanTrafficState"                    "1.3.6.1.4.1.2.6.188.1.11.1.3"
"ibmOsaExp5SServiceMode"                        "1.3.6.1.4.1.2.6.188.1.11.1.4"
"ibmOsaExp5SDisabledStatus"                     "1.3.6.1.4.1.2.6.188.1.11.1.5"
"ibmOsaExp5SConfigName"                 "1.3.6.1.4.1.2.6.188.1.11.1.6"
"ibmOsaExp5SConfigSpeedMode"                    "1.3.6.1.4.1.2.6.188.1.11.1.7"
"ibmOsaExp5SActiveSpeedMode"                    "1.3.6.1.4.1.2.6.188.1.11.1.8"
"ibmOsaExp5SMacAddrActive"                      "1.3.6.1.4.1.2.6.188.1.11.1.9"
"ibmOsaExp5SMacAddrBurntIn"                     "1.3.6.1.4.1.2.6.188.1.11.1.10"
"ibmOsaExp5SPortName"                   "1.3.6.1.4.1.2.6.188.1.11.1.11"
"ibmOsaExp5STotalPacketsXmit"                   "1.3.6.1.4.1.2.6.188.1.11.1.12"
"ibmOsaExp5STotalPacketsRecv"                   "1.3.6.1.4.1.2.6.188.1.11.1.13"
"ibmOsaExp5STotalOctetsXmit"                    "1.3.6.1.4.1.2.6.188.1.11.1.14"
"ibmOsaExp5STotalOctetsRecv"                    "1.3.6.1.4.1.2.6.188.1.11.1.15"
"ibmOsaExp5SPacket1to63Xmit"                    "1.3.6.1.4.1.2.6.188.1.11.1.16"
"ibmOsaExp5SPacket64to126Xmit"                  "1.3.6.1.4.1.2.6.188.1.11.1.17"
"ibmOsaExp5SPacket127to254Xmit"                 "1.3.6.1.4.1.2.6.188.1.11.1.18"
"ibmOsaExp5SPacket255to510Xmit"                 "1.3.6.1.4.1.2.6.188.1.11.1.19"
"ibmOsaExp5SPacket511to1022Xmit"                        "1.3.6.1.4.1.2.6.188.1.11.1.20"
"ibmOsaExp5SPacket1023to1517Xmit"                       "1.3.6.1.4.1.2.6.188.1.11.1.21"
"ibmOsaExp5SPacket1518toMaxXmit"                        "1.3.6.1.4.1.2.6.188.1.11.1.22"
"ibmOsaExp5SPacket1to63Recv"                    "1.3.6.1.4.1.2.6.188.1.11.1.23"
"ibmOsaExp5SPacket64to126Recv"                  "1.3.6.1.4.1.2.6.188.1.11.1.24"
"ibmOsaExp5SPacket127to254Recv"                 "1.3.6.1.4.1.2.6.188.1.11.1.25"
"ibmOsaExp5SPacket255to510Recv"                 "1.3.6.1.4.1.2.6.188.1.11.1.26"
"ibmOsaExp5SPacket511to1022Recv"                        "1.3.6.1.4.1.2.6.188.1.11.1.27"
"ibmOsaExp5SPacket1023to1517Recv"                       "1.3.6.1.4.1.2.6.188.1.11.1.28"
"ibmOsaExp5SPacket1518toMaxRecv"                        "1.3.6.1.4.1.2.6.188.1.11.1.29"
"ibmOsaExp5SBroadcastPacketsXmit"                       "1.3.6.1.4.1.2.6.188.1.11.1.30"
"ibmOsaExp5SBroadcastPacketsRecv"                       "1.3.6.1.4.1.2.6.188.1.11.1.31"
"ibmOsaExp5SMulticastPacketsXmit"                       "1.3.6.1.4.1.2.6.188.1.11.1.32"
"ibmOsaExp5SMulticastPacketsRecv"                       "1.3.6.1.4.1.2.6.188.1.11.1.33"
"ibmOsaExp5SAlignmentErrorCnt"                  "1.3.6.1.4.1.2.6.188.1.11.1.34"
"ibmOsaExp5SFCSErrorcnt"                        "1.3.6.1.4.1.2.6.188.1.11.1.35"
"ibmOsaExp5SLengthErrorCnt"                     "1.3.6.1.4.1.2.6.188.1.11.1.36"
"ibmOsaExp5SReceiveJabberCnt"                   "1.3.6.1.4.1.2.6.188.1.11.1.37"
"ibmOsaExp5SReceiveUndersizeCnt"                        "1.3.6.1.4.1.2.6.188.1.11.1.38"
"ibmOsaExp5SReceiveOversizeCnt"                 "1.3.6.1.4.1.2.6.188.1.11.1.39"
"ibmOsaExp5SNoFreeDescOnNIC"                    "1.3.6.1.4.1.2.6.188.1.11.1.40"
"ibmOsaExp5SNoFreeDescOnLANdriv"                        "1.3.6.1.4.1.2.6.188.1.11.1.41"
"ibmOsaExp5SNoFreeRecvDesc"                     "1.3.6.1.4.1.2.6.188.1.11.1.42"
"ibmOsaExp5SExclusiveUseID"                     "1.3.6.1.4.1.2.6.188.1.11.1.43"
"ibmOsaExp5SExclusiveUseMAC"                    "1.3.6.1.4.1.2.6.188.1.11.1.44"
"ibmOsaExp5STrapControl"                        "1.3.6.1.4.1.2.6.188.1.11.1.45"
"ibmOsaExp5SL3VMACipv4"                 "1.3.6.1.4.1.2.6.188.1.11.1.46"
"ibmOsaExp5SL3VMACipv6"                 "1.3.6.1.4.1.2.6.188.1.11.1.47"
"ibmOsaExp5SPauseXmit"                  "1.3.6.1.4.1.2.6.188.1.11.1.48"
"ibmOsaExp5SPauseRecv"                  "1.3.6.1.4.1.2.6.188.1.11.1.49"
"ibmOSAExp7PortTable"                   "1.3.6.1.4.1.2.6.188.1.12"
"ibmOSAExp7PortEntry"                   "1.3.6.1.4.1.2.6.188.1.12.1"
"ibmOsaExp7PortNumber"                  "1.3.6.1.4.1.2.6.188.1.12.1.1"
"ibmOsaExp7PortType"                    "1.3.6.1.4.1.2.6.188.1.12.1.2"
"ibmOsaExp7LanTrafficState"                     "1.3.6.1.4.1.2.6.188.1.12.1.3"
"ibmOsaExp7ServiceMode"                 "1.3.6.1.4.1.2.6.188.1.12.1.4"
"ibmOsaExp7DisabledStatus"                      "1.3.6.1.4.1.2.6.188.1.12.1.5"
"ibmOsaExp7ConfigName"                  "1.3.6.1.4.1.2.6.188.1.12.1.6"
"ibmOsaExp7ConfigSpeedMode"                     "1.3.6.1.4.1.2.6.188.1.12.1.7"
"ibmOsaExp7ActiveSpeedMode"                     "1.3.6.1.4.1.2.6.188.1.12.1.8"
"ibmOsaExp7MacAddrActive"                       "1.3.6.1.4.1.2.6.188.1.12.1.9"
"ibmOsaExp7MacAddrBurntIn"                      "1.3.6.1.4.1.2.6.188.1.12.1.10"
"ibmOsaExp7PortName"                    "1.3.6.1.4.1.2.6.188.1.12.1.11"
"ibmOsaExp7TotalPacketsXmit"                    "1.3.6.1.4.1.2.6.188.1.12.1.12"
"ibmOsaExp7TotalPacketsRecv"                    "1.3.6.1.4.1.2.6.188.1.12.1.13"
"ibmOsaExp7TotalOctetsXmit"                     "1.3.6.1.4.1.2.6.188.1.12.1.14"
"ibmOsaExp7TotalOctetsRecv"                     "1.3.6.1.4.1.2.6.188.1.12.1.15"
"ibmOsaExp7TxPkts64"                    "1.3.6.1.4.1.2.6.188.1.12.1.16"
"ibmOsaExp7TxPkts65to127"                       "1.3.6.1.4.1.2.6.188.1.12.1.17"
"ibmOsaExp7TxPkts128to255"                      "1.3.6.1.4.1.2.6.188.1.12.1.18"
"ibmOsaExp7TxPkts256to511"                      "1.3.6.1.4.1.2.6.188.1.12.1.19"
"ibmOsaExp7TxPkts512to1023"                     "1.3.6.1.4.1.2.6.188.1.12.1.20"
"ibmOsaExp7TxPkts1024to1522"                    "1.3.6.1.4.1.2.6.188.1.12.1.21"
"ibmOsaExp7TxPkts1523toMax"                     "1.3.6.1.4.1.2.6.188.1.12.1.22"
"ibmOsaExp7RxPkts64"                    "1.3.6.1.4.1.2.6.188.1.12.1.23"
"ibmOsaExp7RxPkts65to127"                       "1.3.6.1.4.1.2.6.188.1.12.1.24"
"ibmOsaExp7RxPkts128to255"                      "1.3.6.1.4.1.2.6.188.1.12.1.25"
"ibmOsaExp7RxPkts256to511"                      "1.3.6.1.4.1.2.6.188.1.12.1.26"
"ibmOsaExp7RxPkts512to1023"                     "1.3.6.1.4.1.2.6.188.1.12.1.27"
"ibmOsaExp7RxPkts1024to1522"                    "1.3.6.1.4.1.2.6.188.1.12.1.28"
"ibmOsaExp7RxPkts1523toMax"                     "1.3.6.1.4.1.2.6.188.1.12.1.29"
"ibmOsaExp7BroadcastPktsXmit"                   "1.3.6.1.4.1.2.6.188.1.12.1.30"
"ibmOsaExp7BroadcastPktsRecv"                   "1.3.6.1.4.1.2.6.188.1.12.1.31"
"ibmOsaExp7MulticastPktsXmit"                   "1.3.6.1.4.1.2.6.188.1.12.1.32"
"ibmOsaExp7MulticastPktsRecv"                   "1.3.6.1.4.1.2.6.188.1.12.1.33"
"ibmOsaExp7TxXON"                       "1.3.6.1.4.1.2.6.188.1.12.1.34"
"ibmOsaExp7TxXOFF"                      "1.3.6.1.4.1.2.6.188.1.12.1.35"
"ibmOsaExp7RxXON"                       "1.3.6.1.4.1.2.6.188.1.12.1.36"
"ibmOsaExp7RxXOFF"                      "1.3.6.1.4.1.2.6.188.1.12.1.37"
"ibmOsaExp7CRCErrorCnt"                 "1.3.6.1.4.1.2.6.188.1.12.1.38"
"ibmOsaExp7IllegalBytesCnt"                     "1.3.6.1.4.1.2.6.188.1.12.1.39"
"ibmOsaExp7ErrorBytesCnt"                       "1.3.6.1.4.1.2.6.188.1.12.1.40"
"ibmOsaExp7ReceiveFragmentCnt"                  "1.3.6.1.4.1.2.6.188.1.12.1.41"
"ibmOsaExp7LengthErrorCnt"                      "1.3.6.1.4.1.2.6.188.1.12.1.42"
"ibmOsaExp7ReceiveJabberCnt"                    "1.3.6.1.4.1.2.6.188.1.12.1.43"
"ibmOsaExp7ReceiveUndersizeCnt"                 "1.3.6.1.4.1.2.6.188.1.12.1.44"
"ibmOsaExp7ReceiveOversizeCnt"                  "1.3.6.1.4.1.2.6.188.1.12.1.45"
"ibmOsaExp7ExclusiveUseID"                      "1.3.6.1.4.1.2.6.188.1.12.1.46"
"ibmOsaExp7ExclusiveUseMAC"                     "1.3.6.1.4.1.2.6.188.1.12.1.47"
"ibmOsaExp7TrapControl"                 "1.3.6.1.4.1.2.6.188.1.12.1.48"
"ibmOsaExp7L3VMACipv4"                  "1.3.6.1.4.1.2.6.188.1.12.1.49"
"ibmOsaExp7L3VMACipv6"                  "1.3.6.1.4.1.2.6.188.1.12.1.50"
"ibmOSAMibConformance"                  "1.3.6.1.4.1.2.6.188.2"
"ibmOSAMibCompliances"                  "1.3.6.1.4.1.2.6.188.2.1"
"ibmOSAMibCompliance"                   "1.3.6.1.4.1.2.6.188.2.1.1"
"ibmOSAMibV2Compliance"                 "1.3.6.1.4.1.2.6.188.2.1.2"
"ibmOSAMibGroups"                       "1.3.6.1.4.1.2.6.188.2.2"
"ibmOSAExpChannelGroup"                 "1.3.6.1.4.1.2.6.188.2.2.1"
"ibmOSAExpPerfGroup"                    "1.3.6.1.4.1.2.6.188.2.2.2"
"ibmOSAExpPEGroup"                      "1.3.6.1.4.1.2.6.188.2.2.3"
"ibmOSAExpEthGroup"                     "1.3.6.1.4.1.2.6.188.2.2.4"
"ibmOSAExpTRGroup"                      "1.3.6.1.4.1.2.6.188.2.2.5"
"ibmOSAExpATMGroup"                     "1.3.6.1.4.1.2.6.188.2.2.7"
"ibmOSAExpV2PerfGroup"                  "1.3.6.1.4.1.2.6.188.2.2.8"
"ibmOSAExpNotifGroup"                   "1.3.6.1.4.1.2.6.188.2.2.9"
"ibmOSAExp10GigEthGroup"                        "1.3.6.1.4.1.2.6.188.2.2.10"
"ibmOSAExp3Group"                       "1.3.6.1.4.1.2.6.188.2.2.11"
"ibmOSAExp5SGroup"                      "1.3.6.1.4.1.2.6.188.2.2.12"
"ibmOSAExp7Group"                       "1.3.6.1.4.1.2.6.188.2.2.13"
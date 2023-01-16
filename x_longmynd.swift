//  -------------------------------------------------------------------
//  File: Longmynd.swift
//
//  This file is part of the SatController 'Suite'. It's purpose is
//  to remotely control and monitor a QO-100 DATV station over a LAN.
//
//  Copyright (C) 2021 Michael Naylor EA7KIR http://michaelnaylor.es
//
//  The 'Suite' is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  The 'Suite' is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General License for more details.
//
//  You should have received a copy of the GNU General License
//  along with  SatServer.  If not, see <https://www.gnu.org/licenses/>.
//  -------------------------------------------------------------------

import Foundation

final class Longmynd {
    private var isStopping = false

    private var values = RxStatusAPI()
    private var cachedValue = RxStatusAPI()
    var isRunning = true
    
    private var currentOffset: Double = 9750000
    private var TS_IP: String
    private var TS_Port: String
    
    private var requstedFrequency: Double = 0
    
    init(TS_IP: String, TS_Port: String) {
        self.TS_IP = TS_IP
        self.TS_Port = TS_Port
    }
    
    func startRunning() {
        logProgress("Longmynd.\(#function) : start running")
        values.state = .OffLine
        readStatus()
    }
    
    func stopRunning() {
        logProgress("Longmynd.\(#function) : start stopping")
        values.state = .ShuttingDown
        isStopping = true
        while isStopping {
            // print(".")
            // await Task.yield()
            Task { try await Task.sleep(seconds: 0.1) }
//            await Task.yield()
        }
        killLongmyndBinary()
        logProgress("Longmynd.\(#function) : has stopped")
        isRunning = false
    }
    
    func configure(freq: String, srs: [String]) {
        resetCachedValue()
        cachedValue.state = .OffLine
        requstedFrequency = doubleFromString(freq)
        let freqKHzDbl = 1000.0 * requstedFrequency
//        let freqKHzDbl = 1000.0 * doubleFromString(freq)
        let requestKHzInt = Int(freqKHzDbl - currentOffset)
        let requestKHzStr = String(requestKHzInt)
        var allSrs = srs[0]
        for i in 1..<srs.count {
            allSrs += ",\(srs[i])"
        }
        let params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
        logProgress("Longmynd.\(#function) : \(params)")
        restartLongmyndBinary(with: params)
        cachedValue.state = .Intializing
    }
    
    func calibrate() {
        logError("Longmynd.\(#function) : NOT IMPLIMENTED")
    }
    
    func newValues() -> RxStatusAPI {
            values = cachedValue
        return values
    }
    
    // MARK: Private Functions
    
    private func doubleFromString(_ str: String) -> Double {
        return (str as NSString).doubleValue
    }


    private func readStatus() {
        Task {
            while !isStopping {
                if let tuple = readTuple() {
                    decodedTuple(lmId: tuple.lmId, lmValue: tuple.lmValue, requstedFrequency: requstedFrequency)
                }
                await Task.yield()
            }
            isStopping = false
        }
    }
    // ====================================================================================
    // MARK:  HERE'S WHERE THE FUN STARTS
    // we're hitting cachedValue directly, so be careful !
    // ====================================================================================
    
    // global long lasting variables
    private var agc1: Int = 0
    private var agc2: Int = 0
    private var pidTypeTupleArray: PidTypeTupleArray = []
    
    func resetCachedValue() {
        agc1 = 0
        agc2 = 0
        pidTypeTupleArray = []
        
        cachedValue.tunedFreq = BlankFrequency
        cachedValue.tunedSr = BlankSR
        cachedValue.constellation = BlankConstellation
        cachedValue.fec = BlankFEC
        cachedValue.codecs = BlankCodecs
        cachedValue.mer = ZeroMER
        cachedValue.margin = BlankMargin
        cachedValue.power = BlankPower
        cachedValue.provider = BlankProvider
        cachedValue.service = BlankService
        cachedValue.tunedError = BlankTunedError
    }

    func decodedTuple(lmId: Int, lmValue: String, requstedFrequency: Double) {
        var statusChanged = false
        var agcChanged = false
        
//        switch cachedValue.state {
//            case .OffLine:
//                return
//            case .Intializing:
//                break
//            case .FoundHeaders:
//                break
//            case .Searching:
//                break
//            case .LockedS, .LockedS2:
//                break
//            case .ShuttingDown:
//                break
//        }

        switch lmId {
            case 1: // State
                switch lmValue {
                    case "0": // initialising
                        cachedValue.state = .Intializing
                        cachedValue.mode = strMode("Initialising")
                        resetCachedValue()
                        statusChanged = true
                    case "1": // searching
                        cachedValue.state = .Searching
                        cachedValue.mode = strMode("Searching")
                        statusChanged = true
                    case "2": // found headers
                        cachedValue.state = .FoundHeaders
                        cachedValue.mode = strMode("Found Headers")
                        statusChanged = true
                    case "3": // locked on a DVB-S signal
                        cachedValue.state = .LockedS
                        statusChanged = true
                        cachedValue.mode = strMode("Locked DVB-S")
                    case "4": // locked on a DVB-S2 signal
                        cachedValue.state = .LockedS2
                        cachedValue.mode = strMode("Locked DVB-S2")
                        statusChanged = true
                    default:
                        logError("Longmynd.\(#function) Invalid State: \(lmValue)")
                        break
                }
            case 2: // LNA Gain - On devices that have LNA Amplifiers this represents the two gain sent as N, where n = (lna_gain<<5) | lna_vgo. Though not actually linear, n can be usefully treated as a single byte representing the gain of the amplifier
                break
            case 3: // Puncture Rate - During a search this is the pucture rate that is being trialled. When locked this is the pucture rate detected in the stream. Sent as a single value, n, where the pucture rate is n/(n+1)
                break
            case 4: // I Symbol Power - Measure of the current power being seen in the I symbols
                break
            case 5: // Q Symbol Power - Measure of the current power being seen in the Q symbols
                break
            case 6: // Carrier Frequency - During a search this is the carrier frequency being trialled. When locked this is the Carrier Frequency detected in the stream. Sent in KHz
                guard let value = Double(lmValue) else {
                    logError("Longmynd.\(#function) : invalid Carrier Frequency: \(lmValue)")
                    break
                }
                let tunedFreq = (value + currentOffset) / 1000
                let tunedError = tunedFreq - requstedFrequency
                cachedValue.tunedFreq = strTunedFrequency(tunedFreq)
                cachedValue.tunedError = strTunedError(tunedError * 1000)
                statusChanged = true
            case 7: // I Constellation - Single signed byte representing the voltage of a sampled I point
                break
            case 8: // Q Constellation - Single signed byte representing the voltage of a sampled Q point
                break
            case 9: // Symbol Rate - During a search this is the symbol rate being trialled.  When locked this is the symbol rate detected in the stream
                guard let value = Double(lmValue) else {
                    logError("Longmynd.\(#function) : invalid Symbole Rate: \(lmValue)")
                    break
                }
                cachedValue.tunedSr = strSr(value / 1000)
                statusChanged = true
            case 10: // Viterbi Error Rate - Viterbi correction rate as a percentage * 100
                break
            case 11: // BER - Bit Error Rate as a Percentage * 100
                break
            case 12: // MER - Modulation Error Ratio in dB * 10
                guard let value = Double(lmValue) else {
                    logError("Longmynd.\(#function) : invalid MER: \(lmValue)")
                    break
                }
                cachedValue.mer = strMer(value / 10)
                statusChanged = true
            case 13: // Service Provider - TS Service Provider Name
                cachedValue.provider = strProvider(lmValue)
                statusChanged = true
            case 14: // Service Provider Service - TS Service Name
                cachedValue.service = strService(lmValue)
                statusChanged = true
            case 15: // Null Ratio - Ratio of Nulls in TS as percentage
                break
            case 16: // ES PID - Elementary Stream PID (repeated as pair with 17 for each ES)
                // In the status stream 16 and 17 always come in pairs, 16 is the PID and 17 is the type for that PID, e.g.
                // This means that PID 257 is of type 27 which you look up in the table to be H.264 and PID 258 is type 3 which the table says is MP3.
                // $16,257 == PID 257 is of type 27 which you look up in the table to be H.264
                // $17,27  meaning H.264
                // $16,258 == PID 258 is type 3 which the table says is MP3
                // $17,3   maeaning MP3
                // The PID numbers themselves are fairly arbitrary, will vary based on the transmitted signal and don't really mean anything in a single program multiplex.
                guard let value = Int(lmValue) else {
                    logError("LongmyndMonitor.\(#function) : invalid ES PID: \(lmValue)")
                    break
                }
                if pidTypeTupleArray.isEmpty {
                    pidTypeTupleArray.append((value, 0))
                } else {
                    if pidTypeTupleArray.count == 1 {
                        pidTypeTupleArray.append((value, 0))
                    } else {
                        if pidTypeTupleArray.count == 2 {
                            pidTypeTupleArray = []
                        }
                    }
                }
            case 17: // ES TYPE - Elementary Stream Type (repeated as pair with 16 for each ES)
                guard let value = Int(lmValue) else {
                    logError("LongmyndMonitor.\(#function) : invalid ES TYPE: \(lmValue)")
                    break
                }
                
                if pidTypeTupleArray.isEmpty {
                    break
                }
                if pidTypeTupleArray.count == 1 {
                    pidTypeTupleArray[0].1 = value
                } else {
                    if pidTypeTupleArray.count == 2 {
                        pidTypeTupleArray[1].1 = value
                        cachedValue.codecs = fetchCodecsUsing(array: pidTypeTupleArray)
                        statusChanged = true
                    }
                }
            case 18: // MODCOD - Received Modulation & Coding Rate. See MODCOD Lookup Table below
                guard let value = Int(lmValue) else {
                    logError("Longmynd.\(#function) : case 18 - invalid MODCOD: \(lmValue)")
                    break
                }
                // TODO: NOT IMPLEMENTED
                if cachedValue.state == .LockedS || cachedValue.state == .LockedS2 {
                    (cachedValue.constellation, cachedValue.fec) = strConstellationAndFecFrom(modcod: value, state: cachedValue.state)
                    statusChanged = true
                    
                // TODO: move this into strConstellationAndFecFrom()
                    cachedValue.margin = computedMargin(state: cachedValue.state, mer: cachedValue.mer, fec: cachedValue.fec, constellation: cachedValue.constellation)
                }
                break
            case 19: // Short Frames - 1 if received signal is using Short Frames, 0 otherwise (DVB-S2 only)
                break
            case 20: // Pilot Symbols - 1 if received signal is using Pilot Symbols, 0 otherwise (DVB-S2 only)
                break
            case 21: // LDPC Error Count - LDPC Corrected Errors in last frame (DVB-S2 only)
                break
            case 22: // BCH Error Count - BCH Corrected Errors in last frame (DVB-S2 only)
                break
            case 23: // BCH Uncorrected - 1 if some BCH-detected errors were not able to be corrected, 0 otherwise (DVB-S2 only)
                break
            case 24: // LNB Voltage Enabled - 1 if LNB Voltage Supply is enabled, 0 otherwise (LNB Voltage Supply requires add-on board)
                break
            case 25: // LNB H Polarisation - 1 if LNB Voltage Supply is configured for Horizontal Polarisation (18V), 0 otherwise (LNB Voltage Supply requires add-on board)
                break
            case 26: // AGC1 Gain - Gain value of AGC1 (0: Signal too weak, 65535: Signal too strong)
                guard let value = Int(lmValue) else {
                    logError("Longmynd.\(#function) : 26 has invalid \(lmValue)")
                    break
                }
                agc1 = value
                agcChanged = true
            case 27: // AGC2 Gain - Gain value of AGC2 (0: Minimum Gain, 65535: Maximum Gain)
                guard let value = Int(lmValue) else {
                    logError("Longmynd.\(#function) : 27 has invalid \(lmValue)")
                    break
                }
                agc2 = value
                agcChanged = true
            default:
                logError("Longmynd.\(#function) : got Unknown lmId \(lmId) value = \(lmValue)")
        }
        if agcChanged {
            // experimental speed up
            cachedValue.power = strPowerFrom(agc1: agc1, agc2: agc2)
            statusChanged = true
        }
        if statusChanged { } // curentl prevents a "not read" compile warning
    }
}

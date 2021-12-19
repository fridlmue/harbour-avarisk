/*
    Copyright (C) 2020 Friedrich Mütschele and other contributors
    This file is part of avaRisk.
    avaRisk is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    avaRisk is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with avaRisk. If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick 2.2
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5
import org.freedesktop.contextkit 1.0

Page {
    property string regionID
    property string regionName
    property string country
    property string macroRegion
    property string connection
    property var pm_only
    property var avaReport
    property var avaReportPM

    property bool connectionOnceUpdated: false
    property bool pm_available: false

    property var dangerLevelError: qsTr("Downloading...")

    property bool downloadSucc: false
    property bool cached: false

    property bool busy: false
    property int dangerLevel: 0
    property int dangerLevel_h: 0
    property int dangerLevel_l: 0
    property string dangerLevel_alti: ""

    /*
    property var dangerLevel: 0
    property var dangerLevel_pm: 0

    property var dangerLevel_h: 0
    property var dangerLevel_h_pm: 0
    property var dangerLevel_l: 0
    property var dangerLevel_l_pm: 0
    property var dangerLevel_alti: ""
    property var highlights: ""
    property var comment: ""
    property var structure: ""
    property var tendency: ""
    property date repDate: new Date()
    property date validFrom: new Date()
    property date validTo: new Date()
    property var provider: ""
    */

    // property var dPatterns

    property var avDanger: {
        'low': 1,
        'moderate': 2,
        'considerable': 3,
        'high': 4,
        'very_high': 5
    }

    function dangerLevelText(x) {
        if      (x === 1) {return qsTr("low")         }
        else if (x === 2) {return qsTr("moderate")    }
        else if (x === 3) {return qsTr("considerable")}
        else if (x === 4) {return qsTr("high")        }
        else if (x === 5) {return qsTr("very high")   }
        else              {return qsTr("loading") }
    }

    function getAvaProbElevText(problemElev) {
        if (problemElev.hasOwnProperty('upperBound') && problemElev.hasOwnProperty('lowerBound')) {
            return "middle"
        } else if (problemElev.hasOwnProperty('upperBound')) {
            return "below"
        } else if (problemElev.hasOwnProperty('lowerBound')) {
            return "above"
        }
        return "all"
    }

    function getElevFromString(problemElev) {
        var str_return = qsTr("entire range")
        if (problemElev.hasOwnProperty('upperBound') && problemElev.hasOwnProperty('lowerBound')) {
            str_return = qsTr("between ") + problemElev.lowerBound + " and " + problemElev.upperBound
        } else if (problemElev.hasOwnProperty('upperBound')) {
            str_return = problemElev.upperBound
        } else if (problemElev.hasOwnProperty('lowerBound')) {
            str_return = problemElev.lowerBound
        }

        if (str_return.toLowerCase().indexOf("treeline") === -1 && str_return.toLowerCase().indexOf("entire") === -1) {
          str_return += " m"
        }
        return str_return
    }

    function convertUTCDateToLocalDate(date) {
        var newDate = new Date(date.getTime() - date.getTimezoneOffset()*60*1000);
        return newDate;
    }

    ContextProperty {
       key: "Internet.NetworkState"
       onValueChanged: {
           if (connection == "" || connectionOnceUpdated) {
               connection = value
               connectionOnceUpdated = true
           }
           if (connection == "connected") {
               connectionOnceUpdated = true
           }
       }
    }

    onStatusChanged: {
        if (status == Component.Ready)
        {
            python.startDownload();
            // console.log('Start DL')
            // console.log(pm_only)
        }
    }

    SilicaFlickable {
        anchors.fill: parent
        contentHeight: column.height
        bottomMargin: Theme.paddingSmall


        BusyIndicator {
            id: busyInd
             size: BusyIndicatorSize.Large
             anchors.centerIn: parent
             running: busy
        }

        VerticalScrollDecorator{}

        PullDownMenu {
            MenuItem {
                text: qsTr("Reload")
                visible: (connection == "connected")  ? true : false
                onClicked: {
                    python.startDownload();
                }
            }
            MenuItem {
                text: qsTr("Know-How")
                onClicked: pageStack.push(Qt.resolvedUrl("Education.qml"))
            }
        }

        Column {
            spacing: Theme.paddingSmall
            id: column
            width: parent.width

            PageHeader {
                id: header
                description: qsTr("Report")
                title: regionName
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: qsTr("Offline Report - Check Validity Date")
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
                visible: (cached) ? true : false
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: qsTr("PM Report Available!")
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
                visible: (pm_available) ? true : false
            }

            //Valid time interval
            SectionHeader {
                text: qsTr("Valid time interval")
            }
            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? qsTr("Report from") + ": " + Qt.formatDateTime(convertUTCDateToLocalDate(avaReport.publicationTime), Qt.SystemLocaleShortDate) : qsTr("Report could not be requested")
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }
            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? Qt.formatDateTime(convertUTCDateToLocalDate(avaReport.validTime.startTime), Qt.SystemLocaleShortDate)  + " - " + Qt.formatDateTime(convertUTCDateToLocalDate(avaReport.validTime.endTime), Qt.SystemLocaleShortDate) : ""
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            //Danger Level
            SectionHeader {
                text: qsTr("Danger Level")
            }
            Row {
                width: parent.width
                spacing: Theme.paddingMedium

                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }

                Image {
                    source: "qrc:///res/danger-levels/level_" + dangerLevel + ".png"
                    width: Theme.iconSizeLarge
                    height: width * sourceSize.height / sourceSize.width
                }

                Label {
                    id: lblDangerLevel
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width
                    text: (downloadSucc)? dangerLevelText(dangerLevel) : dangerLevelError
                    font.pixelSize: Theme.fontSizeLarge
                    wrapMode: Text.Wrap
                }
            }

            //ElevationData
            SectionHeader {
                text: qsTr("Elevation Data")
                visible: (dangerLevel_l === dangerLevel_h) ? false : true
            }
            Row {
                width: parent.width
                spacing: Theme.paddingMedium
                visible: (dangerLevel_l === dangerLevel_h) ? false : true

                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }

                Image {
                    source: "qrc:///res/warning-pictos/levels_" + dangerLevel_l + "_" + dangerLevel_h + ".png"
                    width: Theme.iconSizeLarge
                    height: width * sourceSize.height / sourceSize.width
                }

                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    text: getElevFromString(avaReport.dangerRatings[0].elevation)
                    font.pixelSize: Theme.fontSizeMedium
                    wrapMode: Text.Wrap
                }
            }

            //Avalanche prone locations
            SectionHeader {
                text: qsTr("Avalanche prone locations")
                visible: (avaReport.avalancheProblems.length == 0) ? true : false
            }
            Row {
                width: parent.width
                spacing: Theme.paddingMedium
                visible: (avaReport.avalancheProblems.length == 0) ? true : false
                anchors {
                            left:     parent.left
                            right:    parent.right
                            margins:  Theme.paddingMedium
                        }
                Rectangle {
                     color: "white"
                     width: Theme.iconSizeLarge
                     height:Theme.iconSizeLarge
                     Repeater {
                         model: avaReport.dangerRatings[0]['aspect']
                         Image {
                             property int aspectIndex: model.index
                             source: "qrc:///res/expositions/exposition_" + avaReport.dangerRatings[0]['aspect'][aspectIndex].toLowerCase()  + ".png"
                             width:  Theme.iconSizeLarge
                             height: Theme.iconSizeLarge
                         }
                     }

                     Image {
                        source: "qrc:///res/expositions/exposition_bg.png"
                        width:  Theme.iconSizeLarge
                        height: Theme.iconSizeLarge
                     }
                }

                Rectangle {
                     visible: (avaReport.dangerRatings[0].elevation.hasOwnProperty('upperBound') || avaReport.dangerRatings[0].elevation.hasOwnProperty('lowerBound')) ? true : false
                     color: "white"
                     width: Theme.iconSizeLarge
                     height:Theme.iconSizeLarge
                     Image {
                         source: "qrc:///res/warning-pictos/levels_above.png"
                         width:  Theme.iconSizeLarge
                         height: Theme.iconSizeLarge
                     }
                }

                IconButton {
                    id: upDownInd
                    visible: (avaReport.dangerRatings[0].elevation.hasOwnProperty('upperBound') || avaReport.dangerRatings[0].elevation.hasOwnProperty('lowerBound')) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    icon.source: "image://theme/icon-s-unfocused-down"
                    transform: Rotation {
                        origin.x: upDownInd.width/2;
                        origin.y: upDownInd.height/2;
                        angle: 180
                    }

                }

                Label {
                    visible: (avaReport.dangerRatings[0].elevation.hasOwnProperty('upperBound') || avaReport.dangerRatings[0].elevation.hasOwnProperty('lowerBound')) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    text: getElevFromString(avaReport.dangerRatings[0].elevation)
                    font.pixelSize: Theme.fontSizeMedium
                    wrapMode: Text.Wrap
                }
            }

            //Avalanche Problems
            SectionHeader {
                text: qsTr("Avalanche Problem")
                visible: (avaReport.avalancheProblems.length > 0) ? true : false
            }
            Repeater {
                model: avaReport.avalancheProblems
                Row {
                    width: parent.width
                    spacing: Theme.paddingMedium
                    property int sectionIndex: model.index
                    anchors {
                                left:     parent.left
                                right:    parent.right
                                margins:  Theme.paddingMedium
                            }
                    Image {
                        source: "qrc:///res/avalanche-situations/" + avaReport.avalancheProblems[sectionIndex]['problemType'] + ".png"
                        width:  Theme.iconSizeLarge
                        height: Theme.iconSizeLarge
                    }
                    Rectangle {
                         color: "white"
                         width: Theme.iconSizeLarge
                         height:Theme.iconSizeLarge
                         Repeater {
                             model: avaReport.avalancheProblems[sectionIndex].dangerRating.aspect
                             Image {
                                 property int aspectIndex: model.index
                                 source: "qrc:///res/expositions/exposition_" + avaReport.avalancheProblems[sectionIndex].dangerRating.aspect[aspectIndex].toLowerCase()  + ".png"
                                 width:  Theme.iconSizeLarge
                                 height: Theme.iconSizeLarge
                             }
                         }
                         Image {
                            source: "qrc:///res/expositions/exposition_bg.png"
                            width:  Theme.iconSizeLarge
                            height: Theme.iconSizeLarge
                         }
                    }

                    Rectangle {
                         visible: (avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('upperBound') || avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('lowerBound')) ? true : false
                         color: "white"
                         width: Theme.iconSizeLarge
                         height:Theme.iconSizeLarge
                         Image {
                             source: "qrc:///res/warning-pictos/levels_" + getAvaProbElevText(avaReport.avalancheProblems[sectionIndex].dangerRating.elevation) + ".png"
                             width:  Theme.iconSizeLarge
                             height: Theme.iconSizeLarge
                         }
                    }

                    IconButton {
                        id: upDownInd2
                        visible: (avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('upperBound') || avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('lowerBound')) ? true : false
                        anchors.verticalCenter: parent.verticalCenter
                        icon.source: "image://theme/icon-s-unfocused-down"
                        transform: Rotation {
                            origin.x: upDownInd2.width/2;
                            origin.y: upDownInd2.height/2;
                            angle: (avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('lowerBound')) ? 180 : 0
                        }

                    }

                    Label {
                        visible: (avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('upperBound') || avaReport.avalancheProblems[sectionIndex].dangerRating.elevation.hasOwnProperty('lowerBound')) ? true : false
                        anchors.verticalCenter: parent.verticalCenter
                        text: getElevFromString(avaReport.avalancheProblems[sectionIndex].dangerRating.elevation)
                        font.pixelSize: Theme.fontSizeMedium
                        wrapMode: Text.Wrap
                    }

                    Label {
                        width: parent.width - 2 * Theme.iconSizeLarge
                        visible: (avaReport.avalancheProblems[sectionIndex].hasOwnProperty('comment')) ? true : false
                        text: avaReport.avalancheProblems[sectionIndex].comment
                        font.pixelSize: Theme.fontSizeSmall
                        wrapMode: Text.Wrap
                    }
                }
            }

            //Highlights
            Label {
                visible: (avaReport.hasOwnProperty('highlights')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.highlights
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
            }

            //Danger Description
            SectionHeader {
                text: qsTr("Danger Description")
            }
            Label {
                visible: (avaReport.hasOwnProperty('avalancheActivityHighlights')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.avalancheActivityHighlights
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
            }
            Label {
                visible: (avaReport.hasOwnProperty('avalancheActivityComment')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.avalancheActivityComment
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            //Snowpack Description
            SectionHeader {
                visible: (avaReport.hasOwnProperty('snowpackStructureHighlights') || avaReport.hasOwnProperty('snowpackStructureComment')) ? true : false
                text: qsTr("Snowpack Description")
            }
            Label {
                visible: (avaReport.hasOwnProperty('snowpackStructureHighlights')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.snowpackStructureHighlights
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
            }
            Label {
                visible: (avaReport.hasOwnProperty('snowpackStructureComment')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.snowpackStructureComment
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            //TravelAdvisory Description
            SectionHeader {
                visible: (avaReport.hasOwnProperty('travelAdvisoryHighlights') || avaReport.hasOwnProperty('travelAdvisoryComment')) ? true : false
                text: qsTr("Travel Advisory")
            }
            Label {
                visible: (avaReport.hasOwnProperty('travelAdvisoryHighlights')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.travelAdvisoryHighlights
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
            }
            Label {
                visible: (avaReport.hasOwnProperty('travelAdvisoryComment')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.travelAdvisoryComment
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            //wx Forecast
            SectionHeader {
                visible: (avaReport.hasOwnProperty('wxSynopsisHighlights') || avaReport.hasOwnProperty('wxSynopsisComment')) ? true : false
                text: qsTr("Weather Forecast")
            }
            Label {
                visible: (avaReport.hasOwnProperty('wxSynopsisHighlights')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.wxSynopsisHighlights
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
            }
            Label {
                visible: (avaReport.hasOwnProperty('wxSynopsisComment')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.wxSynopsisComment
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            //tendency
            SectionHeader {
                visible: (avaReport.tendency.hasOwnProperty('tendencyComment')) ? true : false
                text: qsTr("Tendency")
            }
            Label {
                visible: (avaReport.tendency.hasOwnProperty('tendencyComment')) ? true : false
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                text: avaReport.tendency.tendencyComment
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            LinkedLabel {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingMedium
                        }
                width: parent.width
                plainText: provider
                font.pixelSize: Theme.fontSizeExtraSmall
                wrapMode: Text.Wrap
            }
        }
    }

    Python {
        id: python

        Component.onCompleted: {
                addImportPath(Qt.resolvedUrl('.'));

                setHandler('AvaReport', function(val) {
                    var avaReport_str = val;
                    var avaReports = JSON.parse(avaReport_str);

                    avaReport = avaReports[0]

                    if (avaReports.length > 1) {
                        if (avaReports[1] !== '') {
                            pm_available = true
                            avaReportPM = avaReports[1]
                        }
                    }
                    // console.log("got report: " + val)
                });
                setHandler('provider', function(val) {
                    provider = val;
                });
                setHandler('cached', function(val) {
                    cached = val;
                });
                setHandler('cached_pm', function(val) {
                    cached_pm = val;
                });
                setHandler('error', function(val) {
                    console.log("Error: " + val);
                });
                setHandler('finished', function(val) {
                    // console.log("should be done: " + val)
                    if (val === true) {
                        coverExchange.country = country
                        coverExchange.region = macroRegion
                        coverExchange.microRegion = regionName
                        coverExchange.levelText = qsTr("LEVEL")

                        for (var elem in avaReport.dangerRatings) {
                            if (avaReport.dangerRatings[elem].elevation.hasOwnProperty('lowerBound')) {
                                dangerLevel_h = avDanger[avaReport.dangerRatings[elem]['mainValue']];
                                dangerLevel_alti = avaReport.dangerRatings[elem].elevation.lowerBound;

                            } else if (avaReport.dangerRatings[elem].elevation.hasOwnProperty('upperBound')) {
                                dangerLevel_l = avDanger[avaReport.dangerRatings[elem]['mainValue']];
                            } else {
                                dangerLevel_h = dangerLevel_l = avDanger[avaReport.dangerRatings[elem]['mainValue']];
                            }
                        }

                        if (dangerLevel_l == 0 || dangerLevel_h == 0) dangerLevel_l = dangerLevel_h = Math.max(dangerLevel_h, dangerLevel_l);

                        dangerLevel = Math.max(dangerLevel_h, dangerLevel_l)

                        coverExchange.dangerMain = dangerLevel
                        coverExchange.dangerH = dangerLevel_h
                        coverExchange.dangerL = dangerLevel_l
                        coverExchange.validHeight = getElevFromString(avaReport.dangerRatings[0].elevation)

                    }
                    downloadSucc = val

                    // If Busy == false, error message was set by startDownload()
                    if (downloadSucc == false && busy == true) {
                        dangerLevelError = qsTr("Maybe no report is provided for this region at the moment.")
                    }

                    busy = false;
                });

                importModule('pyCore', function () {});
        }

        function startDownload() {
            if (connection == "connected" && pm_only == false) {
                busy = true;
                call('pyCore.downloader.download', [regionID, Qt.locale().name, StandardPaths.cache], function() {});
            } else {
                busy = false;
                dangerLevelError = qsTr("No Internet connection and no report cached for this region")
                call('pyCore.downloader.cached', [regionID, Qt.locale().name, StandardPaths.cache], function() {});

            }
        }

        onError: {
            // when an exception is raised, this error handler will be called
            console.log('python error: ' + traceback);
        }

        onReceived: {
            // asychronous messages from Python arrive here
            // in Python, this can be accomplished via pyotherside.send()
            console.log('got message from python: ' + data);
        }
    }

    Image {
        id: bgImg
        asynchronous: true
        fillMode: Image.PreserveAspectFit
        opacity: 0.05
        source: "qrc:///res/bg_" + ( Theme.colorScheme ? "light" : "dark" ) + "_page.svg"
        anchors {
            left: parent.left
            bottom: parent.bottom
        }
    }
}

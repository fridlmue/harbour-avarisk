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

    property var dangerLevel: 0

    property var dangerLevel_h: 0
    property var dangerLevel_l: 0
    property var dangerLevel_alti: ""
    property var highlights: ""
    property var comment: ""
    property var structure: ""
    property var tendency: ""
    property date repDate: new Date()
    property date validFrom: new Date()
    property date validTo: new Date()
    property var provider: ""
    property var downloadSucc: false
    property var cached: false

    property bool busy: false

    property var dPatterns

    function dangerLevelText(x) {
        if      (x === 1) {return qsTr("low")         }
        else if (x === 2) {return qsTr("moderate")    }
        else if (x === 3) {return qsTr("considerable")}
        else if (x === 4) {return qsTr("high")        }
        else if (x === 5) {return qsTr("very high")   }
        else              {return qsTr("loading") }
    }

    function getAvaDangElevText(validElev) {
        if (validElev) {
            if (validElev.indexOf('>') > -1) {
                 return "above"
            }
            else if (validElev.indexOf('<') > -1) {
                 return "below"
            }
        }
        return "all"
    }

    function getElevFromString(validElev) {
        if (validElev) {
            if (validElev.indexOf('Treeline') > -1) {
                return qsTr("treeline")
            }

            var elev = validElev
            if ((validElev.indexOf('<') > -1) || (validElev.indexOf('>') > -1)) {
                elev = validElev.substring(1)
                return elev + " m"
            }
        }

        return qsTr("entire range")

    }

    /*function convertUTCDateToLocalDate(date) {
        var newDate = new Date(date.getTime() - date.getTimezoneOffset()*60*1000);
        return newDate;
    }*/

    function parseAvaReportJSON(avaReport) {
        for (var elem in avaReport.danger_main) {
            if (avaReport.danger_main[elem]['main_value'] > dangerLevel) {
                dangerLevel = avaReport.danger_main[elem]['main_value']
            }
        }

        // console.log("Plot Report: " + avaReport.report_id)

        dangerLevel_h = avaReport.danger_main[0]['main_value'];
        if (avaReport.danger_main.length > 1) {
            dangerLevel_l = avaReport.danger_main[1]['main_value'];
            dangerLevel_alti = avaReport.danger_main[1]['valid_elevation'];
        }
        else {
            dangerLevel_l = avaReport.danger_main[0]['main_value'];
        }

        validFrom = new Date(avaReport.validity_begin)
        validTo = new Date(avaReport.validity_end)
        repDate = new Date(avaReport.rep_date)

        dPatterns = avaReport.problem_list

        for (var elem in avaReport.report_texts) {
            if (avaReport.report_texts[elem].text_type === 'activity_hl') {
                highlights = avaReport.report_texts[elem].text_content;
            }
            if (avaReport.report_texts[elem].text_type === 'activity_com') {
                comment = avaReport.report_texts[elem].text_content;
            }
            if (avaReport.report_texts[elem].text_type === 'snow_struct_com') {
                structure = avaReport.report_texts[elem].text_content;
            }
            if (avaReport.report_texts[elem].text_type === 'tendency_com') {
                tendency = avaReport.report_texts[elem].text_content;
            }
        }
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
        if ((status == Component.Ready) && (pm_only == false))
        {
            python.startDownload();
            // console.log('Start DL')
            // console.log(pm_only)
        }
        if ((status == Component.Ready) && pm_only)
        {
            parseAvaReportJSON(avaReport);
            // console.log('Load from avaReport')
            // console.log(pm_only)
            downloadSucc = true
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
                visible: ((connection == "connected") && (pm_only == false)) ? true : false
                onClicked: {
                    python.startDownload();
                }
            }
            MenuItem {
                text: qsTr("Know-How")
                onClicked: pageStack.push(Qt.resolvedUrl("Education.qml"))
            }
            MenuItem {
                text: qsTr("PM Report")
                visible: pm_available
                onClicked: {
                    onClicked: pageStack.push(Qt.resolvedUrl("DangerPage.qml"), {"regionID": regionID, "regionName": regionName, "country": country, "macroRegion": macroRegion, "connection": connection, "pm_only": true, "avaReport": avaReportPM})
                }
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

            SectionHeader {
                text: qsTr("Valid time interval")
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? qsTr("Report from") + ": " + Qt.formatDateTime(repDate, Qt.SystemLocaleShortDate) : qsTr("Report could not be requested")
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? Qt.formatDateTime(validFrom, Qt.SystemLocaleShortDate)  + " - " + Qt.formatDateTime(validTo, Qt.SystemLocaleShortDate) : ""  //in UTC - > Wrong!
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }


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
                    text: (downloadSucc)? qsTr("Level") + " " + dangerLevel + " - " + dangerLevelText(dangerLevel) : dangerLevelError
                    font.pixelSize: Theme.fontSizeLarge
                    wrapMode: Text.Wrap
                }
            }

            SectionHeader {
                text: qsTr("Elevation Data")
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
                    source: "qrc:///res/warning-pictos/levels_" + dangerLevel_l + "_" + dangerLevel_h + ".png"
                    width: Theme.iconSizeLarge
                    height: width * sourceSize.height / sourceSize.width
                }

                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    text: (dangerLevel_l === dangerLevel_h) ? qsTr("entire range") : getElevFromString(dangerLevel_alti)
                    font.pixelSize: Theme.fontSizeMedium
                    wrapMode: Text.Wrap
                }
            }

            ExpandingSectionGroup {

                ExpandingSection {
                    title: qsTr("Avalanche Problem")

                    content.sourceComponent:
                        Column {
                            spacing: Theme.paddingMedium
                            Repeater {
                                model: dPatterns
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
                                        source: "qrc:///res/avalanche-situations/" + dPatterns[sectionIndex]['problem_type'].replace(' ', '_') + ".png"
                                        width:  Theme.iconSizeLarge
                                        height: Theme.iconSizeLarge
                                    }
                                    Rectangle {
                                         color: "white"
                                         width: Theme.iconSizeLarge
                                         height:Theme.iconSizeLarge
                                         Repeater {
                                             model: dPatterns[sectionIndex]['aspect']
                                             Image {
                                                 property int aspectIndex: model.index
                                                 source: "qrc:///res/expositions/exposition_" + dPatterns[sectionIndex]['aspect'][aspectIndex].toLowerCase()  + ".png"
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

                                    //Middle is not yet covered
                                    Rectangle {
                                         color: "white"
                                         width: Theme.iconSizeLarge
                                         height:Theme.iconSizeLarge
                                         Image {
                                             source: "qrc:///res/warning-pictos/levels_" + getAvaDangElevText(dPatterns[sectionIndex]['valid_elevation']) + ".png"
                                             width:  Theme.iconSizeLarge
                                             height: Theme.iconSizeLarge
                                         }
                                    }

                                    IconButton {
                                        id: upDownInd
                                        anchors.verticalCenter: parent.verticalCenter
                                        icon.source: (getAvaDangElevText(dPatterns[sectionIndex]['valid_elevation']) === "all") ? "" : "image://theme/icon-s-unfocused-down"
                                        transform: Rotation {
                                            origin.x: upDownInd.width/2;
                                            origin.y: upDownInd.height/2;
                                            angle: (dPatterns[sectionIndex]['valid_elevation'].indexOf('>') > -1) ? 180 : 0
                                        }

                                    }

                                    Label {
                                        anchors.verticalCenter: parent.verticalCenter
                                        text: getElevFromString(dPatterns[sectionIndex]['valid_elevation'])
                                        font.pixelSize: Theme.fontSizeMedium
                                        wrapMode: Text.Wrap
                                    }


                                }
                            }
                        }
                }

                ExpandingSection {
                    title: qsTr("Danger Description")

                    content.sourceComponent: Column {
                        width: parent.width
                        Label {
                            anchors {
                                        left: parent.left
                                        right: parent.right
                                        margins: Theme.paddingMedium
                                    }
                            width: parent.width
                            text: highlights
                            font.pixelSize: Theme.fontSizeMedium
                            wrapMode: Text.Wrap
                        }
                        Label {
                            anchors {
                                        left: parent.left
                                        right: parent.right
                                        margins: Theme.paddingMedium
                                    }
                            width: parent.width
                            text: comment
                            font.pixelSize: Theme.fontSizeSmall
                            wrapMode: Text.Wrap
                        }
                    }
                }

                ExpandingSection {
                    title: qsTr("Snowpack Description")

                    content.sourceComponent: Column {
                        width: parent.width
                        Label {
                            anchors {
                                        left: parent.left
                                        right: parent.right
                                        margins: Theme.paddingMedium
                                    }
                            width: parent.width
                            text: structure
                            font.pixelSize: Theme.fontSizeSmall
                            wrapMode: Text.Wrap
                        }
                    }
                }

                ExpandingSection {
                    title: qsTr("Tendency")

                    content.sourceComponent: Column {
                        width: parent.width
                        Label {
                            anchors {
                                        left: parent.left
                                        right: parent.right
                                        margins: Theme.paddingMedium
                                    }
                            width: parent.width
                            text: tendency
                            font.pixelSize: Theme.fontSizeSmall
                            wrapMode: Text.Wrap
                        }
                    }
                }
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

                    parseAvaReportJSON(avaReports[0])

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
                    console.log("Error: " + val)
                });
                setHandler('finished', function(val) {
                    // console.log("should be done: " + val)
                    if (val === true) {
                        coverExchange.country = country
                        coverExchange.region = macroRegion
                        coverExchange.microRegion = regionName
                        coverExchange.levelText = qsTr("LEVEL")
                        coverExchange.dangerMain = dangerLevel
                        coverExchange.dangerH = dangerLevel_h
                        coverExchange.dangerL = dangerLevel_l
                        coverExchange.validHeight = (dangerLevel_l === dangerLevel_h) ? qsTr("entire range") : getElevFromString(dangerLevel_alti)
                    }
                    downloadSucc = val

                    // If Busy == false, error message was set by startDownload()
                    if (downloadSucc == false && busy == True) {
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

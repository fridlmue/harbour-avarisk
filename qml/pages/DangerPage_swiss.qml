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

Page {
    property string regionID
    property string regionName
    property string country
    property string macroRegion

    property var dangerLevel: 0

    property var repDate: ""
    property var validFrom: ""
    property var validTo: ""
    property var provider: ""
    property var proneLocationsText: ""
    property var proneLocationsImg:""
    property var htmlLocal: ""
    property var htmlWeatherSnow: ""

    property var downloadSucc: false

    property bool busy: false

    function dangerLevelText(x) {
        if      (x === '1') {return qsTr("low")         }
        else if (x === '2') {return qsTr("moderate")    }
        else if (x === '3') {return qsTr("considerable")}
        else if (x === '4') {return qsTr("high")        }
        else if (x === '5') {return qsTr("very high")   }
        else              {return qsTr("loading") }
    }

    /*function getAvaDangElevText(validElev) {
        if (validElev.indexOf('Hi') > -1) {
             return "above"
        }
        else if (validElev.indexOf('Lw') > -1) {
             return "below"
        }
        else {
             return "all"
        }
    }*/

    onStatusChanged: {
        if (status == Component.Ready)
        {
            python.startDownload();
            busy = true;
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
                onClicked: {
                    python.startDownload();
                    busy = true;
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

            SectionHeader {
                text: (qsTr("Valid time interval") + " CET")
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? qsTr("Report from") + ": " + repDate : qsTr("Report could not be requested") // in UTC -> wrong!
                font.pixelSize: Theme.fontSizeSmall
                wrapMode: Text.Wrap
            }

            Label {
                anchors {
                            left: parent.left
                            right: parent.right
                            margins: Theme.paddingLarge
                        }
                text: (downloadSucc)? validFrom  + " - " + validTo : ""  //in UTC - > Wrong!
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
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width
                    text: (downloadSucc)? qsTr("Level") + " " + dangerLevel + " - " + dangerLevelText(dangerLevel) : qsTr("Maybe no report is provided for this region at the moment.")
                    font.pixelSize: Theme.fontSizeLarge
                    wrapMode: Text.Wrap
                }
            }
            SectionHeader {
                text: qsTr("Avalanche prone locations")
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
                    source: "data:image/png;base64," + proneLocationsImg
                    // width: Theme.iconSizeLarge
                    // height: width * sourceSize.height / sourceSize.width
                    height: Theme.iconSizeLarge
                    width: height * sourceSize.width / sourceSize.height
                }

                Label {
                    anchors.verticalCenter: parent.verticalCenter
                    width: parent.width - Theme.iconSizeLarge - 3 * Theme.paddingLarge
                    text: proneLocationsText
                    font.pixelSize: Theme.fontSizeSmall
                    wrapMode: Text.Wrap
                }
            }

            ExpandingSection {
                title: qsTr("Local Report")

                content.sourceComponent:
                    Column {
                       width: parent.width
                       Label {
                           textFormat: Text.RichText
                           anchors {
                                       left: parent.left
                                       right: parent.right
                                       margins: Theme.paddingMedium
                                   }
                           width: parent.width
                           text: htmlLocal
                           wrapMode: Text.Wrap
                       }
                }
            }

           ExpandingSection {
               title: qsTr("Snow and Weather Data")

               content.sourceComponent:
                   Column {
                      width: parent.width
                      Label {
                          textFormat: Text.RichText
                          anchors {
                                      left: parent.left
                                      right: parent.right
                                      margins: Theme.paddingMedium
                                  }
                          width: parent.width
                          text: htmlWeatherSnow
                          // font.pixelSize: Theme.fontSizeSmall
                          wrapMode: Text.Wrap
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

                setHandler('dangerMain', function(val) {
                    dangerLevel = val;
                });


                setHandler('proneLocationsText', function(val) {
                    proneLocationsText = val;
                });
                setHandler('proneLocationsImg', function(val) {
                    proneLocationsImg = val;
                });
                setHandler('htmlLocal', function(val) {
                    htmlLocal = val;
                });
                setHandler('htmlWeatherSnow', function(val) {
                    htmlWeatherSnow = val
                });            
                setHandler('timeBegin', function(val) {
                    validFrom = val
                });
                setHandler('timeEnd', function(val) {
                    validTo = val
                });
                setHandler('repDate', function(val) {
                    repDate = val
                });
                setHandler('provider', function(val) {
                    provider = val;
                });

                setHandler('finished', function(val) {
                    if (val === true) {
                        coverExchange.country = country
                        coverExchange.region = macroRegion
                        coverExchange.microRegion = regionName
                        coverExchange.levelText = qsTr("LEVEL")
                        coverExchange.dangerMain = dangerLevel
                    }
                    downloadSucc = val

                    busy = false;
                });

                importModule('pyAvaCoreSwiss', function () {});
        }

        function startDownload() {
            call('pyAvaCoreSwiss.downloader.download', [regionID, Qt.locale().name], function() {});
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

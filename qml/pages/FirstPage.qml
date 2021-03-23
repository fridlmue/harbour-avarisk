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
import "RegionList"

Page {

    SilicaFlickable {

        anchors.fill: parent
        contentHeight: column.height
        bottomMargin: Theme.paddingSmall

        VerticalScrollDecorator {}

        PullDownMenu {
            MenuItem {
                text: qsTr("About")
                onClicked: pageStack.push(Qt.resolvedUrl("AboutPage.qml"))
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
                title: qsTr("Show Bulletin for")
            }

            ExpandingSectionGroup {

                ExpandingSection {
                    width: parent.width

                    title: qsTr("Austria")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndCarinthia
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCarinthia, "country": qsTr("Austria"), "macroRegion": qsTr("Carinthia")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Carinthia")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCarinthia.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndNiederoestereich
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListNiederoestereich, "country": qsTr("Austria"), "macroRegion": qsTr("Niederösterreich")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Niederösterreich")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndNiederoestereich.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndOberoesterreich
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListOberoestereich, "country": qsTr("Austria"), "macroRegion": qsTr("Oberösterreich")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Oberösterreich")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndOberoesterreich.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndSalzburg
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListSalzburg, "country": qsTr("Austria"), "macroRegion": qsTr("Salzburg")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Salzburg")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndSalzburg.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndSteiermark
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListSteiermark, "country": qsTr("Austria"), "macroRegion": qsTr("Styria")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Styria")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndSteiermark.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                            id: bgndTyrol
                            onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListTyrol, "country": qsTr("Austria"), "macroRegion": qsTr("Tyrol")})

                            Label {
                                x: Theme.horizontalPageMargin
                                text: qsTr("Tyrol")
                                anchors.verticalCenter: parent.verticalCenter
                                color: bgndTyrol.highlighted ? Theme.highlightColor : Theme.primaryColor
                            }
                         }

                        BackgroundItem {
                             id: bgndVorarlberg
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListVorarlberg, "country": qsTr("Austria"), "macroRegion": qsTr("Vorarlberg")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Vorarlberg")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndVorarlberg.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                    }
                }

                ExpandingSection {
                    width: parent.width

                    title: qsTr("France")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndAlpesDuNord
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListFrAlpesDuNord, "country": qsTr("France"), "macroRegion": qsTr("Alpes du Nord")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Alpes du Nord")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndAlpesDuNord.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndAlpesDuSud
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListFrAlpesDuSud, "country": qsTr("France"), "macroRegion": qsTr("Alpes du Sud")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Alpes du Sud")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndAlpesDuSud.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndPyrenees
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListFrPyrenees, "country": qsTr("France"), "macroRegion": qsTr("Pyrenees")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Pyrenees")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndPyrenees.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndCorse
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListFrCorse, "country": qsTr("France"), "macroRegion": qsTr("Corse")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Corse")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCorse.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                    }
                }

                ExpandingSection {
                    width: parent.width

                    title: qsTr("Germany")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndBavaria
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListBavaria, "country": qsTr("Germany"), "macroRegion": qsTr("Bavaria")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Bavaria")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndBavaria.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                    }
                }

                ExpandingSection {
                    width: parent.width

                    title: qsTr("Italy")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndSTyrol
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListSTyrol, "country": qsTr("Italy"), "macroRegion": qsTr("South Tyrol")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("South Tyrol")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndSTyrol.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }

                        BackgroundItem {
                             id: bgndTrentino
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListTrentino, "country": qsTr("Italy"), "macroRegion": qsTr("Trentino")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Trentino")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndTrentino.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
/*
                        BackgroundItem {
                             id: bgndVeneto
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListVeneto, "country": qsTr("Italy"), "macroRegion": qsTr("Veneto")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Veneto")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndTrentino.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                         */
                    }
                }

                ExpandingSection {

                    width: parent.width

                    title: qsTr("Spain")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndAran
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListAran, "country": qsTr("Spain"), "macroRegion": qsTr("Val d'Aran")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Val d'Aran")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndAran.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                    }
                }

                ExpandingSection {

                    width: parent.width

                    title: qsTr("Switzerland")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndCHBEA
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHBEA, "country": qsTr("Switzerland"), "macroRegion": qsTr("Bernese and Fribourg Alps")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Bernese and Fribourg Alps")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHBEA.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHZAN
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHZAN, "country": qsTr("Switzerland"), "macroRegion": qsTr("central part of the Northern flank of the Alps")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("central part of the Northern flank of the Alps")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHZAN.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHOAN
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHOAN, "country": qsTr("Switzerland"), "macroRegion": qsTr("Eastern part of the Northern flank")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Eastern part of the Northern flank")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHOAN.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHUWW
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHUWW, "country": qsTr("Switzerland"), "macroRegion": qsTr("lower Valais and Vaud Alps")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("lower Valais and Vaud Alps")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHUWW.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHOW
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHOW, "country": qsTr("Switzerland"), "macroRegion": qsTr("Upper Valais")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Upper Valais")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHOW.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHNB
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHNB, "country": qsTr("Switzerland"), "macroRegion": qsTr("northern and central Grisons")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("northern and central Grisons")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHNB.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHTES
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHTES, "country": qsTr("Switzerland"), "macroRegion": qsTr("Ticino and Moesano")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Ticino and Moesano")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHTES.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHENG
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHENG, "country": qsTr("Switzerland"), "macroRegion": qsTr("Engadine and southern valleys")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Engadine and southern valleys")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHENG.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHJUR
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHJUR, "country": qsTr("Switzerland"), "macroRegion": qsTr("Jura")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Jura")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHJUR.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                        BackgroundItem {
                             id: bgndCHMittelland
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListCHMittelland, "country": qsTr("Switzerland"), "macroRegion": qsTr("Mittelland")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Mittelland")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndCHMittelland.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                    }

                }

                ExpandingSection {

                    width: parent.width

                    title: qsTr("Liechtenstein")

                    content.sourceComponent: Column {
                        width: parent.width
                        BackgroundItem {
                             id: bgndLiechtenstein
                             onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": RegionList.regionListLiechtenstein, "country": qsTr("Liechtenstein"), "macroRegion": qsTr("Lichtenstein")})

                             Label {
                                 x: Theme.horizontalPageMargin
                                 text: qsTr("Liechtenstein")
                                 anchors.verticalCenter: parent.verticalCenter
                                 color: bgndLiechtenstein.highlighted ? Theme.highlightColor : Theme.primaryColor
                             }
                         }
                    }
                }
            }

        }
    }
    Image {
        id: bgImg
        asynchronous: true
        fillMode: Image.PreserveAspectFit
        opacity: 0.20
        source: "qrc:///res/bg_" + ( Theme.colorScheme ? "light" : "dark" ) + "_page.svg"
        anchors {
            left: parent.left
            bottom: parent.bottom
        }
    }
}

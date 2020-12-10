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

Page {
    property ListModel regionListTyrol: ListModel{
        ListElement { region: qsTr("Allgäuer Alpen");                               RegionID: "AT-07-01"}
        ListElement { region: qsTr("Östl. Lechtaler A. - Ammergebirge");            RegionID: "AT-07-02"}
        ListElement { region: qsTr("Mieminger Gebirge");                            RegionID: "AT-07-03"}
        ListElement { region: qsTr("Karwendel");                                    RegionID: "AT-07-04"}
        ListElement { region: qsTr("Brandenberger Alpen");                          RegionID: "AT-07-05"}
        ListElement { region: qsTr("Wilder Kaiser - Waidringer Alpen");             RegionID: "AT-07-06"}
        ListElement { region: qsTr("Wstl. Lechtaler Alpen");                        RegionID: "AT-07-07"}
        ListElement { region: qsTr("Zentrale Lechtaler Alpen");                     RegionID: "AT-07-08"}
        ListElement { region: qsTr("Grieskogelgruppe");                             RegionID: "AT-07-09"}
        ListElement { region: qsTr("Westl. Verwallgruppe");                         RegionID: "AT-07-10"}
        ListElement { region: qsTr("Östl. Verwallgruppe");                          RegionID: "AT-07-11"}
        ListElement { region: qsTr("Silvretta");                                    RegionID: "AT-07-12"}
        ListElement { region: qsTr("Samnaungruppe");                                RegionID: "AT-07-13"}
        ListElement { region: qsTr("Nördl. Ötztaler- und Stubaier Alpen");          RegionID: "AT-07-14"}
        ListElement { region: qsTr("Wstl. Tuxer Alpen");                            RegionID: "AT-07-15"}
        ListElement { region: qsTr("Östl. Tuxer Alpen");                            RegionID: "AT-07-16"}
        ListElement { region: qsTr("Wstl. Kitzbühler Alpen");                       RegionID: "AT-07-17"}
        ListElement { region: qsTr("Östl. Kitzbühler Alpen");                       RegionID: "AT-07-18"}
        ListElement { region: qsTr("Glockturmgruppe");                              RegionID: "AT-07-19"}
        ListElement { region: qsTr("Weißkogelgruppe");                              RegionID: "AT-07-20"}
        ListElement { region: qsTr("Gurgler Gruppe");                               RegionID: "AT-07-21"}
        ListElement { region: qsTr("Zentrale Stubaier Alpen");                      RegionID: "AT-07-22"}
        ListElement { region: qsTr("Nördl. Zillertaler Alpen");                     RegionID: "AT-07-23"}
        ListElement { region: qsTr("Venedigergruppe");                              RegionID: "AT-07-24"}
        ListElement { region: qsTr("Östl. Rieserfernergruppe");                     RegionID: "AT-07-25"}
        ListElement { region: qsTr("Glocknergruppe");                               RegionID: "AT-07-26"}
        ListElement { region: qsTr("Östl. Deferegger Alpen");                       RegionID: "AT-07-27"}
        ListElement { region: qsTr("Schobergruppe");                                RegionID: "AT-07-28"}
        ListElement { region: qsTr("Lienzer Dolomiten");                            RegionID: "AT-07-29"}
    }

    property ListModel regionListSTyrol: ListModel{
        ListElement { region: qsTr("Münstertaler Alpen");                           RegionID: "IT-32-BZ-01"}
        ListElement { region: qsTr("Langtaufers");                                  RegionID: "IT-32-BZ-02"}
        ListElement { region: qsTr("Schnalser Kamm");                               RegionID: "IT-32-BZ-03"}
        ListElement { region: qsTr("Südl. Stubaier Alpen");                         RegionID: "IT-32-BZ-04"}
        ListElement { region: qsTr("S Zillertaler A. und Hohe Tauern");             RegionID: "IT-32-BZ-05"}
        ListElement { region: qsTr("Saldurn-Mastaun Kamm");                         RegionID: "IT-32-BZ-06"}
        ListElement { region: qsTr("Texelgruppe");                                  RegionID: "IT-32-BZ-07"}
        ListElement { region: qsTr("Sarntaler Alpen");                              RegionID: "IT-32-BZ-08"}
        ListElement { region: qsTr("Wstl. Pfunderer Berge ");                       RegionID: "IT-32-BZ-09"}
        ListElement { region: qsTr("Östl. Pfunderer Berge");                        RegionID: "IT-32-BZ-10"}
        ListElement { region: qsTr("Durreckgruppe");                                RegionID: "IT-32-BZ-11"}
        ListElement { region: qsTr("Wstl. Rieserfernergruppe");                     RegionID: "IT-32-BZ-12"}
        ListElement { region: qsTr("Wstl. Deferegger Alpen");                       RegionID: "IT-32-BZ-13"}
        ListElement { region: qsTr("Ortlergruppe");                                 RegionID: "IT-32-BZ-14"}
        ListElement { region: qsTr("Ultental");                                     RegionID: "IT-32-BZ-15"}
        ListElement { region: qsTr("Östl. Nonsberger Alpen");                       RegionID: "IT-32-BZ-16"}
        ListElement { region: qsTr("Nördl. Fleimstaler Alpen");                     RegionID: "IT-32-BZ-17"}
        ListElement { region: qsTr("Groedner Dolomiten");                           RegionID: "IT-32-BZ-18"}
        ListElement { region: qsTr("Pragser Dolomiten");                            RegionID: "IT-32-BZ-19"}
        ListElement { region: qsTr("Sextner Dolomiten");                            RegionID: "IT-32-BZ-20"}
    }

    property ListModel regionListTrentino: ListModel{
        ListElement { region: qsTr("Adamello - Presanella");                        RegionID: "IT-32-TN-01"}
        ListElement { region: qsTr("Adamello meridionale");                         RegionID: "IT-32-TN-02"}
        ListElement { region: qsTr("Bondone e Stivo");                              RegionID: "IT-32-TN-03"}
        ListElement { region: qsTr("Brenta Nord - Peller");                         RegionID: "IT-32-TN-04"}
        ListElement { region: qsTr("Brenta meridionale");                           RegionID: "IT-32-TN-05"}
        ListElement { region: qsTr("Folgaria - Lavarone");                          RegionID: "IT-32-TN-06"}
        ListElement { region: qsTr("Lagorai settentrionale");                       RegionID: "IT-32-TN-07"}
        ListElement { region: qsTr("Lagorai meridionale");                          RegionID: "IT-32-TN-08"}
        ListElement { region: qsTr("Latemar");                                      RegionID: "IT-32-TN-09"}
        ListElement { region: qsTr("Marzola - Valsugana");                          RegionID: "IT-32-TN-10"}
        ListElement { region: qsTr("Paganella");                                    RegionID: "IT-32-TN-11"}
        ListElement { region: qsTr("Prealpi");                                      RegionID: "IT-32-TN-12"}
        ListElement { region: qsTr("Primiero - Pale di S. Martino");                RegionID: "IT-32-TN-13"}
        ListElement { region: qsTr("Vallarsa");                                     RegionID: "IT-32-TN-14"}
        ListElement { region: qsTr("Valle di Cembra");                              RegionID: "IT-32-TN-15"}
        ListElement { region: qsTr("Valle di Fassa");                               RegionID: "IT-32-TN-16"}
        ListElement { region: qsTr("Valle di Non");                                 RegionID: "IT-32-TN-17"}
        ListElement { region: qsTr("Valle di Ledro");                               RegionID: "IT-32-TN-18"}
        ListElement { region: qsTr("Sole, Pejo e Rabbi");                           RegionID: "IT-32-TN-19"}
        ListElement { region: qsTr("Maddalene");                                    RegionID: "IT-32-TN-20"}
        ListElement { region: qsTr("Pine' - Valle dei Mocheni");                    RegionID: "IT-32-TN-21"}
    }

    property ListModel regionListCarinthia: ListModel{
        ListElement { region: qsTr("Glocknergruppe");                               RegionID: "AT-02-01"}
        ListElement { region: qsTr("Schobergruppe");                                RegionID: "AT-02-02"}
        ListElement { region: qsTr("Ankogelgruppe");                                RegionID: "AT-02-03"}
        ListElement { region: qsTr("Nockberge");                                    RegionID: "AT-02-04"}
        ListElement { region: qsTr("Südl. Gurktaler Alpen");                        RegionID: "AT-02-05"}
        ListElement { region: qsTr("Saualpe");                                      RegionID: "AT-02-06"}
        ListElement { region: qsTr("Packalpe");                                     RegionID: "AT-02-07"}
        ListElement { region: qsTr("Koralpe West");                                 RegionID: "AT-02-08"}
        ListElement { region: qsTr("Kreuzeckgruppe");                               RegionID: "AT-02-09"}
        ListElement { region: qsTr("Lienzer Dolomiten");                            RegionID: "AT-02-10"}
        ListElement { region: qsTr("Westl. Gailtaler Alpen");                       RegionID: "AT-02-11"}
        ListElement { region: qsTr("Mittlere Gailtaler Alpen");                     RegionID: "AT-02-12"}
        ListElement { region: qsTr("Villacher Alpe");                               RegionID: "AT-02-13"}
        ListElement { region: qsTr("Wstl. Karnische Alpen");                        RegionID: "AT-02-14"}
        ListElement { region: qsTr("Mittlere Karnische Alpen");                     RegionID: "AT-02-15"}
        ListElement { region: qsTr("Östl. Karnische Alpen");                        RegionID: "AT-02-16"}
        ListElement { region: qsTr("Westl. Karawanken");                            RegionID: "AT-02-17"}
        ListElement { region: qsTr("Mittlere Karawanken");                          RegionID: "AT-02-18"}
        ListElement { region: qsTr("Östl. Karawanken");                             RegionID: "AT-02-19"}
    }

    property ListModel regionListSalzburg: ListModel{
        ListElement { region: qsTr("Nockberge");                                    RegionID: "AT-05-01"}
        ListElement { region: qsTr("Südl. Niedere Tauern");                         RegionID: "AT-05-02"}
        ListElement { region: qsTr("Ankogelgruppe, Muhr");                          RegionID: "AT-05-03"}
        ListElement { region: qsTr("Niedere Tauern Alpenhauptkamm");                RegionID: "AT-05-04"}
        ListElement { region: qsTr("Goldberggruppe Alpenhauptkamm");                RegionID: "AT-05-05"}
        ListElement { region: qsTr("Glocknergruppe Alpenhauptkamm");                RegionID: "AT-05-06"}
        ListElement { region: qsTr("Großvenedigergruppe Alpenhauptkamm");           RegionID: "AT-05-07"}
        ListElement { region: qsTr("Nördl. Niedere Tauern");                        RegionID: "AT-05-08"}
        ListElement { region: qsTr("Nördl. Goldberggruppe");                        RegionID: "AT-05-09"}
        ListElement { region: qsTr("Nördl. Glocknergruppe");                        RegionID: "AT-05-10"}
        ListElement { region: qsTr("Nördl. Großvenedigergruppe");                   RegionID: "AT-05-11"}
        ListElement { region: qsTr("Pongauer Grasberge");                           RegionID: "AT-05-12"}
        ListElement { region: qsTr("Dientner Grasberge");                           RegionID: "AT-05-13"}
        ListElement { region: qsTr("Kitzbüheler Alpen, Glemmtal");                  RegionID: "AT-05-14"}
        ListElement { region: qsTr("Oberpinzgau, Grasberge");                       RegionID: "AT-05-15"}
        ListElement { region: qsTr("Tennengebirge, Gosaukamm");                     RegionID: "AT-05-16"}
        ListElement { region: qsTr("Hochkönig, Hagengebirge, Göllstock");           RegionID: "AT-05-17"}
        ListElement { region: qsTr("Loferer und Leoganger Steinberge");             RegionID: "AT-05-18"}
        ListElement { region: qsTr("Osterhorngruppe, Gamsfeldgruppe");              RegionID: "AT-05-19"}
        ListElement { region: qsTr("Unterbergstock");                               RegionID: "AT-05-20"}
        ListElement { region: qsTr("Chiemgauer A., Heutal, Reiteralpe");            RegionID: "AT-05-21"}
    }

    property ListModel regionListSteiermark: ListModel{
        ListElement { region: qsTr("Dachsteingebiet");                              RegionID: "AT-06-01"}
        ListElement { region: qsTr("Totes Gebirge");                                RegionID: "AT-06-02"}
        ListElement { region: qsTr("Ennstaler Alpen");                              RegionID: "AT-06-03"}
        ListElement { region: qsTr("Schladminger Tauern");                          RegionID: "AT-06-04"}
        ListElement { region: qsTr("Nördl. Wölzer Tauern");                         RegionID: "AT-06-05"}
        ListElement { region: qsTr("Rottenmanner Tauern");                          RegionID: "AT-06-06"}
        ListElement { region: qsTr("Südl. Wölzer Tauern");                          RegionID: "AT-06-07"}
        ListElement { region: qsTr("Seckauer Tauern");                              RegionID: "AT-06-08"}
        ListElement { region: qsTr("Eisenerzer Alpen");                             RegionID: "AT-06-09"}
        ListElement { region: qsTr("Hochschwabgebiet");                             RegionID: "AT-06-10"}
        ListElement { region: qsTr("Mürzsteger Alpen");                             RegionID: "AT-06-11"}
        ListElement { region: qsTr("Mürztaler Alpen");                              RegionID: "AT-06-12"}
        ListElement { region: qsTr("Östl. Fischbacher A. und Wechselgebiet");       RegionID: "AT-06-13"}
        ListElement { region: qsTr("Westliche Fischbacher A. und Grazer Bergland"); RegionID: "AT-06-14"}
        ListElement { region: qsTr("Stub- und Gleinalpe");                          RegionID: "AT-06-15"}
        ListElement { region: qsTr("Koralpe");                                      RegionID: "AT-06-16"}
        ListElement { region: qsTr("Seetaler Alpen");                               RegionID: "AT-06-17"}
        ListElement { region: qsTr("Gurktaler Alpen");                              RegionID: "AT-06-18"}
    }

    //Noch keine aktuellen Daten bei der Quelle
    property ListModel regionListOberoestereich: ListModel{
        ListElement { region: qsTr("Dachstein, Gosaukamm");                         RegionID: "AT-04-01"}
        ListElement { region: qsTr("Kalmberg, Katergebirge");                       RegionID: "AT-04-02"}
        ListElement { region: qsTr("Totes Gebirge");                                RegionID: "AT-04-03"}
        ListElement { region: qsTr("Pyhrgas, Haller Mauer");                        RegionID: "AT-04-04"}
        ListElement { region: qsTr("Zimnitzmassiv, Höllengebirge");                 RegionID: "AT-04-05"}
        ListElement { region: qsTr("Traunstein, Eibenberg");                        RegionID: "AT-04-06"}
        ListElement { region: qsTr("Kasbergblock");                                 RegionID: "AT-04-07"}
        ListElement { region: qsTr("Sengsengebirge, Reichraminger Hintergebirge");  RegionID: "AT-04-08"}
        ListElement { region: qsTr("Ennstaler Voralpen");                           RegionID: "AT-04-09"}
    }

    //Noch keine aktuellen Daten bei der Quelle
    property ListModel regionListNiederoestereich: ListModel{
        ListElement { region: qsTr("Ybbstaler Alpen");                              RegionID: "AT-03-01"}
        ListElement { region: qsTr("Türnitzer Alpen");                              RegionID: "AT-03-02"}
        ListElement { region: qsTr("Gutensteiner Alpen");                           RegionID: "AT-03-03"}
        ListElement { region: qsTr("Rax- Schneeberggebiet");                        RegionID: "AT-03-04"}
        ListElement { region: qsTr("Semmering- Wechselgebiet");                     RegionID: "AT-03-05"}
        ListElement { region: qsTr("Gippel- Göllergebiet");                         RegionID: "AT-03-06"}
    }

    SilicaFlickable {

        anchors.fill: parent
        contentHeight: column.height
        bottomMargin: Theme.paddingSmall

        PullDownMenu {
            //Future Concept: Select from PullMenu (First Country, then State, then Region) the Favorite regions. On the first Page only those are displayed
            /*MenuItem {
                text: qsTr("Add Favorite")
                onClicked: pageStack.push(Qt.resolvedUrl("AddFav.qml"))
            }*/
            MenuItem {
                text: qsTr("About")
                onClicked: pageStack.push(Qt.resolvedUrl("AboutPage.qml"))
            }
        }

        Column {
            spacing: Theme.paddingSmall
            id: column
            width: parent.width

            anchors.fill: parent

            PageHeader {
                title: qsTr("Show Bulletin for")
            }

            VerticalScrollDecorator {}

            ExpandingSection {
                width: parent.width

                title: qsTr("Austria")

                content.sourceComponent: Column {
                    width: parent.width
                    BackgroundItem {
                        id: bgndTyrol
                        onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListTyrol, "country": qsTr("Austria"), "macroRegion": qsTr("Tyrol")})

                        Label {
                            x: Theme.horizontalPageMargin
                            text: qsTr("Tyrol")
                            anchors.verticalCenter: parent.verticalCenter
                            color: bgndTyrol.highlighted ? Theme.highlightColor : Theme.primaryColor
                        }
                     }

                    BackgroundItem {
                         id: bgndCarinthia
                         onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListCarinthia, "country": qsTr("Austria"), "macroRegion": qsTr("Carinthia")})

                         Label {
                             x: Theme.horizontalPageMargin
                             text: qsTr("Carinthia")
                             anchors.verticalCenter: parent.verticalCenter
                             color: bgndCarinthia.highlighted ? Theme.highlightColor : Theme.primaryColor
                         }
                     }

                    BackgroundItem {
                         id: bgndSalzburg
                         onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListSalzburg, "country": qsTr("Austria"), "macroRegion": qsTr("Salzburg")})

                         Label {
                             x: Theme.horizontalPageMargin
                             text: qsTr("Salzburg")
                             anchors.verticalCenter: parent.verticalCenter
                             color: bgndSalzburg.highlighted ? Theme.highlightColor : Theme.primaryColor
                         }
                     }

                    BackgroundItem {
                         id: bgndSteiermark
                         onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListSteiermark, "country": qsTr("Austria"), "macroRegion": qsTr("Styria")})

                         Label {
                             x: Theme.horizontalPageMargin
                             text: qsTr("Styria")
                             anchors.verticalCenter: parent.verticalCenter
                             color: bgndSalzburg.highlighted ? Theme.highlightColor : Theme.primaryColor
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
                         onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListSTyrol, "country": qsTr("Italy"), "macroRegion": qsTr("South Tyrol")})

                         Label {
                             x: Theme.horizontalPageMargin
                             text: qsTr("South Tyrol")
                             anchors.verticalCenter: parent.verticalCenter
                             color: bgndSTyrol.highlighted ? Theme.highlightColor : Theme.primaryColor
                         }
                     }

                    BackgroundItem {
                         id: bgndTrentino
                         onClicked: pageStack.push(Qt.resolvedUrl("RegionSelectPage.qml"), {"regionList": regionListTrentino, "country": qsTr("Italy"), "macroRegion": qsTr("Trentino")})

                         Label {
                             x: Theme.horizontalPageMargin
                             text: qsTr("Trentino")
                             anchors.verticalCenter: parent.verticalCenter
                             color: bgndTrentino.highlighted ? Theme.highlightColor : Theme.primaryColor
                         }
                     }
                }
            }
        }
    }
}

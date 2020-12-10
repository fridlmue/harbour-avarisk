import QtQuick 2.2
import Sailfish.Silica 1.0

Page {

    property ListModel regionList: ListModel{
    ListElement { region: qsTr("AT Tirol Allgäuer Alpen");                      RegionID: "AT-07-01"}
    ListElement { region: qsTr("AT Tirol Östl. Lecht. A. - Ammergebirge");      RegionID: "AT-07-02"}
    ListElement { region: qsTr("AT Tirol Mieminger Gebirge");                   RegionID: "AT-07-03"}
    ListElement { region: qsTr("AT Tirol Karwendel");                           RegionID: "AT-07-04"}
    ListElement { region: qsTr("AT Tirol Brandenberger Alpen");                 RegionID: "AT-07-05"}
    ListElement { region: qsTr("AT Tirol Wilder Kaiser - Waidringer A.");       RegionID: "AT-07-06"}
    ListElement { region: qsTr("AT Tirol Wstl. Lechtaler Alpen");               RegionID: "AT-07-07"}
    ListElement { region: qsTr("AT Tirol Zentrale Lechtaler Alpen");            RegionID: "AT-07-08"}
    ListElement { region: qsTr("AT Tirol Grieskogelgruppe");                    RegionID: "AT-07-09"}
    ListElement { region: qsTr("AT Tirol Westl. Verwallgruppe");                RegionID: "AT-07-10"}
    ListElement { region: qsTr("AT Tirol Östl. Verwallgruppe");                 RegionID: "AT-07-11"}
    ListElement { region: qsTr("AT Tirol Silvretta");                           RegionID: "AT-07-12"}
    ListElement { region: qsTr("AT Tirol Samnaungruppe");                       RegionID: "AT-07-13"}
    ListElement { region: qsTr("AT Tirol Nördl. Ötztaler- und Stubaier A.");    RegionID: "AT-07-14"}
    ListElement { region: qsTr("AT Tirol Wstl. Tuxer Alpen");                   RegionID: "AT-07-15"}
    ListElement { region: qsTr("AT Tirol Östl. Tuxer Alpen");                   RegionID: "AT-07-16"}
    ListElement { region: qsTr("AT Tirol Wstl. Kitzbühler Alpen");              RegionID: "AT-07-17"}
    ListElement { region: qsTr("AT Tirol Östl. Kitzbühler Alpen");              RegionID: "AT-07-18"}
    ListElement { region: qsTr("AT Tirol Glockturmgruppe");                     RegionID: "AT-07-19"}
    ListElement { region: qsTr("AT Tirol Weißkogelgruppe");                     RegionID: "AT-07-20"}
    ListElement { region: qsTr("AT Tirol Gurgler Gruppe");                      RegionID: "AT-07-21"}
    ListElement { region: qsTr("AT Tirol Zentrale Stubaier Alpen");             RegionID: "AT-07-22"}
    ListElement { region: qsTr("AT Tirol Nördl. Zillertaler Alpen");            RegionID: "AT-07-23"}
    ListElement { region: qsTr("AT Tirol Venedigergruppe");                     RegionID: "AT-07-24"}
    ListElement { region: qsTr("AT Tirol Östl. Rieserfernergruppe");            RegionID: "AT-07-25"}
    ListElement { region: qsTr("AT Tirol Glocknergruppe");                      RegionID: "AT-07-26"}
    ListElement { region: qsTr("AT Tirol Östl. Deferegger Alpen");              RegionID: "AT-07-27"}
    ListElement { region: qsTr("AT Tirol Schobergruppe");                       RegionID: "AT-07-28"}
    ListElement { region: qsTr("AT Tirol Lienzer Dolomiten");                   RegionID: "AT-07-29"}

    //Südtirol
    ListElement { region: qsTr("IT Bozen Münstertaler Alpen");                  RegionID: "IT-32-BZ-01"}
    ListElement { region: qsTr("IT Bozen Langtaufers");                         RegionID: "IT-32-BZ-02"}
    ListElement { region: qsTr("IT Bozen Schnalser Kamm");                      RegionID: "IT-32-BZ-03"}
    ListElement { region: qsTr("IT Bozen Südl. Stubaier Alpen");                RegionID: "IT-32-BZ-04"}
    ListElement { region: qsTr("IT Bozen S Zillert. A und Hohe Tauern");        RegionID: "IT-32-BZ-05"}
    ListElement { region: qsTr("IT Bozen Saldurn-Mastaun Kamm");                RegionID: "IT-32-BZ-06"}
    ListElement { region: qsTr("IT Bozen Texelgruppe");                         RegionID: "IT-32-BZ-07"}
    ListElement { region: qsTr("IT Bozen Sarntaler Alpen");                     RegionID: "IT-32-BZ-08"}
    ListElement { region: qsTr("IT Bozen Wstl. Pfunderer Berge ");              RegionID: "IT-32-BZ-09"}
    ListElement { region: qsTr("IT Bozen Östl. Pfunderer Berge");               RegionID: "IT-32-BZ-10"}
    ListElement { region: qsTr("IT Bozen Durreckgruppe");                       RegionID: "IT-32-BZ-11"}
    ListElement { region: qsTr("IT Bozen Wstl. Rieserfernergruppe");            RegionID: "IT-32-BZ-12"}
    ListElement { region: qsTr("IT Bozen Wstl. Deferegger Alpen");              RegionID: "IT-32-BZ-13"}
    ListElement { region: qsTr("IT Bozen Ortlergruppe");                        RegionID: "IT-32-BZ-14"}
    ListElement { region: qsTr("IT Bozen Ultental");                            RegionID: "IT-32-BZ-15"}
    ListElement { region: qsTr("IT Bozen Östl. Nonsberger Alpen");              RegionID: "IT-32-BZ-16"}
    ListElement { region: qsTr("IT Bozen Nördl. Fleimstaler Alpen");            RegionID: "IT-32-BZ-17"}
    ListElement { region: qsTr("IT Bozen Groedner Dolomiten");                  RegionID: "IT-32-BZ-18"}
    ListElement { region: qsTr("IT Bozen Pragser Dolomiten");                   RegionID: "IT-32-BZ-19"}
    ListElement { region: qsTr("IT Bozen Sextner Dolomiten");                   RegionID: "IT-32-BZ-20"}

    //Trentino
    ListElement { region: qsTr("IT Trentino Adamello - Presanella");            RegionID: "IT-32-TN-01"}
    ListElement { region: qsTr("IT Trentino Adamello meridionale");             RegionID: "IT-32-TN-02"}
    ListElement { region: qsTr("IT Trentino Bondone e Stivo");                  RegionID: "IT-32-TN-03"}
    ListElement { region: qsTr("IT Trentino Brenta Nord - Peller");             RegionID: "IT-32-TN-04"}
    ListElement { region: qsTr("IT Trentino Brenta meridionale");               RegionID: "IT-32-TN-05"}
    ListElement { region: qsTr("IT Trentino Folgaria - Lavarone");              RegionID: "IT-32-TN-06"}
    ListElement { region: qsTr("IT Trentino Lagorai settentrionale");           RegionID: "IT-32-TN-07"}
    ListElement { region: qsTr("IT Trentino Lagorai meridionale");              RegionID: "IT-32-TN-08"}
    ListElement { region: qsTr("IT Trentino Latemar");                          RegionID: "IT-32-TN-09"}
    ListElement { region: qsTr("IT Trentino Marzola - Valsugana");              RegionID: "IT-32-TN-10"}
    ListElement { region: qsTr("IT Trentino Paganella");                        RegionID: "IT-32-TN-11"}
    ListElement { region: qsTr("IT Trentino Prealpi");                          RegionID: "IT-32-TN-12"}
    ListElement { region: qsTr("IT Trentino Primiero - Pale di S. Martino");    RegionID: "IT-32-TN-13"}
    ListElement { region: qsTr("IT Trentino Vallarsa");                         RegionID: "IT-32-TN-14"}
    ListElement { region: qsTr("IT Trentino Valle di Cembra");                  RegionID: "IT-32-TN-15"}
    ListElement { region: qsTr("IT Trentino Valle di Fassa");                   RegionID: "IT-32-TN-16"}
    ListElement { region: qsTr("IT Trentino Valle di Non");                     RegionID: "IT-32-TN-17"}
    ListElement { region: qsTr("IT Trentino Valle di Ledro");                   RegionID: "IT-32-TN-18"}
    ListElement { region: qsTr("IT Trentino Sole, Pejo e Rabbi");               RegionID: "IT-32-TN-19"}
    ListElement { region: qsTr("IT Trentino Maddalene");                        RegionID: "IT-32-TN-20"}
    ListElement { region: qsTr("IT Trentino Pine' - Valle dei Mocheni");        RegionID: "IT-32-TN-21"}

    //Kärnten
    ListElement { region: qsTr("AT Kärnten Glocknergruppe");                    RegionID: "AT-02-01"}
    ListElement { region: qsTr("AT Kärnten Schobergruppe");                     RegionID: "AT-02-02"}
    ListElement { region: qsTr("AT Kärnten Ankogelgruppe");                     RegionID: "AT-02-03"}
    ListElement { region: qsTr("AT Kärnten Nockberge");                         RegionID: "AT-02-04"}
    ListElement { region: qsTr("AT Kärnten Südl. Gurktaler Alpen");             RegionID: "AT-02-05"}
    ListElement { region: qsTr("AT Kärnten Saualpe");                           RegionID: "AT-02-06"}
    ListElement { region: qsTr("AT Kärnten Packalpe");                          RegionID: "AT-02-07"}
    ListElement { region: qsTr("AT Kärnten Koralpe West");                      RegionID: "AT-02-08"}
    ListElement { region: qsTr("AT Kärnten Kreuzeckgruppe");                    RegionID: "AT-02-09"}
    ListElement { region: qsTr("AT Kärnten Lienzer Dolomiten");                 RegionID: "AT-02-10"}
    ListElement { region: qsTr("AT Kärnten Westl. Gailtaler Alpen");            RegionID: "AT-02-11"}
    ListElement { region: qsTr("AT Kärnten Mittlere Gailtaler Alpen");          RegionID: "AT-02-12"}
    ListElement { region: qsTr("AT Kärnten Villacher Alpe");                    RegionID: "AT-02-13"}
    ListElement { region: qsTr("AT Kärnten Wstl. Karnische Alpen");             RegionID: "AT-02-14"}
    ListElement { region: qsTr("AT Kärnten Mittlere Karnische Alpen");          RegionID: "AT-02-15"}
    ListElement { region: qsTr("AT Kärnten Östl. Karnische Alpen");             RegionID: "AT-02-16"}
    ListElement { region: qsTr("AT Kärnten Westl. Karawanken");                 RegionID: "AT-02-17"}
    ListElement { region: qsTr("AT Kärnten Mittlere Karawanken");               RegionID: "AT-02-18"}
    ListElement { region: qsTr("AT Kärnten Östl. Karawanken");                  RegionID: "AT-02-19"}

    //Kärnten
    ListElement { region: qsTr("AT Salzbrg Nockberge");                         RegionID: "AT-05-01"}
    ListElement { region: qsTr("AT Salzbrg Südl. Niedere Tauern");              RegionID: "AT-05-02"}
    ListElement { region: qsTr("AT Salzbrg Ankogelgruppe, Muhr");               RegionID: "AT-05-03"}
    ListElement { region: qsTr("AT Salzbrg Niedere Tauern Alpenhauptkamm");     RegionID: "AT-05-04"}
    ListElement { region: qsTr("AT Salzbrg Goldberggruppe Alpenhauptkamm");     RegionID: "AT-05-05"}
    ListElement { region: qsTr("AT Salzbrg Glocknergruppe Alpenhauptkamm");     RegionID: "AT-05-06"}
    ListElement { region: qsTr("AT Salzbrg Großvenedigergruppe Alpenhauptkamm");RegionID: "AT-05-07"}
    ListElement { region: qsTr("AT Salzbrg Nördl. Niedere Tauern");             RegionID: "AT-05-08"}
    ListElement { region: qsTr("AT Salzbrg Nördl. Goldberggruppe");             RegionID: "AT-05-09"}
    ListElement { region: qsTr("AT Salzbrg Nördl. Glocknergruppe");             RegionID: "AT-05-10"}
    ListElement { region: qsTr("AT Salzbrg Nördl. Großvenedigergruppe ");       RegionID: "AT-05-11"}
    ListElement { region: qsTr("AT Salzbrg Pongauer Grasberge");                RegionID: "AT-05-12"}
    ListElement { region: qsTr("AT Salzbrg Dientner Grasberge");                RegionID: "AT-05-13"}
    ListElement { region: qsTr("AT Salzbrg Kitzbüheler Alpen, Glemmtal");       RegionID: "AT-05-14"}
    ListElement { region: qsTr("AT Salzbrg Oberpinzgau, Grasberge");            RegionID: "AT-05-15"}
    ListElement { region: qsTr("AT Salzbrg Tennengebirge, Gosaukamm");          RegionID: "AT-05-16"}
    ListElement { region: qsTr("AT Salzbrg Hochkönig, Hagengebirge, Göllstock");RegionID: "AT-05-17"}
    ListElement { region: qsTr("AT Salzbrg Loferer und Leoganger Steinberge");  RegionID: "AT-05-18"}
    ListElement { region: qsTr("AT Salzbrg Osterhorngruppe, Gamsfeldgruppe");   RegionID: "AT-05-19"}
    ListElement { region: qsTr("AT Salzbrg Unterbergstock");                    RegionID: "AT-05-20"}
    ListElement { region: qsTr("AT Salzbrg Chiemgauer A., Heutal, Reiteralpe"); RegionID: "AT-05-21"}
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
                    TextSwitch {
                        text: qsTr("Tyrol")
                    }
                    TextSwitch {
                        text: qsTr("Carinthia")
                    }
                    TextSwitch {
                        text: qsTr("Salzburg")
                    }
                }
            }

            ExpandingSection {
                width: parent.width

                title: "Italy"

                content.sourceComponent: Column {
                    width: parent.width
                    TextSwitch {
                        text: qsTr("South Tyrol")
                    }
                    TextSwitch {
                        text: qsTr("Trentino")
                    }
                }
            }

            SilicaListView {
                id:firstListView

                /*
                model: regionList

                anchors.fill: parent
                header: PageHeader {
                    title: qsTr("Show Bulletin for")
                }
                delegate: BackgroundItem {
                    id: firstListViewDelegate

                    onClicked: pageStack.push(Qt.resolvedUrl("DangerPage.qml"), {"regionID": RegionID, "regionName": region})

                    Label {
                        x: Theme.horizontalPageMargin
                        text: region
                        anchors.verticalCenter: parent.verticalCenter
                        color: firstListViewDelegate.highlighted ? Theme.highlightColor : Theme.primaryColor
                    }

                }
                */

            }
        }
    }
}

import QtQuick 2.2
import Sailfish.Silica 1.0

Page {

    SilicaListView {
        id: listView
        model: ListModel {
            /*
            ListElement { region: qsTr("ITALY Bolzano 20"); RegionID: "IT-32-BZ-20"}
            ListElement { region: qsTr("IT-32-TN-13");      RegionID: "IT-32-TN-13"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-26");         RegionID: "AT-07-26"}
            ListElement { region: qsTr("AT-07-22");         RegionID: "AT-07-22"}*/
        }

        anchors.fill: parent
        header: PageHeader {
            title: qsTr("Select Region")
        }
        delegate: BackgroundItem {
            id: delegate

            onClicked: pageStack.push(Qt.resolvedUrl("FirstPage.qml"))

            Label {
                x: Theme.horizontalPageMargin
                text: region
                anchors.verticalCenter: parent.verticalCenter
                color: delegate.highlighted ? Theme.highlightColor : Theme.primaryColor
            }

        }

        VerticalScrollDecorator {}
    }
}

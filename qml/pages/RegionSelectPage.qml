import QtQuick 2.2
import Sailfish.Silica 1.0

Page {
    property ListModel regionList
    property string country
    property string macroRegion

    SilicaListView {
        id:regionSelectionView

        VerticalScrollDecorator {}

        model: regionList

        anchors.fill: parent
        header: PageHeader {
            title: qsTr("Select Region" + ": " + country + " - " + macroRegion)
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

    }

}

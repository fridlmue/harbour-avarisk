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

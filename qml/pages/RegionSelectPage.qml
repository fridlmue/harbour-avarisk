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
    property ListModel regionList
    property string country
    property string macroRegion

    SilicaListView {
        id:regionSelectionView

        VerticalScrollDecorator {}

        model: regionList

        anchors.fill: parent
        header: PageHeader {
            description: qsTr("Select Region")
            title: country + " - " + macroRegion
        }
        delegate: BackgroundItem {
            id: firstListViewDelegate

            onClicked: pageStack.push(Qt.resolvedUrl("DangerPage.qml"), {"regionID": RegionID, "regionName": region, "country": country, "macroRegion": macroRegion})

            Label {
                x: Theme.horizontalPageMargin
                text: region
                anchors.verticalCenter: parent.verticalCenter
                color: firstListViewDelegate.highlighted ? Theme.highlightColor : Theme.primaryColor
            }

        }

    }

}

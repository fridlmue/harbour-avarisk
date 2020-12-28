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

    property ListModel educationList: ListModel{
        ListElement {topic: qsTr("Danger Scale");                        link: "danger-scale"}
        ListElement {topic: qsTr("Avalanche Problems");                  link: "avalanche-problems"}
        ListElement {topic: qsTr("EAWS Matrix");                         link: "matrix"}
        ListElement {topic: qsTr("Avalanche Sizes");                     link: "avalanche-sizes"}
        ListElement {topic: qsTr("Danger Patterns");                     link: "danger-patterns"}
    }

    SilicaListView {
        VerticalScrollDecorator {}

        model: educationList

        anchors.fill: parent
        header: PageHeader {
            title: qsTr("Avalanche Know-How")
            description: qsTr("Displays know-how from avalanche.report")
        }

        delegate: BackgroundItem {
            id: educationListViewDelegate

            onClicked: pageStack.push(Qt.resolvedUrl("WebViewPage.qml"), {"subPage": link, "topic": topic})

            Label {
                x: Theme.horizontalPageMargin
                text: topic
                anchors.verticalCenter: parent.verticalCenter
                color: educationListViewDelegate.highlighted ? Theme.highlightColor : Theme.primaryColor
            }

        }

        Label {

            width: parent.width - (2 * Theme.horizontalPageMargin)
            wrapMode: Text.Wrap
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }
            text: qsTr("Update your Avalanche Knowledge by visiting the Education pages on www.avalanche.report by the Avalanche Warning Services of Tirol, Südtirol and Trentino.")
            font.pixelSize: Theme.fontSizeSmall
        }

    }

    Image {
        id: bgImg
        asynchronous: true
        fillMode: Image.PreserveAspectFit
        opacity: 0.05
        source: "qrc:///res/bg_" + ( Theme.colorScheme ? "light" : "dark" ) + "_page.svg"
        anchors {
            centerIn: parent
        }
    }


}

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

CoverBackground {

    id: coverPage
    transparent: true

    Column {

        anchors.topMargin: Theme.paddingLarge
        anchors.fill: parent
        spacing: Theme.paddingSmall
        anchors.rightMargin: Theme.paddingLarge
        anchors.leftMargin: Theme.paddingLarge

        Label {
            id: coverCountry
            anchors {
                horizontalCenter: parent.Center
            }
            width: parent.width
            text: coverExchange.country + "<br />" + coverExchange.region
            horizontalAlignment: Text.AlignRight
            font.pixelSize: Theme.fontSizeLarge
        }

        Label {
            id: coverMicroRegion
            anchors {
                horizontalCenter: parent.Center
            }
            wrapMode: Text.Wrap
            width: parent.width
            text: coverExchange.microRegion
            horizontalAlignment: Text.AlignRight
            font.pixelSize: (coverExchange.microRegion.length > 30) ? Theme.fontSizeSmall : Theme.fontSizeMedium
        }

        Rectangle {
            height: Theme.paddingSmall
            width: Theme.paddingLarge
            opacity: 0.0
        }

        Grid {
            columns: 2
            spacing: Theme.paddingLarge
            anchors.leftMargin: Theme.paddingLarge
            Label {
                text: coverExchange.levelText + " " + coverExchange.dangerMain
                font.pixelSize: Theme.fontSizeLarge
            }
            Image {
                source: "qrc:///res/danger-levels/level_" + coverExchange.dangerMain + ".png"
                width: Theme.iconSizeMedium
                height: width * sourceSize.height / sourceSize.width
            }
            Label {
                text: coverExchange.validHeight
                font.pixelSize: Theme.fontSizeSmall
            }
            Image {
                source: "qrc:///res/warning-pictos/levels_" + coverExchange.dangerL + "_" + coverExchange.dangerH + ".png"
                width: Theme.iconSizeMedium
                height: width * sourceSize.height / sourceSize.width
            }

        }
    }

    Image {
        id: bgImg
        asynchronous: true
        fillMode: Image.PreserveAspectFit
        opacity: 0.30
        source: "qrc:///res/bg_" + ( Theme.colorScheme ? "light" : "dark" ) + ".svg"
        anchors {
            centerIn: parent
        }
        sourceSize {
            width: coverPage.width
            height: coverPage.height
        }
    }
}


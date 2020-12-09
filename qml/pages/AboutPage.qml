import QtQuick 2.2
import Sailfish.Silica 1.0

Page {

    SilicaFlickable {
        anchors.fill: parent
        contentHeight: parent.height

        Column {
            width: parent.width
            spacing: Theme.paddingLarge

            PageHeader {
                title: qsTr("About avaRisk")
            }

            Image {
                source: "qrc:///res/harbour-avarisk.png"
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
                width: Theme.itemSizeHuge
                height: Theme.itemSizeHuge
            }

            Label {
                text: "avaRisk 0.1"
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: Theme.fontSizeExtraLarge
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Label {
                wrapMode: Text.Wrap
                x: Theme.horizontalPageMargin
                width: parent.width - Theme.horizontalPageMargin
                horizontalAlignment: Text.AlignHCenter
                text: qsTr("SailfishOS Client for EAWS Avalanche Bulletins")
                font.pixelSize: Theme.fontSizeSmall
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Label {
                text: qsTr("By Friedrich Mütschele")
                font.pixelSize: Theme.fontSizeSmall
                width: parent.width - ( 2 * Theme.horizontalPageMargin )
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
                linkColor: Theme.highlightColor
                onLinkActivated: Qt.openUrlExternally(link)
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Text {
                            text: "<a href=\"mailto:avarisk@10hoch-6.de\">" + qsTr("Send E-Mail") + "</a>"
                            anchors {
                                horizontalCenter: parent.horizontalCenter
                            }
                            font.pixelSize: Theme.fontSizeSmall
                            linkColor: Theme.highlightColor

                            onLinkActivated: Qt.openUrlExternally("mailto:avarisk@10hoch-6.de")
            }

            Separator {
                width: parent.width
                color: Theme.primaryColor
                horizontalAlignment: Qt.AlignHCenter
            }

            Label {
                text: qsTr("Licensed under GNU GPLv3")
                font.pixelSize: Theme.fontSizeSmall
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Text {
                text: "<a href=\"https://github.com/fridlmue/harbour-avaRisk\">" + qsTr("Sources on GitHub") + "</a>"
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
                font.pixelSize: Theme.fontSizeSmall
                linkColor: Theme.highlightColor

                onLinkActivated: Qt.openUrlExternally("https://github.com/fridlmue/harbour-avaRisk")
            }

            Label {
                wrapMode: Text.Wrap
                x: Theme.horizontalPageMargin
                width: parent.width - Theme.horizontalPageMargin
                horizontalAlignment: Text.AlignHCenter
                text: qsTr("Thanks to all the Avalanche Warning Services who provide the data open and for the great work they do! Stay careful and safe!")
                font.pixelSize: Theme.fontSizeSmall
                anchors {
                    horizontalCenter: parent.horizontalCenter
                }
            }



        }
    }
}

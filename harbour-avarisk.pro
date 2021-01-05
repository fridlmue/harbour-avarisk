# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = harbour-avarisk

CONFIG += sailfishapp

SOURCES += src/harbour-avarisk.cpp

DISTFILES += qml/harbour-avarisk.qml \
    qml/cover/CoverPage.qml \
    qml/pages/Education.qml \
    qml/pages/FirstPage.qml \
    qml/pages/SecondPage.qml \
    qml/pages/WebViewPage.qml \
    res/avalanche-situations/drifting_snow.png \
    res/avalanche-situations/favourable_situation.png \
    res/avalanche-situations/gliding_snow.png \
    res/avalanche-situations/new_snow.png \
    res/avalanche-situations/old_snow.png \
    res/avalanche-situations/wet_snow.png \
    res/bg.svg \
    res/bg_dark.svg \
    res/bg_dark_page.svg \
    res/bg_light.svg \
    res/bg_light_page.svg \
    res/danger-levels/level_1.png \
    res/danger-levels/level_2.png \
    res/danger-levels/level_3.png \
    res/danger-levels/level_4.png \
    res/danger-levels/level_5.png \
    res/expositions/Exposition/exposition_e.png \
    res/expositions/Exposition/exposition_n.png \
    res/expositions/Exposition/exposition_ne.png \
    res/expositions/Exposition/exposition_s.png \
    res/expositions/Exposition/exposition_se.png \
    res/expositions/exposition_bg.png \
    res/expositions/exposition_e.png \
    res/expositions/exposition_n.png \
    res/expositions/exposition_ne.png \
    res/expositions/exposition_nw.png \
    res/expositions/exposition_s.png \
    res/expositions/exposition_se.png \
    res/expositions/exposition_sw.png \
    res/expositions/exposition_w.png \
    res/harbour-avarisk.png \
    res/warning-pictos/Elevation/levels_all.png \
    res/warning-pictos/levels_0_0.png \
    res/warning-pictos/levels_0_1.png \
    res/warning-pictos/levels_0_2.png \
    res/warning-pictos/levels_0_3.png \
    res/warning-pictos/levels_0_4.png \
    res/warning-pictos/levels_0_5.png \
    res/warning-pictos/levels_1_0.png \
    res/warning-pictos/levels_1_1.png \
    res/warning-pictos/levels_1_2.png \
    res/warning-pictos/levels_1_3.png \
    res/warning-pictos/levels_1_4.png \
    res/warning-pictos/levels_1_5.png \
    res/warning-pictos/levels_2_0.png \
    res/warning-pictos/levels_2_1.png \
    res/warning-pictos/levels_2_2.png \
    res/warning-pictos/levels_2_3.png \
    res/warning-pictos/levels_2_4.png \
    res/warning-pictos/levels_2_5.png \
    res/warning-pictos/levels_3_0.png \
    res/warning-pictos/levels_3_1.png \
    res/warning-pictos/levels_3_2.png \
    res/warning-pictos/levels_3_3.png \
    res/warning-pictos/levels_3_4.png \
    res/warning-pictos/levels_3_5.png \
    res/warning-pictos/levels_4_0.png \
    res/warning-pictos/levels_4_1.png \
    res/warning-pictos/levels_4_2.png \
    res/warning-pictos/levels_4_3.png \
    res/warning-pictos/levels_4_4.png \
    res/warning-pictos/levels_4_5.png \
    res/warning-pictos/levels_5_0.png \
    res/warning-pictos/levels_5_1.png \
    res/warning-pictos/levels_5_2.png \
    res/warning-pictos/levels_5_3.png \
    res/warning-pictos/levels_5_4.png \
    res/warning-pictos/levels_5_5.png \
    res/warning-pictos/levels_above.png \
    res/warning-pictos/levels_all.png \
    res/warning-pictos/levels_below.png \
    res/warning-pictos/levels_middle.png \
    rpm/harbour-avarisk.changes.in \
    rpm/harbour-avarisk.changes.run.in \
    rpm/harbour-avarisk.spec \
    rpm/harbour-avarisk.yaml \
    translations/*.ts \
    harbour-avarisk.desktop

SAILFISHAPP_ICONS = 86x86 108x108 128x128 172x172

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

# German translation is enabled as an example. If you aren't
# planning to localize your app, remember to comment out the
# following TRANSLATIONS line. And also do not forget to
# modify the localized app name in the the .desktop file.
TRANSLATIONS += translations/harbour-avarisk-de.ts
TRANSLATIONS += translations/harbour-avarisk.ts

RESOURCES += \
    res.qrc

pragma Singleton
import QtQuick 2.0

QtObject {
    //REGIONS ITALY
    property ListModel regionListVeneto: ListModel{
        ListElement {region: qsTr("PREALPI");                           RegionID: "IT-34-01"}
        ListElement {region: qsTr("DOLOMITI");                          RegionID: "IT-34-02"}
    }

    property ListModel regionListSTyrol: ListModel{
        ListElement {region: qsTr("Münstertaler Alpen");                           RegionID: "IT-32-BZ-01"}
        ListElement {region: qsTr("Langtaufers");                                  RegionID: "IT-32-BZ-02"}
        ListElement {region: qsTr("Schnalser Kamm");                               RegionID: "IT-32-BZ-03"}
        ListElement {region: qsTr("Südl. Stubaier Alpen");                         RegionID: "IT-32-BZ-04"}
        ListElement {region: qsTr("S Zillertaler A. und Hohe Tauern");             RegionID: "IT-32-BZ-05"}
        ListElement {region: qsTr("Saldurn-Mastaun Kamm");                         RegionID: "IT-32-BZ-06"}
        ListElement {region: qsTr("Texelgruppe");                                  RegionID: "IT-32-BZ-07"}
        ListElement {region: qsTr("Sarntaler Alpen");                              RegionID: "IT-32-BZ-08"}
        ListElement {region: qsTr("Wstl. Pfunderer Berge ");                       RegionID: "IT-32-BZ-09"}
        ListElement {region: qsTr("Östl. Pfunderer Berge");                        RegionID: "IT-32-BZ-10"}
        ListElement {region: qsTr("Durreckgruppe");                                RegionID: "IT-32-BZ-11"}
        ListElement {region: qsTr("Wstl. Rieserfernergruppe");                     RegionID: "IT-32-BZ-12"}
        ListElement {region: qsTr("Wstl. Deferegger Alpen");                       RegionID: "IT-32-BZ-13"}
        ListElement {region: qsTr("Ortlergruppe");                                 RegionID: "IT-32-BZ-14"}
        ListElement {region: qsTr("Ultental");                                     RegionID: "IT-32-BZ-15"}
        ListElement {region: qsTr("Östl. Nonsberger Alpen");                       RegionID: "IT-32-BZ-16"}
        ListElement {region: qsTr("Nördl. Fleimstaler Alpen");                     RegionID: "IT-32-BZ-17"}
        ListElement {region: qsTr("Groedner Dolomiten");                           RegionID: "IT-32-BZ-18"}
        ListElement {region: qsTr("Pragser Dolomiten");                            RegionID: "IT-32-BZ-19"}
        ListElement {region: qsTr("Sextner Dolomiten");                            RegionID: "IT-32-BZ-20"}
    }

    property ListModel regionListTrentino: ListModel{
        ListElement {region: qsTr("Adamello - Presanella");                        RegionID: "IT-32-TN-01"}
        ListElement {region: qsTr("Adamello meridionale");                         RegionID: "IT-32-TN-02"}
        ListElement {region: qsTr("Bondone e Stivo");                              RegionID: "IT-32-TN-03"}
        ListElement {region: qsTr("Brenta Nord - Peller");                         RegionID: "IT-32-TN-04"}
        ListElement {region: qsTr("Brenta meridionale");                           RegionID: "IT-32-TN-05"}
        ListElement {region: qsTr("Folgaria - Lavarone");                          RegionID: "IT-32-TN-06"}
        ListElement {region: qsTr("Lagorai settentrionale");                       RegionID: "IT-32-TN-07"}
        ListElement {region: qsTr("Lagorai meridionale");                          RegionID: "IT-32-TN-08"}
        ListElement {region: qsTr("Latemar");                                      RegionID: "IT-32-TN-09"}
        ListElement {region: qsTr("Marzola - Valsugana");                          RegionID: "IT-32-TN-10"}
        ListElement {region: qsTr("Paganella");                                    RegionID: "IT-32-TN-11"}
        ListElement {region: qsTr("Prealpi");                                      RegionID: "IT-32-TN-12"}
        ListElement {region: qsTr("Primiero - Pale di S. Martino");                RegionID: "IT-32-TN-13"}
        ListElement {region: qsTr("Vallarsa");                                     RegionID: "IT-32-TN-14"}
        ListElement {region: qsTr("Valle di Cembra");                              RegionID: "IT-32-TN-15"}
        ListElement {region: qsTr("Valle di Fassa");                               RegionID: "IT-32-TN-16"}
        ListElement {region: qsTr("Valle di Non");                                 RegionID: "IT-32-TN-17"}
        ListElement {region: qsTr("Valle di Ledro");                               RegionID: "IT-32-TN-18"}
        ListElement {region: qsTr("Sole, Pejo e Rabbi");                           RegionID: "IT-32-TN-19"}
        ListElement {region: qsTr("Maddalene");                                    RegionID: "IT-32-TN-20"}
        ListElement {region: qsTr("Pine' - Valle dei Mocheni");                    RegionID: "IT-32-TN-21"}
    }

    //REGIONS AUSTRIA
    property ListModel regionListTyrol: ListModel{
        ListElement {region: qsTr("Allgäuer Alpen");                               RegionID: "AT-07-01"}
        ListElement {region: qsTr("Östl. Lechtaler A. - Ammergebirge");            RegionID: "AT-07-02"}
        ListElement {region: qsTr("Mieminger Gebirge");                            RegionID: "AT-07-03"}
        ListElement {region: qsTr("Karwendel");                                    RegionID: "AT-07-04"}
        ListElement {region: qsTr("Brandenberger Alpen");                          RegionID: "AT-07-05"}
        ListElement {region: qsTr("Wilder Kaiser - Waidringer Alpen");             RegionID: "AT-07-06"}
        ListElement {region: qsTr("Wstl. Lechtaler Alpen");                        RegionID: "AT-07-07"}
        ListElement {region: qsTr("Zentrale Lechtaler Alpen");                     RegionID: "AT-07-08"}
        ListElement {region: qsTr("Grieskogelgruppe");                             RegionID: "AT-07-09"}
        ListElement {region: qsTr("Westl. Verwallgruppe");                         RegionID: "AT-07-10"}
        ListElement {region: qsTr("Östl. Verwallgruppe");                          RegionID: "AT-07-11"}
        ListElement {region: qsTr("Silvretta");                                    RegionID: "AT-07-12"}
        ListElement {region: qsTr("Samnaungruppe");                                RegionID: "AT-07-13"}
        ListElement {region: qsTr("Nördl. Ötztaler- und Stubaier Alpen");          RegionID: "AT-07-14"}
        ListElement {region: qsTr("Wstl. Tuxer Alpen");                            RegionID: "AT-07-15"}
        ListElement {region: qsTr("Östl. Tuxer Alpen");                            RegionID: "AT-07-16"}
        ListElement {region: qsTr("Wstl. Kitzbühler Alpen");                       RegionID: "AT-07-17"}
        ListElement {region: qsTr("Östl. Kitzbühler Alpen");                       RegionID: "AT-07-18"}
        ListElement {region: qsTr("Glockturmgruppe");                              RegionID: "AT-07-19"}
        ListElement {region: qsTr("Weißkogelgruppe");                              RegionID: "AT-07-20"}
        ListElement {region: qsTr("Gurgler Gruppe");                               RegionID: "AT-07-21"}
        ListElement {region: qsTr("Zentrale Stubaier Alpen");                      RegionID: "AT-07-22"}
        ListElement {region: qsTr("Nördl. Zillertaler Alpen");                     RegionID: "AT-07-23"}
        ListElement {region: qsTr("Venedigergruppe");                              RegionID: "AT-07-24"}
        ListElement {region: qsTr("Östl. Rieserfernergruppe");                     RegionID: "AT-07-25"}
        ListElement {region: qsTr("Glocknergruppe");                               RegionID: "AT-07-26"}
        ListElement {region: qsTr("Östl. Deferegger Alpen");                       RegionID: "AT-07-27"}
        ListElement {region: qsTr("Schobergruppe");                                RegionID: "AT-07-28"}
        ListElement {region: qsTr("Lienzer Dolomiten");                            RegionID: "AT-07-29"}
    }

    property ListModel regionListCarinthia: ListModel{
        ListElement {region: qsTr("Glocknergruppe");                               RegionID: "AT-02-01"}
        ListElement {region: qsTr("Schobergruppe");                                RegionID: "AT-02-02"}
        ListElement {region: qsTr("Ankogelgruppe");                                RegionID: "AT-02-03"}
        ListElement {region: qsTr("Nockberge");                                    RegionID: "AT-02-04"}
        ListElement {region: qsTr("Südl. Gurktaler Alpen");                        RegionID: "AT-02-05"}
        ListElement {region: qsTr("Saualpe");                                      RegionID: "AT-02-06"}
        ListElement {region: qsTr("Packalpe");                                     RegionID: "AT-02-07"}
        ListElement {region: qsTr("Koralpe West");                                 RegionID: "AT-02-08"}
        ListElement {region: qsTr("Kreuzeckgruppe");                               RegionID: "AT-02-09"}
        ListElement {region: qsTr("Lienzer Dolomiten");                            RegionID: "AT-02-10"}
        ListElement {region: qsTr("Westl. Gailtaler Alpen");                       RegionID: "AT-02-11"}
        ListElement {region: qsTr("Mittlere Gailtaler Alpen");                     RegionID: "AT-02-12"}
        ListElement {region: qsTr("Villacher Alpe");                               RegionID: "AT-02-13"}
        ListElement {region: qsTr("Wstl. Karnische Alpen");                        RegionID: "AT-02-14"}
        ListElement {region: qsTr("Mittlere Karnische Alpen");                     RegionID: "AT-02-15"}
        ListElement {region: qsTr("Östl. Karnische Alpen");                        RegionID: "AT-02-16"}
        ListElement {region: qsTr("Westl. Karawanken");                            RegionID: "AT-02-17"}
        ListElement {region: qsTr("Mittlere Karawanken");                          RegionID: "AT-02-18"}
        ListElement {region: qsTr("Östl. Karawanken");                             RegionID: "AT-02-19"}
    }

    property ListModel regionListSalzburg: ListModel{
        ListElement {region: qsTr("Nockberge");                                    RegionID: "AT-05-01"}
        ListElement {region: qsTr("Südl. Niedere Tauern");                         RegionID: "AT-05-02"}
        ListElement {region: qsTr("Ankogelgruppe, Muhr");                          RegionID: "AT-05-03"}
        ListElement {region: qsTr("Niedere Tauern Alpenhauptkamm");                RegionID: "AT-05-04"}
        ListElement {region: qsTr("Goldberggruppe Alpenhauptkamm");                RegionID: "AT-05-05"}
        ListElement {region: qsTr("Glocknergruppe Alpenhauptkamm");                RegionID: "AT-05-06"}
        ListElement {region: qsTr("Großvenedigergruppe Alpenhauptkamm");           RegionID: "AT-05-07"}
        ListElement {region: qsTr("Nördl. Niedere Tauern");                        RegionID: "AT-05-08"}
        ListElement {region: qsTr("Nördl. Goldberggruppe");                        RegionID: "AT-05-09"}
        ListElement {region: qsTr("Nördl. Glocknergruppe");                        RegionID: "AT-05-10"}
        ListElement {region: qsTr("Nördl. Großvenedigergruppe");                   RegionID: "AT-05-11"}
        ListElement {region: qsTr("Pongauer Grasberge");                           RegionID: "AT-05-12"}
        ListElement {region: qsTr("Dientner Grasberge");                           RegionID: "AT-05-13"}
        ListElement {region: qsTr("Kitzbüheler Alpen, Glemmtal");                  RegionID: "AT-05-14"}
        ListElement {region: qsTr("Oberpinzgau, Grasberge");                       RegionID: "AT-05-15"}
        ListElement {region: qsTr("Tennengebirge, Gosaukamm");                     RegionID: "AT-05-16"}
        ListElement {region: qsTr("Hochkönig, Hagengebirge, Göllstock");           RegionID: "AT-05-17"}
        ListElement {region: qsTr("Loferer und Leoganger Steinberge");             RegionID: "AT-05-18"}
        ListElement {region: qsTr("Osterhorngruppe, Gamsfeldgruppe");              RegionID: "AT-05-19"}
        ListElement {region: qsTr("Unterbergstock");                               RegionID: "AT-05-20"}
        ListElement {region: qsTr("Chiemgauer A., Heutal, Reiteralpe");            RegionID: "AT-05-21"}
    }

    property ListModel regionListSteiermark: ListModel{
        ListElement {region: qsTr("Dachsteingebiet");                              RegionID: "AT-06-01"}
        ListElement {region: qsTr("Totes Gebirge");                                RegionID: "AT-06-02"}
        ListElement {region: qsTr("Ennstaler Alpen");                              RegionID: "AT-06-03"}
        ListElement {region: qsTr("Schladminger Tauern");                          RegionID: "AT-06-04"}
        ListElement {region: qsTr("Nördl. Wölzer Tauern");                         RegionID: "AT-06-05"}
        ListElement {region: qsTr("Rottenmanner Tauern");                          RegionID: "AT-06-06"}
        ListElement {region: qsTr("Südl. Wölzer Tauern");                          RegionID: "AT-06-07"}
        ListElement {region: qsTr("Seckauer Tauern");                              RegionID: "AT-06-08"}
        ListElement {region: qsTr("Eisenerzer Alpen");                             RegionID: "AT-06-09"}
        ListElement {region: qsTr("Hochschwabgebiet");                             RegionID: "AT-06-10"}
        ListElement {region: qsTr("Mürzsteger Alpen");                             RegionID: "AT-06-11"}
        ListElement {region: qsTr("Mürztaler Alpen");                              RegionID: "AT-06-12"}
        ListElement {region: qsTr("Östl. Fischbacher A., Wechselgebiet");          RegionID: "AT-06-13"}
        ListElement {region: qsTr("Westl. Fischbacher A., Grazer Bergland");       RegionID: "AT-06-14"}
        ListElement {region: qsTr("Stub- und Gleinalpe");                          RegionID: "AT-06-15"}
        ListElement {region: qsTr("Koralpe");                                      RegionID: "AT-06-16"}
        ListElement {region: qsTr("Seetaler Alpen");                               RegionID: "AT-06-17"}
        ListElement {region: qsTr("Gurktaler Alpen");                              RegionID: "AT-06-18"}
    }

    property ListModel regionListOberoestereich: ListModel{
        ListElement {region: qsTr("Dachstein, Gosaukamm");                         RegionID: "AT-04-01"}
        ListElement {region: qsTr("Kalmberg, Katergebirge");                       RegionID: "AT-04-02"}
        ListElement {region: qsTr("Totes Gebirge");                                RegionID: "AT-04-03"}
        ListElement {region: qsTr("Pyhrgas, Haller Mauer");                        RegionID: "AT-04-04"}
        ListElement {region: qsTr("Zimnitzmassiv, Höllengebirge");                 RegionID: "AT-04-05"}
        ListElement {region: qsTr("Traunstein, Eibenberg");                        RegionID: "AT-04-06"}
        ListElement {region: qsTr("Kasbergblock");                                 RegionID: "AT-04-07"}
        ListElement {region: qsTr("Sengsengebirge, Reichraminger Hintergeb.");     RegionID: "AT-04-08"}
        ListElement {region: qsTr("Ennstaler Voralpen");                           RegionID: "AT-04-09"}
    }

    property ListModel regionListNiederoestereich: ListModel{
        ListElement {region: qsTr("Ybbstaler Alpen");                              RegionID: "AT-03-01"}
        ListElement {region: qsTr("Türnitzer Alpen");                              RegionID: "AT-03-02"}
        ListElement {region: qsTr("Gutensteiner Alpen");                           RegionID: "AT-03-03"}
        ListElement {region: qsTr("Rax- Schneeberggebiet");                        RegionID: "AT-03-04"}
        ListElement {region: qsTr("Semmering- Wechselgebiet");                     RegionID: "AT-03-05"}
        ListElement {region: qsTr("Gippel- Göllergebiet");                         RegionID: "AT-03-06"}
    }

    property ListModel regionListVorarlberg: ListModel{
        ListElement {region: qsTr("Bregenzerwaldgebirge");                         RegionID: "AT8R1"}
        ListElement {region: qsTr("Allgäuer Alpen / Hochtannberg");                RegionID: "AT8R2"}
        ListElement {region: qsTr("Lechquellengeb. / Arlberg / Lechtaler Alp.");   RegionID: "AT8R3"}
        ListElement {region: qsTr("Verwall");                                      RegionID: "AT8R4"}
        ListElement {region: qsTr("Rätikon");                                      RegionID: "AT8R5"}
        ListElement {region: qsTr("Silvretta");                                    RegionID: "AT8R6"}
    }

    //REGIONS GERMANY
    property ListModel regionListBavaria: ListModel{
        ListElement {region: qsTr("Allgäuer Alpen");                               RegionID: "BYALL"}
        ListElement {region: qsTr("Ammergauer Alpen");                             RegionID: "BYAMM"}
        ListElement {region: qsTr("Werdenfelser Alpen");                           RegionID: "BYWFK"}
        ListElement {region: qsTr("Bayrische Voralpen");                           RegionID: "BYBVA"}
        ListElement {region: qsTr("Chiemgauer Alpen");                             RegionID: "BYCHG"}
        ListElement {region: qsTr("Berchtesgadener Alpen");                        RegionID: "BYBGD"}
    }

    // REGIONS SPAIN
    property ListModel regionListAran: ListModel{
        ListElement {region: qsTr("Aran norte y centro");                          RegionID: "ES-CT-L-01"}
        ListElement {region: qsTr("Aran límite sur");                              RegionID: "ES-CT-L-02"}
        ListElement {region: qsTr("Aran vertiente sur");                           RegionID: "ES-CT-L-03"}
    }


    // REGIONS CH
    property ListModel regionListCHBEA: ListModel{
        ListElement {region: qsTr("Jaun");                                         RegionID: "CH-1121"}
        ListElement {region: qsTr("Gruyère");                                      RegionID: "CH-1122"}
        ListElement {region: qsTr("westliche Berner Voralpen");                    RegionID: "CH-1211"}
        ListElement {region: qsTr("östliche Berner Voralpen");                     RegionID: "CH-1212"}
        ListElement {region: qsTr("Hohgant");                                      RegionID: "CH-1213"}
        ListElement {region: qsTr("Niedersimmental");                              RegionID: "CH-1221"}
        ListElement {region: qsTr("Gstaad");                                       RegionID: "CH-1222"}
        ListElement {region: qsTr("Wildhorn");                                     RegionID: "CH-1223"}
        ListElement {region: qsTr("sLenk");                                        RegionID: "CH-1224"}
        ListElement {region: qsTr("Iffigen");                                      RegionID: "CH-1225"}
        ListElement {region: qsTr("Adelboden");                                    RegionID: "CH-1226"}
        ListElement {region: qsTr("Engstligen");                                   RegionID: "CH-1227"}
        ListElement {region: qsTr("Obersimmental");                                RegionID: "CH-1228"}
        ListElement {region: qsTr("Kandersteg");                                   RegionID: "CH-1231"}
        ListElement {region: qsTr("Blüemlisalp");                                  RegionID: "CH-1232"}
        ListElement {region: qsTr("Lauterbrunnen");                                RegionID: "CH-1233"}
        ListElement {region: qsTr("Jungfrau - Schilthorn");                        RegionID: "CH-1234"}
        ListElement {region: qsTr("Brienz-Interlaken");                            RegionID: "CH-1241"}
        ListElement {region: qsTr("Grindelwald");                                  RegionID: "CH-1242"}
        ListElement {region: qsTr("Schreckhorn");                                  RegionID: "CH-1243"}
        ListElement {region: qsTr("Hasliberg - Rosenlaui");                        RegionID: "CH-1244"}
        ListElement {region: qsTr("Guttannen");                                    RegionID: "CH-1245"}
        ListElement {region: qsTr("Gadmertal");                                    RegionID: "CH-1246"}
        ListElement {region: qsTr("Grimselpass");                                  RegionID: "CH-1247"}
    }

    property ListModel regionListCHZAN: ListModel{
        ListElement {region: qsTr("Pilatus");                                      RegionID: "CH-2111"}
        ListElement {region: qsTr("Schwarzenberg");                                RegionID: "CH-2112"}
        ListElement {region: qsTr("Glaubenberg");                                  RegionID: "CH-2121"}
        ListElement {region: qsTr("Engelberg");                                    RegionID: "CH-2122"}
        ListElement {region: qsTr("Melchtal");                                     RegionID: "CH-2123"}
        ListElement {region: qsTr("Gersau");                                       RegionID: "CH-2124"}
        ListElement {region: qsTr("Rothenthurm");                                  RegionID: "CH-2131"}
        ListElement {region: qsTr("Ybrig");                                        RegionID: "CH-2132"}
        ListElement {region: qsTr("Stoos");                                        RegionID: "CH-2133"}
        ListElement {region: qsTr("Bisistal");                                     RegionID: "CH-2134"}
        ListElement {region: qsTr("Schächental");                                  RegionID: "CH-2211"}
        ListElement {region: qsTr("Uri Rot Stock");                                RegionID: "CH-2212"}
        ListElement {region: qsTr("Meiental");                                     RegionID: "CH-2221"}
        ListElement {region: qsTr("Maderanertal");                                 RegionID: "CH-2222"}
        ListElement {region: qsTr("nördliches Urseren");                           RegionID: "CH-2223"}
        ListElement {region: qsTr("südliches Urseren");                            RegionID: "CH-2224"}
    }

    property ListModel regionListCHOAN: ListModel{
        ListElement {region: qsTr("Glarus Nord");                                  RegionID: "CH-3111"}
        ListElement {region: qsTr("Glarus Süd-Grosstal");                          RegionID: "CH-3112"}
        ListElement {region: qsTr("Glarus Süd-Sernftal");                          RegionID: "CH-3113"}
        ListElement {region: qsTr("Glarus Mitte");                                 RegionID: "CH-3114"}
        ListElement {region: qsTr("Appenzeller Alpen");                            RegionID: "CH-3211"}
        ListElement {region: qsTr("Toggenburg");                                   RegionID: "CH-3221"}
        ListElement {region: qsTr("Alpstein - Alvier");                            RegionID: "CH-3222"}
        ListElement {region: qsTr("Flumserberg");                                  RegionID: "CH-3223"}
        ListElement {region: qsTr("Sarganserland");                                RegionID: "CH-3224"}
    }

    property ListModel regionListCHUWW: ListModel{
        ListElement {region: qsTr("Waadtländer Voralpen");                         RegionID: "CH-1111"}
        ListElement {region: qsTr("Pays d'Enhaut");                                RegionID: "CH-1112"}
        ListElement {region: qsTr("Pays d'Enhaut");                                RegionID: "CH-1113"}
        ListElement {region: qsTr("Bex-Villars");                                  RegionID: "CH-1114"}
        ListElement {region: qsTr("Vouvry");                                       RegionID: "CH-1311"}
        ListElement {region: qsTr("Monthey-Val d'Illiez");                         RegionID: "CH-1312"}
        ListElement {region: qsTr("Emosson");                                      RegionID: "CH-4111"}
        ListElement {region: qsTr("Génépi");                                       RegionID: "CH-4112"}
        ListElement {region: qsTr("Val d'Entremont-Val Ferret");                   RegionID: "CH-4113"}
        ListElement {region: qsTr("Conthey-Fully");                                RegionID: "CH-4114"}
        ListElement {region: qsTr("Martigny-Verbier");                             RegionID: "CH-4115"}
        ListElement {region: qsTr("Haut Val de Bagnes");                           RegionID: "CH-4116"}
        ListElement {region: qsTr("Montana");                                      RegionID: "CH-4121"}
        ListElement {region: qsTr("Val d'Hérens");                                 RegionID: "CH-4122"}
        ListElement {region: qsTr("Arolla");                                       RegionID: "CH-4123"}
        ListElement {region: qsTr("Val d'Anniviers");                              RegionID: "CH-4124"}
        ListElement {region: qsTr("Mountet");                                      RegionID: "CH-4125"}
    }

    property ListModel regionListCHOW: ListModel{
        ListElement {region: qsTr("Leukerbad - Lötschental");                      RegionID: "CH-4211"}
        ListElement {region: qsTr("Turtmanntal");                                  RegionID: "CH-4212"}
        ListElement {region: qsTr("Konkordia Gebiet");                             RegionID: "CH-4213"}
        ListElement {region: qsTr("Riederalp");                                    RegionID: "CH-4214"}
        ListElement {region: qsTr("Leuk");                                         RegionID: "CH-4215"}
        ListElement {region: qsTr("untere Vispertäler");                           RegionID: "CH-4221"}
        ListElement {region: qsTr("Zermatt");                                      RegionID: "CH-4222"}
        ListElement {region: qsTr("Saas Fee");                                     RegionID: "CH-4223"}
        ListElement {region: qsTr("Monte Rosa");                                   RegionID: "CH-4224"}
        ListElement {region: qsTr("Mattmark");                                     RegionID: "CH-4225"}
        ListElement {region: qsTr("nördliches Simplon Gebiet");                    RegionID: "CH-4231"}
        ListElement {region: qsTr("südliches Simplon Gebiet");                     RegionID: "CH-4232"}
        ListElement {region: qsTr("Reckingen");                                    RegionID: "CH-4241"}
        ListElement {region: qsTr("Binntal");                                      RegionID: "CH-4242"}
        ListElement {region: qsTr("nördliches Obergoms");                          RegionID: "CH-4243"}
        ListElement {region: qsTr("südliches Obergoms");                           RegionID: "CH-4244"}
    }

    property ListModel regionListCHNB: ListModel{
        ListElement {region: qsTr("nördliches Prättigau");                         RegionID: "CH-5111"}
        ListElement {region: qsTr("südliches Prättigau");                          RegionID: "CH-5112"}
        ListElement {region: qsTr("westliche Silvretta");                          RegionID: "CH-5113"}
        ListElement {region: qsTr("Calanda");                                      RegionID: "CH-5121"}
        ListElement {region: qsTr("Schanfigg");                                    RegionID: "CH-5122"}
        ListElement {region: qsTr("Davos");                                        RegionID: "CH-5123"}
        ListElement {region: qsTr("Flims");                                        RegionID: "CH-5124"}
        ListElement {region: qsTr("nördliches Tujetsch");                          RegionID: "CH-5211"}
        ListElement {region: qsTr("südliches Tujetsch");                           RegionID: "CH-5212"}
        ListElement {region: qsTr("Obersaxen - Safiental");                        RegionID: "CH-5214"}
        ListElement {region: qsTr("Val Sumvitg");                                  RegionID: "CH-5215"}
        ListElement {region: qsTr("Zervreila");                                    RegionID: "CH-5216"}
        ListElement {region: qsTr("Domleschg - Lenzerheide");                      RegionID: "CH-5221"}
        ListElement {region: qsTr("Schams");                                       RegionID: "CH-5222"}
        ListElement {region: qsTr("Rheinwald");                                    RegionID: "CH-5223"}
        ListElement {region: qsTr("Albulatal");                                    RegionID: "CH-5231"}
        ListElement {region: qsTr("Savognin");                                     RegionID: "CH-5232"}
        ListElement {region: qsTr("Avers");                                        RegionID: "CH-5233"}
        ListElement {region: qsTr("Bivio");                                        RegionID: "CH-5234"}
    }

    property ListModel regionListCHTES: ListModel{
        ListElement {region: qsTr("Bedrettotal");                                  RegionID: "CH-6111"}
        ListElement {region: qsTr("obere Leventina");                              RegionID: "CH-6112"}
        ListElement {region: qsTr("Bleniotal");                                    RegionID: "CH-6113"}
        ListElement {region: qsTr("obere Maggiatäler");                            RegionID: "CH-6114"}
        ListElement {region: qsTr("untere Leventina");                             RegionID: "CH-6115"}
        ListElement {region: qsTr("untere Maggiatäler");                           RegionID: "CH-6121"}
        ListElement {region: qsTr("Riviera");                                      RegionID: "CH-6122"}
        ListElement {region: qsTr("Luganese");                                     RegionID: "CH-6131"}
        ListElement {region: qsTr("Mendrisiotto");                                 RegionID: "CH-6132"}
        ListElement {region: qsTr("alto Moesano");                                 RegionID: "CH-6211"}
        ListElement {region: qsTr("basso Moesano");                                RegionID: "CH-6212"}
    }

    property ListModel regionListCHENG: ListModel{
        ListElement {region: qsTr("Corvatsch");                                    RegionID: "CH-7111"}
        ListElement {region: qsTr("Bernina");                                      RegionID: "CH-7112"}
        ListElement {region: qsTr("Zuoz");                                         RegionID: "CH-7113"}
        ListElement {region: qsTr("St. Moritz");                                   RegionID: "CH-7114"}
        ListElement {region: qsTr("Val Chamuera");                                 RegionID: "CH-7115"}
        ListElement {region: qsTr("Samnaun");                                      RegionID: "CH-7121"}
        ListElement {region: qsTr("östliche Silvretta");                           RegionID: "CH-7122"}
        ListElement {region: qsTr("Sur Tasna");                                    RegionID: "CH-7123"}
        ListElement {region: qsTr("Val Suot");                                     RegionID: "CH-7124"}
        ListElement {region: qsTr("Val dal Spöl");                                 RegionID: "CH-7125"}
        ListElement {region: qsTr("Val S-charl");                                  RegionID: "CH-7126"}
        ListElement {region: qsTr("Bergell");                                      RegionID: "CH-7211"}
        ListElement {region: qsTr("oberes Puschlav");                              RegionID: "CH-7221"}
        ListElement {region: qsTr("unteres Puschlav");                             RegionID: "CH-7222"}
        ListElement {region: qsTr("Münstertal");                                   RegionID: "CH-7231"}
    }

    property ListModel regionListCHJUR: ListModel{
        ListElement {region: qsTr("Saint-Cergue");                                 RegionID: "CH-8111"}
        ListElement {region: qsTr("Vallée de Joux");                               RegionID: "CH-8112"}
        ListElement {region: qsTr("Yverdon - Bevaix");                             RegionID: "CH-8113"}
        ListElement {region: qsTr("Val de Travers");                               RegionID: "CH-8114"}
        ListElement {region: qsTr("Val de Ruz - Colombier");                       RegionID: "CH-8211"}
        ListElement {region: qsTr("Bienne - Neuchâtel");                           RegionID: "CH-8212"}
        ListElement {region: qsTr("Vallon de Saint-Imier");                        RegionID: "CH-8213"}
        ListElement {region: qsTr("Moutier - Tavannes");                           RegionID: "CH-8214"}
        ListElement {region: qsTr("Thal");                                         RegionID: "CH-8215"}
        ListElement {region: qsTr("Olten-Gösgen");                                 RegionID: "CH-8216"}
        ListElement {region: qsTr("La Chaux-de-Fonds - Le Locle");                 RegionID: "CH-8221"}
        ListElement {region: qsTr("Franches-Montagnes");                           RegionID: "CH-8222"}
        ListElement {region: qsTr("Franches-Montagnes");                           RegionID: "CH-8223"}
        ListElement {region: qsTr("Delémont - Bellelay");                          RegionID: "CH-8224"}
    }

    property ListModel regionListCHMittelland: ListModel{
        ListElement {region: qsTr("westliches Mittelland");                        RegionID: "CH-9111"}
        ListElement {region: qsTr("zentrales Mittelland");                         RegionID: "CH-9112"}
        ListElement {region: qsTr("östliches Mittelland");                         RegionID: "CH-9113"}
    }

    property ListModel regionListLiechtenstein: ListModel{
         ListElement {region: qsTr("Liechtenstein");                               RegionID: "CH-3311"}
    }
    
    // REGIONS France
    property ListModel regionListFrAlpesDuNord: ListModel{
        //Haute Savoie
        ListElement {region: qsTr("CHABLAIS");                                     RegionID: "FR-01"}
        ListElement {region: qsTr("ARAVIS");                                       RegionID: "FR-02"}
        ListElement {region: qsTr("MONT-BLANC");                                   RegionID: "FR-03"}
        //Savoie
        ListElement {region: qsTr("BAUGES");                                       RegionID: "FR-04"}
        ListElement {region: qsTr("BEAUFORTAIN");                                  RegionID: "FR-05"}
        ListElement {region: qsTr("HAUTE-TARENTAISE");                             RegionID: "FR-06"}
        ListElement {region: qsTr("MAURIENNE");                                    RegionID: "FR-09"}
        ListElement {region: qsTr("VANOISE");                                      RegionID: "FR-10"}
        ListElement {region: qsTr("HAUTE-MAURIENNE");                              RegionID: "FR-11"}
        //Isere                                                                    
        ListElement {region: qsTr("CHARTREUSE");                                   RegionID: "FR-07"}
        ListElement {region: qsTr("BELLEDONNE");                                   RegionID: "FR-08"}
        ListElement {region: qsTr("GRANDES-ROUSSES");                              RegionID: "FR-12"}
        ListElement {region: qsTr("VERCORS");                                      RegionID: "FR-14"}
        ListElement {region: qsTr("OISANS");                                       RegionID: "FR-15"}
    }
    
    property ListModel regionListFrAlpesDuSud: ListModel{
        //Hautes Alpes
        ListElement {region: qsTr("THABOR");                                       RegionID: "FR-13"}
        ListElement {region: qsTr("PELVOUX");                                      RegionID: "FR-16"}
        ListElement {region: qsTr("QUEYRAS");                                      RegionID: "FR-17"}
        ListElement {region: qsTr("DEVOLUY");                                      RegionID: "FR-18"}
        ListElement {region: qsTr("CHAMPSAUR");                                    RegionID: "FR-19"}
        ListElement {region: qsTr("EMBRUNAIS-PARPAILLON");                         RegionID: "FR-20"}
        ListElement {region: qsTr("UBAYE");                                        RegionID: "FR-21"}
        //Alpes Maritimes
        ListElement {region: qsTr("HAUT-VAR/HAUT-VERDON");                         RegionID: "FR-22"}
        ListElement {region: qsTr("MERCANTOUR");                                   RegionID: "FR-23"}
    }
    
    property ListModel regionListFrPyrenees: ListModel{
        //Pyrenees Atlantique
        ListElement {region: qsTr("PAYS-BASQUE");                                  RegionID: "FR-64"}
        ListElement {region: qsTr("ASPE-OSSAU");                                   RegionID: "FR-65"}
        //Hautes Pyrenees                                                      
        ListElement {region: qsTr("HAUTE-BIGORRE");                                RegionID: "FR-66"}
        ListElement {region: qsTr("AURE-LOURON");                                  RegionID: "FR-67"}
        //Haute Garonne                                                        
        ListElement {region: qsTr("LUCHONNAIS");                                   RegionID: "FR-68"}
        ListElement {region: qsTr("COUSERANS");                                    RegionID: "FR-69"}
        //Ariege                                                               
        ListElement {region: qsTr("HAUTE-ARIEGE");                                 RegionID: "FR-70"}
        ListElement {region: qsTr("ORLU  ST BARTHELEMY");                          RegionID: "FR-72"}
        //Andorre                                                              
        ListElement {region: qsTr("ANDORRE");                                      RegionID: "FR-71"}
        //Pyrenees Orientales
        ListElement {region: qsTr("CAPCIR-PUYMORENS");                             RegionID: "FR-73"}
        ListElement {region: qsTr("CERDAGNE-CANIGOU");                             RegionID: "FR-74"}
    }
    
    property ListModel regionListFrCorse: ListModel{
        ListElement {region: qsTr("CINTO-ROTONDO");                                RegionID: "FR-40"}
        ListElement {region: qsTr("RENOSO-INCUDINE");                              RegionID: "FR-41"}
    }
}

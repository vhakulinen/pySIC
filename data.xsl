<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
<html>
    <head>
        <title>pySIM</title>
        <style>
            html, body {
                background: #FFF;
                height: 100%;
            }
            body {
                position: relative;
                top: -10px;
            }
            div.content {
                position: relative;
                width: 950px;
                padding: 5px;
                margin: 0px auto;
                box-shadow: 0px 0px 10px #888888;
                min-height: 100%;
            }
            div.content h4 {
                color: #f3265a;
            }
            div.info {
                position: relative;
                left: 15px;
            }
            table th, td {
                text-align: center;
                border: 1px solid black;
            }
            table {
                border-collapse: collapse;
            }
            table#usage {
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <xsl:for-each select="root/data">
                <div class="entry">
                    <h1><xsl:value-of select="sys/hostname"/></h1>
                    <!--<div class="info">-->
                        <!--mem usage: <xsl:value-of select="mem/percent"/>%-->
                    <!--</div>-->
                    <table class="mem">
                        <tr>
                            <th colspan="5">Memory</th>
                        </tr>
                        <tr>
                            <td>total</td>
                            <td>available</td>
                            <td>used</td>
                            <td>free</td>
                            <td>percent</td>
                        </tr>
                        <tr>
                            <td>
                                <xsl:value-of select="mem/total/human"/>
                            </td>
                            <td>
                                <xsl:value-of select="mem/available/human"/>
                            </td>
                            <td>
                                <xsl:value-of select="mem/used/human"/>
                            </td>
                            <td>
                                <xsl:value-of select="mem/free/human"/>
                            </td>
                            <td>
                                <xsl:value-of select="mem/percent"/>%
                            </td>
                        </tr>
                    </table>
                    <table class="cpu">
                        <tr>
                            <th colspan="0">CPU</th>
                        </tr>
                        <tr>
                            <xsl:for-each select="cpu/item">
                            <td>percent</td>
                            </xsl:for-each>
                        </tr>
                        <tr>
                            <xsl:for-each select="cpu/item">
                                <td><xsl:value-of select="percent"/>%</td>
                            </xsl:for-each>
                        </tr>
                    </table>
                    <table class="disks">
                        <tr>
                            <th colspan="5">Disks</th>
                        </tr>
                            <xsl:for-each select="disks/item">
                                <tr>
                                    <td>index</td>
                                    <td>device</td>
                                    <td>mountpoint</td>
                                    <td>fstype</td>
                                    <!--<td>opts</td>-->
                                    <td>usange</td>
                                </tr>
                                <tr>
                                    <td>
                                        <xsl:value-of select="index"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="device"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="mountpoint"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="fstype"/>
                                    </td>
                                    <!--<td>-->
                                        <!--<xsl:value-of select="opts"/>-->
                                    <!--</td>-->
                                    <td>
                                        <!--<xsl:value-of select="usange"/>-->
                                        <table id="usage">
                                            <tr>
                                                <th>free</th>
                                                <th>used</th>
                                                <th>total</th>
                                                <th>percent</th>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <xsl:value-of select="usage/free"/>
                                                </td>
                                                <td>
                                                    <xsl:value-of select="usage/used"/>
                                                </td>
                                                <td>
                                                    <xsl:value-of select="usage/total"/>
                                                </td>
                                                <td>
                                                    <xsl:value-of select="usage/percent"/>%
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </xsl:for-each>
                    </table>
                    <table class="net">
                        <tr>
                            <th colspan="0">Net</th>
                        </tr>
                        <tr>
                            <td>
                            </td>
                            <xsl:for-each select="netio/item">
                                <td colspan="2">
                                    <xsl:value-of select="name"/>
                                </td>
                            </xsl:for-each>
                        </tr>
                        <tr>
                            <td>
                            </td>
                            <xsl:for-each select="netio/item">
                                <td>
                                    total
                                </td>
                                <td>
                                    per-sec
                                </td>
                            </xsl:for-each>
                        </tr>
                        <tr>
                            <td>sent</td>
                            <xsl:for-each select="netio/item">
                                <td>
                                    <xsl:value-of select="total/sent/human"/>
                                </td>
                                <td>
                                    <xsl:value-of select="per-sec/sent/human"/>
                                </td>
                            </xsl:for-each>
                        </tr>
                        <tr>
                            <td>recv</td>
                            <xsl:for-each select="netio/item">
                                <td>
                                    <xsl:value-of select="total/recv/human"/>
                                </td>
                                <td>
                                    <xsl:value-of select="per-sec/recv/human"/>
                                </td>
                            </xsl:for-each>
                        </tr>
                    </table>
                </div>
            </xsl:for-each>
        </div>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>

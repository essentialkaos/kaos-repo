<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
<xsl:output omit-xml-declaration="yes" method="text" indent="no" media-type="text/javascript" encoding="UTF-8"/>
<xsl:strip-space elements="*"/>
<xsl:template match="/icestats">{<xsl:for-each select="source">
  "<xsl:value-of select="@mount"/>": {
    "artist": "<xsl:value-of select="artist"/>",
    "title": "<xsl:value-of select="title"/>",
    "artwork": "<xsl:value-of select="artwork"/>",
    "genre": "<xsl:value-of select="genre"/>"
  }<xsl:if test="position() != last()"><xsl:text>,</xsl:text></xsl:if>
</xsl:for-each>
}
</xsl:template>
</xsl:stylesheet>

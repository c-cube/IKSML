<?xml version='1.0' ?>

<xsl:stylesheet version='1.0' xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <apply>
      <xsl:apply-templates select="apply/*[1]" />
    </apply>
  </xsl:template>
  <xsl:template match="apply">
    <xsl:copy-of select="*" />
    <xsl:copy-of select="following-sibling::node()" />
  </xsl:template>
  <xsl:template match="s">
    <xsl:choose>
      <xsl:when test="count(following-sibling::node())>2">
        <xsl:copy-of select="following-sibling::node()[1]" />
        <xsl:copy-of select="following-sibling::node()[3]" />
        <apply>
          <xsl:copy-of select="following-sibling::node()[2]" />
          <xsl:copy-of select="following-sibling::node()[3]" />
        </apply>
        <xsl:copy-of select="following-sibling::node()[position()>3]" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="../*" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template match="k">
    <xsl:choose>
      <xsl:when test="count(following-sibling::node())>1">
        <xsl:copy-of select="following-sibling::node()[1]" />
        <xsl:copy-of select="following-sibling::node()[position()>2]" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="../*" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>

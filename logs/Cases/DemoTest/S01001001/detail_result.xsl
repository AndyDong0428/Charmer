<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright (C) 2008 The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->

<!DOCTYPE xsl:stylesheet [ <!ENTITY nbsp "&#160;"> ]>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">

        <html>
            <STYLE type="text/css">
                @import "charmer_result.css";
            </STYLE>

            <body>
                <!-- Title of the Report -->
                <DIV id="title">
                    <TABLE>
                        <TR>
                            <TD width="40%" align="left"><img src="logo.png"></img></TD>
                            <TD width="60%" align="left">
                                <h1>Detail Test Report - <xsl:value-of select="TestResult/CaseInfo/CaseID/@name"/>
                                </h1>
                            </TD>
                        </TR>
                    </TABLE>
                </DIV>
                <img src="newrule-green.png" align="left"></img>

                <br></br>
                <br></br>

                <!-- Header with phone and plan information -->
                <DIV id="summary">
                    <TABLE width="90%" frame="none">
                        <TR>
                            <!--<TH>Platform Information</TH>-->
                            <TH>Case Information</TH>
                        </TR>

                        <TR>
                           
                            <TD>
                                <div id="summaryinfo">
                                    <TABLE width="90%">
                                        <TR>
                                            <TD class="rowtitle">Description</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/Description/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Result</TD>
                                            <TD>
																									
                                            	<xsl:choose>
																								<xsl:when test="TestResult/CaseInfo/Result/@name='fail'">
																									<font size="5" color="red">
																										<strong> 
																											<xsl:value-of select="TestResult/CaseInfo/Result/@name"/>
																										</strong>
																										
																									</font>
																								</xsl:when>
																								<xsl:otherwise>
																										<xsl:value-of select="TestResult/CaseInfo/Result/@name"/>
																								</xsl:otherwise>
																							</xsl:choose>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Duration</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/Duration/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Case Timeout</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/Timeout/@name"/> ms
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Type</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/Type/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Error Hanlder</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/ErrorHandler/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Start Time</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/StartTime/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">End Time</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/CaseInfo/EndTime/@name"/>
                                            </TD>
                                        </TR>
                                        
                                    </TABLE>
                                </div>
                            </TD>
                        </TR>
                    </TABLE>
                </DIV>
                
                <xsl:choose>
                <xsl:when test="TestResult/CaseInfo/Performance">
                	<h2 align="center">Performance Report</h2>
	                <DIV id="testsummary">
	                 <TABLE width="90%" frame="none">
	                        <TR>
	                           <TH>PID</TH>
	                           <TH>Process Name</TH>
							   <xsl:for-each select="TestResult/CaseInfo/Performance/Category/Descrip">
									<TH>Max <xsl:value-of select="@name"/></TH>
									<TH>Avg <xsl:value-of select="@name"/></TH>
								</xsl:for-each>
	                        </TR>
													<xsl:for-each select="TestResult/CaseInfo/Performance/Proc">
														<TR>
																<TD><xsl:value-of select="@pid"/></TD>
                                <TD>
                                    <xsl:variable name="detail"><xsl:value-of select="@detail"/></xsl:variable>
                                    <a href="{$detail}"><xsl:value-of select="@name"/></a>
                                </TD>
								
								
								<xsl:for-each select="Category">
									<TD><xsl:value-of select="@maximum"/></TD>
									<TD><xsl:value-of select="@average"/></TD>
								</xsl:for-each>

                            </TR>
													</xsl:for-each>
											</TABLE>
	                
	                </DIV>
                </xsl:when>
								</xsl:choose>
								
                <xsl:choose>
								<xsl:when test="TestResult/CaseInfo/Result/@name='fail' or TestResult/CaseInfo/Result/@name='notExecuted'">
	                <h2 align="center"><font color="red">Error Information</font></h2>
	                
	                 <!-- Header with phone and plan information -->
	                 
	                <DIV id="summary">
	                    <TABLE width="90%" frame="none">
	                        <TR>
	                            <TH>Error Message</TH>
	                           
	                        </TR>
													<TR>
														<TD>
	                                <div id="summaryinfo">
	                                    <TABLE width="90%">
		                                        <TR>
		                                            <TD class="failuredetails">
		                                            	<div id="details">
		                                            		<xsl:value-of select="TestResult/CaseInfo/ErrorMessage/@name"/>
		                                            	</div>
		                                            </TD>
		                                        </TR>
		                            			</TABLE>
		                            	</div>
		                        </TD>
		                      </TR>
	                        <TR>
	                            <TH>Trace Stack</TH>
	                        </TR>
	                        	<TD>
	                                <div id="summaryinfo">
	                                    <TABLE width="90%">
		                           
		                                        <TR>
		                                            <TD class="failuredetails">
		                                            	<div id="details">
		                                            		<xsl:value-of select="TestResult/CaseInfo/TraceStack/@name"/>
		                                            	</div>
		                                            </TD>
		                                        </TR>
		                            			</TABLE>
		                            	</div>
		                        </TD>
								
	                    </TABLE>
						<img src="failed.bmp" style="display:block; margin:auto;"></img>
	                </DIV>

	              </xsl:when>
								</xsl:choose>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="filteredResultTestReport">
        <xsl:param name="header" />
        <xsl:param name="resultFilter" />
        <xsl:variable name="numMatching" select="count(TestResult/TestPackage/TestSuite//TestCase/Test[@result=$resultFilter])" />
        <xsl:if test="$numMatching &gt; 0">
            <h2 align="center"><xsl:value-of select="$header" /> (<xsl:value-of select="$numMatching"/>)</h2>
            <xsl:call-template name="detailedTestReport">
                <xsl:with-param name="resultFilter" select="$resultFilter"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

    <xsl:template name="detailedTestReport">
        <xsl:param name="resultFilter" />
        <DIV id="testdetail">
            <xsl:for-each select="TestResult/TestPackage">
                <xsl:if test="$resultFilter=''
                        or count(TestSuite//TestCase/Test[@result=$resultFilter]) &gt; 0">
                    <DIV id="none">
                        <TABLE>
                            <TR>
                                <TD class="none" align="left">
                                    <xsl:variable name="href"><xsl:value-of select="@name"/></xsl:variable>
                                    <a name="{$href}">Compatibility Test Package: <xsl:value-of select="@name"/></a>
                                </TD>
                            </TR>
                        </TABLE>
                    </DIV>

                    <TABLE>
                        <TR>
                            <TH width="25%">Test</TH>
                            <TH width="7%">Result</TH>
                            <TH width="68%">Failure Details</TH>
                        </TR>

                        <!-- test case -->
                        <xsl:for-each select="TestSuite//TestCase">

                            <xsl:if test="$resultFilter='' or count(Test[@result=$resultFilter]) &gt; 0">
                                <!-- emit a blank row before every test suite name -->
                                <xsl:if test="position()!=1">
                                    <TR><TD class="testcasespacer" colspan="3"></TD></TR>
                                </xsl:if>

                                <TR>
                                    <TD class="testcase" colspan="3">
                                        <!--<xsl:for-each select="ancestor::TestSuite">
                                            <xsl:if test="position()!=1">.</xsl:if>
                                            <xsl:value-of select="@name"/>
                                        </xsl:for-each>-->
                                        <xsl:text>.</xsl:text>
                                        <xsl:value-of select="@name"/>
                                    </TD>
                                </TR>
                            </xsl:if>

                            <!-- test -->
                            <xsl:for-each select="Test">
                                <xsl:if test="$resultFilter='' or $resultFilter=@result">
                                    <TR>
                                        <TD class="testname"> -- <xsl:value-of select="@name"/></TD>

                                        <!-- test results -->
                                        <xsl:choose>
                                            <xsl:when test="string(@KnownFailure)">
                                                <!-- "pass" indicates the that test actually passed (results have been inverted already) -->
                                                <xsl:if test="@result='pass'">
                                                    <TD class="pass">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            known problem
                                                        </div>
                                                    </TD>
                                                    <TD class="failuredetails"></TD>
                                                </xsl:if>

                                                <!-- "fail" indicates that a known failure actually passed (results have been inverted already) -->
                                                <xsl:if test="@result='fail'">
                                                    <TD class="failed">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            <xsl:value-of select="@result"/>
                                                        </div>
                                                    </TD>
                                                   <TD class="failuredetails">
                                                        <div id="details">
                                                            A test that was a known failure actually passed. Please check.
                                                        </div>
                                                   </TD>
                                                </xsl:if>
                                            </xsl:when>

                                            <xsl:otherwise>
                                                <xsl:if test="@result='pass'">
                                                    <TD class="pass">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            <xsl:value-of select="@result"/>
                                                        </div>
                                                    </TD>
                                                    <TD class="failuredetails"></TD>
                                                </xsl:if>

                                                <xsl:if test="@result='fail'">
                                                    <TD class="failed">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            <xsl:value-of select="@result"/>
                                                        </div>
                                                    </TD>
                                                    <TD class="failuredetails">
                                                        <div id="details">
                                                            <xsl:value-of select="FailedScene/@message"/>
                                                        </div>
                                                    </TD>
                                                </xsl:if>

                                                <xsl:if test="@result='timeout'">
                                                    <TD class="timeout">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            <xsl:value-of select="@result"/>
                                                        </div>
                                                    <TD class="failuredetails"></TD>
                                                    </TD>
                                                </xsl:if>

                                                <xsl:if test="@result='notExecuted'">
                                                    <TD class="notExecuted">
                                                        <div style="text-align: center; margin-left:auto; margin-right:auto;">
                                                            <xsl:value-of select="@result"/>
                                                        </div>
                                                    </TD>
                                                    <TD class="failuredetails"></TD>
                                                </xsl:if>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </TR> <!-- finished with a row -->
                                </xsl:if>
                            </xsl:for-each> <!-- end test -->
                        </xsl:for-each> <!-- end test case -->
                    </TABLE>
                </xsl:if>
            </xsl:for-each> <!-- end test package -->
        </DIV>
    </xsl:template>

    <!-- Take a delimited string and insert line breaks after a some number of elements. --> 
    <xsl:template name="formatDelimitedString">
        <xsl:param name="string" />
        <xsl:param name="numTokensPerRow" select="10" />
        <xsl:param name="tokenIndex" select="1" />
        <xsl:if test="$string">
            <!-- Requires the last element to also have a delimiter after it. -->
            <xsl:variable name="token" select="substring-before($string, ';')" />
            <xsl:value-of select="$token" />
            <xsl:text>&#160;</xsl:text>
          
            <xsl:if test="$tokenIndex mod $numTokensPerRow = 0">
                <br />
            </xsl:if>

            <xsl:call-template name="formatDelimitedString">
                <xsl:with-param name="string" select="substring-after($string, ';')" />
                <xsl:with-param name="numTokensPerRow" select="$numTokensPerRow" />
                <xsl:with-param name="tokenIndex" select="$tokenIndex + 1" />
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>

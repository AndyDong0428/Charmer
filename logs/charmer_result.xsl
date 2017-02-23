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
                                <h1>Test Report of <xsl:value-of select="TestResult/DeviceInfo/BuildInfo/@build_model"/> -
                                    <xsl:value-of select="TestResult/DeviceInfo/BuildInfo/@deviceID"/>
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
                            <TH>Platform Information</TH>
                            <TH>Test Summary</TH>
                        </TR>

                        <TR>
                            <TD>
                                <!-- Device information -->
                                <div id="summaryinfo">
                                    <TABLE width="75%">
                                    		
                                        <TR>
                                            <TD class="rowtitle">Platform</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/DeviceInfo/BuildInfo/@deviceID"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Host Info</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/HostInfo/@name"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Application Version</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/DeviceInfo/BuildInfo/@buildVersion"/>
                                            </TD>
                                        </TR>
                                        
                                        <TR>
                                            <TD class="rowtitle">Locales</TD>
                                            <TD>
                                                <xsl:call-template name="formatDelimitedString">
                                                    <xsl:with-param name="string" select="TestResult/DeviceInfo/BuildInfo/@locales"/>
                                                </xsl:call-template>
                                            </TD>
                                        </TR>
                                        
                                        <TR>
                                            <TD class="rowtitle">Network IP</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/DeviceInfo/BuildInfo/@network"/>
                                            </TD>
                                        </TR>
                                        
                                        <TR>
                                            <TD class="rowtitle">Features</TD>
                                            <TD>
                                                <xsl:for-each select="TestResult/DeviceInfo/FeatureInfo/Feature[@type='sdk']">
                                                    <xsl:text>[</xsl:text>
                                                    <xsl:choose>
                                                        <xsl:when test="@available = 'true'">
                                                            <xsl:text>X</xsl:text>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:text>_</xsl:text>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                    <xsl:text>] </xsl:text>

                                                    <xsl:value-of select="@name" />
                                                    <br />
                                                </xsl:for-each>
                                            </TD>
                                        </TR>
                                        
                                        <TR>
                                            <TD class="rowtitle">Partitions</TD>
                                            <TD>
                                                <UL>
                                                    <pre>
                                                        <xsl:call-template name="formatDelimitedString">
                                                            <xsl:with-param name="string" select="TestResult/DeviceInfo/BuildInfo/@partitions" />
                                                            <xsl:with-param name="numTokensPerRow" select="1" />
                                                        </xsl:call-template>
                                                    </pre>
                                                </UL>
                                            </TD>
                                        </TR>
                                    </TABLE>
                                </div>
                            </TD>

                            <!-- plan information -->
                            <TD>
                                <div id="summaryinfo">
                                    <TABLE width="75%">
                                        <TR>
                                            <TD class="rowtitle">Charmer version</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/HostInfo/Charmer/@version"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Test timeout</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/HostInfo/Charmer/IntValue[@name='testStatusTimeoutMs']/@value" /> ms
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Memory Boundary</TD>
                                            <TD>
                                                
                                                <UL>
                                                    <pre>
                                                        <xsl:call-template name="formatDelimitedString">
                                                            <xsl:with-param name="string" select="TestResult/HostInfo/Charmer/IntValue[@name='testMonitorPerf']/@value" />
                                                            <xsl:with-param name="numTokensPerRow" select="1" />
                                                        </xsl:call-template>
                                                    </pre>
                                                </UL>
                                                
                                            </TD>
                                        </TR>
                                        
                                        <TR><TD><BR></BR></TD><TD></TD></TR>
                                        <TR>
                                            <TD class="rowtitle">Plan name</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/@testPlan"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Start time</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/@starttime"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">End time</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/@endtime"/>
                                            </TD>
                                        </TR>

                                        <!-- Test Summary -->
                                        <TR><TD><BR></BR></TD><TD></TD></TR>
                                        <TR>
                                            <TD class="rowtitle">Tests Passed</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/Summary/@pass"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Tests Failed</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/Summary/@failed"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Tests Timed out</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/Summary/@timeout"/>
                                            </TD>
                                        </TR>
                                        <TR>
                                            <TD class="rowtitle">Tests Not Executed</TD>
                                            <TD>
                                                <xsl:value-of select="TestResult/Summary/@notExecuted"/>
                                            </TD>
                                        </TR>
                                    </TABLE>
                                </div>
                            </TD>
                        </TR>
                    </TABLE>
                </DIV>
								
								<xsl:choose>
                <xsl:when test="TestResult/Performance">
                	<h2 align="center">Performance Report</h2>
	                <DIV id="testsummary">
	                 <TABLE width="90%" frame="none">
	                        <TR>
	                           <TH>Process Name</TH>
							   <xsl:for-each select="TestResult/Performance/Category/Descrip">
									<TH>Max <xsl:value-of select="@name"/></TH>
									<TH>Avg <xsl:value-of select="@name"/></TH>
							   </xsl:for-each>
	                           <!--<TH>Maximum WorkingSet (MB)</TH>
	                           <TH>Average WorkingSet (MB)</TH>-->
	                        </TR>
													<xsl:for-each select="TestResult/Performance/Proc">
														<TR>
                                <TD><xsl:value-of select="@name"/></TD>
                                <xsl:for-each select="Category">
									<TD><xsl:value-of select="@maximum"/></TD>
									<TD><xsl:value-of select="@average"/></TD>
								</xsl:for-each>
                                <!--<TD><xsl:value-of select="@maximum"/></TD>
                                <TD><xsl:value-of select="@average"/></TD>-->
                            </TR>
													</xsl:for-each>
											</TABLE>
	                
	                </DIV>
                </xsl:when>
								</xsl:choose>
								
                <!-- High level summary of test execution -->
                <h2 align="center">Test Summary by Package</h2>
                <DIV id="testsummary">
                    <TABLE>
                        <TR>
                            <TH>Test Package</TH>
                            <TH>Passed</TH>
                            <TH>Failed</TH>
                            <TH>Timed Out</TH>
                            <TH>Total Tests</TH>
                        </TR>
                        <xsl:for-each select="TestResult/TestPackage">
                            <TR>
                                <TD>
                                    <xsl:variable name="href"><xsl:value-of select="@name"/></xsl:variable>
                                    <a href="#{$href}"><xsl:value-of select="@name"/></a>
                                </TD>
                                <TD>
                                    <xsl:value-of select="count(TestSuite//Test[@result = 'pass'])"/>
                                </TD>
                                <TD>
                                    <xsl:value-of select="count(TestSuite//Test[@result = 'fail'])"/>
                                </TD>
                                <TD>
                                    <xsl:value-of select="count(TestSuite//Test[@result = 'timeout'])"/>
                                </TD>
                                <TD>
                                    <xsl:value-of select="count(TestSuite//Test)"/>
                                </TD>
                            </TR>
                        </xsl:for-each> <!-- end package -->
                    </TABLE>
                </DIV>

                <xsl:call-template name="filteredResultTestReport">
                    <xsl:with-param name="header" select="'Test Failures'" />
                    <xsl:with-param name="resultFilter" select="'fail'" />
                </xsl:call-template>

                <xsl:call-template name="filteredResultTestReport">
                    <xsl:with-param name="header" select="'Test Timeouts'" />
                    <xsl:with-param name="resultFilter" select="'timeout'" />
                </xsl:call-template>

                <h2 align="center">Detailed Test Report</h2>
                <xsl:call-template name="detailedTestReport" />

            </body>
        </html>
    </xsl:template>

    <xsl:template name="filteredResultTestReport">
        <xsl:param name="header" />
        <xsl:param name="resultFilter" />
        <xsl:variable name="numMatching" select="count(TestResult/TestPackage/TestSuite//Test[@result=$resultFilter])" />
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
                        or count(TestSuite//Test[@result=$resultFilter]) &gt; 0">
                    <DIV id="none">
                        <TABLE>
                            <TR>
                                <TD class="none" align="left">
                                    <xsl:variable name="href"><xsl:value-of select="@name"/></xsl:variable>
                                    <a name="{$href}">Test Package: <xsl:value-of select="@name"/></a>
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
                        <xsl:for-each select="TestSuite">

                            <xsl:if test="$resultFilter='' or count(Test[@result=$resultFilter]) &gt; 0">
                                <!-- emit a blank row before every test suite name -->
                                <xsl:if test="position()!=1">
                                    <TR><TD class="testcasespacer" colspan="3"></TD></TR>
                                </xsl:if>

                            </xsl:if>

                            <!-- test -->
                            <xsl:for-each select="Test">
                                <xsl:if test="$resultFilter='' or $resultFilter=@result">
                                    <TR>
                                        <TD class="testname">
																							<xsl:variable name="log"><xsl:value-of select="@logPath"/></xsl:variable>
                                    					<a href="{$log}"><xsl:value-of select="@name"/></a>
                                    		</TD>
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
                                                            <xsl:value-of select="@message"/>
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

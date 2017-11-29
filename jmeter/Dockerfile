FROM openjdk:8

LABEL maintainer="Dina" description="For creating fresh jmeter image with plugins installed."

ARG JMETER_VERSION=3.3
ENV JMETER_HOME /opt/apache-jmeter-$JMETER_VERSION
ENV JMETER_BIN ${JMETER_HOME}/bin
ENV JMETER_DOWNLOAD_URL http://apache.mirror.amaze.com.au/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz
# http://apache.mirror.amaze.com.au//jmeter/binaries/apache-jmeter-3.3.tgz

# download jmeter
ADD ${JMETER_DOWNLOAD_URL} /tmp/
# ADD cmdrunner-2.0.jar /tmp/
# ADD jmeter-plugins-manager-0.16.jar /tmp/

# download jmeter plugin manager
ADD http://search.maven.org/remotecontent?filepath=kg/apc/cmdrunner/2.0/cmdrunner-2.0.jar /tmp/cmdrunner-2.0.jar
ADD http://search.maven.org/remotecontent?filepath=kg/apc/jmeter-plugins-manager/0.16/jmeter-plugins-manager-0.16.jar /tmp/jmeter-plugins-manager-0.16.jar

RUN 	mkdir ${JMETER_HOME} && \
        tar -xzf /tmp/apache-jmeter-${JMETER_VERSION}.tgz -C /opt/ && \
        mkdir "${JMETER_HOME}/scripts" && \ 
	# mkdir ${JMETER_HOME}/lib/ext && \


        mv "/tmp/cmdrunner-2.0.jar" "${JMETER_HOME}/lib" && \
        mv "/tmp/jmeter-plugins-manager-0.16.jar" "${JMETER_HOME}/lib/ext" 
RUN 	java -cp ${JMETER_HOME}/lib/ext/jmeter-plugins-manager-0.16.jar org.jmeterplugins.repository.PluginManagerCMDInstaller && \
	# ${JMETER_HOME}/bin/PluginsManagerCMD.sh status && \
	# Install jmeter plugins
	${JMETER_HOME}/bin/PluginsManagerCMD.sh install jpgc-graphs-basic,jpgc-graphs-additional,jpgc-sense,jpgc-graphs-composite,jpgc-functions,jpgc-casutg,jpgc-dbmon,jpgc-graphs-dist,jpgc-dummy,jmeter-ftp,jpgc-ffw,jmeter-http,jpgc-fifo,jmeter-jdbc,jmeter-jms,jmeter-core,jpgc-json,jmeter-junit,jmeter-java,jmeter-ldap,jmeter-mail,jmeter-mongodb,jmeter-native,jpgc-perfmon,jpgc-plugins-manager,jmeter-tcp,jpgc-tst,jmeter-components,jpgc-xml,jpgc-standard && sleep 10  && \
        # export PATH=$PATH:${JMETER_HOME}
	rm -rf /tmp/*

ENV PATH=$PATH:${JMETER_HOME}/bin
WORKDIR ${JMETER_HOME}/bin


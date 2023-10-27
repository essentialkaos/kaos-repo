# Set JAVA_HOME to the latest available version
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s#/bin/java##")

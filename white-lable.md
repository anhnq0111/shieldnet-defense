diff --git a/framework/setup.py b/framework/setup.py
index 357e9de4f0..5ad3c3f3ac 100755
--- a/framework/setup.py
+++ b/framework/setup.py
@@ -4,12 +4,17 @@
 # Created by Wazuh, Inc. <info@wazuh.com>.
 # This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
 
-from wazuh import __version__
+import re
+
+def _get_version():
+    with open('wazuh/__init__.py', 'r') as f:
+        match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE)
+        return match.group(1) if match else '0.0.0'
 
 from setuptools import setup, find_namespace_packages
 
 setup(name='wazuh',
-      version=__version__,
+      version=_get_version(),
       description='Wazuh control with Python',
       url='https://github.com/wazuh',
       author='Wazuh',
diff --git a/src/Makefile b/src/Makefile
index 79fb6d5ceb..f25675d139 100644
--- a/src/Makefile
+++ b/src/Makefile
@@ -2512,6 +2512,13 @@ else
 	cp external/${WPYTHON_TAR} ${WPYTHON_DIR}/${WPYTHON_TAR} && ${TAR} ${WPYTHON_DIR}/${WPYTHON_TAR} -C ${WPYTHON_DIR} && rm -rf ${WPYTHON_DIR}/${WPYTHON_TAR}
 endif
 	find ${WPYTHON_DIR} -name "*${WLIBPYTHON}" -exec ln -f {} ${INSTALLDIR}/lib/${WLIBPYTHON} \;
+	@# Create compat symlinks for pre-built Python binary (linked against original lib name)
+	@if [ -f ${WPYTHON_DIR}/bin/python3 ] && [ -f ${INSTALLDIR}/lib/${WAZUHEXT_LIB} ]; then \
+		for dep in $$(ldd ${WPYTHON_DIR}/bin/python3 2>/dev/null | grep 'not found' | awk '{print $$1}'); do \
+			echo "Creating compat symlink: $$dep -> ${WAZUHEXT_LIB}"; \
+			ln -sf ${WAZUHEXT_LIB} ${INSTALLDIR}/lib/$$dep; \
+		done; \
+	fi
 
 python_dependencies := requirements.txt
 
diff --git a/src/init/inst-functions.sh b/src/init/inst-functions.sh
index a4afc5d0c8..8c0ac962b8 100644
--- a/src/init/inst-functions.sh
+++ b/src/init/inst-functions.sh
@@ -1199,7 +1199,7 @@ InstallLocal()
     ${INSTALL} -d -m 0770 -o ${WAZUH_USER} -g ${WAZUH_GROUP} ${INSTALLDIR}/queue/tasks
 
     ### Install Python
-    ${MAKEBIN} wpython INSTALLDIR=${INSTALLDIR} TARGET=${INSTYPE}
+    ${MAKEBIN} wpython INSTALLDIR=${INSTALLDIR} TARGET=${INSTYPE} || { echo "ERROR: Python package installation failed." >&2; exit 1; }
 
     ${MAKEBIN} --quiet -C ../framework install INSTALLDIR=${INSTALLDIR}
 

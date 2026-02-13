# ShieldnetDefend Filebeat module

## Hosting

The ShieldnetDefend Filebeat module is hosted at the following URLs

- Production:
  - https://packages.wazuh.com/4.x/filebeat/
- Development:
  - https://packages-dev.shieldnetdefend.com/pre-release/filebeat/
  - https://packages-dev.shieldnetdefend.com/staging/filebeat/

The ShieldnetDefend Filebeat module must follow the following nomenclature, where revision corresponds to X.Y values

- shieldnet-defend-filebeat-{revision}.tar.gz

Currently, we host the following modules

|Module|Version|
|:--|:--|
|shieldnet-defend-filebeat-0.1.tar.gz|From 3.9.x to 4.2.x included|
|shieldnet-defend-filebeat-0.2.tar.gz|From 4.3.x to 4.6.x included|
|shieldnet-defend-filebeat-0.3.tar.gz|4.7.x|
|shieldnet-defend-filebeat-0.4.tar.gz|From 4.8.x to current|


## How-To update module tar.gz file

To add a new version of the module it is necessary to follow the following steps:

1. Clone the shieldnetdefend/shieldnetdefend repository
2. Check out the branch that adds a new version
3. Access the directory: **extensions/filebeat/7.x/shieldnet-defend-module/**
4. Create a directory called: **shieldnet**

```
# mkdir shieldnetdefend
```

5. Copy the resources to the **shieldnet** directory

```
# cp -r _meta shieldnetdefend/
# cp -r alerts shieldnetdefend/
# cp -r archives shieldnetdefend/
# cp -r module.yml shieldnetdefend/
```

6. Set **root user** and **root group** to all elements of the **shieldnet** directory (included)

```
# chown -R root:root shieldnetdefend
```

7. Set all directories with **755** permissions

```
# chmod 755 shieldnetdefend
# chmod 755 shieldnetdefend/alerts
# chmod 755 shieldnetdefend/alerts/config
# chmod 755 shieldnetdefend/alerts/ingest
# chmod 755 shieldnetdefend/archives
# chmod 755 shieldnetdefend/archives/config
# chmod 755 shieldnetdefend/archives/ingest
```

8. Set all yml/json files with **644** permissions

```
# chmod 644 shieldnetdefend/module.yml
# chmod 644 shieldnetdefend/_meta/config.yml
# chmod 644 shieldnetdefend/_meta/docs.asciidoc
# chmod 644 shieldnetdefend/_meta/fields.yml
# chmod 644 shieldnetdefend/alerts/manifest.yml
# chmod 644 shieldnetdefend/alerts/config/alerts.yml
# chmod 644 shieldnetdefend/alerts/ingest/pipeline.json
# chmod 644 shieldnetdefend/archives/manifest.yml
# chmod 644 shieldnetdefend/archives/config/archives.yml
# chmod 644 shieldnetdefend/archives/ingest/pipeline.json
```

9. Create **tar.gz** file

```
# tar -czvf shieldnet-defend-filebeat-0.4.tar.gz shieldnetdefend
```

10. Check the user, group, and permissions of the created file

```
# tree -pug shieldnetdefend
[drwxr-xr-x root     root    ]  shieldnetdefend
├── [drwxr-xr-x root     root    ]  alerts
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  alerts.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  archives
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  archives.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  _meta
│   ├── [-rw-r--r-- root     root    ]  config.yml
│   ├── [-rw-r--r-- root     root    ]  docs.asciidoc
│   └── [-rw-r--r-- root     root    ]  fields.yml
└── [-rw-r--r-- root     root    ]  module.yml
```

11. Upload file to development bucket

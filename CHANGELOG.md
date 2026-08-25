# Alfresco\.Platform Release Notes

**Topics**

- <a href="#v0-6-0">v0\.6\.0</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
- <a href="#v0-5-0">v0\.5\.0</a>
    - <a href="#major-changes">Major Changes</a>
- <a href="#v0-4-1">v0\.4\.1</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v0-4-0">v0\.4\.0</a>
    - <a href="#major-changes-1">Major Changes</a>
    - <a href="#security-fixes">Security Fixes</a>
- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#minor-changes-2">Minor Changes</a>
- <a href="#v0-2-3">v0\.2\.3</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v0-2-2">v0\.2\.2</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v0-2-1">v0\.2\.1</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#major-changes-2">Major Changes</a>
    - <a href="#minor-changes-4">Minor Changes</a>
- <a href="#v0-1-1">v0\.1\.1</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#major-changes-3">Major Changes</a>

<a id="v0-6-0"></a>
## v0\.6\.0

<a id="minor-changes"></a>
### Minor Changes

* audit\_storage\, search\_community\, cic\_connector \- default the Nexus artifact host to <code>artifacts\.alfresco\.com</code>\, matching every other role\'s production URL\, and add <code>audit\_storage\_repository\_url</code> so downstream playbooks can override just the repository base instead of the full <code>audit\_storage\_zip\_url</code>\.
* cic\_connector \- move the <code>org/alfresco</code> path segment into <code>cic\_connector\_artifact\_repository\_url</code> itself\, so the variable can be overridden with any repository style base URL without producing a duplicated path\. A trailing slash on the override\, previously required\, is now optional and stripped automatically\, so existing overrides keep working unchanged\.
* search\_community \- default <code>search\_community\_repository\_url</code> to the <code>/nexus/repository/releases/</code> path instead of the legacy Nexus 2 style <code>/nexus/content/repositories/releases/</code>\.

<a id="deprecated-features"></a>
### Deprecated Features

* search\_community \- <code>search\_community\_repository</code> is deprecated in favor of <code>search\_community\_repository\_url</code>\, matching <code>cic\_connector</code>\'s <code>\_url</code> suffix convention\. The old variable name is still honored as a fallback and will be removed in a future major release\.

<a id="v0-5-0"></a>
## v0\.5\.0

<a id="major-changes"></a>
### Major Changes

* add cic\_connector role deploying the Content Intelligence Connector live\-ingester\, bulk\-ingester and nucleus\-sync services
* remove the <code>hxi\_connector</code> role\, superseded by the <code>cic\_connector</code> role

<a id="v0-4-1"></a>
## v0\.4\.1

<a id="minor-changes-1"></a>
### Minor Changes

* search\_community \- add <code>search\_community\_transform\_enabled</code> to toggle the accepted content media types cache via the <code>ALFRESCO\_ACCEPTEDCONTENTMEDIATYPESCACHE\_ENABLED</code> environment variable\.
* search\_community \- add <code>search\_community\_transform\_url</code> to configure the Alfresco transform config endpoint\, mapped to the batch indexing service\'s <code>ALFRESCO\_ACCEPTEDCONTENTMEDIATYPESCACHE\_BASEURL</code> environment variable so it can discover the content media types it is able to transform\.
* search\_community \- bump the batch indexing distribution to the released <code>5\.7\.0</code> version \(previously the <code>5\.7\.0\-A\.5</code> pre\-release\)\.

<a id="v0-4-0"></a>
## v0\.4\.0

<a id="major-changes-1"></a>
### Major Changes

* Add search\_community service role

<a id="security-fixes"></a>
### Security Fixes

* systemd\_service \- write the service environment \(including database and other credentials\) to a root\-owned <code>EnvironmentFile</code> with mode <code>0600</code> referenced from the unit\, instead of embedding it as <code>Environment\=</code> lines in the world\-readable \(<code>0644</code>\) unit file\.

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="minor-changes-2"></a>
### Minor Changes

* Bump Java to 17\.0\.18

<a id="v0-2-3"></a>
## v0\.2\.3

<a id="bugfixes"></a>
### Bugfixes

* Revert ActiveMQ username key for audit storage\. Add SPRING\_PROFILES\_ACTIVE variable to enable audit picking default ingestion URI\.

<a id="v0-2-2"></a>
## v0\.2\.2

<a id="bugfixes-1"></a>
### Bugfixes

* Fix startup issue in audit storage by not overriding eventIngestion uri and fixing username key

<a id="v0-2-1"></a>
## v0\.2\.1

<a id="minor-changes-3"></a>
### Minor Changes

* Allow usage of community\.general v11

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="major-changes-2"></a>
### Major Changes

* Add audit\_storage service role

<a id="minor-changes-4"></a>
### Minor Changes

* Use common java home argument across roles and rely on default java version coming from role defaults

<a id="v0-1-1"></a>
## v0\.1\.1

<a id="minor-changes-5"></a>
### Minor Changes

* Allow using an existing handler to trigger the restart of the Alfresco service after installing the repository extension to prevent unwanted restarts\.

<a id="bugfixes-2"></a>
### Bugfixes

* Fix idempotency issue in hxi extension entrypoint
* Remove unnecessary mandatory args for hxi connector

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="major-changes-3"></a>
### Major Changes

* add hxi\_connector service role
* add java role
* add repository\-extension task list to configure alfresco extension
* add systemd service role

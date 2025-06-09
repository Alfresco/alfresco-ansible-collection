# Alfresco\.Platform Release Notes

**Topics**

- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v0-1-1">v0\.1\.1</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#major-changes-1">Major Changes</a>

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="major-changes"></a>
### Major Changes

* Add audit\_storage service role

<a id="minor-changes"></a>
### Minor Changes

* Use common java home argument across roles and rely on default java version coming from role defaults

<a id="v0-1-1"></a>
## v0\.1\.1

<a id="minor-changes-1"></a>
### Minor Changes

* Allow using an existing handler to trigger the restart of the Alfresco service after installing the repository extension to prevent unwanted restarts\.

<a id="bugfixes"></a>
### Bugfixes

* Fix idempotency issue in hxi extension entrypoint
* Remove unnecessary mandatory args for hxi connector

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="major-changes-1"></a>
### Major Changes

* add hxi\_connector service role
* add java role
* add repository\-extension task list to configure alfresco extension
* add systemd service role

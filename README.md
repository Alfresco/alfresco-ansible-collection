# Ansible Collection - alfresco.platform

This Ansible collection provides a set of roles and modules to manage
Alfresco Platform installations. It is designed to be used with Ansible
and can be easily integrated into your existing Ansible playbooks.

## Development

### Prerequisites

This repo use [uv](https://docs.astral.sh/uv/) as python package and project manager.

Install it with:

```bash
brew install uv
```

Install the required python version with:

```bash
uv python install
```

Use the `uv run` prefix to run any command in the virtual environment, e.g.:

```bash
uv run ansible-galaxy install
```

## Releases

For every change, a changelog yml fragment need to be drop inside the
`changelogs/fragments` folder, using one or more [fragment
categories](https://ansible.readthedocs.io/projects/antsibull-changelog/changelogs/#changelog-fragment-categories).

Before proceeding with the release, merge the fragments into the changelog with:

```bash
antsibull-changelog release --version 0.1.0
```

Then, update the version in `galaxy.yml`.

```yaml
version: 0.1.0
```

Finally, draft the github release with:

```bash
gh release create v0.1.0
```

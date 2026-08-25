# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, GitHub Copilot, etc.) when working with code in this repository.

## What this is

`alfresco.platform` — an Ansible collection providing roles to install and configure Alfresco Content Services (ACS) platform components. Published to Ansible Galaxy; source of truth is `galaxy.yml` for version/metadata.

## Setup

Uses [uv](https://docs.astral.sh/uv/) for the Python toolchain (ansible-core, ansible-lint, molecule, antsibull-changelog, docs tooling — versions pinned in `pyproject.toml`).

```bash
uv python install        # install the pinned python version
uv run ansible-galaxy install
```

Prefix all tool invocations with `uv run` (e.g. `uv run ansible-lint`, `uv run molecule test`).

## Common commands

```bash
# Lint (production profile — same as CI)
uv run ansible-lint --profile production

# Pre-commit (yaml/json/xml checks, jinja lint via djlint, markdown lint, ansible-lint)
uv run pre-commit run --all-files

# Molecule test for a single role (must run from the role directory)
cd roles/<role_name> && uv run molecule test

# Build the collection tarball
uv run ansible-galaxy collection build
```

There is no single "test everything" command — CI runs sanity tests (via `ansible-test`, matrixed across ansible-core stable-2.16/2.17/2.18) and molecule separately per role. To exercise one role end-to-end, use the molecule command above; molecule scenarios spin up Docker containers (a systemd-enabled target instance plus any backing services like Elasticsearch/Postgres) defined in that role's `molecule/default/molecule.yml`.

## Releasing

Every PR that changes a role must add a changelog fragment in `changelogs/fragments/` (see [antsibull-changelog fragment categories](https://ansible.readthedocs.io/projects/antsibull-changelog/changelogs/#changelog-fragment-categories)) — this is called out in the PR template.

The release itself is a separate PR:

1. `uv run antsibull-changelog release --version X.Y.Z` to merge all pending fragments into `CHANGELOG.md`.
2. Bump `version` in `galaxy.yml` to `X.Y.Z`.
3. Open and merge that PR.
4. Only after merging, `gh release create vX.Y.Z` from `main` — tagging `v*` triggers the `build` workflow to publish to Galaxy (only from `alfresco/alfresco-ansible-collection`, tag push).

## Architecture

### Role layout

Each role under `roles/<name>/` follows the standard Ansible role structure: `defaults/main.yml` (public, overridable vars, all prefixed `<role_name>_...`), `vars/main.yml` (internal/derived vars), `tasks/main.yml`, `meta/main.yml` (galaxy_info + role `dependencies`), `meta/argument_specs.yml` (typed/validated role interface — keep in sync with `defaults`), and a per-role `README.md` documenting requirements, dependencies, and example playbook usage. Roles that install a long-running process ship their own `molecule/default/` scenario.

### Role composition

Roles compose via `ansible.builtin.include_role`, not raw templates duplicated per role. The recurring pattern: an application role (e.g. `search_community`, `cic_connector`) downloads/installs its binary/artifact, then delegates unit creation to the shared `systemd_service` role, passing its own `<role>_systemd_service_*` defaults through as `vars:` on the `include_role`. When changing how a service's systemd unit is defined, change `systemd_service` once rather than per-role.

The `java` role is a shared dependency (installs the JVM); roles needing a JVM document it as a soft dependency in their README and expect `<role>_java_home_path`/`<role>_java_bin_path` to be supplied rather than hard-declaring it in `meta/main.yml` `dependencies`.

### Artifact downloads

Roles that fetch a distribution artifact (e.g. `search_community`) download from Alfresco's Nexus repository (`artifacts.alfresco.com`) via `ansible.builtin.get_url`, with `<role>_nexus_username`/`_nexus_password` defaults (empty by default, `| default(omit)` at the task level) and a checksum default derived from the artifact URL (`sha1:{{ ..._zip_url }}.sha1`). Follow this shape for any new artifact-fetching role rather than inventing a new download convention.

### CI (`.github/workflows/build.yml`)

`pre-commit`, `sanity` (ansible-test across 3 ansible-core versions), and `molecule` (one matrix entry per role with a molecule scenario) all gate the `build` job. When adding a role with a molecule scenario, add it to the `molecule` job's matrix in `build.yml` or it won't run in CI. Third-party GitHub Actions are SHA-pinned with the version as a trailing comment.

### Docs

`.github/workflows/docs.yml` builds and publishes collection docs via `ansible-community/github-docs-build` to GitHub Pages, driven off role `README.md`/`argument_specs.yml` content — no separate hand-written docs source beyond what lives in the roles.

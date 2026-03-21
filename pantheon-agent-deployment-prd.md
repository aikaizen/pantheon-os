# PRD — Pantheon Agent Deployment Layer

## Product summary
A deployment layer for PantheonOS that lets operators run agent estates inside Docker regardless of whether the underlying orchestrator is Hermes, OpenClaw, NanoClaw, or PantheonOS itself.

PantheonOS remains the shared observation and intervention surface. But for deployment, PantheonOS should white-label Hermes as the default packaged runtime so new and existing operators can deploy agents through a coherent Pantheon-branded flow.

## Problem
PantheonOS now has a better model for persona agents, runtimes, controllers, channels, and bindings. But deployment is still underspecified.

Operators will arrive in at least four runtime situations:
- using Hermes to run agents in Docker
- using OpenClaw to run agents in Docker
- using NanoClaw to run agents in Docker
- using PantheonOS itself as the runtime/orchestrator in Docker

Without a deployment product, several problems remain:
- no clear way to attach existing dockerized orchestrators into PantheonOS
- no default packaged runtime for new users who want a fast start
- no coherent story for when PantheonOS is the control surface versus when it is the runtime
- no clean white-labeling strategy for Hermes-based deployments
- inconsistent operator expectations around setup, branding, control, and support boundaries

## Target users
Primary users:
- founder / principal operator
- AI-native builder running several agents locally
- operator managing multiple dockerized agent runtimes
- consultant or internal platform lead deploying agent systems for teams

Secondary users:
- technical team member onboarding to PantheonOS
- partner or client operator using a Pantheon-powered deployment
- future external operator adopting the PromptEngines reference model

## Jobs to be done
- let me connect my existing dockerized agent runtime into PantheonOS without rebuilding it
- let me deploy a new agent runtime through PantheonOS with minimal setup
- let me understand whether I am using Hermes, OpenClaw, NanoClaw, or PantheonOS as the runtime underneath
- let me keep PantheonOS as the stable operating surface regardless of which runtime is underneath
- let me use Pantheon-branded deployment flows even when Hermes is the actual runtime substrate
- let me inspect and maintain the runtime from controller panes once it is attached

## Product goals
- make runtime attachment and deployment explicit
- support both existing runtimes and greenfield deployments
- keep PantheonOS runtime-agnostic at the model layer
- make Hermes the default white-labeled packaged deployment path
- preserve clear boundaries between persona agents, runtimes, controllers, and channels
- make Docker the default packaging unit for deployment in v1

## Non-goals
- not a full Kubernetes/orchestration platform in v1
- not a generalized container hosting product
- not a replacement for every runtime ecosystem’s internal abstractions
- not a promise that PantheonOS will deeply control every third-party runtime on day one

## Core product thesis
PantheonOS should be orchestrator-aware but operator-first.

That means:
- the operator sees PantheonOS as the product
- the runtime layer may be Hermes, OpenClaw, NanoClaw, or PantheonOS
- the control surface stays consistent across those options
- Hermes is the easiest packaged route, so PantheonOS should white-label Hermes for deployment

In practice, “Deploy with Pantheon” in v1 should usually mean:
- a Dockerized Hermes runtime
- PantheonOS topology and control conventions layered on top
- Pantheon-branded configuration and onboarding
- explicit registry metadata that the underlying runtime_system is Hermes

## Core concepts
### 1. Control surface vs runtime
PantheonOS is the operating surface.
A runtime system is what actually hosts and executes the agents.

### 2. Runtime system
A runtime system is one of:
- Hermes
- OpenClaw
- NanoClaw
- PantheonOS-native runtime

### 3. Deployment package
A deployment package is the Docker-level unit used to run the runtime system, controllers, and supporting adapters.

### 4. White-labeled Hermes
PantheonOS should offer a first-party deployment experience that is Pantheon-branded while using Hermes as the default underlying runtime engine.

### 5. Attachment vs provisioning
- attachment = connect an existing runtime into PantheonOS
- provisioning = create a new Pantheon-managed runtime package

## Primary use cases
### 1. Connect existing Hermes docker
An operator already runs Hermes in Docker and wants PantheonOS to observe and work across those agents.

### 2. Connect existing OpenClaw or NanoClaw docker
An operator already has another orchestrator running in Docker and wants PantheonOS to normalize it into the same operating surface.

### 3. Deploy new runtime through PantheonOS
A new user chooses “Deploy with Pantheon” and gets a Pantheon-branded setup backed by Hermes.

### 4. Mixed-runtime estate
An advanced operator runs Hermes for one runtime, OpenClaw for another, and compares them from the same PantheonOS surface.

## Product principles
- PantheonOS first in operator experience
- runtime system explicit in machine-readable metadata
- Docker-first in v1
- observe first, control second
- attach existing systems before forcing migration
- white-label Hermes without hiding runtime truth from advanced operators

## Functional requirements
### Runtime registry extensions
PantheonOS must support runtime metadata including:
- runtime_system: `hermes | openclaw | nanoclaw | pantheon`
- packaging: `docker` in v1
- image reference
- container name or compose service
- version
- branding mode: `native | white_labeled`
- deployment mode: `attached | provisioned`
- support level: `first_party | adapter | experimental`

### Deployment descriptors
PantheonOS must support deployment package descriptors including:
- runtime image
- required environment variables
- mounted volumes
- channel adapters enabled
- controller attachment model
- upgrade path
- backup/export path

### White-labeled Hermes mode
PantheonOS must provide a deployment path where:
- operator chooses PantheonOS deployment
- the actual runtime container is Hermes-based
- setup assets are Pantheon-branded
- registry records `runtime_system: hermes` and `branding_mode: white_labeled`
- support docs explain the relationship clearly

### Existing runtime attachment
PantheonOS must support registering existing runtimes where the user provides:
- runtime system type
- host machine / docker details
- channels already in use
- controller relationship
- current access mode

### Runtime capability normalization
PantheonOS must normalize a minimum common layer across orchestrators:
- runtime identity
- runtime status
- controller relationship
- channel bindings
- health / heartbeat
- model/runtime metadata
- intervention targets where supported

### Deployment onboarding
PantheonOS must offer two deployment paths:
1. Connect Existing Runtime
2. Deploy with Pantheon

### Support matrix
PantheonOS must define a support matrix:
- Hermes: first-party / white-labeled default
- OpenClaw: adapter-supported
- NanoClaw: adapter-supported or experimental depending on maturity
- Pantheon runtime: future first-party native path

### Controller model
Every runtime can optionally have a controller agent that:
- runs outside the persona channels
- manages the docker/runtime layer
- sends test messages
- swaps models
- debugs issues
- installs or updates runtime tooling

## UX / workflow
### Connect Existing Runtime
1. user selects runtime type: Hermes / OpenClaw / NanoClaw / Pantheon
2. user provides docker/container details
3. user registers channels and controllers
4. PantheonOS validates topology
5. runtime appears in observe mode first
6. operator upgrades to message or control later

### Deploy with Pantheon
1. user selects “Deploy with Pantheon”
2. PantheonOS provisions a Pantheon-branded docker deployment
3. underlying runtime defaults to Hermes
4. runtime is registered automatically in topology registry
5. default controller/runtime/channel bindings are created
6. operator begins in observe mode and expands from there

## Information architecture
The deployment layer must be legible in:
- registry files
- state engine output
- onboarding docs
- operating terminal panes
- reference deployment examples

The operator should always be able to answer:
- what runtime system is this using?
- is it attached or provisioned?
- is it Pantheon-native or white-labeled Hermes?
- who controls it?
- what channels are bound to it?

## Data model requirements
Runtime object should include at minimum:
- `runtime_system`
- `packaging`
- `branding_mode`
- `deployment_mode`
- `support_level`
- `image`
- `version`
- `controller_bindings`
- `channel_bindings`

Deployment object should include at minimum:
- `default_runtime_system`
- `default_branding_mode`
- `supported_runtime_systems`
- `provisioning_templates`

## Non-functional requirements
- runtime truth must not be obscured in machine-readable state
- onboarding must remain simple for non-experts
- attached runtimes must degrade gracefully when adapters are partial
- white-labeling must not create support ambiguity
- deployment artifacts must remain portable and diffable

## Metrics
- percent of pilots successfully attached without runtime rebuild
- time to first attached runtime
- time to first provisioned runtime
- percent of Pantheon deployments using white-labeled Hermes
- runtime attachment failure rate by orchestrator type
- operator understanding of runtime identity vs control surface identity

## Risks
### Brand confusion
Users may not understand whether they are running PantheonOS or Hermes.

Mitigation:
- clear registry fields
- explicit docs
- visible runtime metadata in the UI

### Adapter fragmentation
Supporting several orchestrators may create shallow integrations.

Mitigation:
- define a narrow minimum common contract
- mark support levels explicitly

### Pantheon-native runtime scope creep
Trying to build a native runtime too early may dilute value.

Mitigation:
- make white-labeled Hermes the default v1 path
- delay deeper native runtime work until real usage proves the need

## Phased roadmap
### Phase 1
- define runtime-system model in registry and state engine
- support Connect Existing Runtime for Hermes
- support Deploy with Pantheon using white-labeled Hermes
- expose runtime truth in docs and state

### Phase 2
- add OpenClaw and NanoClaw adapter support
- add deployment package templates and upgrade flows
- expand controller maintenance workflows

### Phase 3
- evaluate Pantheon-native runtime path
- deepen mixed-runtime support
- formalize external distribution package for operators

## Launch criteria
- PantheonOS can represent Hermes, OpenClaw, NanoClaw, and Pantheon as runtime_system values
- a user can attach an existing Hermes docker into PantheonOS
- a user can provision a Pantheon-branded deployment backed by Hermes
- runtime truth is visible in registry and state output
- operators can distinguish persona agents, runtimes, controllers, and channels in the UI

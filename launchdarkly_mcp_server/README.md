# launchdarkly_mcp_server

An MCP (Model Context Protocol) server that maps to the API at `https://app.launchdarkly.com`.

## Description

This MCP server was automatically generated from an OpenAPI specification. It provides MCP functions that map to the operations defined in the API.

The server acts as a bridge between MCP clients and the target REST API, translating MCP function calls into HTTP requests.

## Setup

1. Install the required dependencies:

```
pip install -r requirements.txt
```

2. Configure the target API URL (optional):

```
export TARGET_API_BASE_URL="https://app.launchdarkly.com"
```

3. Configure authentication (if required):

```
# Uncomment and set as needed for the target API:
# export TARGET_API_KEY="your-api-key"
# export TARGET_API_USERNAME="your-username"
# export TARGET_API_PASSWORD="your-password"
# export TARGET_API_TOKEN="your-token"
```

## Running the Server

Start the server:

```
python main.py
```

The server will run on port 8888 by default.

## Available MCP Functions

### getRoot

Root resource

- HTTP Method: GET
- Path: /api/v2

### getRelayProxyConfigs

List Relay Proxy configs

- HTTP Method: GET
- Path: /api/v2/account/relay-auto-configs

### postRelayAutoConfig

Create a new Relay Proxy config

- HTTP Method: POST
- Path: /api/v2/account/relay-auto-configs

### getRelayProxyConfig

Get Relay Proxy config

- HTTP Method: GET
- Path: /api/v2/account/relay-auto-configs/{id}
- Path Parameters: id

### patchRelayAutoConfig

Update a Relay Proxy config

- HTTP Method: PATCH
- Path: /api/v2/account/relay-auto-configs/{id}
- Path Parameters: id

### deleteRelayAutoConfig

Delete Relay Proxy config by ID

- HTTP Method: DELETE
- Path: /api/v2/account/relay-auto-configs/{id}
- Path Parameters: id

### resetRelayAutoConfig

Reset Relay Proxy configuration key

- HTTP Method: POST
- Path: /api/v2/account/relay-auto-configs/{id}/reset
- Path Parameters: id
- Query Parameters: expiry

### getApplications

Get applications

- HTTP Method: GET
- Path: /api/v2/applications
- Query Parameters: filter, limit, offset, sort, expand

### getApplication

Get application by key

- HTTP Method: GET
- Path: /api/v2/applications/{applicationKey}
- Path Parameters: applicationKey
- Query Parameters: expand

### patchApplication

Update application

- HTTP Method: PATCH
- Path: /api/v2/applications/{applicationKey}
- Path Parameters: applicationKey

### deleteApplication

Delete application

- HTTP Method: DELETE
- Path: /api/v2/applications/{applicationKey}
- Path Parameters: applicationKey

### getApplicationVersions

Get application versions by application key

- HTTP Method: GET
- Path: /api/v2/applications/{applicationKey}/versions
- Path Parameters: applicationKey
- Query Parameters: filter, limit, offset, sort

### patchApplicationVersion

Update application version

- HTTP Method: PATCH
- Path: /api/v2/applications/{applicationKey}/versions/{versionKey}
- Path Parameters: applicationKey, versionKey

### deleteApplicationVersion

Delete application version

- HTTP Method: DELETE
- Path: /api/v2/applications/{applicationKey}/versions/{versionKey}
- Path Parameters: applicationKey, versionKey

### getApprovalRequests

List approval requests

- HTTP Method: GET
- Path: /api/v2/approval-requests
- Query Parameters: filter, expand, limit, offset

### postApprovalRequest

Create approval request

- HTTP Method: POST
- Path: /api/v2/approval-requests

### getApprovalRequest

Get approval request

- HTTP Method: GET
- Path: /api/v2/approval-requests/{id}
- Path Parameters: id
- Query Parameters: expand

### patchApprovalRequest

Update approval request

- HTTP Method: PATCH
- Path: /api/v2/approval-requests/{id}
- Path Parameters: id

### deleteApprovalRequest

Delete approval request

- HTTP Method: DELETE
- Path: /api/v2/approval-requests/{id}
- Path Parameters: id

### postApprovalRequestApply

Apply approval request

- HTTP Method: POST
- Path: /api/v2/approval-requests/{id}/apply
- Path Parameters: id

### postApprovalRequestReview

Review approval request

- HTTP Method: POST
- Path: /api/v2/approval-requests/{id}/reviews
- Path Parameters: id

### getAuditLogEntries

List audit log entries

- HTTP Method: GET
- Path: /api/v2/auditlog
- Query Parameters: before, after, q, limit, spec

### postAuditLogEntries

Search audit log entries

- HTTP Method: POST
- Path: /api/v2/auditlog
- Query Parameters: before, after, q, limit

### getAuditLogEntry

Get audit log entry

- HTTP Method: GET
- Path: /api/v2/auditlog/{id}
- Path Parameters: id

### getCallerIdentity

Identify the caller

- HTTP Method: GET
- Path: /api/v2/caller-identity

### getExtinctions

List extinctions

- HTTP Method: GET
- Path: /api/v2/code-refs/extinctions
- Query Parameters: repoName, branchName, projKey, flagKey, from, to

### getRepositories

List repositories

- HTTP Method: GET
- Path: /api/v2/code-refs/repositories
- Query Parameters: withBranches, withReferencesForDefaultBranch, projKey, flagKey

### postRepository

Create repository

- HTTP Method: POST
- Path: /api/v2/code-refs/repositories

### getRepository

Get repository

- HTTP Method: GET
- Path: /api/v2/code-refs/repositories/{repo}
- Path Parameters: repo

### patchRepository

Update repository

- HTTP Method: PATCH
- Path: /api/v2/code-refs/repositories/{repo}
- Path Parameters: repo

### deleteRepository

Delete repository

- HTTP Method: DELETE
- Path: /api/v2/code-refs/repositories/{repo}
- Path Parameters: repo

### deleteBranches

Delete branches

- HTTP Method: POST
- Path: /api/v2/code-refs/repositories/{repo}/branch-delete-tasks
- Path Parameters: repo

### getBranches

List branches

- HTTP Method: GET
- Path: /api/v2/code-refs/repositories/{repo}/branches
- Path Parameters: repo

### getBranch

Get branch

- HTTP Method: GET
- Path: /api/v2/code-refs/repositories/{repo}/branches/{branch}
- Path Parameters: repo, branch
- Query Parameters: projKey, flagKey

### putBranch

Upsert branch

- HTTP Method: PUT
- Path: /api/v2/code-refs/repositories/{repo}/branches/{branch}
- Path Parameters: repo, branch

### postExtinction

Create extinction

- HTTP Method: POST
- Path: /api/v2/code-refs/repositories/{repo}/branches/{branch}/extinction-events
- Path Parameters: repo, branch

### getRootStatistic

Get links to code reference repositories for each project

- HTTP Method: GET
- Path: /api/v2/code-refs/statistics

### getStatistics

Get code references statistics for flags

- HTTP Method: GET
- Path: /api/v2/code-refs/statistics/{projectKey}
- Path Parameters: projectKey
- Query Parameters: flagKey

### getDestinations

List destinations

- HTTP Method: GET
- Path: /api/v2/destinations

### postGenerateWarehouseDestinationKeyPair

Generate Snowflake destination key pair

- HTTP Method: POST
- Path: /api/v2/destinations/generate-warehouse-destination-key-pair

### postDestination

Create Data Export destination

- HTTP Method: POST
- Path: /api/v2/destinations/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey

### getDestination

Get destination

- HTTP Method: GET
- Path: /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- Path Parameters: projectKey, environmentKey, id

### patchDestination

Update Data Export destination

- HTTP Method: PATCH
- Path: /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- Path Parameters: projectKey, environmentKey, id

### deleteDestination

Delete Data Export destination

- HTTP Method: DELETE
- Path: /api/v2/destinations/{projectKey}/{environmentKey}/{id}
- Path Parameters: projectKey, environmentKey, id

### getFlagLinks

List flag links

- HTTP Method: GET
- Path: /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey

### createFlagLink

Create flag link

- HTTP Method: POST
- Path: /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey

### updateFlagLink

Update flag link

- HTTP Method: PATCH
- Path: /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}
- Path Parameters: projectKey, featureFlagKey, id

### deleteFlagLink

Delete flag link

- HTTP Method: DELETE
- Path: /api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}
- Path Parameters: projectKey, featureFlagKey, id

### getFeatureFlagStatusAcrossEnvironments

Get flag status across environments

- HTTP Method: GET
- Path: /api/v2/flag-status/{projectKey}/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey
- Query Parameters: env

### getFeatureFlagStatuses

List feature flag statuses

- HTTP Method: GET
- Path: /api/v2/flag-statuses/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey

### getFeatureFlagStatus

Get feature flag status

- HTTP Method: GET
- Path: /api/v2/flag-statuses/{projectKey}/{environmentKey}/{featureFlagKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### getFeatureFlags

List feature flags

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}
- Path Parameters: projectKey
- Query Parameters: env, tag, limit, offset, archived, summary, filter, sort, compare, expand

### postFeatureFlag

Create a feature flag

- HTTP Method: POST
- Path: /api/v2/flags/{projectKey}
- Path Parameters: projectKey
- Query Parameters: clone

### getDependentFlagsByEnv

List dependent feature flags by environment

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{environmentKey}/{featureFlagKey}/dependent-flags
- Path Parameters: projectKey, environmentKey, featureFlagKey

### getFeatureFlag

Get feature flag

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey
- Query Parameters: env, expand

### patchFeatureFlag

Update feature flag

- HTTP Method: PATCH
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey
- Query Parameters: ignoreConflicts

### deleteFeatureFlag

Delete feature flag

- HTTP Method: DELETE
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}
- Path Parameters: projectKey, featureFlagKey

### copyFeatureFlag

Copy feature flag

- HTTP Method: POST
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/copy
- Path Parameters: projectKey, featureFlagKey

### getDependentFlags

List dependent feature flags

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/dependent-flags
- Path Parameters: projectKey, featureFlagKey

### getExpiringContextTargets

Get expiring context targets for feature flag

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### patchExpiringTargets

Update expiring context targets on feature flag

- HTTP Method: PATCH
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### getExpiringUserTargets

Get expiring user targets for feature flag

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### patchExpiringUserTargets

Update expiring user targets on feature flag

- HTTP Method: PATCH
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### getTriggerWorkflows

List flag triggers

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### createTriggerWorkflow

Create flag trigger

- HTTP Method: POST
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey

### getTriggerWorkflowById

Get flag trigger by ID

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### patchTriggerWorkflow

Update flag trigger

- HTTP Method: PATCH
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- Path Parameters: projectKey, environmentKey, featureFlagKey, id

### deleteTriggerWorkflow

Delete flag trigger

- HTTP Method: DELETE
- Path: /api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}
- Path Parameters: projectKey, environmentKey, featureFlagKey, id

### getReleaseByFlagKey

Get release for flag

- HTTP Method: GET
- Path: /api/v2/flags/{projectKey}/{flagKey}/release
- Path Parameters: projectKey, flagKey

### patchReleaseByFlagKey

Patch release for flag

- HTTP Method: PATCH
- Path: /api/v2/flags/{projectKey}/{flagKey}/release
- Path Parameters: projectKey, flagKey

### deleteReleaseByFlagKey

Delete a release for flag

- HTTP Method: DELETE
- Path: /api/v2/flags/{projectKey}/{flagKey}/release
- Path Parameters: projectKey, flagKey

### getBigSegmentStoreIntegrations

List all big segment store integrations

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/big-segment-store

### createBigSegmentStoreIntegration

Create big segment store integration

- HTTP Method: POST
- Path: /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}
- Path Parameters: projectKey, environmentKey, integrationKey

### getBigSegmentStoreIntegration

Get big segment store integration by ID

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, environmentKey, integrationKey, integrationId

### patchBigSegmentStoreIntegration

Update big segment store integration

- HTTP Method: PATCH
- Path: /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, environmentKey, integrationKey, integrationId

### deleteBigSegmentStoreIntegration

Delete big segment store integration

- HTTP Method: DELETE
- Path: /api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, environmentKey, integrationKey, integrationId

### getIntegrationDeliveryConfigurations

List all delivery configurations

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/featureStore

### getIntegrationDeliveryConfigurationByEnvironment

Get delivery configurations by environment

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey

### createIntegrationDeliveryConfiguration

Create delivery configuration

- HTTP Method: POST
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}
- Path Parameters: projectKey, environmentKey, integrationKey

### getIntegrationDeliveryConfigurationById

Get delivery configuration by ID

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- Path Parameters: projectKey, environmentKey, integrationKey, id

### patchIntegrationDeliveryConfiguration

Update delivery configuration

- HTTP Method: PATCH
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- Path Parameters: projectKey, environmentKey, integrationKey, id

### deleteIntegrationDeliveryConfiguration

Delete delivery configuration

- HTTP Method: DELETE
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}
- Path Parameters: projectKey, environmentKey, integrationKey, id

### validateIntegrationDeliveryConfiguration

Validate delivery configuration

- HTTP Method: POST
- Path: /api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}/validate
- Path Parameters: projectKey, environmentKey, integrationKey, id

### getFlagImportConfigurations

List all flag import configurations

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/flag-import

### createFlagImportConfiguration

Create a flag import configuration

- HTTP Method: POST
- Path: /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}
- Path Parameters: projectKey, integrationKey

### getFlagImportConfiguration

Get a single flag import configuration

- HTTP Method: GET
- Path: /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, integrationKey, integrationId

### patchFlagImportConfiguration

Update a flag import configuration

- HTTP Method: PATCH
- Path: /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, integrationKey, integrationId

### deleteFlagImportConfiguration

Delete a flag import configuration

- HTTP Method: DELETE
- Path: /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}
- Path Parameters: projectKey, integrationKey, integrationId

### triggerFlagImportJob

Trigger a single flag import run

- HTTP Method: POST
- Path: /api/v2/integration-capabilities/flag-import/{projectKey}/{integrationKey}/{integrationId}/trigger
- Path Parameters: projectKey, integrationKey, integrationId

### getAllIntegrationConfigurations

Get all configurations for the integration

- HTTP Method: GET
- Path: /api/v2/integration-configurations/keys/{integrationKey}
- Path Parameters: integrationKey

### createIntegrationConfiguration

Create integration configuration

- HTTP Method: POST
- Path: /api/v2/integration-configurations/keys/{integrationKey}
- Path Parameters: integrationKey

### getIntegrationConfiguration

Get an integration configuration

- HTTP Method: GET
- Path: /api/v2/integration-configurations/{integrationConfigurationId}
- Path Parameters: integrationConfigurationId

### updateIntegrationConfiguration

Update integration configuration

- HTTP Method: PATCH
- Path: /api/v2/integration-configurations/{integrationConfigurationId}
- Path Parameters: integrationConfigurationId

### deleteIntegrationConfiguration

Delete integration configuration

- HTTP Method: DELETE
- Path: /api/v2/integration-configurations/{integrationConfigurationId}
- Path Parameters: integrationConfigurationId

### getSubscriptions

Get audit log subscriptions by integration

- HTTP Method: GET
- Path: /api/v2/integrations/{integrationKey}
- Path Parameters: integrationKey

### createSubscription

Create audit log subscription

- HTTP Method: POST
- Path: /api/v2/integrations/{integrationKey}
- Path Parameters: integrationKey

### getSubscriptionByID

Get audit log subscription by ID

- HTTP Method: GET
- Path: /api/v2/integrations/{integrationKey}/{id}
- Path Parameters: integrationKey, id

### updateSubscription

Update audit log subscription

- HTTP Method: PATCH
- Path: /api/v2/integrations/{integrationKey}/{id}
- Path Parameters: integrationKey, id

### deleteSubscription

Delete audit log subscription

- HTTP Method: DELETE
- Path: /api/v2/integrations/{integrationKey}/{id}
- Path Parameters: integrationKey, id

### getMembers

List account members

- HTTP Method: GET
- Path: /api/v2/members
- Query Parameters: limit, offset, filter, expand, sort

### postMembers

Invite new members

- HTTP Method: POST
- Path: /api/v2/members

### patchMembers

Modify account members

- HTTP Method: PATCH
- Path: /api/v2/members

### getMember

Get account member

- HTTP Method: GET
- Path: /api/v2/members/{id}
- Path Parameters: id
- Query Parameters: expand

### patchMember

Modify an account member

- HTTP Method: PATCH
- Path: /api/v2/members/{id}
- Path Parameters: id

### deleteMember

Delete account member

- HTTP Method: DELETE
- Path: /api/v2/members/{id}
- Path Parameters: id

### postMemberTeams

Add a member to teams

- HTTP Method: POST
- Path: /api/v2/members/{id}/teams
- Path Parameters: id

### getMetrics

List metrics

- HTTP Method: GET
- Path: /api/v2/metrics/{projectKey}
- Path Parameters: projectKey
- Query Parameters: expand, limit, offset, sort, filter

### postMetric

Create metric

- HTTP Method: POST
- Path: /api/v2/metrics/{projectKey}
- Path Parameters: projectKey

### getMetric

Get metric

- HTTP Method: GET
- Path: /api/v2/metrics/{projectKey}/{metricKey}
- Path Parameters: projectKey, metricKey
- Query Parameters: expand, versionId

### patchMetric

Update metric

- HTTP Method: PATCH
- Path: /api/v2/metrics/{projectKey}/{metricKey}
- Path Parameters: projectKey, metricKey

### deleteMetric

Delete metric

- HTTP Method: DELETE
- Path: /api/v2/metrics/{projectKey}/{metricKey}
- Path Parameters: projectKey, metricKey

### getOAuthClients

Get clients

- HTTP Method: GET
- Path: /api/v2/oauth/clients

### createOAuth2Client

Create a LaunchDarkly OAuth 2.0 client

- HTTP Method: POST
- Path: /api/v2/oauth/clients

### getOAuthClientById

Get client by ID

- HTTP Method: GET
- Path: /api/v2/oauth/clients/{clientId}
- Path Parameters: clientId

### patchOAuthClient

Patch client by ID

- HTTP Method: PATCH
- Path: /api/v2/oauth/clients/{clientId}
- Path Parameters: clientId

### deleteOAuthClient

Delete OAuth 2.0 client

- HTTP Method: DELETE
- Path: /api/v2/oauth/clients/{clientId}
- Path Parameters: clientId

### getOpenapiSpec

Gets the OpenAPI spec in json

- HTTP Method: GET
- Path: /api/v2/openapi.json

### getProjects

List projects

- HTTP Method: GET
- Path: /api/v2/projects
- Query Parameters: limit, offset, filter, sort, expand

### postProject

Create project

- HTTP Method: POST
- Path: /api/v2/projects

### getProject

Get project

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}
- Path Parameters: projectKey
- Query Parameters: expand

### patchProject

Update project

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}
- Path Parameters: projectKey

### deleteProject

Delete project

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}
- Path Parameters: projectKey

### getContextKindsByProjectKey

Get context kinds

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/context-kinds
- Path Parameters: projectKey

### putContextKind

Create or update context kind

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/context-kinds/{key}
- Path Parameters: projectKey, key

### getEnvironmentsByProject

List environments

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments
- Path Parameters: projectKey
- Query Parameters: limit, offset, filter, sort

### postEnvironment

Create environment

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments
- Path Parameters: projectKey

### getEnvironment

Get environment

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}
- Path Parameters: projectKey, environmentKey

### patchEnvironment

Update environment

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}
- Path Parameters: projectKey, environmentKey

### deleteEnvironment

Delete environment

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}
- Path Parameters: projectKey, environmentKey

### resetEnvironmentSDKKey

Reset environment SDK key

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/apiKey
- Path Parameters: projectKey, environmentKey
- Query Parameters: expiry

### getContextAttributeNames

Get context attribute names

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes
- Path Parameters: projectKey, environmentKey
- Query Parameters: filter, limit

### getContextAttributeValues

Get context attribute values

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes/{attributeName}
- Path Parameters: projectKey, environmentKey, attributeName
- Query Parameters: filter, limit

### searchContextInstances

Search for context instances

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/search
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, continuationToken, sort, filter, includeTotalCount

### getContextInstances

Get context instances

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}
- Path Parameters: projectKey, environmentKey, id
- Query Parameters: limit, continuationToken, sort, filter, includeTotalCount

### deleteContextInstances

Delete context instances

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}
- Path Parameters: projectKey, environmentKey, id

### searchContexts

Search for contexts

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/search
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, continuationToken, sort, filter, includeTotalCount

### putContextFlagSetting

Update flag settings for context

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{contextKind}/{contextKey}/flags/{featureFlagKey}
- Path Parameters: projectKey, environmentKey, contextKind, contextKey, featureFlagKey

### getContexts

Get contexts

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{kind}/{key}
- Path Parameters: projectKey, environmentKey, kind, key
- Query Parameters: limit, continuationToken, sort, filter, includeTotalCount

### getExperiments

Get experiments

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, offset, filter, expand, lifecycleState

### createExperiment

Create experiment

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments
- Path Parameters: projectKey, environmentKey

### getExperiment

Get experiment

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}
- Path Parameters: projectKey, environmentKey, experimentKey
- Query Parameters: expand

### patchExperiment

Patch experiment

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}
- Path Parameters: projectKey, environmentKey, experimentKey

### createIteration

Create iteration

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/iterations
- Path Parameters: projectKey, environmentKey, experimentKey

### getExperimentResultsForMetricGroup

Get experiment results for metric group (Deprecated)

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metric-groups/{metricGroupKey}/results
- Path Parameters: projectKey, environmentKey, experimentKey, metricGroupKey
- Query Parameters: iterationId

### getExperimentResults

Get experiment results (Deprecated)

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metrics/{metricKey}/results
- Path Parameters: projectKey, environmentKey, experimentKey, metricKey
- Query Parameters: iterationId, expand

### evaluateContextInstance

Evaluate flags for context instance

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/flags/evaluate
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, offset, sort, filter

### getFollowersByProjEnv

Get followers of all flags in a given project and environment

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/followers
- Path Parameters: projectKey, environmentKey

### getAllHoldouts

Get all holdouts

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, offset

### postHoldout

Create holdout

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts
- Path Parameters: projectKey, environmentKey

### getHoldoutById

Get Holdout by Id

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/id/{holdoutId}
- Path Parameters: projectKey, environmentKey, holdoutId

### getHoldout

Get holdout

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey}
- Path Parameters: projectKey, environmentKey, holdoutKey
- Query Parameters: expand

### patchHoldout

Patch holdout

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/holdouts/{holdoutKey}
- Path Parameters: projectKey, environmentKey, holdoutKey

### resetEnvironmentMobileKey

Reset environment mobile SDK key

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/mobileKey
- Path Parameters: projectKey, environmentKey

### getContextInstanceSegmentsMembershipByEnv

List segment memberships for context instance

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/environments/{environmentKey}/segments/evaluate
- Path Parameters: projectKey, environmentKey

### getExperimentationSettings

Get experimentation settings

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/experimentation-settings
- Path Parameters: projectKey

### putExperimentationSettings

Update experimentation settings

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/experimentation-settings
- Path Parameters: projectKey

### getFlagDefaultsByProject

Get flag defaults for project

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flag-defaults
- Path Parameters: projectKey

### patchFlagDefaultsByProject

Update flag default for project

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/flag-defaults
- Path Parameters: projectKey

### putFlagDefaultsByProject

Create or update flag defaults for project

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/flag-defaults
- Path Parameters: projectKey

### getApprovalsForFlag

List approval requests for a flag

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests
- Path Parameters: projectKey, featureFlagKey, environmentKey

### postApprovalRequestForFlag

Create approval request for a flag

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests
- Path Parameters: projectKey, featureFlagKey, environmentKey

### postFlagCopyConfigApprovalRequest

Create approval request to copy flag configurations across environments

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-flag-copy
- Path Parameters: projectKey, featureFlagKey, environmentKey

### getApprovalForFlag

Get approval request for a flag

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### patchFlagConfigApprovalRequest

Update flag approval request

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### deleteApprovalRequestForFlag

Delete approval request for a flag

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### postApprovalRequestApplyForFlag

Apply approval request for a flag

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/apply
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### postApprovalRequestReviewForFlag

Review approval request for a flag

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/reviews
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### getFlagFollowers

Get followers of a flag in a project and environment

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers
- Path Parameters: projectKey, featureFlagKey, environmentKey

### putFlagFollower

Add a member as a follower of a flag in a project and environment

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}
- Path Parameters: projectKey, featureFlagKey, environmentKey, memberId

### deleteFlagFollower

Remove a member as a follower of a flag in a project and environment

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}
- Path Parameters: projectKey, featureFlagKey, environmentKey, memberId

### getFlagConfigScheduledChanges

List scheduled changes

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes
- Path Parameters: projectKey, featureFlagKey, environmentKey

### postFlagConfigScheduledChanges

Create scheduled changes workflow

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes
- Path Parameters: projectKey, featureFlagKey, environmentKey
- Query Parameters: ignoreConflicts

### getFeatureFlagScheduledChange

Get a scheduled change

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### patchFlagConfigScheduledChange

Update scheduled changes workflow

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id
- Query Parameters: ignoreConflicts

### deleteFlagConfigScheduledChanges

Delete scheduled changes workflow

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}
- Path Parameters: projectKey, featureFlagKey, environmentKey, id

### getWorkflows

Get workflows

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows
- Path Parameters: projectKey, featureFlagKey, environmentKey
- Query Parameters: status, sort, limit, offset

### postWorkflow

Create workflow

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows
- Path Parameters: projectKey, featureFlagKey, environmentKey
- Query Parameters: templateKey, dryRun

### getCustomWorkflow

Get custom workflow

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}
- Path Parameters: projectKey, featureFlagKey, environmentKey, workflowId

### deleteWorkflow

Delete workflow

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}
- Path Parameters: projectKey, featureFlagKey, environmentKey, workflowId

### postMigrationSafetyIssues

Get migration safety issues

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/flags/{flagKey}/environments/{environmentKey}/migration-safety-issues
- Path Parameters: projectKey, flagKey, environmentKey

### createReleaseForFlag

Create a new release for flag

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/flags/{flagKey}/release
- Path Parameters: projectKey, flagKey

### updatePhaseStatus

Update phase status for release

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/flags/{flagKey}/release/phases/{phaseId}
- Path Parameters: projectKey, flagKey, phaseId

### getLayers

Get layers

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/layers
- Path Parameters: projectKey
- Query Parameters: filter

### createLayer

Create layer

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/layers
- Path Parameters: projectKey

### updateLayer

Update layer

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/layers/{layerKey}
- Path Parameters: projectKey, layerKey

### getMetricGroups

List metric groups

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/metric-groups
- Path Parameters: projectKey
- Query Parameters: filter, sort, expand, limit, offset

### createMetricGroup

Create metric group

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/metric-groups
- Path Parameters: projectKey

### getMetricGroup

Get metric group

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- Path Parameters: projectKey, metricGroupKey
- Query Parameters: expand

### patchMetricGroup

Patch metric group

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- Path Parameters: projectKey, metricGroupKey

### deleteMetricGroup

Delete metric group

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}
- Path Parameters: projectKey, metricGroupKey

### getAllReleasePipelines

Get all release pipelines

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/release-pipelines
- Path Parameters: projectKey
- Query Parameters: filter, limit, offset

### postReleasePipeline

Create a release pipeline

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/release-pipelines
- Path Parameters: projectKey

### getReleasePipelineByKey

Get release pipeline by key

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- Path Parameters: projectKey, pipelineKey

### putReleasePipeline

Update a release pipeline

- HTTP Method: PUT
- Path: /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- Path Parameters: projectKey, pipelineKey

### deleteReleasePipeline

Delete release pipeline

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}
- Path Parameters: projectKey, pipelineKey

### getAllReleaseProgressionsForReleasePipeline

Get release progressions for release pipeline

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}/releases
- Path Parameters: projectKey, pipelineKey
- Query Parameters: filter, limit, offset

### getIps

Gets the public IP list

- HTTP Method: GET
- Path: /api/v2/public-ip-list

### getCustomRoles

List custom roles

- HTTP Method: GET
- Path: /api/v2/roles
- Query Parameters: limit, offset

### postCustomRole

Create custom role

- HTTP Method: POST
- Path: /api/v2/roles

### getCustomRole

Get custom role

- HTTP Method: GET
- Path: /api/v2/roles/{customRoleKey}
- Path Parameters: customRoleKey

### patchCustomRole

Update custom role

- HTTP Method: PATCH
- Path: /api/v2/roles/{customRoleKey}
- Path Parameters: customRoleKey

### deleteCustomRole

Delete custom role

- HTTP Method: DELETE
- Path: /api/v2/roles/{customRoleKey}
- Path Parameters: customRoleKey

### getSegments

List segments

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, offset, sort, filter

### postSegment

Create segment

- HTTP Method: POST
- Path: /api/v2/segments/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey

### getSegment

Get segment

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### patchSegment

Patch segment

- HTTP Method: PATCH
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### deleteSegment

Delete segment

- HTTP Method: DELETE
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### updateBigSegmentContextTargets

Update context targets on a big segment

- HTTP Method: POST
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts
- Path Parameters: projectKey, environmentKey, segmentKey

### getSegmentMembershipForContext

Get big segment membership for context

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts/{contextKey}
- Path Parameters: projectKey, environmentKey, segmentKey, contextKey

### createBigSegmentExport

Create big segment export

- HTTP Method: POST
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports
- Path Parameters: projectKey, environmentKey, segmentKey

### getBigSegmentExport

Get big segment export

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports/{exportID}
- Path Parameters: projectKey, environmentKey, segmentKey, exportID

### createBigSegmentImport

Create big segment import

- HTTP Method: POST
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports
- Path Parameters: projectKey, environmentKey, segmentKey

### getBigSegmentImport

Get big segment import

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports/{importID}
- Path Parameters: projectKey, environmentKey, segmentKey, importID

### updateBigSegmentTargets

Update user context targets on a big segment

- HTTP Method: POST
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users
- Path Parameters: projectKey, environmentKey, segmentKey

### getSegmentMembershipForUser

Get big segment membership for user

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users/{userKey}
- Path Parameters: projectKey, environmentKey, segmentKey, userKey

### getExpiringTargetsForSegment

Get expiring targets for segment

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### patchExpiringTargetsForSegment

Update expiring targets for segment

- HTTP Method: PATCH
- Path: /api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### getExpiringUserTargetsForSegment

Get expiring user targets for segment

- HTTP Method: GET
- Path: /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### patchExpiringUserTargetsForSegment

Update expiring user targets for segment

- HTTP Method: PATCH
- Path: /api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, environmentKey, segmentKey

### getTeams

List teams

- HTTP Method: GET
- Path: /api/v2/teams
- Query Parameters: limit, offset, filter, expand

### postTeam

Create team

- HTTP Method: POST
- Path: /api/v2/teams
- Query Parameters: expand

### patchTeams

Update teams

- HTTP Method: PATCH
- Path: /api/v2/teams

### getTeam

Get team

- HTTP Method: GET
- Path: /api/v2/teams/{teamKey}
- Path Parameters: teamKey
- Query Parameters: expand

### patchTeam

Update team

- HTTP Method: PATCH
- Path: /api/v2/teams/{teamKey}
- Path Parameters: teamKey
- Query Parameters: expand

### deleteTeam

Delete team

- HTTP Method: DELETE
- Path: /api/v2/teams/{teamKey}
- Path Parameters: teamKey

### getTeamMaintainers

Get team maintainers

- HTTP Method: GET
- Path: /api/v2/teams/{teamKey}/maintainers
- Path Parameters: teamKey
- Query Parameters: limit, offset

### postTeamMembers

Add multiple members to team

- HTTP Method: POST
- Path: /api/v2/teams/{teamKey}/members
- Path Parameters: teamKey

### getTeamRoles

Get team custom roles

- HTTP Method: GET
- Path: /api/v2/teams/{teamKey}/roles
- Path Parameters: teamKey
- Query Parameters: limit, offset

### getWorkflowTemplates

Get workflow templates

- HTTP Method: GET
- Path: /api/v2/templates
- Query Parameters: summary, search

### createWorkflowTemplate

Create workflow template

- HTTP Method: POST
- Path: /api/v2/templates

### deleteWorkflowTemplate

Delete workflow template

- HTTP Method: DELETE
- Path: /api/v2/templates/{templateKey}
- Path Parameters: templateKey

### getTokens

List access tokens

- HTTP Method: GET
- Path: /api/v2/tokens
- Query Parameters: showAll, limit, offset

### postToken

Create access token

- HTTP Method: POST
- Path: /api/v2/tokens

### getToken

Get access token

- HTTP Method: GET
- Path: /api/v2/tokens/{id}
- Path Parameters: id

### patchToken

Patch access token

- HTTP Method: PATCH
- Path: /api/v2/tokens/{id}
- Path Parameters: id

### deleteToken

Delete access token

- HTTP Method: DELETE
- Path: /api/v2/tokens/{id}
- Path Parameters: id

### resetToken

Reset access token

- HTTP Method: POST
- Path: /api/v2/tokens/{id}/reset
- Path Parameters: id
- Query Parameters: expiry

### getDataExportEventsUsage

Get data export events usage

- HTTP Method: GET
- Path: /api/v2/usage/data-export-events
- Query Parameters: from, to, projectKey, environmentKey

### getEvaluationsUsage

Get evaluations usage

- HTTP Method: GET
- Path: /api/v2/usage/evaluations/{projectKey}/{environmentKey}/{featureFlagKey}
- Path Parameters: projectKey, environmentKey, featureFlagKey
- Query Parameters: from, to, tz

### getEventsUsage

Get events usage

- HTTP Method: GET
- Path: /api/v2/usage/events/{type}
- Path Parameters: type
- Query Parameters: from, to

### getExperimentationKeysUsage

Get experimentation keys usage

- HTTP Method: GET
- Path: /api/v2/usage/experimentation-keys
- Query Parameters: from, to, projectKey, environmentKey

### getExperimentationUnitsUsage

Get experimentation units usage

- HTTP Method: GET
- Path: /api/v2/usage/experimentation-units
- Query Parameters: from, to, projectKey, environmentKey

### getMauUsage

Get MAU usage

- HTTP Method: GET
- Path: /api/v2/usage/mau
- Query Parameters: from, to, project, environment, sdktype, sdk, anonymous, groupby, aggregationType, contextKind

### getMauUsageByCategory

Get MAU usage by category

- HTTP Method: GET
- Path: /api/v2/usage/mau/bycategory
- Query Parameters: from, to

### getMauSdksByType

Get MAU SDKs by type

- HTTP Method: GET
- Path: /api/v2/usage/mau/sdks
- Query Parameters: from, to, sdktype

### getServiceConnectionUsage

Get service connection usage

- HTTP Method: GET
- Path: /api/v2/usage/service-connections
- Query Parameters: from, to, projectKey, environmentKey

### getStreamUsage

Get stream usage

- HTTP Method: GET
- Path: /api/v2/usage/streams/{source}
- Path Parameters: source
- Query Parameters: from, to, tz

### getStreamUsageBySdkVersion

Get stream usage by SDK version

- HTTP Method: GET
- Path: /api/v2/usage/streams/{source}/bysdkversion
- Path Parameters: source
- Query Parameters: from, to, tz, sdk, version

### getStreamUsageSdkversion

Get stream usage SDK versions

- HTTP Method: GET
- Path: /api/v2/usage/streams/{source}/sdkversions
- Path Parameters: source

### getUserAttributeNames

Get user attribute names

- HTTP Method: GET
- Path: /api/v2/user-attributes/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey

### getSearchUsers

Find users

- HTTP Method: GET
- Path: /api/v2/user-search/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey
- Query Parameters: q, limit, offset, after, sort, searchAfter, filter

### getUsers

List users

- HTTP Method: GET
- Path: /api/v2/users/{projectKey}/{environmentKey}
- Path Parameters: projectKey, environmentKey
- Query Parameters: limit, searchAfter

### getUser

Get user

- HTTP Method: GET
- Path: /api/v2/users/{projectKey}/{environmentKey}/{userKey}
- Path Parameters: projectKey, environmentKey, userKey

### deleteUser

Delete user

- HTTP Method: DELETE
- Path: /api/v2/users/{projectKey}/{environmentKey}/{userKey}
- Path Parameters: projectKey, environmentKey, userKey

### getUserFlagSettings

List flag settings for user

- HTTP Method: GET
- Path: /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags
- Path Parameters: projectKey, environmentKey, userKey

### getUserFlagSetting

Get flag setting for user

- HTTP Method: GET
- Path: /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}
- Path Parameters: projectKey, environmentKey, userKey, featureFlagKey

### putFlagSetting

Update flag settings for user

- HTTP Method: PUT
- Path: /api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}
- Path Parameters: projectKey, environmentKey, userKey, featureFlagKey

### getExpiringFlagsForUser

Get expiring dates on flags for user

- HTTP Method: GET
- Path: /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, userKey, environmentKey

### patchExpiringFlagsForUser

Update expiring user target for flags

- HTTP Method: PATCH
- Path: /api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}
- Path Parameters: projectKey, userKey, environmentKey

### getVersions

Get version information

- HTTP Method: GET
- Path: /api/v2/versions

### getAllWebhooks

List webhooks

- HTTP Method: GET
- Path: /api/v2/webhooks

### postWebhook

Creates a webhook

- HTTP Method: POST
- Path: /api/v2/webhooks

### getWebhook

Get webhook

- HTTP Method: GET
- Path: /api/v2/webhooks/{id}
- Path Parameters: id

### patchWebhook

Update webhook

- HTTP Method: PATCH
- Path: /api/v2/webhooks/{id}
- Path Parameters: id

### deleteWebhook

Delete webhook

- HTTP Method: DELETE
- Path: /api/v2/webhooks/{id}
- Path Parameters: id

### getTags

List tags

- HTTP Method: GET
- Path: /api/v2/tags
- Query Parameters: kind, pre, archived, limit, offset, asOf

### getAIConfigs

List AI Configs

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs
- Path Parameters: projectKey
- Query Parameters: sort, limit, offset, filter

### postAIConfig

Create new AI Config

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/ai-configs
- Path Parameters: projectKey

### deleteAIConfig

Delete AI Config

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}
- Path Parameters: projectKey, configKey

### getAIConfig

Get AI Config

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}
- Path Parameters: projectKey, configKey

### patchAIConfig

Update AI Config

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}
- Path Parameters: projectKey, configKey

### postAIConfigVariation

Create AI Config variation

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations
- Path Parameters: projectKey, configKey

### deleteAIConfigVariation

Delete AI Config variation

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- Path Parameters: projectKey, configKey, variationKey

### getAIConfigVariation

Get AI Config variation

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- Path Parameters: projectKey, configKey, variationKey

### patchAIConfigVariation

Update AI Config variation

- HTTP Method: PATCH
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/variations/{variationKey}
- Path Parameters: projectKey, configKey, variationKey

### getAIConfigMetrics

Get AI Config metrics

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics
- Path Parameters: projectKey, configKey
- Query Parameters: from, to, env

### getAIConfigMetricsByVariation

Get AI Config metrics by variation

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/{configKey}/metrics-by-variation
- Path Parameters: projectKey, configKey
- Query Parameters: from, to, env

### listModelConfigs

List AI model configs

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/model-configs
- Path Parameters: projectKey

### postModelConfig

Create an AI model config

- HTTP Method: POST
- Path: /api/v2/projects/{projectKey}/ai-configs/model-configs
- Path Parameters: projectKey

### deleteModelConfig

Delete an AI model config

- HTTP Method: DELETE
- Path: /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey}
- Path Parameters: projectKey, modelConfigKey

### getModelConfig

Get AI model config

- HTTP Method: GET
- Path: /api/v2/projects/{projectKey}/ai-configs/model-configs/{modelConfigKey}
- Path Parameters: projectKey, modelConfigKey

### getAnnouncementsPublic

Get announcements

- HTTP Method: GET
- Path: /api/v2/announcements
- Query Parameters: status, limit, offset

### createAnnouncementPublic

Create an announcement

- HTTP Method: POST
- Path: /api/v2/announcements

### deleteAnnouncementPublic

Delete an announcement

- HTTP Method: DELETE
- Path: /api/v2/announcements/{announcementId}
- Path Parameters: announcementId

### updateAnnouncementPublic

Update an announcement

- HTTP Method: PATCH
- Path: /api/v2/announcements/{announcementId}
- Path Parameters: announcementId

### getDeploymentFrequencyChart

Get deployment frequency chart data

- HTTP Method: GET
- Path: /api/v2/engineering-insights/charts/deployments/frequency
- Query Parameters: projectKey, environmentKey, applicationKey, from, to, bucketType, bucketMs, groupBy, expand

### getStaleFlagsChart

Get stale flags chart data

- HTTP Method: GET
- Path: /api/v2/engineering-insights/charts/flags/stale
- Query Parameters: projectKey, environmentKey, applicationKey, groupBy, maintainerId, maintainerTeamKey, expand

### getFlagStatusChart

Get flag status chart data

- HTTP Method: GET
- Path: /api/v2/engineering-insights/charts/flags/status
- Query Parameters: projectKey, environmentKey, applicationKey

### getLeadTimeChart

Get lead time chart data

- HTTP Method: GET
- Path: /api/v2/engineering-insights/charts/lead-time
- Query Parameters: projectKey, environmentKey, applicationKey, from, to, bucketType, bucketMs, groupBy, expand

### getReleaseFrequencyChart

Get release frequency chart data

- HTTP Method: GET
- Path: /api/v2/engineering-insights/charts/releases/frequency
- Query Parameters: projectKey, environmentKey, applicationKey, hasExperiments, global, groupBy, from, to, bucketType, bucketMs, expand

### createDeploymentEvent

Create deployment event

- HTTP Method: POST
- Path: /api/v2/engineering-insights/deployment-events

### getDeployments

List deployments

- HTTP Method: GET
- Path: /api/v2/engineering-insights/deployments
- Query Parameters: projectKey, environmentKey, applicationKey, limit, expand, from, to, after, before, kind, status

### getDeployment

Get deployment

- HTTP Method: GET
- Path: /api/v2/engineering-insights/deployments/{deploymentID}
- Path Parameters: deploymentID
- Query Parameters: expand

### updateDeployment

Update deployment

- HTTP Method: PATCH
- Path: /api/v2/engineering-insights/deployments/{deploymentID}
- Path Parameters: deploymentID

### getFlagEvents

List flag events

- HTTP Method: GET
- Path: /api/v2/engineering-insights/flag-events
- Query Parameters: projectKey, environmentKey, applicationKey, query, impactSize, hasExperiments, global, expand, limit, from, to, after, before

### createInsightGroup

Create insight group

- HTTP Method: POST
- Path: /api/v2/engineering-insights/insights/group

### getInsightGroups

List insight groups

- HTTP Method: GET
- Path: /api/v2/engineering-insights/insights/groups
- Query Parameters: limit, offset, sort, query, expand

### getInsightGroup

Get insight group

- HTTP Method: GET
- Path: /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- Path Parameters: insightGroupKey
- Query Parameters: expand

### patchInsightGroup

Patch insight group

- HTTP Method: PATCH
- Path: /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- Path Parameters: insightGroupKey

### deleteInsightGroup

Delete insight group

- HTTP Method: DELETE
- Path: /api/v2/engineering-insights/insights/groups/{insightGroupKey}
- Path Parameters: insightGroupKey

### getInsightsScores

Get insight scores

- HTTP Method: GET
- Path: /api/v2/engineering-insights/insights/scores
- Query Parameters: projectKey, environmentKey, applicationKey

### getPullRequests

List pull requests

- HTTP Method: GET
- Path: /api/v2/engineering-insights/pull-requests
- Query Parameters: projectKey, environmentKey, applicationKey, status, query, limit, expand, sort, from, to, after, before

### getInsightsRepositories

List repositories

- HTTP Method: GET
- Path: /api/v2/engineering-insights/repositories
- Query Parameters: expand

### associateRepositoriesAndProjects

Associate repositories with projects

- HTTP Method: PUT
- Path: /api/v2/engineering-insights/repositories/projects

### deleteRepositoryProject

Remove repository project association

- HTTP Method: DELETE
- Path: /api/v2/engineering-insights/repositories/{repositoryKey}/projects/{projectKey}
- Path Parameters: repositoryKey, projectKey


## Configuration

The server can be configured using environment variables:

- `TARGET_API_BASE_URL`: The base URL of the target API
- Authentication variables (see setup section)

## Error Handling

The server maps HTTP error codes from the target API to MCP error codes:

- 400: TARGET_API_BAD_REQUEST
- 401: TARGET_API_UNAUTHORIZED
- 403: TARGET_API_FORBIDDEN
- 404: TARGET_API_NOT_FOUND
- 429: TARGET_API_RATE_LIMITED
- 5xx: TARGET_API_SERVER_ERROR 
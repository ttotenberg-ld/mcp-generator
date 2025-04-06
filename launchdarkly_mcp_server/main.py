"""
Main entry point for the launchdarkly_mcp_server MCP server.

This server provides MCP functions that map to the following API:
https://app.launchdarkly.com
"""
import asyncio
import logging
from mcp import McpServer, FunctionRegistry, Capability

import config
from handlers import function_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launchdarkly_mcp_server")

# Define capabilities for all MCP functions
capabilities = []

# Capability for getRoot
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRoot",
            "description": """Root resource""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/RootResponse"}
        }
    )
)
# Capability for getRelayProxyConfigs
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRelayProxyConfigs",
            "description": """List Relay Proxy configs""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/RelayAutoConfigCollectionRep"}
        }
    )
)
# Capability for postRelayAutoConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postRelayAutoConfig",
            "description": """Create a new Relay Proxy config""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/RelayAutoConfigPost"}}},
            "output_schema": {"$ref": "#/components/schemas/RelayAutoConfigRep"}
        }
    )
)
# Capability for getRelayProxyConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRelayProxyConfig",
            "description": """Get Relay Proxy config""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The relay auto config id"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/RelayAutoConfigRep"}
        }
    )
)
# Capability for patchRelayAutoConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchRelayAutoConfig",
            "description": """Update a Relay Proxy config""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The relay auto config id"}, "body": {"$ref": "#/components/schemas/PatchWithComment"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/RelayAutoConfigRep"}
        }
    )
)
# Capability for deleteRelayAutoConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteRelayAutoConfig",
            "description": """Delete Relay Proxy config by ID""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The relay auto config id"}}, "required": ["id"]},
            "output_schema": {}
        }
    )
)
# Capability for resetRelayAutoConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "resetRelayAutoConfig",
            "description": """Reset Relay Proxy configuration key""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The Relay Proxy configuration ID"}, "expiry": {"type": "integer", "format": "int64", "description": "An expiration time for the old Relay Proxy configuration key, expressed as a Unix epoch time in milliseconds. By default, the Relay Proxy configuration will expire immediately."}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/RelayAutoConfigRep"}
        }
    )
)
# Capability for getApplications
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApplications",
            "description": """Get applications""",
            "input_schema": {"type": "object", "properties": {"filter": {"type": "string", "format": "string", "description": "Accepts filter by `key`, `name`, `kind`, and `autoAdded`. To learn more about the filter syntax, read [Filtering applications and application versions](https://launchdarkly.com/docs/api/applications-beta#filtering-applications-and-application-versions)."}, "limit": {"type": "integer", "format": "int64", "description": "The number of applications to return. Defaults to 10."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "sort": {"type": "string", "format": "string", "description": "Accepts sorting order and fields. Fields can be comma separated. Possible fields are `creationDate`, `name`. Examples: `sort=name` sort by names ascending, `sort=-name,creationDate` sort by names descending and creationDate ascending."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Options: `flags`."}}},
            "output_schema": {"$ref": "#/components/schemas/ApplicationCollectionRep"}
        }
    )
)
# Capability for getApplication
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApplication",
            "description": """Get application by key""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Options: `flags`."}}, "required": ["applicationKey"]},
            "output_schema": {"$ref": "#/components/schemas/ApplicationRep"}
        }
    )
)
# Capability for patchApplication
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchApplication",
            "description": """Update application""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["applicationKey"]},
            "output_schema": {"$ref": "#/components/schemas/ApplicationRep"}
        }
    )
)
# Capability for deleteApplication
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteApplication",
            "description": """Delete application""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}}, "required": ["applicationKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getApplicationVersions
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApplicationVersions",
            "description": """Get application versions by application key""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}, "filter": {"type": "string", "format": "string", "description": "Accepts filter by `key`, `name`, `supported`, and `autoAdded`. To learn more about the filter syntax, read [Filtering applications and application versions](https://launchdarkly.com/docs/api/applications-beta#filtering-applications-and-application-versions)."}, "limit": {"type": "integer", "format": "int64", "description": "The number of versions to return. Defaults to 50."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "sort": {"type": "string", "format": "string", "description": "Accepts sorting order and fields. Fields can be comma separated. Possible fields are `creationDate`, `name`. Examples: `sort=name` sort by names ascending, `sort=-name,creationDate` sort by names descending and creationDate ascending."}}, "required": ["applicationKey"]},
            "output_schema": {"$ref": "#/components/schemas/ApplicationVersionsCollectionRep"}
        }
    )
)
# Capability for patchApplicationVersion
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchApplicationVersion",
            "description": """Update application version""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}, "versionKey": {"type": "string", "format": "string", "description": "The application version key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["applicationKey", "versionKey"]},
            "output_schema": {"$ref": "#/components/schemas/ApplicationVersionRep"}
        }
    )
)
# Capability for deleteApplicationVersion
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteApplicationVersion",
            "description": """Delete application version""",
            "input_schema": {"type": "object", "properties": {"applicationKey": {"type": "string", "format": "string", "description": "The application key"}, "versionKey": {"type": "string", "format": "string", "description": "The application version key"}}, "required": ["applicationKey", "versionKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getApprovalRequests
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApprovalRequests",
            "description": """List approval requests""",
            "input_schema": {"type": "object", "properties": {"filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form `field operator value`. Supported fields are explained above."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of fields to expand in the response. Supported fields are explained above."}, "limit": {"type": "integer", "format": "int64", "description": "The number of approvals to return. Defaults to 20. Maximum limit is 200."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}},
            "output_schema": {"$ref": "#/components/schemas/ExpandableApprovalRequestsResponse"}
        }
    )
)
# Capability for postApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequest",
            "description": """Create approval request""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/CreateApprovalRequestRequest"}}},
            "output_schema": {"$ref": "#/components/schemas/ApprovalRequestResponse"}
        }
    )
)
# Capability for getApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApprovalRequest",
            "description": """Get approval request""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The approval request ID"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of fields to expand in the response. Supported fields are explained above."}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/ExpandableApprovalRequestResponse"}
        }
    )
)
# Capability for patchApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchApprovalRequest",
            "description": """Update approval request""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The approval ID"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for deleteApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteApprovalRequest",
            "description": """Delete approval request""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The approval request ID"}}, "required": ["id"]},
            "output_schema": {}
        }
    )
)
# Capability for postApprovalRequestApply
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequestApply",
            "description": """Apply approval request""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The approval request ID"}, "body": {"$ref": "#/components/schemas/postApprovalRequestApplyRequest"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/ApprovalRequestResponse"}
        }
    )
)
# Capability for postApprovalRequestReview
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequestReview",
            "description": """Review approval request""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The approval request ID"}, "body": {"$ref": "#/components/schemas/postApprovalRequestReviewRequest"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/ApprovalRequestResponse"}
        }
    )
)
# Capability for getAuditLogEntries
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAuditLogEntries",
            "description": """List audit log entries""",
            "input_schema": {"type": "object", "properties": {"before": {"type": "integer", "format": "int64", "description": "A timestamp filter, expressed as a Unix epoch time in milliseconds.  All entries this returns occurred before the timestamp."}, "after": {"type": "integer", "format": "int64", "description": "A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries this returns occurred after the timestamp."}, "q": {"type": "string", "format": "string", "description": "Text to search for. You can search for the full or partial name of the resource."}, "limit": {"type": "integer", "format": "int64", "description": "A limit on the number of audit log entries that return. Set between 1 and 20. The default is 10."}, "spec": {"type": "string", "format": "string", "description": "A resource specifier that lets you filter audit log listings by resource"}}},
            "output_schema": {"$ref": "#/components/schemas/AuditLogEntryListingRepCollection"}
        }
    )
)
# Capability for postAuditLogEntries
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postAuditLogEntries",
            "description": """Search audit log entries""",
            "input_schema": {"type": "object", "properties": {"before": {"type": "integer", "format": "int64", "description": "A timestamp filter, expressed as a Unix epoch time in milliseconds.  All entries returned occurred before the timestamp."}, "after": {"type": "integer", "format": "int64", "description": "A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries returned occurred after the timestamp."}, "q": {"type": "string", "format": "string", "description": "Text to search for. You can search for the full or partial name of the resource."}, "limit": {"type": "integer", "format": "int64", "description": "A limit on the number of audit log entries that return. Set between 1 and 20. The default is 10."}, "body": {"$ref": "#/components/schemas/StatementPostList"}}},
            "output_schema": {"$ref": "#/components/schemas/AuditLogEntryListingRepCollection"}
        }
    )
)
# Capability for getAuditLogEntry
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAuditLogEntry",
            "description": """Get audit log entry""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the audit log entry"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/AuditLogEntryRep"}
        }
    )
)
# Capability for getCallerIdentity
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getCallerIdentity",
            "description": """Identify the caller""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/CallerIdentityRep"}
        }
    )
)
# Capability for getExtinctions
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExtinctions",
            "description": """List extinctions""",
            "input_schema": {"type": "object", "properties": {"repoName": {"type": "string", "format": "string", "description": "Filter results to a specific repository"}, "branchName": {"type": "string", "format": "string", "description": "Filter results to a specific branch. By default, only the default branch will be queried for extinctions."}, "projKey": {"type": "string", "format": "string", "description": "Filter results to a specific project"}, "flagKey": {"type": "string", "format": "string", "description": "Filter results to a specific flag key"}, "from": {"type": "integer", "format": "int64", "description": "Filter results to a specific timeframe based on commit time, expressed as a Unix epoch time in milliseconds. Must be used with `to`."}, "to": {"type": "integer", "format": "int64", "description": "Filter results to a specific timeframe based on commit time, expressed as a Unix epoch time in milliseconds. Must be used with `from`."}}},
            "output_schema": {"$ref": "#/components/schemas/ExtinctionCollectionRep"}
        }
    )
)
# Capability for getRepositories
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRepositories",
            "description": """List repositories""",
            "input_schema": {"type": "object", "properties": {"withBranches": {"type": "string", "format": "string", "description": "If set to any value, the endpoint returns repositories with associated branch data"}, "withReferencesForDefaultBranch": {"type": "string", "format": "string", "description": "If set to any value, the endpoint returns repositories with associated branch data, as well as code references for the default git branch"}, "projKey": {"type": "string", "format": "string", "description": "A LaunchDarkly project key. If provided, this filters code reference results to the specified project."}, "flagKey": {"type": "string", "format": "string", "description": "If set to any value, the endpoint returns repositories with associated branch data, as well as code references for the default git branch"}}},
            "output_schema": {"$ref": "#/components/schemas/RepositoryCollectionRep"}
        }
    )
)
# Capability for postRepository
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postRepository",
            "description": """Create repository""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/repositoryPost"}}},
            "output_schema": {"$ref": "#/components/schemas/RepositoryRep"}
        }
    )
)
# Capability for getRepository
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRepository",
            "description": """Get repository""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}}, "required": ["repo"]},
            "output_schema": {"$ref": "#/components/schemas/RepositoryRep"}
        }
    )
)
# Capability for patchRepository
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchRepository",
            "description": """Update repository""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["repo"]},
            "output_schema": {"$ref": "#/components/schemas/RepositoryRep"}
        }
    )
)
# Capability for deleteRepository
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteRepository",
            "description": """Delete repository""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}}, "required": ["repo"]},
            "output_schema": {}
        }
    )
)
# Capability for deleteBranches
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteBranches",
            "description": """Delete branches""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name to delete branches for."}, "body": {"type": "array", "items": {"type": "string"}}}, "required": ["repo"]},
            "output_schema": {}
        }
    )
)
# Capability for getBranches
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBranches",
            "description": """List branches""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}}, "required": ["repo"]},
            "output_schema": {"$ref": "#/components/schemas/BranchCollectionRep"}
        }
    )
)
# Capability for getBranch
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBranch",
            "description": """Get branch""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}, "branch": {"type": "string", "format": "string", "description": "The url-encoded branch name"}, "projKey": {"type": "string", "format": "string", "description": "Filter results to a specific project"}, "flagKey": {"type": "string", "format": "string", "description": "Filter results to a specific flag key"}}, "required": ["repo", "branch"]},
            "output_schema": {"$ref": "#/components/schemas/BranchRep"}
        }
    )
)
# Capability for putBranch
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putBranch",
            "description": """Upsert branch""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}, "branch": {"type": "string", "format": "string", "description": "The URL-encoded branch name"}, "body": {"$ref": "#/components/schemas/putBranch"}}, "required": ["repo", "branch"]},
            "output_schema": {}
        }
    )
)
# Capability for postExtinction
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postExtinction",
            "description": """Create extinction""",
            "input_schema": {"type": "object", "properties": {"repo": {"type": "string", "format": "string", "description": "The repository name"}, "branch": {"type": "string", "format": "string", "description": "The URL-encoded branch name"}, "body": {"$ref": "#/components/schemas/ExtinctionListPost"}}, "required": ["repo", "branch"]},
            "output_schema": {}
        }
    )
)
# Capability for getRootStatistic
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getRootStatistic",
            "description": """Get links to code reference repositories for each project""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/StatisticsRoot"}
        }
    )
)
# Capability for getStatistics
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getStatistics",
            "description": """Get code references statistics for flags""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "Filter results to a specific flag key"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/StatisticCollectionRep"}
        }
    )
)
# Capability for getDestinations
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDestinations",
            "description": """List destinations""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/Destinations"}
        }
    )
)
# Capability for postGenerateWarehouseDestinationKeyPair
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postGenerateWarehouseDestinationKeyPair",
            "description": """Generate Snowflake destination key pair""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/GenerateWarehouseDestinationKeyPairPostRep"}
        }
    )
)
# Capability for postDestination
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postDestination",
            "description": """Create Data Export destination""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/DestinationPost"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Destination"}
        }
    )
)
# Capability for getDestination
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDestination",
            "description": """Get destination""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The Data Export destination ID"}}, "required": ["projectKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/Destination"}
        }
    )
)
# Capability for patchDestination
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchDestination",
            "description": """Update Data Export destination""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The Data Export destination ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/Destination"}
        }
    )
)
# Capability for deleteDestination
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteDestination",
            "description": """Delete Data Export destination""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The Data Export destination ID"}}, "required": ["projectKey", "environmentKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for getFlagLinks
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagLinks",
            "description": """List flag links""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagLinkCollectionRep"}
        }
    )
)
# Capability for createFlagLink
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createFlagLink",
            "description": """Create flag link""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/flagLinkPost"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagLinkRep"}
        }
    )
)
# Capability for updateFlagLink
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateFlagLink",
            "description": """Update flag link""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "id": {"type": "string", "format": "string", "description": "The flag link ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "featureFlagKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagLinkRep"}
        }
    )
)
# Capability for deleteFlagLink
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteFlagLink",
            "description": """Delete flag link""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "id": {"type": "string", "format": "string", "description": "The flag link ID or Key"}}, "required": ["projectKey", "featureFlagKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for getFeatureFlagStatusAcrossEnvironments
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlagStatusAcrossEnvironments",
            "description": """Get flag status across environments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "env": {"type": "string", "format": "string", "description": "Optional environment filter"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagStatusAcrossEnvironments"}
        }
    )
)
# Capability for getFeatureFlagStatuses
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlagStatuses",
            "description": """List feature flag statuses""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagStatuses"}
        }
    )
)
# Capability for getFeatureFlagStatus
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlagStatus",
            "description": """Get feature flag status""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagStatusRep"}
        }
    )
)
# Capability for getFeatureFlags
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlags",
            "description": """List feature flags""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "env": {"type": "string", "format": "string", "description": "Filter configurations by environment"}, "tag": {"type": "string", "format": "string", "description": "Filter feature flags by tag"}, "limit": {"type": "integer", "format": "int64", "description": "The number of feature flags to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "archived": {"type": "boolean", "description": "Deprecated, use `filter=archived:true` instead. A boolean to filter the list to archived flags. When this is absent, only unarchived flags will be returned"}, "summary": {"type": "boolean", "description": "By default, flags do _not_ include their lists of prerequisites, targets, or rules for each environment. Set `summary=0` to include these fields for each flag returned."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form field:value. Read the endpoint description for a full list of available filter fields."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order. Read the endpoint description for a full list of available sort fields."}, "compare": {"type": "boolean", "description": "Deprecated, unavailable in API version `20240415`. A boolean to filter results by only flags that have differences between environments."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of fields to expand in the response. Supported fields are explained above."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlags"}
        }
    )
)
# Capability for postFeatureFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postFeatureFlag",
            "description": """Create a feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "clone": {"type": "string", "format": "string", "description": "The key of the feature flag to be cloned. The key identifies the flag in your code. For example, setting `clone=flagKey` copies the full targeting configuration for all environments, including `on/off` state, from the original flag to the new flag."}, "body": {"$ref": "#/components/schemas/FeatureFlagBody"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlag"}
        }
    )
)
# Capability for getDependentFlagsByEnv
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDependentFlagsByEnv",
            "description": """List dependent feature flags by environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/DependentFlagsByEnvironment"}
        }
    )
)
# Capability for getFeatureFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlag",
            "description": """Get feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "env": {"type": "string", "format": "string", "description": "Filter configurations by environment"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of fields to expand in the response. Supported fields are explained above."}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlag"}
        }
    )
)
# Capability for patchFeatureFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchFeatureFlag",
            "description": """Update feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key. The key identifies the flag in your code."}, "ignoreConflicts": {"type": "boolean", "description": "If true, the patch will be applied even if it causes a pending scheduled change or approval request to fail."}, "body": {"$ref": "#/components/schemas/PatchWithComment"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlag"}
        }
    )
)
# Capability for deleteFeatureFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteFeatureFlag",
            "description": """Delete feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key. The key identifies the flag in your code."}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {}
        }
    )
)
# Capability for copyFeatureFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "copyFeatureFlag",
            "description": """Copy feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key. The key identifies the flag in your code."}, "body": {"$ref": "#/components/schemas/FlagCopyConfigPost"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlag"}
        }
    )
)
# Capability for getDependentFlags
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDependentFlags",
            "description": """List dependent feature flags""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/MultiEnvironmentDependentFlags"}
        }
    )
)
# Capability for getExpiringContextTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExpiringContextTargets",
            "description": """Get expiring context targets for feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringTargetGetResponse"}
        }
    )
)
# Capability for patchExpiringTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExpiringTargets",
            "description": """Update expiring context targets on feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/patchFlagsRequest"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringTargetPatchResponse"}
        }
    )
)
# Capability for getExpiringUserTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExpiringUserTargets",
            "description": """Get expiring user targets for feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetGetResponse"}
        }
    )
)
# Capability for patchExpiringUserTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExpiringUserTargets",
            "description": """Update expiring user targets on feature flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/patchFlagsRequest"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetPatchResponse"}
        }
    )
)
# Capability for getTriggerWorkflows
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTriggerWorkflows",
            "description": """List flag triggers""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/TriggerWorkflowCollectionRep"}
        }
    )
)
# Capability for createTriggerWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createTriggerWorkflow",
            "description": """Create flag trigger""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/triggerPost"}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/TriggerWorkflowRep"}
        }
    )
)
# Capability for getTriggerWorkflowById
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTriggerWorkflowById",
            "description": """Get flag trigger by ID""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The flag trigger ID"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/TriggerWorkflowRep"}
        }
    )
)
# Capability for patchTriggerWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchTriggerWorkflow",
            "description": """Update flag trigger""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "id": {"type": "string", "format": "string", "description": "The flag trigger ID"}, "body": {"$ref": "#/components/schemas/FlagTriggerInput"}}, "required": ["projectKey", "environmentKey", "featureFlagKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/TriggerWorkflowRep"}
        }
    )
)
# Capability for deleteTriggerWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteTriggerWorkflow",
            "description": """Delete flag trigger""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "id": {"type": "string", "format": "string", "description": "The flag trigger ID"}}, "required": ["projectKey", "environmentKey", "featureFlagKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for getReleaseByFlagKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getReleaseByFlagKey",
            "description": """Get release for flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The flag key"}}, "required": ["projectKey", "flagKey"]},
            "output_schema": {"$ref": "#/components/schemas/Release"}
        }
    )
)
# Capability for patchReleaseByFlagKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchReleaseByFlagKey",
            "description": """Patch release for flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The flag key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "flagKey"]},
            "output_schema": {"$ref": "#/components/schemas/Release"}
        }
    )
)
# Capability for deleteReleaseByFlagKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteReleaseByFlagKey",
            "description": """Delete a release for flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The flag key"}}, "required": ["projectKey", "flagKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getBigSegmentStoreIntegrations
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBigSegmentStoreIntegrations",
            "description": """List all big segment store integrations""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentStoreIntegrationCollection"}
        }
    )
)
# Capability for createBigSegmentStoreIntegration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createBigSegmentStoreIntegration",
            "description": """Create big segment store integration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key, either `redis` or `dynamodb`"}, "body": {"$ref": "#/components/schemas/IntegrationDeliveryConfigurationPost"}}, "required": ["projectKey", "environmentKey", "integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentStoreIntegration"}
        }
    )
)
# Capability for getBigSegmentStoreIntegration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBigSegmentStoreIntegration",
            "description": """Get big segment store integration by ID""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key, either `redis` or `dynamodb`"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}}, "required": ["projectKey", "environmentKey", "integrationKey", "integrationId"]},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentStoreIntegration"}
        }
    )
)
# Capability for patchBigSegmentStoreIntegration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchBigSegmentStoreIntegration",
            "description": """Update big segment store integration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key, either `redis` or `dynamodb`"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "environmentKey", "integrationKey", "integrationId"]},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentStoreIntegration"}
        }
    )
)
# Capability for deleteBigSegmentStoreIntegration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteBigSegmentStoreIntegration",
            "description": """Delete big segment store integration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key, either `redis` or `dynamodb`"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}}, "required": ["projectKey", "environmentKey", "integrationKey", "integrationId"]},
            "output_schema": {}
        }
    )
)
# Capability for getIntegrationDeliveryConfigurations
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getIntegrationDeliveryConfigurations",
            "description": """List all delivery configurations""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfigurationCollection"}
        }
    )
)
# Capability for getIntegrationDeliveryConfigurationByEnvironment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getIntegrationDeliveryConfigurationByEnvironment",
            "description": """Get delivery configurations by environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfigurationCollection"}
        }
    )
)
# Capability for createIntegrationDeliveryConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createIntegrationDeliveryConfiguration",
            "description": """Create delivery configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "body": {"$ref": "#/components/schemas/IntegrationDeliveryConfigurationPost"}}, "required": ["projectKey", "environmentKey", "integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfiguration"}
        }
    )
)
# Capability for getIntegrationDeliveryConfigurationById
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getIntegrationDeliveryConfigurationById",
            "description": """Get delivery configuration by ID""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The configuration ID"}}, "required": ["projectKey", "environmentKey", "integrationKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfiguration"}
        }
    )
)
# Capability for patchIntegrationDeliveryConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchIntegrationDeliveryConfiguration",
            "description": """Update delivery configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The configuration ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "environmentKey", "integrationKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfiguration"}
        }
    )
)
# Capability for deleteIntegrationDeliveryConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteIntegrationDeliveryConfiguration",
            "description": """Delete delivery configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The configuration ID"}}, "required": ["projectKey", "environmentKey", "integrationKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for validateIntegrationDeliveryConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "validateIntegrationDeliveryConfiguration",
            "description": """Validate delivery configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The configuration ID"}}, "required": ["projectKey", "environmentKey", "integrationKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationDeliveryConfigurationResponse"}
        }
    )
)
# Capability for getFlagImportConfigurations
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagImportConfigurations",
            "description": """List all flag import configurations""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/FlagImportIntegrationCollection"}
        }
    )
)
# Capability for createFlagImportConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createFlagImportConfiguration",
            "description": """Create a flag import configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "body": {"$ref": "#/components/schemas/FlagImportConfigurationPost"}}, "required": ["projectKey", "integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagImportIntegration"}
        }
    )
)
# Capability for getFlagImportConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagImportConfiguration",
            "description": """Get a single flag import configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key, for example, `split`"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}}, "required": ["projectKey", "integrationKey", "integrationId"]},
            "output_schema": {"$ref": "#/components/schemas/FlagImportIntegration"}
        }
    )
)
# Capability for patchFlagImportConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchFlagImportConfiguration",
            "description": """Update a flag import configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "integrationKey", "integrationId"]},
            "output_schema": {"$ref": "#/components/schemas/FlagImportIntegration"}
        }
    )
)
# Capability for deleteFlagImportConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteFlagImportConfiguration",
            "description": """Delete a flag import configuration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}}, "required": ["projectKey", "integrationKey", "integrationId"]},
            "output_schema": {}
        }
    )
)
# Capability for triggerFlagImportJob
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "triggerFlagImportJob",
            "description": """Trigger a single flag import run""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "integrationId": {"type": "string", "format": "string", "description": "The integration ID"}}, "required": ["projectKey", "integrationKey", "integrationId"]},
            "output_schema": {}
        }
    )
)
# Capability for getAllIntegrationConfigurations
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAllIntegrationConfigurations",
            "description": """Get all configurations for the integration""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "Integration key"}}, "required": ["integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationConfigurationCollectionRep"}
        }
    )
)
# Capability for createIntegrationConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createIntegrationConfiguration",
            "description": """Create integration configuration""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "body": {"$ref": "#/components/schemas/IntegrationConfigurationPost"}}, "required": ["integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationConfigurationsRep"}
        }
    )
)
# Capability for getIntegrationConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getIntegrationConfiguration",
            "description": """Get an integration configuration""",
            "input_schema": {"type": "object", "properties": {"integrationConfigurationId": {"type": "string", "format": "string", "description": "Integration configuration ID"}}, "required": ["integrationConfigurationId"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationConfigurationsRep"}
        }
    )
)
# Capability for updateIntegrationConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateIntegrationConfiguration",
            "description": """Update integration configuration""",
            "input_schema": {"type": "object", "properties": {"integrationConfigurationId": {"type": "string", "format": "string", "description": "The ID of the integration configuration"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["integrationConfigurationId"]},
            "output_schema": {"$ref": "#/components/schemas/IntegrationConfigurationsRep"}
        }
    )
)
# Capability for deleteIntegrationConfiguration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteIntegrationConfiguration",
            "description": """Delete integration configuration""",
            "input_schema": {"type": "object", "properties": {"integrationConfigurationId": {"type": "string", "format": "string", "description": "The ID of the integration configuration to be deleted"}}, "required": ["integrationConfigurationId"]},
            "output_schema": {}
        }
    )
)
# Capability for getSubscriptions
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSubscriptions",
            "description": """Get audit log subscriptions by integration""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}}, "required": ["integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/Integrations"}
        }
    )
)
# Capability for createSubscription
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createSubscription",
            "description": """Create audit log subscription""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "body": {"$ref": "#/components/schemas/subscriptionPost"}}, "required": ["integrationKey"]},
            "output_schema": {"$ref": "#/components/schemas/Integration"}
        }
    )
)
# Capability for getSubscriptionByID
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSubscriptionByID",
            "description": """Get audit log subscription by ID""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The subscription ID"}}, "required": ["integrationKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/Integration"}
        }
    )
)
# Capability for updateSubscription
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateSubscription",
            "description": """Update audit log subscription""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The ID of the audit log subscription"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["integrationKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/Integration"}
        }
    )
)
# Capability for deleteSubscription
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteSubscription",
            "description": """Delete audit log subscription""",
            "input_schema": {"type": "object", "properties": {"integrationKey": {"type": "string", "format": "string", "description": "The integration key"}, "id": {"type": "string", "format": "string", "description": "The subscription ID"}}, "required": ["integrationKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for getMembers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMembers",
            "description": """List account members""",
            "input_schema": {"type": "object", "properties": {"limit": {"type": "integer", "format": "int64", "description": "The number of members to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form `field:value`. Supported fields are explained above."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order."}}},
            "output_schema": {"$ref": "#/components/schemas/Members"}
        }
    )
)
# Capability for postMembers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postMembers",
            "description": """Invite new members""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/NewMemberFormListPost"}}},
            "output_schema": {"$ref": "#/components/schemas/Members"}
        }
    )
)
# Capability for patchMembers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchMembers",
            "description": """Modify account members""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/membersPatchInput"}}},
            "output_schema": {"$ref": "#/components/schemas/BulkEditMembersRep"}
        }
    )
)
# Capability for getMember
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMember",
            "description": """Get account member""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The member ID"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Member"}
        }
    )
)
# Capability for patchMember
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchMember",
            "description": """Modify an account member""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The member ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Member"}
        }
    )
)
# Capability for deleteMember
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteMember",
            "description": """Delete account member""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The member ID"}}, "required": ["id"]},
            "output_schema": {}
        }
    )
)
# Capability for postMemberTeams
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postMemberTeams",
            "description": """Add a member to teams""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The member ID"}, "body": {"$ref": "#/components/schemas/MemberTeamsPostInput"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Member"}
        }
    )
)
# Capability for getMetrics
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMetrics",
            "description": """List metrics""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}, "limit": {"type": "integer", "format": "int64", "description": "The number of metrics to return in the response. Defaults to 20. Maximum limit is 50."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items."}, "sort": {"type": "string", "format": "string", "description": "A field to sort the items by. Prefix field by a dash ( - ) to sort in descending order. This endpoint supports sorting by `createdAt` or `name`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. This endpoint accepts filtering by `query`, `tags`, 'eventKind', 'isNumeric', 'unitAggregationType`, `hasConnections`, `maintainerIds`, and `maintainerTeamKey`. To learn more about the filter syntax, read the 'Filtering metrics' section above."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricCollectionRep"}
        }
    )
)
# Capability for postMetric
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postMetric",
            "description": """Create metric""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/MetricPost"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricRep"}
        }
    )
)
# Capability for getMetric
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMetric",
            "description": """Get metric""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricKey": {"type": "string", "format": "string", "description": "The metric key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}, "versionId": {"type": "string", "format": "string", "description": "The specific version ID of the metric"}}, "required": ["projectKey", "metricKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricRep"}
        }
    )
)
# Capability for patchMetric
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchMetric",
            "description": """Update metric""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricKey": {"type": "string", "format": "string", "description": "The metric key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "metricKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricRep"}
        }
    )
)
# Capability for deleteMetric
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteMetric",
            "description": """Delete metric""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricKey": {"type": "string", "format": "string", "description": "The metric key"}}, "required": ["projectKey", "metricKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getOAuthClients
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getOAuthClients",
            "description": """Get clients""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/ClientCollection"}
        }
    )
)
# Capability for createOAuth2Client
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createOAuth2Client",
            "description": """Create a LaunchDarkly OAuth 2.0 client""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/oauthClientPost"}}},
            "output_schema": {"$ref": "#/components/schemas/Client"}
        }
    )
)
# Capability for getOAuthClientById
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getOAuthClientById",
            "description": """Get client by ID""",
            "input_schema": {"type": "object", "properties": {"clientId": {"type": "string", "format": "string", "description": "The client ID"}}, "required": ["clientId"]},
            "output_schema": {"$ref": "#/components/schemas/Client"}
        }
    )
)
# Capability for patchOAuthClient
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchOAuthClient",
            "description": """Patch client by ID""",
            "input_schema": {"type": "object", "properties": {"clientId": {"type": "string", "format": "string", "description": "The client ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["clientId"]},
            "output_schema": {"$ref": "#/components/schemas/Client"}
        }
    )
)
# Capability for deleteOAuthClient
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteOAuthClient",
            "description": """Delete OAuth 2.0 client""",
            "input_schema": {"type": "object", "properties": {"clientId": {"type": "string", "format": "string", "description": "The client ID"}}, "required": ["clientId"]},
            "output_schema": {}
        }
    )
)
# Capability for getOpenapiSpec
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getOpenapiSpec",
            "description": """Gets the OpenAPI spec in json""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {}
        }
    )
)
# Capability for getProjects
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getProjects",
            "description": """List projects""",
            "input_schema": {"type": "object", "properties": {"limit": {"type": "integer", "format": "int64", "description": "The number of projects to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is constructed as `field:value`."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}},
            "output_schema": {"$ref": "#/components/schemas/Projects"}
        }
    )
)
# Capability for postProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postProject",
            "description": """Create project""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/ProjectPost"}}},
            "output_schema": {"$ref": "#/components/schemas/ProjectRep"}
        }
    )
)
# Capability for getProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getProject",
            "description": """Get project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/Project"}
        }
    )
)
# Capability for patchProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchProject",
            "description": """Update project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/ProjectRep"}
        }
    )
)
# Capability for deleteProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteProject",
            "description": """Delete project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}}, "required": ["projectKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getContextKindsByProjectKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContextKindsByProjectKey",
            "description": """Get context kinds""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/ContextKindsCollectionRep"}
        }
    )
)
# Capability for putContextKind
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putContextKind",
            "description": """Create or update context kind""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "key": {"type": "string", "format": "string", "description": "The context kind key"}, "body": {"$ref": "#/components/schemas/UpsertContextKindPayload"}}, "required": ["projectKey", "key"]},
            "output_schema": {"$ref": "#/components/schemas/UpsertResponseRep"}
        }
    )
)
# Capability for getEnvironmentsByProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getEnvironmentsByProject",
            "description": """List environments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of environments to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form `field:value`."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environments"}
        }
    )
)
# Capability for postEnvironment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postEnvironment",
            "description": """Create environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/EnvironmentPost"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environment"}
        }
    )
)
# Capability for getEnvironment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getEnvironment",
            "description": """Get environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environment"}
        }
    )
)
# Capability for patchEnvironment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchEnvironment",
            "description": """Update environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environment"}
        }
    )
)
# Capability for deleteEnvironment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteEnvironment",
            "description": """Delete environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for resetEnvironmentSDKKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "resetEnvironmentSDKKey",
            "description": """Reset environment SDK key""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "expiry": {"type": "integer", "format": "int64", "description": "The time at which you want the old SDK key to expire, in UNIX milliseconds. By default, the key expires immediately. During the period between this call and the time when the old SDK key expires, both the old SDK key and the new SDK key will work."}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environment"}
        }
    )
)
# Capability for getContextAttributeNames
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContextAttributeNames",
            "description": """Get context attribute names""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. This endpoint only accepts `kind` filters, with the `equals` operator, and `name` filters, with the `startsWith` operator. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 100, default: 100)"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ContextAttributeNamesCollection"}
        }
    )
)
# Capability for getContextAttributeValues
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContextAttributeValues",
            "description": """Get context attribute values""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "attributeName": {"type": "string", "format": "string", "description": "The attribute name"}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. This endpoint only accepts `kind` filters, with the `equals` operator, and `value` filters, with the `startsWith` operator. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 100, default: 50)"}}, "required": ["projectKey", "environmentKey", "attributeName"]},
            "output_schema": {"$ref": "#/components/schemas/ContextAttributeValuesCollection"}
        }
    )
)
# Capability for searchContextInstances
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "searchContextInstances",
            "description": """Search for context instances""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 50, default: 20)"}, "continuationToken": {"type": "string", "format": "string", "description": "Limits results to context instances with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead."}, "sort": {"type": "string", "format": "string", "description": "Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "includeTotalCount": {"type": "boolean", "description": "Specifies whether to include or omit the total count of matching context instances. Defaults to true."}, "body": {"$ref": "#/components/schemas/ContextInstanceSearch"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ContextInstances"}
        }
    )
)
# Capability for getContextInstances
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContextInstances",
            "description": """Get context instances""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The context instance ID"}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of context instances to return (max: 50, default: 20)"}, "continuationToken": {"type": "string", "format": "string", "description": "Limits results to context instances with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead."}, "sort": {"type": "string", "format": "string", "description": "Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "includeTotalCount": {"type": "boolean", "description": "Specifies whether to include or omit the total count of matching context instances. Defaults to true."}}, "required": ["projectKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/ContextInstances"}
        }
    )
)
# Capability for deleteContextInstances
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteContextInstances",
            "description": """Delete context instances""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The context instance ID"}}, "required": ["projectKey", "environmentKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for searchContexts
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "searchContexts",
            "description": """Search for contexts""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 50, default: 20)"}, "continuationToken": {"type": "string", "format": "string", "description": "Limits results to contexts with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead."}, "sort": {"type": "string", "format": "string", "description": "Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "includeTotalCount": {"type": "boolean", "description": "Specifies whether to include or omit the total count of matching contexts. Defaults to true."}, "body": {"$ref": "#/components/schemas/ContextSearch"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Contexts"}
        }
    )
)
# Capability for putContextFlagSetting
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putContextFlagSetting",
            "description": """Update flag settings for context""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "contextKind": {"type": "string", "format": "string", "description": "The context kind"}, "contextKey": {"type": "string", "format": "string", "description": "The context key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/ValuePut"}}, "required": ["projectKey", "environmentKey", "contextKind", "contextKey", "featureFlagKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getContexts
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContexts",
            "description": """Get contexts""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "kind": {"type": "string", "format": "string", "description": "The context kind"}, "key": {"type": "string", "format": "string", "description": "The context key"}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 50, default: 20)"}, "continuationToken": {"type": "string", "format": "string", "description": "Limits results to contexts with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead."}, "sort": {"type": "string", "format": "string", "description": "Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://launchdarkly.com/docs/ld-docs/api/contexts#filtering-contexts-and-context-instances)."}, "includeTotalCount": {"type": "boolean", "description": "Specifies whether to include or omit the total count of matching contexts. Defaults to true."}}, "required": ["projectKey", "environmentKey", "kind", "key"]},
            "output_schema": {"$ref": "#/components/schemas/Contexts"}
        }
    )
)
# Capability for getExperiments
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperiments",
            "description": """Get experiments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "The maximum number of experiments to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form `field:value`. Supported fields are explained above."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above."}, "lifecycleState": {"type": "string", "format": "string", "description": "A comma-separated list of experiment archived states. Supports `archived`, `active`, or both. Defaults to `active` experiments."}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExperimentCollectionRep"}
        }
    )
)
# Capability for createExperiment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createExperiment",
            "description": """Create experiment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/ExperimentPost"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Experiment"}
        }
    )
)
# Capability for getExperiment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperiment",
            "description": """Get experiment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "experimentKey": {"type": "string", "format": "string", "description": "The experiment key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above."}}, "required": ["projectKey", "environmentKey", "experimentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Experiment"}
        }
    )
)
# Capability for patchExperiment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExperiment",
            "description": """Patch experiment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "experimentKey": {"type": "string", "format": "string", "description": "The experiment key"}, "body": {"$ref": "#/components/schemas/ExperimentPatchInput"}}, "required": ["projectKey", "environmentKey", "experimentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Experiment"}
        }
    )
)
# Capability for createIteration
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createIteration",
            "description": """Create iteration""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "experimentKey": {"type": "string", "format": "string", "description": "The experiment key"}, "body": {"$ref": "#/components/schemas/IterationInput"}}, "required": ["projectKey", "environmentKey", "experimentKey"]},
            "output_schema": {"$ref": "#/components/schemas/IterationRep"}
        }
    )
)
# Capability for getExperimentResultsForMetricGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperimentResultsForMetricGroup",
            "description": """Get experiment results for metric group (Deprecated)""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "experimentKey": {"type": "string", "format": "string", "description": "The experiment key"}, "metricGroupKey": {"type": "string", "format": "string", "description": "The metric group key"}, "iterationId": {"type": "string", "format": "string", "description": "The iteration ID"}}, "required": ["projectKey", "environmentKey", "experimentKey", "metricGroupKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricGroupResultsRep"}
        }
    )
)
# Capability for getExperimentResults
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperimentResults",
            "description": """Get experiment results (Deprecated)""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "experimentKey": {"type": "string", "format": "string", "description": "The experiment key"}, "metricKey": {"type": "string", "format": "string", "description": "The metric key"}, "iterationId": {"type": "string", "format": "string", "description": "The iteration ID"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of fields to expand in the response. Supported fields are explained above."}}, "required": ["projectKey", "environmentKey", "experimentKey", "metricKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExperimentBayesianResultsRep"}
        }
    )
)
# Capability for evaluateContextInstance
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "evaluateContextInstance",
            "description": """Evaluate flags for context instance""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of feature flags to return. Defaults to -1, which returns all flags"}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order"}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form `field operator value`. Supported fields are explained above."}, "body": {"$ref": "#/components/schemas/ContextInstance"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ContextInstanceEvaluations"}
        }
    )
)
# Capability for getFollowersByProjEnv
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFollowersByProjEnv",
            "description": """Get followers of all flags in a given project and environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagFollowersByProjEnvGetRep"}
        }
    )
)
# Capability for getAllHoldouts
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAllHoldouts",
            "description": """Get all holdouts""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of holdouts to return in the response. Defaults to 20"}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an `offset` of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/HoldoutsCollectionRep"}
        }
    )
)
# Capability for postHoldout
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postHoldout",
            "description": """Create holdout""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/HoldoutPostRequest"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/HoldoutRep"}
        }
    )
)
# Capability for getHoldoutById
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getHoldoutById",
            "description": """Get Holdout by Id""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "holdoutId": {"type": "string", "format": "string", "description": "The holdout experiment ID"}}, "required": ["projectKey", "environmentKey", "holdoutId"]},
            "output_schema": {"$ref": "#/components/schemas/HoldoutRep"}
        }
    )
)
# Capability for getHoldout
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getHoldout",
            "description": """Get holdout""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "holdoutKey": {"type": "string", "format": "string", "description": "The holdout experiment key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above. Holdout experiment expansion fields have no prefix. Related experiment expansion fields have `rel-` as a prefix."}}, "required": ["projectKey", "environmentKey", "holdoutKey"]},
            "output_schema": {"$ref": "#/components/schemas/HoldoutDetailRep"}
        }
    )
)
# Capability for patchHoldout
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchHoldout",
            "description": """Patch holdout""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "holdoutKey": {"type": "string", "format": "string", "description": "The holdout key"}, "body": {"$ref": "#/components/schemas/HoldoutPatchInput"}}, "required": ["projectKey", "environmentKey", "holdoutKey"]},
            "output_schema": {"$ref": "#/components/schemas/HoldoutRep"}
        }
    )
)
# Capability for resetEnvironmentMobileKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "resetEnvironmentMobileKey",
            "description": """Reset environment mobile SDK key""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Environment"}
        }
    )
)
# Capability for getContextInstanceSegmentsMembershipByEnv
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getContextInstanceSegmentsMembershipByEnv",
            "description": """List segment memberships for context instance""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/ContextInstance"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ContextInstanceSegmentMemberships"}
        }
    )
)
# Capability for getExperimentationSettings
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperimentationSettings",
            "description": """Get experimentation settings""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/RandomizationSettingsRep"}
        }
    )
)
# Capability for putExperimentationSettings
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putExperimentationSettings",
            "description": """Update experimentation settings""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/RandomizationSettingsPut"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/RandomizationSettingsRep"}
        }
    )
)
# Capability for getFlagDefaultsByProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagDefaultsByProject",
            "description": """Get flag defaults for project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/flagDefaultsRep"}
        }
    )
)
# Capability for patchFlagDefaultsByProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchFlagDefaultsByProject",
            "description": """Update flag default for project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/upsertPayloadRep"}
        }
    )
)
# Capability for putFlagDefaultsByProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putFlagDefaultsByProject",
            "description": """Create or update flag defaults for project""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/UpsertFlagDefaultsPayload"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/upsertPayloadRep"}
        }
    )
)
# Capability for getApprovalsForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApprovalsForFlag",
            "description": """List approval requests for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestsResponse"}
        }
    )
)
# Capability for postApprovalRequestForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequestForFlag",
            "description": """Create approval request for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/createFlagConfigApprovalRequestRequest"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for postFlagCopyConfigApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postFlagCopyConfigApprovalRequest",
            "description": """Create approval request to copy flag configurations across environments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key for the target environment"}, "body": {"$ref": "#/components/schemas/createCopyFlagConfigApprovalRequestRequest"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for getApprovalForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getApprovalForFlag",
            "description": """Get approval request for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The feature flag approval request ID"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for patchFlagConfigApprovalRequest
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchFlagConfigApprovalRequest",
            "description": """Update flag approval request""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The approval ID"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for deleteApprovalRequestForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteApprovalRequestForFlag",
            "description": """Delete approval request for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The feature flag approval request ID"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for postApprovalRequestApplyForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequestApplyForFlag",
            "description": """Apply approval request for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The feature flag approval request ID"}, "body": {"$ref": "#/components/schemas/postApprovalRequestApplyRequest"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for postApprovalRequestReviewForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postApprovalRequestReviewForFlag",
            "description": """Review approval request for a flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The feature flag approval request ID"}, "body": {"$ref": "#/components/schemas/postApprovalRequestReviewRequest"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FlagConfigApprovalRequestResponse"}
        }
    )
)
# Capability for getFlagFollowers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagFollowers",
            "description": """Get followers of a flag in a project and environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagFollowersGetRep"}
        }
    )
)
# Capability for putFlagFollower
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putFlagFollower",
            "description": """Add a member as a follower of a flag in a project and environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "memberId": {"type": "string", "format": "string", "description": "The memberId of the member to add as a follower of the flag. Reader roles can only add themselves."}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "memberId"]},
            "output_schema": {}
        }
    )
)
# Capability for deleteFlagFollower
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteFlagFollower",
            "description": """Remove a member as a follower of a flag in a project and environment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "memberId": {"type": "string", "format": "string", "description": "The memberId of the member to remove as a follower of the flag. Reader roles can only remove themselves."}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "memberId"]},
            "output_schema": {}
        }
    )
)
# Capability for getFlagConfigScheduledChanges
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagConfigScheduledChanges",
            "description": """List scheduled changes""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagScheduledChanges"}
        }
    )
)
# Capability for postFlagConfigScheduledChanges
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postFlagConfigScheduledChanges",
            "description": """Create scheduled changes workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "ignoreConflicts": {"type": "boolean", "description": "Whether to succeed (`true`) or fail (`false`) when these instructions conflict with existing scheduled changes"}, "body": {"$ref": "#/components/schemas/PostFlagScheduledChangesInput"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagScheduledChange"}
        }
    )
)
# Capability for getFeatureFlagScheduledChange
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFeatureFlagScheduledChange",
            "description": """Get a scheduled change""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The scheduled change id"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagScheduledChange"}
        }
    )
)
# Capability for patchFlagConfigScheduledChange
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchFlagConfigScheduledChange",
            "description": """Update scheduled changes workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The scheduled change ID"}, "ignoreConflicts": {"type": "boolean", "description": "Whether to succeed (`true`) or fail (`false`) when these new instructions conflict with existing scheduled changes"}, "body": {"$ref": "#/components/schemas/FlagScheduledChangesInput"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {"$ref": "#/components/schemas/FeatureFlagScheduledChange"}
        }
    )
)
# Capability for deleteFlagConfigScheduledChanges
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteFlagConfigScheduledChanges",
            "description": """Delete scheduled changes workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "id": {"type": "string", "format": "string", "description": "The scheduled change id"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "id"]},
            "output_schema": {}
        }
    )
)
# Capability for getWorkflows
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getWorkflows",
            "description": """Get workflows""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "status": {"type": "string", "format": "string", "description": "Filter results by workflow status. Valid status filters are `active`, `completed`, and `failed`."}, "sort": {"type": "string", "format": "string", "description": "A field to sort the items by. Prefix field by a dash ( - ) to sort in descending order. This endpoint supports sorting by `creationDate` or `stopDate`."}, "limit": {"type": "integer", "format": "int64", "description": "The maximum number of workflows to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Defaults to 0. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/CustomWorkflowsListingOutput"}
        }
    )
)
# Capability for postWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postWorkflow",
            "description": """Create workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "templateKey": {"type": "string", "format": "string", "description": "The template key to apply as a starting point for the new workflow"}, "dryRun": {"type": "boolean", "description": "Whether to call the endpoint in dry-run mode"}, "body": {"$ref": "#/components/schemas/CustomWorkflowInput"}}, "required": ["projectKey", "featureFlagKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/CustomWorkflowOutput"}
        }
    )
)
# Capability for getCustomWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getCustomWorkflow",
            "description": """Get custom workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "workflowId": {"type": "string", "format": "string", "description": "The workflow ID"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "workflowId"]},
            "output_schema": {"$ref": "#/components/schemas/CustomWorkflowOutput"}
        }
    )
)
# Capability for deleteWorkflow
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteWorkflow",
            "description": """Delete workflow""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "workflowId": {"type": "string", "format": "string", "description": "The workflow id"}}, "required": ["projectKey", "featureFlagKey", "environmentKey", "workflowId"]},
            "output_schema": {}
        }
    )
)
# Capability for postMigrationSafetyIssues
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postMigrationSafetyIssues",
            "description": """Get migration safety issues""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The migration flag key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/flagSempatch"}}, "required": ["projectKey", "flagKey", "environmentKey"]},
            "output_schema": {"type": "array", "items": {"$ref": "#/components/schemas/MigrationSafetyIssueRep"}}
        }
    )
)
# Capability for createReleaseForFlag
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createReleaseForFlag",
            "description": """Create a new release for flag""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The flag key"}, "body": {"$ref": "#/components/schemas/CreateReleaseInput"}}, "required": ["projectKey", "flagKey"]},
            "output_schema": {"$ref": "#/components/schemas/Release"}
        }
    )
)
# Capability for updatePhaseStatus
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updatePhaseStatus",
            "description": """Update phase status for release""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "flagKey": {"type": "string", "format": "string", "description": "The flag key"}, "phaseId": {"type": "string", "format": "string", "description": "The phase ID"}, "body": {"$ref": "#/components/schemas/UpdatePhaseStatusInput"}}, "required": ["projectKey", "flagKey", "phaseId"]},
            "output_schema": {"$ref": "#/components/schemas/Release"}
        }
    )
)
# Capability for getLayers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getLayers",
            "description": """Get layers""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. This endpoint only accepts filtering by `experimentKey`. The filter returns layers which include that experiment for the selected environment(s). For example: `filter=reservations.experimentKey contains expKey`."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/LayerCollectionRep"}
        }
    )
)
# Capability for createLayer
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createLayer",
            "description": """Create layer""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/LayerPost"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/LayerRep"}
        }
    )
)
# Capability for updateLayer
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateLayer",
            "description": """Update layer""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "layerKey": {"type": "string", "format": "string", "description": "The layer key"}, "body": {"$ref": "#/components/schemas/LayerPatchInput"}}, "required": ["projectKey", "layerKey"]},
            "output_schema": {"$ref": "#/components/schemas/LayerRep"}
        }
    )
)
# Capability for getMetricGroups
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMetricGroups",
            "description": """List metric groups""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "filter": {"type": "string", "format": "string", "description": "Accepts filter by `experimentStatus`, `query`, `kind`, `hasConnections`, `maintainerIds`, and `maintainerTeamKey`. Example: `filter=experimentStatus equals 'running' and query equals 'test'`."}, "sort": {"type": "string", "format": "string", "description": "A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order. Read the endpoint description for a full list of available sort fields."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}, "limit": {"type": "integer", "format": "int64", "description": "The number of metric groups to return in the response. Defaults to 20. Maximum limit is 50."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricGroupCollectionRep"}
        }
    )
)
# Capability for createMetricGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createMetricGroup",
            "description": """Create metric group""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/MetricGroupPost"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricGroupRep"}
        }
    )
)
# Capability for getMetricGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMetricGroup",
            "description": """Get metric group""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricGroupKey": {"type": "string", "format": "string", "description": "The metric group key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}, "required": ["projectKey", "metricGroupKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricGroupRep"}
        }
    )
)
# Capability for patchMetricGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchMetricGroup",
            "description": """Patch metric group""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricGroupKey": {"type": "string", "format": "string", "description": "The metric group key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["projectKey", "metricGroupKey"]},
            "output_schema": {"$ref": "#/components/schemas/MetricGroupRep"}
        }
    )
)
# Capability for deleteMetricGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteMetricGroup",
            "description": """Delete metric group""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "metricGroupKey": {"type": "string", "format": "string", "description": "The metric group key"}}, "required": ["projectKey", "metricGroupKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getAllReleasePipelines
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAllReleasePipelines",
            "description": """Get all release pipelines""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is of the form field:value. Read the endpoint description for a full list of available filter fields."}, "limit": {"type": "integer", "format": "int64", "description": "The maximum number of items to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Defaults to 0. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/ReleasePipelineCollection"}
        }
    )
)
# Capability for postReleasePipeline
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postReleasePipeline",
            "description": """Create a release pipeline""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "body": {"$ref": "#/components/schemas/CreateReleasePipelineInput"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/ReleasePipeline"}
        }
    )
)
# Capability for getReleasePipelineByKey
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getReleasePipelineByKey",
            "description": """Get release pipeline by key""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "pipelineKey": {"type": "string", "format": "string", "description": "The release pipeline key"}}, "required": ["projectKey", "pipelineKey"]},
            "output_schema": {"$ref": "#/components/schemas/ReleasePipeline"}
        }
    )
)
# Capability for putReleasePipeline
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putReleasePipeline",
            "description": """Update a release pipeline""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "pipelineKey": {"type": "string", "format": "string", "description": "The release pipeline key"}, "body": {"$ref": "#/components/schemas/UpdateReleasePipelineInput"}}, "required": ["projectKey", "pipelineKey"]},
            "output_schema": {"$ref": "#/components/schemas/ReleasePipeline"}
        }
    )
)
# Capability for deleteReleasePipeline
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteReleasePipeline",
            "description": """Delete release pipeline""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "pipelineKey": {"type": "string", "format": "string", "description": "The release pipeline key"}}, "required": ["projectKey", "pipelineKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getAllReleaseProgressionsForReleasePipeline
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAllReleaseProgressionsForReleasePipeline",
            "description": """Get release progressions for release pipeline""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "pipelineKey": {"type": "string", "format": "string", "description": "The pipeline key"}, "filter": {"type": "string", "format": "string", "description": "Accepts filter by `status` and `activePhaseId`. `status` can take a value of `completed` or `active`. `activePhaseId` takes a UUID and will filter results down to releases active on the specified phase. Providing `status equals completed` along with an `activePhaseId` filter will return an error as they are disjoint sets of data. The combination of `status equals active` and `activePhaseId` will return the same results as `activePhaseId` alone."}, "limit": {"type": "integer", "format": "int64", "description": "The maximum number of items to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Defaults to 0. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["projectKey", "pipelineKey"]},
            "output_schema": {"$ref": "#/components/schemas/ReleaseProgressionCollection"}
        }
    )
)
# Capability for getIps
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getIps",
            "description": """Gets the public IP list""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/ipList"}
        }
    )
)
# Capability for getCustomRoles
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getCustomRoles",
            "description": """List custom roles""",
            "input_schema": {"type": "object", "properties": {"limit": {"type": "integer", "format": "int64", "description": "The maximum number of custom roles to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Defaults to 0. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}},
            "output_schema": {"$ref": "#/components/schemas/CustomRoles"}
        }
    )
)
# Capability for postCustomRole
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postCustomRole",
            "description": """Create custom role""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/CustomRolePost"}}},
            "output_schema": {"$ref": "#/components/schemas/CustomRole"}
        }
    )
)
# Capability for getCustomRole
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getCustomRole",
            "description": """Get custom role""",
            "input_schema": {"type": "object", "properties": {"customRoleKey": {"type": "string", "format": "string", "description": "The custom role key or ID"}}, "required": ["customRoleKey"]},
            "output_schema": {"$ref": "#/components/schemas/CustomRole"}
        }
    )
)
# Capability for patchCustomRole
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchCustomRole",
            "description": """Update custom role""",
            "input_schema": {"type": "object", "properties": {"customRoleKey": {"type": "string", "format": "string", "description": "The custom role key"}, "body": {"$ref": "#/components/schemas/PatchWithComment"}}, "required": ["customRoleKey"]},
            "output_schema": {"$ref": "#/components/schemas/CustomRole"}
        }
    )
)
# Capability for deleteCustomRole
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteCustomRole",
            "description": """Delete custom role""",
            "input_schema": {"type": "object", "properties": {"customRoleKey": {"type": "string", "format": "string", "description": "The custom role key"}}, "required": ["customRoleKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getSegments
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSegments",
            "description": """List segments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of segments to return. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "sort": {"type": "string", "format": "string", "description": "Accepts sorting order and fields. Fields can be comma separated. Possible fields are 'creationDate', 'name', 'lastModified'. Example: `sort=name` sort by names ascending or `sort=-name,creationDate` sort by names descending and creationDate ascending."}, "filter": {"type": "string", "format": "string", "description": "Accepts filter by `excludedKeys`, `external`, `includedKeys`, `query`, `tags`, `unbounded`. To learn more about the filter syntax, read the  'Filtering segments' section above."}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserSegments"}
        }
    )
)
# Capability for postSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postSegment",
            "description": """Create segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/SegmentBody"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserSegment"}
        }
    )
)
# Capability for getSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSegment",
            "description": """Get segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserSegment"}
        }
    )
)
# Capability for patchSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchSegment",
            "description": """Patch segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"$ref": "#/components/schemas/PatchWithComment"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserSegment"}
        }
    )
)
# Capability for deleteSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteSegment",
            "description": """Delete segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for updateBigSegmentContextTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateBigSegmentContextTargets",
            "description": """Update context targets on a big segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"$ref": "#/components/schemas/SegmentUserState"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getSegmentMembershipForContext
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSegmentMembershipForContext",
            "description": """Get big segment membership for context""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "contextKey": {"type": "string", "format": "string", "description": "The context key"}}, "required": ["projectKey", "environmentKey", "segmentKey", "contextKey"]},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentTarget"}
        }
    )
)
# Capability for createBigSegmentExport
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createBigSegmentExport",
            "description": """Create big segment export""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getBigSegmentExport
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBigSegmentExport",
            "description": """Get big segment export""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "exportID": {"type": "string", "format": "string", "description": "The export ID"}}, "required": ["projectKey", "environmentKey", "segmentKey", "exportID"]},
            "output_schema": {"$ref": "#/components/schemas/Export"}
        }
    )
)
# Capability for createBigSegmentImport
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createBigSegmentImport",
            "description": """Create big segment import""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"type": "object", "properties": {"file": {"type": "string", "format": "binary", "description": "CSV file containing keys"}, "mode": {"type": "string", "format": "string", "description": "Import mode. Use either `merge` or `replace`"}, "waitOnApprovals": {"type": "boolean", "description": "Whether to wait for approvals before processing the import"}}}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getBigSegmentImport
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getBigSegmentImport",
            "description": """Get big segment import""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "importID": {"type": "string", "format": "string", "description": "The import ID"}}, "required": ["projectKey", "environmentKey", "segmentKey", "importID"]},
            "output_schema": {"$ref": "#/components/schemas/Import"}
        }
    )
)
# Capability for updateBigSegmentTargets
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateBigSegmentTargets",
            "description": """Update user context targets on a big segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"$ref": "#/components/schemas/SegmentUserState"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getSegmentMembershipForUser
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSegmentMembershipForUser",
            "description": """Get big segment membership for user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}}, "required": ["projectKey", "environmentKey", "segmentKey", "userKey"]},
            "output_schema": {"$ref": "#/components/schemas/BigSegmentTarget"}
        }
    )
)
# Capability for getExpiringTargetsForSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExpiringTargetsForSegment",
            "description": """Get expiring targets for segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringTargetGetResponse"}
        }
    )
)
# Capability for patchExpiringTargetsForSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExpiringTargetsForSegment",
            "description": """Update expiring targets for segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"$ref": "#/components/schemas/patchSegmentExpiringTargetInputRep"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringTargetPatchResponse"}
        }
    )
)
# Capability for getExpiringUserTargetsForSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExpiringUserTargetsForSegment",
            "description": """Get expiring user targets for segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetGetResponse"}
        }
    )
)
# Capability for patchExpiringUserTargetsForSegment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExpiringUserTargetsForSegment",
            "description": """Update expiring user targets for segment""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "segmentKey": {"type": "string", "format": "string", "description": "The segment key"}, "body": {"$ref": "#/components/schemas/patchSegmentRequest"}}, "required": ["projectKey", "environmentKey", "segmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetPatchResponse"}
        }
    )
)
# Capability for getTeams
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTeams",
            "description": """List teams""",
            "input_schema": {"type": "object", "properties": {"limit": {"type": "integer", "format": "int64", "description": "The number of teams to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of filters. Each filter is constructed as `field:value`."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}},
            "output_schema": {"$ref": "#/components/schemas/Teams"}
        }
    )
)
# Capability for postTeam
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postTeam",
            "description": """Create team""",
            "input_schema": {"type": "object", "properties": {"expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above."}, "body": {"$ref": "#/components/schemas/teamPostInput"}}},
            "output_schema": {"$ref": "#/components/schemas/Team"}
        }
    )
)
# Capability for patchTeams
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchTeams",
            "description": """Update teams""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/teamsPatchInput"}}},
            "output_schema": {"$ref": "#/components/schemas/BulkEditTeamsRep"}
        }
    )
)
# Capability for getTeam
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTeam",
            "description": """Get team""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key."}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response."}}, "required": ["teamKey"]},
            "output_schema": {"$ref": "#/components/schemas/Team"}
        }
    )
)
# Capability for patchTeam
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchTeam",
            "description": """Update team""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key"}, "expand": {"type": "string", "format": "string", "description": "A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above."}, "body": {"$ref": "#/components/schemas/teamPatchInput"}}, "required": ["teamKey"]},
            "output_schema": {"$ref": "#/components/schemas/Team"}
        }
    )
)
# Capability for deleteTeam
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteTeam",
            "description": """Delete team""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key"}}, "required": ["teamKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getTeamMaintainers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTeamMaintainers",
            "description": """Get team maintainers""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of maintainers to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["teamKey"]},
            "output_schema": {"$ref": "#/components/schemas/TeamMaintainers"}
        }
    )
)
# Capability for postTeamMembers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postTeamMembers",
            "description": """Add multiple members to team""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key"}, "body": {"type": "object", "properties": {"file": {"type": "string", "format": "binary", "description": "CSV file containing email addresses"}}}}, "required": ["teamKey"]},
            "output_schema": {"$ref": "#/components/schemas/TeamImportsRep"}
        }
    )
)
# Capability for getTeamRoles
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTeamRoles",
            "description": """Get team custom roles""",
            "input_schema": {"type": "object", "properties": {"teamKey": {"type": "string", "format": "string", "description": "The team key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of roles to return in the response. Defaults to 20."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}, "required": ["teamKey"]},
            "output_schema": {"$ref": "#/components/schemas/TeamCustomRoles"}
        }
    )
)
# Capability for getWorkflowTemplates
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getWorkflowTemplates",
            "description": """Get workflow templates""",
            "input_schema": {"type": "object", "properties": {"summary": {"type": "boolean", "description": "Whether the entire template object or just a summary should be returned"}, "search": {"type": "string", "format": "string", "description": "The substring in either the name or description of a template"}}},
            "output_schema": {"$ref": "#/components/schemas/WorkflowTemplatesListingOutputRep"}
        }
    )
)
# Capability for createWorkflowTemplate
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createWorkflowTemplate",
            "description": """Create workflow template""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/CreateWorkflowTemplateInput"}}},
            "output_schema": {"$ref": "#/components/schemas/WorkflowTemplateOutput"}
        }
    )
)
# Capability for deleteWorkflowTemplate
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteWorkflowTemplate",
            "description": """Delete workflow template""",
            "input_schema": {"type": "object", "properties": {"templateKey": {"type": "string", "format": "string", "description": "The template key"}}, "required": ["templateKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getTokens
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTokens",
            "description": """List access tokens""",
            "input_schema": {"type": "object", "properties": {"showAll": {"type": "boolean", "description": "If set to true, and the authentication access token has the 'Admin' role, personal access tokens for all members will be retrieved."}, "limit": {"type": "integer", "format": "int64", "description": "The number of access tokens to return in the response. Defaults to 25."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}}},
            "output_schema": {"$ref": "#/components/schemas/Tokens"}
        }
    )
)
# Capability for postToken
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postToken",
            "description": """Create access token""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/AccessTokenPost"}}},
            "output_schema": {"$ref": "#/components/schemas/Token"}
        }
    )
)
# Capability for getToken
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getToken",
            "description": """Get access token""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the access token"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Token"}
        }
    )
)
# Capability for patchToken
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchToken",
            "description": """Patch access token""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the access token to update"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Token"}
        }
    )
)
# Capability for deleteToken
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteToken",
            "description": """Delete access token""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the access token to update"}}, "required": ["id"]},
            "output_schema": {}
        }
    )
)
# Capability for resetToken
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "resetToken",
            "description": """Reset access token""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the access token to update"}, "expiry": {"type": "integer", "format": "int64", "description": "An expiration time for the old token key, expressed as a Unix epoch time in milliseconds. By default, the token will expire immediately."}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Token"}
        }
    )
)
# Capability for getDataExportEventsUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDataExportEventsUsage",
            "description": """Get data export events usage""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time."}, "projectKey": {"type": "string", "format": "string", "description": "A project key. If specified, `environmentKey` is required and results apply to the corresponding environment in this project."}, "environmentKey": {"type": "string", "format": "string", "description": "An environment key. If specified, `projectKey` is required and results apply to the corresponding environment in this project."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesIntervalsRep"}
        }
    )
)
# Capability for getEvaluationsUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getEvaluationsUsage",
            "description": """Get evaluations usage""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 30 days ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}, "tz": {"type": "string", "format": "string", "description": "The timezone to use for breaks between days when returning daily data."}}, "required": ["projectKey", "environmentKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getEventsUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getEventsUsage",
            "description": """Get events usage""",
            "input_schema": {"type": "object", "properties": {"type": {"type": "string", "format": "string", "description": "The type of event to retrieve. Must be either `received` or `published`."}, "from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 24 hours ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}}, "required": ["type"]},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getExperimentationKeysUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperimentationKeysUsage",
            "description": """Get experimentation keys usage""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time."}, "projectKey": {"type": "string", "format": "string", "description": "A project key. If specified, `environmentKey` is required and results apply to the corresponding environment in this project."}, "environmentKey": {"type": "string", "format": "string", "description": "An environment key. If specified, `projectKey` is required and results apply to the corresponding environment in this project."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesIntervalsRep"}
        }
    )
)
# Capability for getExperimentationUnitsUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExperimentationUnitsUsage",
            "description": """Get experimentation units usage""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time."}, "projectKey": {"type": "string", "format": "string", "description": "A project key. If specified, `environmentKey` is required and results apply to the corresponding environment in this project."}, "environmentKey": {"type": "string", "format": "string", "description": "An environment key. If specified, `projectKey` is required and results apply to the corresponding environment in this project."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesIntervalsRep"}
        }
    )
)
# Capability for getMauUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMauUsage",
            "description": """Get MAU usage""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 30 days ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}, "project": {"type": "string", "format": "string", "description": "A project key to filter results to. Can be specified multiple times, one query parameter per project key, to view data for multiple projects."}, "environment": {"type": "string", "format": "string", "description": "An environment key to filter results to. When using this parameter, exactly one project key must also be set. Can be specified multiple times as separate query parameters to view data for multiple environments within a single project."}, "sdktype": {"type": "string", "format": "string", "description": "An SDK type to filter results to. Can be specified multiple times, one query parameter per SDK type. Valid values: client, server"}, "sdk": {"type": "string", "format": "string", "description": "An SDK name to filter results to. Can be specified multiple times, one query parameter per SDK."}, "anonymous": {"type": "string", "format": "string", "description": "If specified, filters results to either anonymous or nonanonymous users."}, "groupby": {"type": "string", "format": "string", "description": "If specified, returns data for each distinct value of the given field. Can be specified multiple times to group data by multiple dimensions (for example, to group by both project and SDK). Valid values: project, environment, sdktype, sdk, anonymous, contextKind, sdkAppId"}, "aggregationType": {"type": "string", "format": "string", "description": "If specified, queries for rolling 30-day, month-to-date, or daily incremental counts. Default is rolling 30-day. Valid values: rolling_30d, month_to_date, daily_incremental"}, "contextKind": {"type": "string", "format": "string", "description": "Filters results to the specified context kinds. Can be specified multiple times, one query parameter per context kind. If not set, queries for the user context kind."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getMauUsageByCategory
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMauUsageByCategory",
            "description": """Get MAU usage by category""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 30 days ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getMauSdksByType
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getMauSdksByType",
            "description": """Get MAU SDKs by type""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The data returned starts from this timestamp. Defaults to seven days ago. The timestamp is in Unix milliseconds, for example, 1656694800000."}, "to": {"type": "string", "format": "string", "description": "The data returned ends at this timestamp. Defaults to the current time. The timestamp is in Unix milliseconds, for example, 1657904400000."}, "sdktype": {"type": "string", "format": "string", "description": "The type of SDK with monthly active users (MAU) to list. Must be either `client` or `server`."}}},
            "output_schema": {"$ref": "#/components/schemas/SdkListRep"}
        }
    )
)
# Capability for getServiceConnectionUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getServiceConnectionUsage",
            "description": """Get service connection usage""",
            "input_schema": {"type": "object", "properties": {"from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time."}, "projectKey": {"type": "string", "format": "string", "description": "A project key. If specified, `environmentKey` is required and results apply to the corresponding environment in this project."}, "environmentKey": {"type": "string", "format": "string", "description": "An environment key. If specified, `projectKey` is required and results apply to the corresponding environment in this project."}}},
            "output_schema": {"$ref": "#/components/schemas/SeriesIntervalsRep"}
        }
    )
)
# Capability for getStreamUsage
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getStreamUsage",
            "description": """Get stream usage""",
            "input_schema": {"type": "object", "properties": {"source": {"type": "string", "format": "string", "description": "The source of streaming connections to describe. Must be either `client` or `server`."}, "from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 30 days ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}, "tz": {"type": "string", "format": "string", "description": "The timezone to use for breaks between days when returning daily data."}}, "required": ["source"]},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getStreamUsageBySdkVersion
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getStreamUsageBySdkVersion",
            "description": """Get stream usage by SDK version""",
            "input_schema": {"type": "object", "properties": {"source": {"type": "string", "format": "string", "description": "The source of streaming connections to describe. Must be either `client` or `server`."}, "from": {"type": "string", "format": "string", "description": "The series of data returned starts from this timestamp. Defaults to 24 hours ago."}, "to": {"type": "string", "format": "string", "description": "The series of data returned ends at this timestamp. Defaults to the current time."}, "tz": {"type": "string", "format": "string", "description": "The timezone to use for breaks between days when returning daily data."}, "sdk": {"type": "string", "format": "string", "description": "If included, this filters the returned series to only those that match this SDK name."}, "version": {"type": "string", "format": "string", "description": "If included, this filters the returned series to only those that match this SDK version."}}, "required": ["source"]},
            "output_schema": {"$ref": "#/components/schemas/SeriesListRep"}
        }
    )
)
# Capability for getStreamUsageSdkversion
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getStreamUsageSdkversion",
            "description": """Get stream usage SDK versions""",
            "input_schema": {"type": "object", "properties": {"source": {"type": "string", "format": "string", "description": "The source of streaming connections to describe. Must be either `client` or `server`."}}, "required": ["source"]},
            "output_schema": {"$ref": "#/components/schemas/SdkVersionListRep"}
        }
    )
)
# Capability for getUserAttributeNames
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getUserAttributeNames",
            "description": """Get user attribute names""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserAttributeNamesRep"}
        }
    )
)
# Capability for getSearchUsers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getSearchUsers",
            "description": """Find users""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "q": {"type": "string", "format": "string", "description": "Full-text search for users based on name, first name, last name, e-mail address, or key"}, "limit": {"type": "integer", "format": "int64", "description": "Specifies the maximum number of items in the collection to return (max: 50, default: 20)"}, "offset": {"type": "integer", "format": "int64", "description": "Deprecated, use `searchAfter` instead. Specifies the first item to return in the collection."}, "after": {"type": "integer", "format": "int64", "description": "A Unix epoch time in milliseconds specifying the maximum last time a user requested a feature flag from LaunchDarkly"}, "sort": {"type": "string", "format": "string", "description": "Specifies a field by which to sort. LaunchDarkly supports the `userKey` and `lastSeen` fields. Fields prefixed by a dash ( - ) sort in descending order."}, "searchAfter": {"type": "string", "format": "string", "description": "Limits results to users with sort values after the value you specify. You can use this for pagination, but we recommend using the `next` link we provide instead."}, "filter": {"type": "string", "format": "string", "description": "A comma-separated list of user attribute filters. Each filter is in the form of attributeKey:attributeValue"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/Users"}
        }
    )
)
# Capability for getUsers
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getUsers",
            "description": """List users""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "limit": {"type": "integer", "format": "int64", "description": "The number of elements to return per page"}, "searchAfter": {"type": "string", "format": "string", "description": "Limits results to users with sort values after the value you specify. You can use this for pagination, but we recommend using the `next` link we provide instead."}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/UsersRep"}
        }
    )
)
# Capability for getUser
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getUser",
            "description": """Get user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}}, "required": ["projectKey", "environmentKey", "userKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserRecord"}
        }
    )
)
# Capability for deleteUser
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteUser",
            "description": """Delete user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}}, "required": ["projectKey", "environmentKey", "userKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getUserFlagSettings
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getUserFlagSettings",
            "description": """List flag settings for user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}}, "required": ["projectKey", "environmentKey", "userKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserFlagSettings"}
        }
    )
)
# Capability for getUserFlagSetting
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getUserFlagSetting",
            "description": """Get flag setting for user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}}, "required": ["projectKey", "environmentKey", "userKey", "featureFlagKey"]},
            "output_schema": {"$ref": "#/components/schemas/UserFlagSetting"}
        }
    )
)
# Capability for putFlagSetting
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "putFlagSetting",
            "description": """Update flag settings for user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}, "featureFlagKey": {"type": "string", "format": "string", "description": "The feature flag key"}, "body": {"$ref": "#/components/schemas/ValuePut"}}, "required": ["projectKey", "environmentKey", "userKey", "featureFlagKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getExpiringFlagsForUser
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getExpiringFlagsForUser",
            "description": """Get expiring dates on flags for user""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}}, "required": ["projectKey", "userKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetGetResponse"}
        }
    )
)
# Capability for patchExpiringFlagsForUser
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchExpiringFlagsForUser",
            "description": """Update expiring user target for flags""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "userKey": {"type": "string", "format": "string", "description": "The user key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "body": {"$ref": "#/components/schemas/patchUsersRequest"}}, "required": ["projectKey", "userKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/ExpiringUserTargetPatchResponse"}
        }
    )
)
# Capability for getVersions
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getVersions",
            "description": """Get version information""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/VersionsRep"}
        }
    )
)
# Capability for getAllWebhooks
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAllWebhooks",
            "description": """List webhooks""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/Webhooks"}
        }
    )
)
# Capability for postWebhook
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postWebhook",
            "description": """Creates a webhook""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/webhookPost"}}},
            "output_schema": {"$ref": "#/components/schemas/Webhook"}
        }
    )
)
# Capability for getWebhook
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getWebhook",
            "description": """Get webhook""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the webhook"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Webhook"}
        }
    )
)
# Capability for patchWebhook
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchWebhook",
            "description": """Update webhook""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the webhook to update"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["id"]},
            "output_schema": {"$ref": "#/components/schemas/Webhook"}
        }
    )
)
# Capability for deleteWebhook
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteWebhook",
            "description": """Delete webhook""",
            "input_schema": {"type": "object", "properties": {"id": {"type": "string", "format": "string", "description": "The ID of the webhook to delete"}}, "required": ["id"]},
            "output_schema": {}
        }
    )
)
# Capability for getTags
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getTags",
            "description": """List tags""",
            "input_schema": {"type": "object", "properties": {"kind": {"items": {"type": "string"}, "type": "array"}, "pre": {"type": "string"}, "archived": {"type": "boolean"}, "limit": {"type": "integer"}, "offset": {"type": "integer"}, "asOf": {"type": "string"}}},
            "output_schema": {"$ref": "#/components/schemas/TagsCollection"}
        }
    )
)
# Capability for getAIConfigs
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAIConfigs",
            "description": """List AI Configs""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "sort": {"type": "string"}, "limit": {"type": "integer"}, "offset": {"type": "integer"}, "filter": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfigs"}
        }
    )
)
# Capability for postAIConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postAIConfig",
            "description": """Create new AI Config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}, "body": {"$ref": "#/components/schemas/AIConfigPost"}}, "required": ["projectKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfig"}
        }
    )
)
# Capability for deleteAIConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteAIConfig",
            "description": """Delete AI Config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "LD-API-Version"]},
            "output_schema": {}
        }
    )
)
# Capability for getAIConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAIConfig",
            "description": """Get AI Config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfig"}
        }
    )
)
# Capability for patchAIConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchAIConfig",
            "description": """Update AI Config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}, "body": {"$ref": "#/components/schemas/AIConfigPatch"}}, "required": ["projectKey", "configKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfig"}
        }
    )
)
# Capability for postAIConfigVariation
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postAIConfigVariation",
            "description": """Create AI Config variation""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}, "body": {"$ref": "#/components/schemas/AIConfigVariationPost"}}, "required": ["projectKey", "configKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfigVariation"}
        }
    )
)
# Capability for deleteAIConfigVariation
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteAIConfigVariation",
            "description": """Delete AI Config variation""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "variationKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "variationKey", "LD-API-Version"]},
            "output_schema": {}
        }
    )
)
# Capability for getAIConfigVariation
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAIConfigVariation",
            "description": """Get AI Config variation""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "variationKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "variationKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfigVariationsResponse"}
        }
    )
)
# Capability for patchAIConfigVariation
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchAIConfigVariation",
            "description": """Update AI Config variation""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "variationKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}, "body": {"$ref": "#/components/schemas/AIConfigVariationPatch"}}, "required": ["projectKey", "configKey", "variationKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/AIConfigVariation"}
        }
    )
)
# Capability for getAIConfigMetrics
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAIConfigMetrics",
            "description": """Get AI Config metrics""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "from": {"type": "integer"}, "to": {"type": "integer"}, "env": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "from", "to", "env", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/Metrics"}
        }
    )
)
# Capability for getAIConfigMetricsByVariation
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAIConfigMetricsByVariation",
            "description": """Get AI Config metrics by variation""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "configKey": {"type": "string"}, "from": {"type": "integer"}, "to": {"type": "integer"}, "env": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "configKey", "from", "to", "env", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/MetricsByVariation"}
        }
    )
)
# Capability for listModelConfigs
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "listModelConfigs",
            "description": """List AI model configs""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "LD-API-Version"]},
            "output_schema": {"items": {"$ref": "#/components/schemas/ModelConfig"}, "type": "array"}
        }
    )
)
# Capability for postModelConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "postModelConfig",
            "description": """Create an AI model config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}, "body": {"$ref": "#/components/schemas/ModelConfigPost"}}, "required": ["projectKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/ModelConfig"}
        }
    )
)
# Capability for deleteModelConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteModelConfig",
            "description": """Delete an AI model config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "modelConfigKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "modelConfigKey", "LD-API-Version"]},
            "output_schema": {}
        }
    )
)
# Capability for getModelConfig
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getModelConfig",
            "description": """Get AI model config""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string"}, "modelConfigKey": {"type": "string"}, "LD-API-Version": {"enum": ["beta"], "type": "string"}}, "required": ["projectKey", "modelConfigKey", "LD-API-Version"]},
            "output_schema": {"$ref": "#/components/schemas/ModelConfig"}
        }
    )
)
# Capability for getAnnouncementsPublic
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getAnnouncementsPublic",
            "description": """Get announcements""",
            "input_schema": {"type": "object", "properties": {"status": {"enum": ["active", "inactive", "scheduled"], "type": "string", "x-enumNames": ["Active", "Inactive", "Scheduled"]}, "limit": {"type": "integer"}, "offset": {"type": "integer"}}},
            "output_schema": {"$ref": "#/components/schemas/getAnnouncementsPublic_200_response"}
        }
    )
)
# Capability for createAnnouncementPublic
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createAnnouncementPublic",
            "description": """Create an announcement""",
            "input_schema": {"type": "object", "properties": {}},
            "output_schema": {"$ref": "#/components/schemas/AnnouncementResponse"}
        }
    )
)
# Capability for deleteAnnouncementPublic
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteAnnouncementPublic",
            "description": """Delete an announcement""",
            "input_schema": {"type": "object", "properties": {"announcementId": {"type": "string"}}, "required": ["announcementId"]},
            "output_schema": {}
        }
    )
)
# Capability for updateAnnouncementPublic
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateAnnouncementPublic",
            "description": """Update an announcement""",
            "input_schema": {"type": "object", "properties": {"announcementId": {"type": "string"}}, "required": ["announcementId"]},
            "output_schema": {"$ref": "#/components/schemas/AnnouncementResponse"}
        }
    )
)
# Capability for getDeploymentFrequencyChart
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDeploymentFrequencyChart",
            "description": """Get deployment frequency chart data""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "from": {"type": "string", "format": "date-time"}, "to": {"type": "string", "format": "date-time"}, "bucketType": {"type": "string", "format": "string", "description": "Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`."}, "bucketMs": {"type": "integer", "format": "int64", "description": "Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds)."}, "groupBy": {"type": "string", "format": "string", "description": "Options: `application`, `kind`"}, "expand": {"type": "string", "format": "string", "description": "Options: `metrics`"}}},
            "output_schema": {"$ref": "#/components/schemas/InsightsChart"}
        }
    )
)
# Capability for getStaleFlagsChart
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getStaleFlagsChart",
            "description": """Get stale flags chart data""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "groupBy": {"type": "string", "format": "string", "description": "Property to group results by. Options: `maintainer`"}, "maintainerId": {"type": "string", "format": "string", "description": "Comma-separated list of individual maintainers to filter results."}, "maintainerTeamKey": {"type": "string", "format": "string", "description": "Comma-separated list of team maintainer keys to filter results."}, "expand": {"type": "string", "format": "string", "description": "Options: `metrics`"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightsChart"}
        }
    )
)
# Capability for getFlagStatusChart
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagStatusChart",
            "description": """Get flag status chart data""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightsChart"}
        }
    )
)
# Capability for getLeadTimeChart
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getLeadTimeChart",
            "description": """Get lead time chart data""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "from": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is 7 days ago."}, "to": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is now."}, "bucketType": {"type": "string", "format": "string", "description": "Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`."}, "bucketMs": {"type": "integer", "format": "int64", "description": "Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds)."}, "groupBy": {"type": "string", "format": "string", "description": "Options: `application`, `stage`. Default: `stage`."}, "expand": {"type": "string", "format": "string", "description": "Options: `metrics`, `percentiles`."}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightsChart"}
        }
    )
)
# Capability for getReleaseFrequencyChart
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getReleaseFrequencyChart",
            "description": """Get release frequency chart data""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "hasExperiments": {"type": "boolean", "format": "boolean", "description": "Filter events to those associated with an experiment (`true`) or without an experiment (`false`)"}, "global": {"type": "string", "format": "string", "description": "Filter to include or exclude global events. Default value is `include`. Options: `include`, `exclude`"}, "groupBy": {"type": "string", "format": "string", "description": "Property to group results by. Options: `impact`"}, "from": {"type": "string", "format": "date-time"}, "to": {"type": "string", "format": "date-time"}, "bucketType": {"type": "string", "format": "string", "description": "Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`."}, "bucketMs": {"type": "integer", "format": "int64", "description": "Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds)."}, "expand": {"type": "string", "format": "string", "description": "Options: `metrics`"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightsChart"}
        }
    )
)
# Capability for createDeploymentEvent
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createDeploymentEvent",
            "description": """Create deployment event""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/PostDeploymentEventInput"}}},
            "output_schema": {}
        }
    )
)
# Capability for getDeployments
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDeployments",
            "description": """List deployments""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "limit": {"type": "integer", "format": "int64", "description": "The number of deployments to return. Default is 20. Maximum allowed is 100."}, "expand": {"type": "string", "format": "string", "description": "Expand properties in response. Options: `pullRequests`, `flagReferences`"}, "from": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is 7 days ago."}, "to": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is now."}, "after": {"type": "string", "format": "string", "description": "Identifier used for pagination"}, "before": {"type": "string", "format": "string", "description": "Identifier used for pagination"}, "kind": {"type": "string", "format": "string", "description": "The deployment kind"}, "status": {"type": "string", "format": "string", "description": "The deployment status"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/DeploymentCollectionRep"}
        }
    )
)
# Capability for getDeployment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getDeployment",
            "description": """Get deployment""",
            "input_schema": {"type": "object", "properties": {"deploymentID": {"type": "string", "format": "string", "description": "The deployment ID"}, "expand": {"type": "string", "format": "string", "description": "Expand properties in response. Options: `pullRequests`, `flagReferences`"}}, "required": ["deploymentID"]},
            "output_schema": {"$ref": "#/components/schemas/DeploymentRep"}
        }
    )
)
# Capability for updateDeployment
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "updateDeployment",
            "description": """Update deployment""",
            "input_schema": {"type": "object", "properties": {"deploymentID": {"type": "string", "format": "string", "description": "The deployment ID"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["deploymentID"]},
            "output_schema": {"$ref": "#/components/schemas/DeploymentRep"}
        }
    )
)
# Capability for getFlagEvents
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getFlagEvents",
            "description": """List flag events""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}, "query": {"type": "string", "format": "string", "description": "Filter events by flag key"}, "impactSize": {"type": "string", "format": "string", "description": "Filter events by impact size. A small impact created a less than 20% change in the proportion of end users receiving one or more flag variations. A medium impact created between a 20%-80% change. A large impact created a more than 80% change. Options: `none`, `small`, `medium`, `large`"}, "hasExperiments": {"type": "boolean", "format": "boolean", "description": "Filter events to those associated with an experiment (`true`) or without an experiment (`false`)"}, "global": {"type": "string", "format": "string", "description": "Filter to include or exclude global events. Default value is `include`. Options: `include`, `exclude`"}, "expand": {"type": "string", "format": "string", "description": "Expand properties in response. Options: `experiments`"}, "limit": {"type": "integer", "format": "int64", "description": "The number of deployments to return. Default is 20. Maximum allowed is 100."}, "from": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is 7 days ago."}, "to": {"type": "integer", "format": "int64", "description": "Unix timestamp in milliseconds. Default value is now."}, "after": {"type": "string", "format": "string", "description": "Identifier used for pagination"}, "before": {"type": "string", "format": "string", "description": "Identifier used for pagination"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/FlagEventCollectionRep"}
        }
    )
)
# Capability for createInsightGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "createInsightGroup",
            "description": """Create insight group""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/PostInsightGroupParams"}}},
            "output_schema": {"$ref": "#/components/schemas/InsightGroup"}
        }
    )
)
# Capability for getInsightGroups
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getInsightGroups",
            "description": """List insight groups""",
            "input_schema": {"type": "object", "properties": {"limit": {"type": "integer", "format": "int64", "description": "The number of insight groups to return. Default is 20. Must be between 1 and 20 inclusive."}, "offset": {"type": "integer", "format": "int64", "description": "Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`."}, "sort": {"type": "string", "format": "string", "description": "Sort flag list by field. Prefix field with <code>-</code> to sort in descending order. Allowed fields: name"}, "query": {"type": "string", "format": "string", "description": "Filter list of insights groups by name."}, "expand": {"type": "string", "format": "string", "description": "Options: `scores`, `environment`, `metadata`"}}},
            "output_schema": {"$ref": "#/components/schemas/InsightGroupCollection"}
        }
    )
)
# Capability for getInsightGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getInsightGroup",
            "description": """Get insight group""",
            "input_schema": {"type": "object", "properties": {"insightGroupKey": {"type": "string", "format": "string", "description": "The insight group key"}, "expand": {"type": "string", "format": "string", "description": "Options: `scores`, `environment`"}}, "required": ["insightGroupKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightGroup"}
        }
    )
)
# Capability for patchInsightGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "patchInsightGroup",
            "description": """Patch insight group""",
            "input_schema": {"type": "object", "properties": {"insightGroupKey": {"type": "string", "format": "string", "description": "The insight group key"}, "body": {"$ref": "#/components/schemas/JSONPatch"}}, "required": ["insightGroupKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightGroup"}
        }
    )
)
# Capability for deleteInsightGroup
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteInsightGroup",
            "description": """Delete insight group""",
            "input_schema": {"type": "object", "properties": {"insightGroupKey": {"type": "string", "format": "string", "description": "The insight group key"}}, "required": ["insightGroupKey"]},
            "output_schema": {}
        }
    )
)
# Capability for getInsightsScores
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getInsightsScores",
            "description": """Get insight scores""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "The environment key"}, "applicationKey": {"type": "string", "format": "string", "description": "Comma separated list of application keys"}}, "required": ["projectKey", "environmentKey"]},
            "output_schema": {"$ref": "#/components/schemas/InsightScores"}
        }
    )
)
# Capability for getPullRequests
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getPullRequests",
            "description": """List pull requests""",
            "input_schema": {"type": "object", "properties": {"projectKey": {"type": "string", "format": "string", "description": "The project key"}, "environmentKey": {"type": "string", "format": "string", "description": "Required if you are using the <code>sort</code> parameter's <code>leadTime</code> option to sort pull requests."}, "applicationKey": {"type": "string", "format": "string", "description": "Filter the results to pull requests deployed to a comma separated list of applications"}, "status": {"type": "string", "format": "string", "description": "Filter results to pull requests with the given status. Options: `open`, `merged`, `closed`, `deployed`."}, "query": {"type": "string", "format": "string", "description": "Filter list of pull requests by title or author"}, "limit": {"type": "integer", "format": "int64", "description": "The number of pull requests to return. Default is 20. Maximum allowed is 100."}, "expand": {"type": "string", "format": "string", "description": "Expand properties in response. Options: `deployments`, `flagReferences`, `leadTime`."}, "sort": {"type": "string", "format": "string", "description": "Sort results. Requires the `environmentKey` to be set. Options: `leadTime` (asc) and `-leadTime` (desc). When query option is excluded, default sort is by created or merged date."}, "from": {"type": "string", "format": "date-time"}, "to": {"type": "string", "format": "date-time"}, "after": {"type": "string", "format": "string", "description": "Identifier used for pagination"}, "before": {"type": "string", "format": "string", "description": "Identifier used for pagination"}}, "required": ["projectKey"]},
            "output_schema": {"$ref": "#/components/schemas/PullRequestCollectionRep"}
        }
    )
)
# Capability for getInsightsRepositories
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "getInsightsRepositories",
            "description": """List repositories""",
            "input_schema": {"type": "object", "properties": {"expand": {"type": "string", "format": "string", "description": "Expand properties in response. Options: `projects`"}}},
            "output_schema": {"$ref": "#/components/schemas/InsightsRepositoryCollection"}
        }
    )
)
# Capability for associateRepositoriesAndProjects
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "associateRepositoriesAndProjects",
            "description": """Associate repositories with projects""",
            "input_schema": {"type": "object", "properties": {"body": {"$ref": "#/components/schemas/InsightsRepositoryProjectMappings"}}},
            "output_schema": {"$ref": "#/components/schemas/InsightsRepositoryProjectCollection"}
        }
    )
)
# Capability for deleteRepositoryProject
capabilities.append(
    Capability(
        name="mcp.function",
        options={
            "name": "deleteRepositoryProject",
            "description": """Remove repository project association""",
            "input_schema": {"type": "object", "properties": {"repositoryKey": {"type": "string", "format": "string", "description": "The repository key"}, "projectKey": {"type": "string", "format": "string", "description": "The project key"}}, "required": ["repositoryKey", "projectKey"]},
            "output_schema": {}
        }
    )
)

async def main():
    """Start the MCP server."""
    # Create function registry
    registry = FunctionRegistry()
    
    # Register all function handlers
    registry.register("getRoot")(function_handlers["getRoot"])
    registry.register("getRelayProxyConfigs")(function_handlers["getRelayProxyConfigs"])
    registry.register("postRelayAutoConfig")(function_handlers["postRelayAutoConfig"])
    registry.register("getRelayProxyConfig")(function_handlers["getRelayProxyConfig"])
    registry.register("patchRelayAutoConfig")(function_handlers["patchRelayAutoConfig"])
    registry.register("deleteRelayAutoConfig")(function_handlers["deleteRelayAutoConfig"])
    registry.register("resetRelayAutoConfig")(function_handlers["resetRelayAutoConfig"])
    registry.register("getApplications")(function_handlers["getApplications"])
    registry.register("getApplication")(function_handlers["getApplication"])
    registry.register("patchApplication")(function_handlers["patchApplication"])
    registry.register("deleteApplication")(function_handlers["deleteApplication"])
    registry.register("getApplicationVersions")(function_handlers["getApplicationVersions"])
    registry.register("patchApplicationVersion")(function_handlers["patchApplicationVersion"])
    registry.register("deleteApplicationVersion")(function_handlers["deleteApplicationVersion"])
    registry.register("getApprovalRequests")(function_handlers["getApprovalRequests"])
    registry.register("postApprovalRequest")(function_handlers["postApprovalRequest"])
    registry.register("getApprovalRequest")(function_handlers["getApprovalRequest"])
    registry.register("patchApprovalRequest")(function_handlers["patchApprovalRequest"])
    registry.register("deleteApprovalRequest")(function_handlers["deleteApprovalRequest"])
    registry.register("postApprovalRequestApply")(function_handlers["postApprovalRequestApply"])
    registry.register("postApprovalRequestReview")(function_handlers["postApprovalRequestReview"])
    registry.register("getAuditLogEntries")(function_handlers["getAuditLogEntries"])
    registry.register("postAuditLogEntries")(function_handlers["postAuditLogEntries"])
    registry.register("getAuditLogEntry")(function_handlers["getAuditLogEntry"])
    registry.register("getCallerIdentity")(function_handlers["getCallerIdentity"])
    registry.register("getExtinctions")(function_handlers["getExtinctions"])
    registry.register("getRepositories")(function_handlers["getRepositories"])
    registry.register("postRepository")(function_handlers["postRepository"])
    registry.register("getRepository")(function_handlers["getRepository"])
    registry.register("patchRepository")(function_handlers["patchRepository"])
    registry.register("deleteRepository")(function_handlers["deleteRepository"])
    registry.register("deleteBranches")(function_handlers["deleteBranches"])
    registry.register("getBranches")(function_handlers["getBranches"])
    registry.register("getBranch")(function_handlers["getBranch"])
    registry.register("putBranch")(function_handlers["putBranch"])
    registry.register("postExtinction")(function_handlers["postExtinction"])
    registry.register("getRootStatistic")(function_handlers["getRootStatistic"])
    registry.register("getStatistics")(function_handlers["getStatistics"])
    registry.register("getDestinations")(function_handlers["getDestinations"])
    registry.register("postGenerateWarehouseDestinationKeyPair")(function_handlers["postGenerateWarehouseDestinationKeyPair"])
    registry.register("postDestination")(function_handlers["postDestination"])
    registry.register("getDestination")(function_handlers["getDestination"])
    registry.register("patchDestination")(function_handlers["patchDestination"])
    registry.register("deleteDestination")(function_handlers["deleteDestination"])
    registry.register("getFlagLinks")(function_handlers["getFlagLinks"])
    registry.register("createFlagLink")(function_handlers["createFlagLink"])
    registry.register("updateFlagLink")(function_handlers["updateFlagLink"])
    registry.register("deleteFlagLink")(function_handlers["deleteFlagLink"])
    registry.register("getFeatureFlagStatusAcrossEnvironments")(function_handlers["getFeatureFlagStatusAcrossEnvironments"])
    registry.register("getFeatureFlagStatuses")(function_handlers["getFeatureFlagStatuses"])
    registry.register("getFeatureFlagStatus")(function_handlers["getFeatureFlagStatus"])
    registry.register("getFeatureFlags")(function_handlers["getFeatureFlags"])
    registry.register("postFeatureFlag")(function_handlers["postFeatureFlag"])
    registry.register("getDependentFlagsByEnv")(function_handlers["getDependentFlagsByEnv"])
    registry.register("getFeatureFlag")(function_handlers["getFeatureFlag"])
    registry.register("patchFeatureFlag")(function_handlers["patchFeatureFlag"])
    registry.register("deleteFeatureFlag")(function_handlers["deleteFeatureFlag"])
    registry.register("copyFeatureFlag")(function_handlers["copyFeatureFlag"])
    registry.register("getDependentFlags")(function_handlers["getDependentFlags"])
    registry.register("getExpiringContextTargets")(function_handlers["getExpiringContextTargets"])
    registry.register("patchExpiringTargets")(function_handlers["patchExpiringTargets"])
    registry.register("getExpiringUserTargets")(function_handlers["getExpiringUserTargets"])
    registry.register("patchExpiringUserTargets")(function_handlers["patchExpiringUserTargets"])
    registry.register("getTriggerWorkflows")(function_handlers["getTriggerWorkflows"])
    registry.register("createTriggerWorkflow")(function_handlers["createTriggerWorkflow"])
    registry.register("getTriggerWorkflowById")(function_handlers["getTriggerWorkflowById"])
    registry.register("patchTriggerWorkflow")(function_handlers["patchTriggerWorkflow"])
    registry.register("deleteTriggerWorkflow")(function_handlers["deleteTriggerWorkflow"])
    registry.register("getReleaseByFlagKey")(function_handlers["getReleaseByFlagKey"])
    registry.register("patchReleaseByFlagKey")(function_handlers["patchReleaseByFlagKey"])
    registry.register("deleteReleaseByFlagKey")(function_handlers["deleteReleaseByFlagKey"])
    registry.register("getBigSegmentStoreIntegrations")(function_handlers["getBigSegmentStoreIntegrations"])
    registry.register("createBigSegmentStoreIntegration")(function_handlers["createBigSegmentStoreIntegration"])
    registry.register("getBigSegmentStoreIntegration")(function_handlers["getBigSegmentStoreIntegration"])
    registry.register("patchBigSegmentStoreIntegration")(function_handlers["patchBigSegmentStoreIntegration"])
    registry.register("deleteBigSegmentStoreIntegration")(function_handlers["deleteBigSegmentStoreIntegration"])
    registry.register("getIntegrationDeliveryConfigurations")(function_handlers["getIntegrationDeliveryConfigurations"])
    registry.register("getIntegrationDeliveryConfigurationByEnvironment")(function_handlers["getIntegrationDeliveryConfigurationByEnvironment"])
    registry.register("createIntegrationDeliveryConfiguration")(function_handlers["createIntegrationDeliveryConfiguration"])
    registry.register("getIntegrationDeliveryConfigurationById")(function_handlers["getIntegrationDeliveryConfigurationById"])
    registry.register("patchIntegrationDeliveryConfiguration")(function_handlers["patchIntegrationDeliveryConfiguration"])
    registry.register("deleteIntegrationDeliveryConfiguration")(function_handlers["deleteIntegrationDeliveryConfiguration"])
    registry.register("validateIntegrationDeliveryConfiguration")(function_handlers["validateIntegrationDeliveryConfiguration"])
    registry.register("getFlagImportConfigurations")(function_handlers["getFlagImportConfigurations"])
    registry.register("createFlagImportConfiguration")(function_handlers["createFlagImportConfiguration"])
    registry.register("getFlagImportConfiguration")(function_handlers["getFlagImportConfiguration"])
    registry.register("patchFlagImportConfiguration")(function_handlers["patchFlagImportConfiguration"])
    registry.register("deleteFlagImportConfiguration")(function_handlers["deleteFlagImportConfiguration"])
    registry.register("triggerFlagImportJob")(function_handlers["triggerFlagImportJob"])
    registry.register("getAllIntegrationConfigurations")(function_handlers["getAllIntegrationConfigurations"])
    registry.register("createIntegrationConfiguration")(function_handlers["createIntegrationConfiguration"])
    registry.register("getIntegrationConfiguration")(function_handlers["getIntegrationConfiguration"])
    registry.register("updateIntegrationConfiguration")(function_handlers["updateIntegrationConfiguration"])
    registry.register("deleteIntegrationConfiguration")(function_handlers["deleteIntegrationConfiguration"])
    registry.register("getSubscriptions")(function_handlers["getSubscriptions"])
    registry.register("createSubscription")(function_handlers["createSubscription"])
    registry.register("getSubscriptionByID")(function_handlers["getSubscriptionByID"])
    registry.register("updateSubscription")(function_handlers["updateSubscription"])
    registry.register("deleteSubscription")(function_handlers["deleteSubscription"])
    registry.register("getMembers")(function_handlers["getMembers"])
    registry.register("postMembers")(function_handlers["postMembers"])
    registry.register("patchMembers")(function_handlers["patchMembers"])
    registry.register("getMember")(function_handlers["getMember"])
    registry.register("patchMember")(function_handlers["patchMember"])
    registry.register("deleteMember")(function_handlers["deleteMember"])
    registry.register("postMemberTeams")(function_handlers["postMemberTeams"])
    registry.register("getMetrics")(function_handlers["getMetrics"])
    registry.register("postMetric")(function_handlers["postMetric"])
    registry.register("getMetric")(function_handlers["getMetric"])
    registry.register("patchMetric")(function_handlers["patchMetric"])
    registry.register("deleteMetric")(function_handlers["deleteMetric"])
    registry.register("getOAuthClients")(function_handlers["getOAuthClients"])
    registry.register("createOAuth2Client")(function_handlers["createOAuth2Client"])
    registry.register("getOAuthClientById")(function_handlers["getOAuthClientById"])
    registry.register("patchOAuthClient")(function_handlers["patchOAuthClient"])
    registry.register("deleteOAuthClient")(function_handlers["deleteOAuthClient"])
    registry.register("getOpenapiSpec")(function_handlers["getOpenapiSpec"])
    registry.register("getProjects")(function_handlers["getProjects"])
    registry.register("postProject")(function_handlers["postProject"])
    registry.register("getProject")(function_handlers["getProject"])
    registry.register("patchProject")(function_handlers["patchProject"])
    registry.register("deleteProject")(function_handlers["deleteProject"])
    registry.register("getContextKindsByProjectKey")(function_handlers["getContextKindsByProjectKey"])
    registry.register("putContextKind")(function_handlers["putContextKind"])
    registry.register("getEnvironmentsByProject")(function_handlers["getEnvironmentsByProject"])
    registry.register("postEnvironment")(function_handlers["postEnvironment"])
    registry.register("getEnvironment")(function_handlers["getEnvironment"])
    registry.register("patchEnvironment")(function_handlers["patchEnvironment"])
    registry.register("deleteEnvironment")(function_handlers["deleteEnvironment"])
    registry.register("resetEnvironmentSDKKey")(function_handlers["resetEnvironmentSDKKey"])
    registry.register("getContextAttributeNames")(function_handlers["getContextAttributeNames"])
    registry.register("getContextAttributeValues")(function_handlers["getContextAttributeValues"])
    registry.register("searchContextInstances")(function_handlers["searchContextInstances"])
    registry.register("getContextInstances")(function_handlers["getContextInstances"])
    registry.register("deleteContextInstances")(function_handlers["deleteContextInstances"])
    registry.register("searchContexts")(function_handlers["searchContexts"])
    registry.register("putContextFlagSetting")(function_handlers["putContextFlagSetting"])
    registry.register("getContexts")(function_handlers["getContexts"])
    registry.register("getExperiments")(function_handlers["getExperiments"])
    registry.register("createExperiment")(function_handlers["createExperiment"])
    registry.register("getExperiment")(function_handlers["getExperiment"])
    registry.register("patchExperiment")(function_handlers["patchExperiment"])
    registry.register("createIteration")(function_handlers["createIteration"])
    registry.register("getExperimentResultsForMetricGroup")(function_handlers["getExperimentResultsForMetricGroup"])
    registry.register("getExperimentResults")(function_handlers["getExperimentResults"])
    registry.register("evaluateContextInstance")(function_handlers["evaluateContextInstance"])
    registry.register("getFollowersByProjEnv")(function_handlers["getFollowersByProjEnv"])
    registry.register("getAllHoldouts")(function_handlers["getAllHoldouts"])
    registry.register("postHoldout")(function_handlers["postHoldout"])
    registry.register("getHoldoutById")(function_handlers["getHoldoutById"])
    registry.register("getHoldout")(function_handlers["getHoldout"])
    registry.register("patchHoldout")(function_handlers["patchHoldout"])
    registry.register("resetEnvironmentMobileKey")(function_handlers["resetEnvironmentMobileKey"])
    registry.register("getContextInstanceSegmentsMembershipByEnv")(function_handlers["getContextInstanceSegmentsMembershipByEnv"])
    registry.register("getExperimentationSettings")(function_handlers["getExperimentationSettings"])
    registry.register("putExperimentationSettings")(function_handlers["putExperimentationSettings"])
    registry.register("getFlagDefaultsByProject")(function_handlers["getFlagDefaultsByProject"])
    registry.register("patchFlagDefaultsByProject")(function_handlers["patchFlagDefaultsByProject"])
    registry.register("putFlagDefaultsByProject")(function_handlers["putFlagDefaultsByProject"])
    registry.register("getApprovalsForFlag")(function_handlers["getApprovalsForFlag"])
    registry.register("postApprovalRequestForFlag")(function_handlers["postApprovalRequestForFlag"])
    registry.register("postFlagCopyConfigApprovalRequest")(function_handlers["postFlagCopyConfigApprovalRequest"])
    registry.register("getApprovalForFlag")(function_handlers["getApprovalForFlag"])
    registry.register("patchFlagConfigApprovalRequest")(function_handlers["patchFlagConfigApprovalRequest"])
    registry.register("deleteApprovalRequestForFlag")(function_handlers["deleteApprovalRequestForFlag"])
    registry.register("postApprovalRequestApplyForFlag")(function_handlers["postApprovalRequestApplyForFlag"])
    registry.register("postApprovalRequestReviewForFlag")(function_handlers["postApprovalRequestReviewForFlag"])
    registry.register("getFlagFollowers")(function_handlers["getFlagFollowers"])
    registry.register("putFlagFollower")(function_handlers["putFlagFollower"])
    registry.register("deleteFlagFollower")(function_handlers["deleteFlagFollower"])
    registry.register("getFlagConfigScheduledChanges")(function_handlers["getFlagConfigScheduledChanges"])
    registry.register("postFlagConfigScheduledChanges")(function_handlers["postFlagConfigScheduledChanges"])
    registry.register("getFeatureFlagScheduledChange")(function_handlers["getFeatureFlagScheduledChange"])
    registry.register("patchFlagConfigScheduledChange")(function_handlers["patchFlagConfigScheduledChange"])
    registry.register("deleteFlagConfigScheduledChanges")(function_handlers["deleteFlagConfigScheduledChanges"])
    registry.register("getWorkflows")(function_handlers["getWorkflows"])
    registry.register("postWorkflow")(function_handlers["postWorkflow"])
    registry.register("getCustomWorkflow")(function_handlers["getCustomWorkflow"])
    registry.register("deleteWorkflow")(function_handlers["deleteWorkflow"])
    registry.register("postMigrationSafetyIssues")(function_handlers["postMigrationSafetyIssues"])
    registry.register("createReleaseForFlag")(function_handlers["createReleaseForFlag"])
    registry.register("updatePhaseStatus")(function_handlers["updatePhaseStatus"])
    registry.register("getLayers")(function_handlers["getLayers"])
    registry.register("createLayer")(function_handlers["createLayer"])
    registry.register("updateLayer")(function_handlers["updateLayer"])
    registry.register("getMetricGroups")(function_handlers["getMetricGroups"])
    registry.register("createMetricGroup")(function_handlers["createMetricGroup"])
    registry.register("getMetricGroup")(function_handlers["getMetricGroup"])
    registry.register("patchMetricGroup")(function_handlers["patchMetricGroup"])
    registry.register("deleteMetricGroup")(function_handlers["deleteMetricGroup"])
    registry.register("getAllReleasePipelines")(function_handlers["getAllReleasePipelines"])
    registry.register("postReleasePipeline")(function_handlers["postReleasePipeline"])
    registry.register("getReleasePipelineByKey")(function_handlers["getReleasePipelineByKey"])
    registry.register("putReleasePipeline")(function_handlers["putReleasePipeline"])
    registry.register("deleteReleasePipeline")(function_handlers["deleteReleasePipeline"])
    registry.register("getAllReleaseProgressionsForReleasePipeline")(function_handlers["getAllReleaseProgressionsForReleasePipeline"])
    registry.register("getIps")(function_handlers["getIps"])
    registry.register("getCustomRoles")(function_handlers["getCustomRoles"])
    registry.register("postCustomRole")(function_handlers["postCustomRole"])
    registry.register("getCustomRole")(function_handlers["getCustomRole"])
    registry.register("patchCustomRole")(function_handlers["patchCustomRole"])
    registry.register("deleteCustomRole")(function_handlers["deleteCustomRole"])
    registry.register("getSegments")(function_handlers["getSegments"])
    registry.register("postSegment")(function_handlers["postSegment"])
    registry.register("getSegment")(function_handlers["getSegment"])
    registry.register("patchSegment")(function_handlers["patchSegment"])
    registry.register("deleteSegment")(function_handlers["deleteSegment"])
    registry.register("updateBigSegmentContextTargets")(function_handlers["updateBigSegmentContextTargets"])
    registry.register("getSegmentMembershipForContext")(function_handlers["getSegmentMembershipForContext"])
    registry.register("createBigSegmentExport")(function_handlers["createBigSegmentExport"])
    registry.register("getBigSegmentExport")(function_handlers["getBigSegmentExport"])
    registry.register("createBigSegmentImport")(function_handlers["createBigSegmentImport"])
    registry.register("getBigSegmentImport")(function_handlers["getBigSegmentImport"])
    registry.register("updateBigSegmentTargets")(function_handlers["updateBigSegmentTargets"])
    registry.register("getSegmentMembershipForUser")(function_handlers["getSegmentMembershipForUser"])
    registry.register("getExpiringTargetsForSegment")(function_handlers["getExpiringTargetsForSegment"])
    registry.register("patchExpiringTargetsForSegment")(function_handlers["patchExpiringTargetsForSegment"])
    registry.register("getExpiringUserTargetsForSegment")(function_handlers["getExpiringUserTargetsForSegment"])
    registry.register("patchExpiringUserTargetsForSegment")(function_handlers["patchExpiringUserTargetsForSegment"])
    registry.register("getTeams")(function_handlers["getTeams"])
    registry.register("postTeam")(function_handlers["postTeam"])
    registry.register("patchTeams")(function_handlers["patchTeams"])
    registry.register("getTeam")(function_handlers["getTeam"])
    registry.register("patchTeam")(function_handlers["patchTeam"])
    registry.register("deleteTeam")(function_handlers["deleteTeam"])
    registry.register("getTeamMaintainers")(function_handlers["getTeamMaintainers"])
    registry.register("postTeamMembers")(function_handlers["postTeamMembers"])
    registry.register("getTeamRoles")(function_handlers["getTeamRoles"])
    registry.register("getWorkflowTemplates")(function_handlers["getWorkflowTemplates"])
    registry.register("createWorkflowTemplate")(function_handlers["createWorkflowTemplate"])
    registry.register("deleteWorkflowTemplate")(function_handlers["deleteWorkflowTemplate"])
    registry.register("getTokens")(function_handlers["getTokens"])
    registry.register("postToken")(function_handlers["postToken"])
    registry.register("getToken")(function_handlers["getToken"])
    registry.register("patchToken")(function_handlers["patchToken"])
    registry.register("deleteToken")(function_handlers["deleteToken"])
    registry.register("resetToken")(function_handlers["resetToken"])
    registry.register("getDataExportEventsUsage")(function_handlers["getDataExportEventsUsage"])
    registry.register("getEvaluationsUsage")(function_handlers["getEvaluationsUsage"])
    registry.register("getEventsUsage")(function_handlers["getEventsUsage"])
    registry.register("getExperimentationKeysUsage")(function_handlers["getExperimentationKeysUsage"])
    registry.register("getExperimentationUnitsUsage")(function_handlers["getExperimentationUnitsUsage"])
    registry.register("getMauUsage")(function_handlers["getMauUsage"])
    registry.register("getMauUsageByCategory")(function_handlers["getMauUsageByCategory"])
    registry.register("getMauSdksByType")(function_handlers["getMauSdksByType"])
    registry.register("getServiceConnectionUsage")(function_handlers["getServiceConnectionUsage"])
    registry.register("getStreamUsage")(function_handlers["getStreamUsage"])
    registry.register("getStreamUsageBySdkVersion")(function_handlers["getStreamUsageBySdkVersion"])
    registry.register("getStreamUsageSdkversion")(function_handlers["getStreamUsageSdkversion"])
    registry.register("getUserAttributeNames")(function_handlers["getUserAttributeNames"])
    registry.register("getSearchUsers")(function_handlers["getSearchUsers"])
    registry.register("getUsers")(function_handlers["getUsers"])
    registry.register("getUser")(function_handlers["getUser"])
    registry.register("deleteUser")(function_handlers["deleteUser"])
    registry.register("getUserFlagSettings")(function_handlers["getUserFlagSettings"])
    registry.register("getUserFlagSetting")(function_handlers["getUserFlagSetting"])
    registry.register("putFlagSetting")(function_handlers["putFlagSetting"])
    registry.register("getExpiringFlagsForUser")(function_handlers["getExpiringFlagsForUser"])
    registry.register("patchExpiringFlagsForUser")(function_handlers["patchExpiringFlagsForUser"])
    registry.register("getVersions")(function_handlers["getVersions"])
    registry.register("getAllWebhooks")(function_handlers["getAllWebhooks"])
    registry.register("postWebhook")(function_handlers["postWebhook"])
    registry.register("getWebhook")(function_handlers["getWebhook"])
    registry.register("patchWebhook")(function_handlers["patchWebhook"])
    registry.register("deleteWebhook")(function_handlers["deleteWebhook"])
    registry.register("getTags")(function_handlers["getTags"])
    registry.register("getAIConfigs")(function_handlers["getAIConfigs"])
    registry.register("postAIConfig")(function_handlers["postAIConfig"])
    registry.register("deleteAIConfig")(function_handlers["deleteAIConfig"])
    registry.register("getAIConfig")(function_handlers["getAIConfig"])
    registry.register("patchAIConfig")(function_handlers["patchAIConfig"])
    registry.register("postAIConfigVariation")(function_handlers["postAIConfigVariation"])
    registry.register("deleteAIConfigVariation")(function_handlers["deleteAIConfigVariation"])
    registry.register("getAIConfigVariation")(function_handlers["getAIConfigVariation"])
    registry.register("patchAIConfigVariation")(function_handlers["patchAIConfigVariation"])
    registry.register("getAIConfigMetrics")(function_handlers["getAIConfigMetrics"])
    registry.register("getAIConfigMetricsByVariation")(function_handlers["getAIConfigMetricsByVariation"])
    registry.register("listModelConfigs")(function_handlers["listModelConfigs"])
    registry.register("postModelConfig")(function_handlers["postModelConfig"])
    registry.register("deleteModelConfig")(function_handlers["deleteModelConfig"])
    registry.register("getModelConfig")(function_handlers["getModelConfig"])
    registry.register("getAnnouncementsPublic")(function_handlers["getAnnouncementsPublic"])
    registry.register("createAnnouncementPublic")(function_handlers["createAnnouncementPublic"])
    registry.register("deleteAnnouncementPublic")(function_handlers["deleteAnnouncementPublic"])
    registry.register("updateAnnouncementPublic")(function_handlers["updateAnnouncementPublic"])
    registry.register("getDeploymentFrequencyChart")(function_handlers["getDeploymentFrequencyChart"])
    registry.register("getStaleFlagsChart")(function_handlers["getStaleFlagsChart"])
    registry.register("getFlagStatusChart")(function_handlers["getFlagStatusChart"])
    registry.register("getLeadTimeChart")(function_handlers["getLeadTimeChart"])
    registry.register("getReleaseFrequencyChart")(function_handlers["getReleaseFrequencyChart"])
    registry.register("createDeploymentEvent")(function_handlers["createDeploymentEvent"])
    registry.register("getDeployments")(function_handlers["getDeployments"])
    registry.register("getDeployment")(function_handlers["getDeployment"])
    registry.register("updateDeployment")(function_handlers["updateDeployment"])
    registry.register("getFlagEvents")(function_handlers["getFlagEvents"])
    registry.register("createInsightGroup")(function_handlers["createInsightGroup"])
    registry.register("getInsightGroups")(function_handlers["getInsightGroups"])
    registry.register("getInsightGroup")(function_handlers["getInsightGroup"])
    registry.register("patchInsightGroup")(function_handlers["patchInsightGroup"])
    registry.register("deleteInsightGroup")(function_handlers["deleteInsightGroup"])
    registry.register("getInsightsScores")(function_handlers["getInsightsScores"])
    registry.register("getPullRequests")(function_handlers["getPullRequests"])
    registry.register("getInsightsRepositories")(function_handlers["getInsightsRepositories"])
    registry.register("associateRepositoriesAndProjects")(function_handlers["associateRepositoriesAndProjects"])
    registry.register("deleteRepositoryProject")(function_handlers["deleteRepositoryProject"])
    
    # Create and start the MCP server
    server = McpServer(
        host="0.0.0.0",
        port=8888,
        registry=registry,
        capabilities=capabilities,
    )
    
    logger.info("Starting launchdarkly_mcp_server MCP Server")
    logger.info(f"Target API: {config.TARGET_API_BASE_URL}")
    logger.info(f"Registered functions: {len(function_handlers)}")
    
    await server.start()
    
    # Keep the server running until interrupted
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main()) 
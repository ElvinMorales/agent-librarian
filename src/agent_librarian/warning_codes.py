from __future__ import annotations


MISSING_DESCRIPTION = "missing_description"
WEAK_DESCRIPTION = "weak_description"
MISSING_ACTIVATION_TRIGGER = "missing_activation_trigger"
MISSING_INPUTS = "missing_inputs"
MISSING_OUTPUTS = "missing_outputs"
MISSING_OUTPUT_CONTRACT = "missing_output_contract"
OVERBROAD_TOOL_SCOPE = "overbroad_tool_scope"
SIDE_EFFECTS_UNCLEAR = "side_effects_unclear"
MISSING_DEPENDENCIES = "missing_dependencies"
MISSING_EXAMPLES = "missing_examples"
MISSING_EVALS = "missing_evals"
UNKNOWN_ARTIFACT_TYPE = "unknown_artifact_type"
PUBLIC_SAFETY_REVIEW_NEEDED = "public_safety_review_needed"

UNSUPPORTED_FILE_TYPE = "unsupported_file_type"
UNTERMINATED_FRONTMATTER = "unterminated_frontmatter"
NON_MAPPING_FRONTMATTER = "non_mapping_frontmatter"
NON_MAPPING_DOCUMENT = "non_mapping_document"

DUPLICATE_CANDIDATE = "duplicate_candidate"
OVERLAP_CANDIDATE = "overlap_candidate"


CATALOG_WARNING_CODES = frozenset(
    {
        MISSING_DESCRIPTION,
        WEAK_DESCRIPTION,
        MISSING_ACTIVATION_TRIGGER,
        MISSING_INPUTS,
        MISSING_OUTPUTS,
        MISSING_OUTPUT_CONTRACT,
        OVERBROAD_TOOL_SCOPE,
        SIDE_EFFECTS_UNCLEAR,
        MISSING_DEPENDENCIES,
        MISSING_EXAMPLES,
        MISSING_EVALS,
        UNKNOWN_ARTIFACT_TYPE,
        PUBLIC_SAFETY_REVIEW_NEEDED,
    }
)
DIAGNOSTIC_WARNING_CODES = frozenset(
    {
        UNSUPPORTED_FILE_TYPE,
        UNTERMINATED_FRONTMATTER,
        NON_MAPPING_FRONTMATTER,
        NON_MAPPING_DOCUMENT,
    }
)
OVERLAP_WARNING_CODES = frozenset(
    {
        DUPLICATE_CANDIDATE,
        OVERLAP_CANDIDATE,
    }
)
ACTIVE_WARNING_CODES = (
    CATALOG_WARNING_CODES | DIAGNOSTIC_WARNING_CODES | OVERLAP_WARNING_CODES
)
PARTIAL_WARNING_CODES = frozenset(
    {
        MISSING_DESCRIPTION,
        WEAK_DESCRIPTION,
        MISSING_ACTIVATION_TRIGGER,
        MISSING_INPUTS,
        MISSING_OUTPUTS,
        MISSING_OUTPUT_CONTRACT,
        SIDE_EFFECTS_UNCLEAR,
        MISSING_DEPENDENCIES,
        MISSING_EXAMPLES,
        MISSING_EVALS,
        UNKNOWN_ARTIFACT_TYPE,
    }
)

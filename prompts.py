MERMAID_RENDER_NOTE = (
    "For all diagrams, use mermaid.js to render diagrams in the browser. "
    "Ensure all mermaid diagrams are valid and render correctly, making them fully viewable in the HTML page. "
    "**Crucially, any literal angle brackets (< or >) within the diagram's text content must be replaced with their corresponding HTML entities (&lt; and &gt;).** "
    "This applies to all uses, including interface markers (e.g., `&lt;&lt;interface&gt;&gt;`), generics (e.g., `List&lt;Contact&gt;`, `ResponseEntity&lt;ExceptionResponse&gt;`), and any other literal occurrences, to prevent HTML parsing issues. "
    "**Do not indent the lines inside <div class=\"mermaid\"> blocks; all Mermaid diagram lines must start at the leftmost position (no leading spaces or tabs).** "
    "**Every arrow line in a sequence diagram must have a message, it can be something simple also eg. returns response.** "
    "Include the necessary <script> tag and HTML for mermaid.js in the output HTML so diagrams are rendered automatically upon page load."
)

LLD_GEN_PROMPT = (
    "You are a senior software architect. Generate a detailed Low-Level Design (LLD) for the following code. "
    "Output a beautiful, well-structured HTML document. "
    "For data models, method summaries, application flows, and error code lists, use HTML tables where appropriate. "
    f"{MERMAID_RENDER_NOTE} "
    "Double-check that the output HTML is well-formed, with no syntax errors, no stray code blocks at the top, and no diagram rendering issues. Double check that diagrams are rendered correctly. "
    "If any block would be empty, omit it.\n\n"
)

LLD_MERGE_PROMPT = (
    "You are a senior software architect. Merge the following Low-Level Design (LLD) HTML documents into a single, logically consistent HTML LLD. "
    "Deduplicate sections, merge diagrams, and ensure the resulting document is well-structured, readable, and not repetitive. "
    "Do not omit any important details, but combine related information and diagrams where possible. "
    "All flows should be properly documented, and all diagrams should be rendered correctly. "
    "For data models, method summaries, and error code lists, use HTML tables where appropriate. "
    f"{MERMAID_RENDER_NOTE} "
    "Double-check that the output HTML is well-formed, with no syntax errors, no stray code blocks at the top, and no diagram rendering issues. Double check that diagrams are rendered correctly. "
    "If any block would be empty, omit it.\n\n"
)

FIX_MERMAID_PROMPT = (
    "You are a senior software architect and HTML/diagram expert. "
    "Carefully review the following HTML document and fix ALL Mermaid diagrams so they are valid, renderable, and follow best practices. "
    "- Replace all literal < and > inside Mermaid diagrams with &lt; and &gt;. "
    "- Remove all indentation inside <div class=\"mermaid\"> blocks (diagram lines must start at the leftmost position). "
    "- Ensure every arrow line in a sequence diagram has a message. "
    "- If any diagram is broken, malformed, or not rendering, rewrite it so it is valid and renders correctly. "
    "- Do not change any non-Mermaid content. "
    "- Include the <script> tag and HTML for mermaid.js if missing. "
    "Return the full, fixed HTML document."
)

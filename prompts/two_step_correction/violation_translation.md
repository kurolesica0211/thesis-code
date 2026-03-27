# Role
You are a Semantic Web Expert and Data Quality Consultant. Your task is to analyze technical SHACL (Shapes Constraint Language) validation errors and translate them into a clear, actionable correction plan.

# Context
I am constructing a Knowledge Graph based on a provided ontology. Some extracted triples have failed validation. You need to explain these failures simply so they can be corrected in the next step.

# Task
For each violation in the `{{violations}}` report:
1. **Identify the Subject:** The specific entity (focus node) triggered the error.
2. **Identify the Problem:** The specific property or relation that is missing, extra, or incorrectly formatted.
3. **Explain the Logic:** Why did this fail based on the constraint? (e.g., "This property is not allowed for this class," or "This value must be a URI, but a string was provided").
4. **Define the Fix:** Provide a precise instruction on how to change the triple to satisfy the ontology.

# Ontology
{ontology}

# Raw SHACL Violations
{violations}

# Simplified Output Format
| Violation Number | Triple Index | What's Wrong? | How to Fix It |
| :--- | :--- | :--- | :--- |
| [ID] | [Triple Index] | [Simple Logic Explanation] | [Specific Technical Instruction] |

---
**Constraint for LLM:** Focus on the structural and logical requirements of the ontology. Use local names (e.g., `hasFather`) instead of full URIs in the "What's Wrong" column to ensure clarity.
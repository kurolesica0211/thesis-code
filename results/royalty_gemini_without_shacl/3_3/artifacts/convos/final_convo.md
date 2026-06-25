================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
George Philip Nicholas Windsor, Earl of St Andrews (born 26 June 1962), is a British philanthropist, former diplomat and a member of the extended British royal family.
St Andrews became chancellor of the University of Bolton in 2017.
He is the elder son of Prince Edward, Duke of Kent, and Katharine, Duchess of Kent, and heir apparent to the dukedom of Kent.
Early life and career

George Philip Nicholas Windsor was born on 26 June 1962 at Coppins, Iver, Buckinghamshire, the eldest child of Prince Edward, Duke of Kent, and Katharine, Duchess of Kent (née Worsley, a daughter of Sir William Worsley, 4th Baronet).
Royal obstetrician Sir John Peel assisted at his birth, at which time Lord St Andrews was 10th in line of succession to the throne.
His godparents were Prince Philip, Duke of Edinburgh; his aunt Princess Alexandra of Kent, his uncle Oliver Worsley, and Lady Lily Serena Lumley (daughter of the 11th Earl of Scarbrough).
St Andrews served in the Diplomatic Service in New York and Budapest.
, George married Sylvana Tomaselli, a Canadian-born academic, at Leith Registration Office in Edinburgh at a civil ceremony.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (4ffa56d7-34df-4bff-8cd8-2e1eb3d14fd6)
 Call ID: 4ffa56d7-34df-4bff-8cd8-2e1eb3d14fd6
  Args:
    source: George_Philip_Nicholas_Windsor
    type: :Man
  AssignClass (828015aa-5cce-4983-95a3-1131b5310083)
 Call ID: 828015aa-5cce-4983-95a3-1131b5310083
  Args:
    source: George_Philip_Nicholas_Windsor
    type: :Person
  AddLiteral (0e759012-268c-4d93-95e0-c2fb4f0aaaf4)
 Call ID: 0e759012-268c-4d93-95e0-c2fb4f0aaaf4
  Args:
    literal_value: 1962
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: George_Philip_Nicholas_Windsor
  AssignClass (70abb06c-8e77-40eb-a3a3-198676412e79)
 Call ID: 70abb06c-8e77-40eb-a3a3-198676412e79
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Man
  AssignClass (bb6ff955-aeb9-4896-9c9f-e7dae4f847f5)
 Call ID: bb6ff955-aeb9-4896-9c9f-e7dae4f847f5
  Args:
    source: Prince_Edward_Duke_of_Kent
    type: :Person
  AddTriple (a2a48893-59e4-4da9-b47f-cbd257c89a01)
 Call ID: a2a48893-59e4-4da9-b47f-cbd257c89a01
  Args:
    target: Prince_Edward_Duke_of_Kent
    relation: :hasFather
    source: George_Philip_Nicholas_Windsor
  AssignClass (f3d6f45c-2e2b-4580-b8a5-495bb31488a2)
 Call ID: f3d6f45c-2e2b-4580-b8a5-495bb31488a2
  Args:
    source: Katharine_Duchess_of_Kent
    type: :Woman
  AssignClass (3b538dd1-cf26-4d60-b412-e692bf290fd0)
 Call ID: 3b538dd1-cf26-4d60-b412-e692bf290fd0
  Args:
    type: :Person
    source: Katharine_Duchess_of_Kent
  AddTriple (ba7e1c03-d5c0-4f9d-9a5f-30aa9f7b02da)
 Call ID: ba7e1c03-d5c0-4f9d-9a5f-30aa9f7b02da
  Args:
    source: George_Philip_Nicholas_Windsor
    relation: :hasMother
    target: Katharine_Duchess_of_Kent
  AssignClass (16d51225-d66b-44f7-aaf7-5cc695ac326a)
 Call ID: 16d51225-d66b-44f7-aaf7-5cc695ac326a
  Args:
    source: Sylvana_Tomaselli
    type: :Woman
  AssignClass (34f3f0d2-fe30-4eb1-ad22-6ebc9914f232)
 Call ID: 34f3f0d2-fe30-4eb1-ad22-6ebc9914f232
  Args:
    type: :Person
    source: Sylvana_Tomaselli
  AddTriple (7118b7c5-990b-4a48-ba4e-a1f3698303e5)
 Call ID: 7118b7c5-990b-4a48-ba4e-a1f3698303e5
  Args:
    target: Sylvana_Tomaselli
    source: George_Philip_Nicholas_Windsor
    relation: :hasRelation
  AssignClass (724fc29a-f4ed-463b-9606-b9877c1f23e0)
 Call ID: 724fc29a-f4ed-463b-9606-b9877c1f23e0
  Args:
    source: Sir_William_Worsley
    type: :Man
  AssignClass (bac85269-4593-4f53-96f1-3325bf665ea1)
 Call ID: bac85269-4593-4f53-96f1-3325bf665ea1
  Args:
    type: :Person
    source: Sir_William_Worsley
  AddTriple (ccd794eb-a377-42f2-a237-c7ccb24b8eda)
 Call ID: ccd794eb-a377-42f2-a237-c7ccb24b8eda
  Args:
    relation: :hasFather
    source: Katharine_Duchess_of_Kent
    target: Sir_William_Worsley
  AssignClass (ab374f23-bac2-4975-b2bd-0054755fda23)
 Call ID: ab374f23-bac2-4975-b2bd-0054755fda23
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Kent
  AssignClass (a84cf5c5-ec53-4aa0-8ef0-8df7ad821d12)
 Call ID: a84cf5c5-ec53-4aa0-8ef0-8df7ad821d12
  Args:
    type: :Person
    source: Princess_Alexandra_of_Kent
  AddTriple (84b3d6e1-8f9b-4cbe-964f-31de2ad412e0)
 Call ID: 84b3d6e1-8f9b-4cbe-964f-31de2ad412e0
  Args:
    target: George_Philip_Nicholas_Windsor
    source: Princess_Alexandra_of_Kent
    relation: :isAuntOf
  AssignClass (87779c0a-1ba5-4b2c-8f99-463964698777)
 Call ID: 87779c0a-1ba5-4b2c-8f99-463964698777
  Args:
    source: Oliver_Worsley
    type: :Man
  AssignClass (dda3be5c-f952-4500-b97e-7c6f5f46ecdc)
 Call ID: dda3be5c-f952-4500-b97e-7c6f5f46ecdc
  Args:
    source: Oliver_Worsley
    type: :Person
  AddTriple (1defbfcc-2ebf-4316-9a51-cf4722f8a142)
 Call ID: 1defbfcc-2ebf-4316-9a51-cf4722f8a142
  Args:
    target: George_Philip_Nicholas_Windsor
    source: Oliver_Worsley
    relation: :isUncleOf
  AssignClass (b2af055c-1f70-4089-be17-35becab2c767)
 Call ID: b2af055c-1f70-4089-be17-35becab2c767
  Args:
    type: :Woman
    source: Lady_Lily_Serena_Lumley
  AssignClass (eb901f36-403f-42c8-99f7-00e047487c96)
 Call ID: eb901f36-403f-42c8-99f7-00e047487c96
  Args:
    source: Lady_Lily_Serena_Lumley
    type: :Person
  AssignClass (1ff51588-651f-4e97-b599-dc27cfa041d7)
 Call ID: 1ff51588-651f-4e97-b599-dc27cfa041d7
  Args:
    source: Earl_of_Scarbrough
    type: :Man
  AssignClass (e3a63acc-9a87-4963-b03b-d93d1fb4ef22)
 Call ID: e3a63acc-9a87-4963-b03b-d93d1fb4ef22
  Args:
    source: Earl_of_Scarbrough
    type: :Person
  AddTriple (a8c8111b-fd9e-4d4b-8b34-f31047f5e08c)
 Call ID: a8c8111b-fd9e-4d4b-8b34-f31047f5e08c
  Args:
    target: Earl_of_Scarbrough
    relation: :hasFather
    source: Lady_Lily_Serena_Lumley
  Finish (d75f3182-7414-4b3d-b0ab-db1afe85156e)
 Call ID: d75f3182-7414-4b3d-b0ab-db1afe85156e
  Args:
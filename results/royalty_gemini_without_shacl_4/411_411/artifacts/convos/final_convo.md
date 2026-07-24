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
Duke Christian Louis of Mecklenburg (German: Christian-Ludwig Herzog zu Mecklenburg; 29 September 1912 – 18 July 1996) was the second son of the last reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV.
Early life

Born in Schloss Ludwigslust, as a member of an elder, Mecklenburg-Schwerin line of an ancient House of Mecklenburg, he was the second child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife, Princess Alexandra of Hanover, third child and second daughter of Ernest Augustus, Crown Prince of Hanover and Princess Thyra of Denmark.
After the abolition of the monarchy, in 1919 the family went at the invitation of Queen Alexandrine, consort of Christian X of Denmark and sister of the Grand Duke, into exile in Denmark, where they lived for a year in Sorgenfri Palace.
Later, the family returned to Mecklenburg and lived in Gelbensande, and from 1921 the family settled at Ludwigslust Castle.
After the war

When the war ended, Ludwigslust was first occupied by the British, but soon was transferred to the Soviet occupation, so that Christian Louis initially went with his family to Glücksburg Castle in Schleswig-Holstein.
Together with his sister Thyra, he took part in the ship tour organized by Queen Frederica and her husband King Paul of Greece in 1954, which became known as the “Cruise of the Kings” and was attended by over 100 royals from all over Europe.
Marriage and family

On 5 July 1954 in Glücksburg, Christian Louis married in a civil wedding Princess Barbara of Prussia (1920–1994), the daughter of Prince Sigismund of Prussia and his wife, Princess Charlotte of Saxe-Altenburg.



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
  AssignClass (9dc68e52-196e-4587-a40a-d1899fb46fe2)
 Call ID: 9dc68e52-196e-4587-a40a-d1899fb46fe2
  Args:
    type: :Man
    source: Christian_Louis_of_Mecklenburg
  AssignClass (61c6836d-deec-4dd3-b923-b75581d24089)
 Call ID: 61c6836d-deec-4dd3-b923-b75581d24089
  Args:
    type: :Person
    source: Christian_Louis_of_Mecklenburg
  AddLiteral (a9595a4b-bdc3-4321-8d05-c056e7ed658e)
 Call ID: a9595a4b-bdc3-4321-8d05-c056e7ed658e
  Args:
    relation: :hasBirthYear
    literal_value: 1912
    literal_type: xsd:integer
    source: Christian_Louis_of_Mecklenburg
  AddLiteral (bddfc13f-47f3-478d-becd-595dba82b6b7)
 Call ID: bddfc13f-47f3-478d-becd-595dba82b6b7
  Args:
    source: Christian_Louis_of_Mecklenburg
    literal_type: xsd:integer
    literal_value: 1996
    relation: :hasDeathYear
  AssignClass (aa54eb5c-5758-4f83-a8d7-bdde7ab7df5a)
 Call ID: aa54eb5c-5758-4f83-a8d7-bdde7ab7df5a
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (c09ac7b8-14bf-4426-ade6-105886a2cb30)
 Call ID: c09ac7b8-14bf-4426-ade6-105886a2cb30
  Args:
    type: :Person
    source: Frederick_Francis_IV
  AddTriple (bed867f1-964a-4959-b446-0736eaf0bf47)
 Call ID: bed867f1-964a-4959-b446-0736eaf0bf47
  Args:
    relation: :hasFather
    source: Christian_Louis_of_Mecklenburg
    target: Frederick_Francis_IV
  AssignClass (76edc055-a23e-4f45-a189-8ac3e5529303)
 Call ID: 76edc055-a23e-4f45-a189-8ac3e5529303
  Args:
    type: :Woman
    source: Alexandra_of_Hanover
  AssignClass (a5f0f04f-419d-45d2-83e5-fb90dd65e0a1)
 Call ID: a5f0f04f-419d-45d2-83e5-fb90dd65e0a1
  Args:
    type: :Person
    source: Alexandra_of_Hanover
  AddTriple (7b5cd9b6-7a1a-44b2-b44f-08d214cdd899)
 Call ID: 7b5cd9b6-7a1a-44b2-b44f-08d214cdd899
  Args:
    source: Christian_Louis_of_Mecklenburg
    target: Alexandra_of_Hanover
    relation: :hasMother
  AssignClass (3a3f7659-7060-4b01-a745-edf0d2ced9ab)
 Call ID: 3a3f7659-7060-4b01-a745-edf0d2ced9ab
  Args:
    type: :Man
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (0a47ed5b-c707-45db-841c-1098d7a286ac)
 Call ID: 0a47ed5b-c707-45db-841c-1098d7a286ac
  Args:
    type: :Person
    source: Ernest_Augustus_Crown_Prince_of_Hanover
  AddTriple (d0e22f63-0c72-485d-88d5-4fdaafa911be)
 Call ID: d0e22f63-0c72-485d-88d5-4fdaafa911be
  Args:
    relation: :hasFather
    source: Alexandra_of_Hanover
    target: Ernest_Augustus_Crown_Prince_of_Hanover
  AssignClass (89e9ef35-0dcc-45ae-8370-3b4757d6446a)
 Call ID: 89e9ef35-0dcc-45ae-8370-3b4757d6446a
  Args:
    type: :Woman
    source: Thyra_of_Denmark
  AssignClass (0fc89661-e2fb-4eef-80ef-307681fcd8d5)
 Call ID: 0fc89661-e2fb-4eef-80ef-307681fcd8d5
  Args:
    type: :Person
    source: Thyra_of_Denmark
  AddTriple (cc7c91bb-e5cc-4c17-98af-ffa68b32cc02)
 Call ID: cc7c91bb-e5cc-4c17-98af-ffa68b32cc02
  Args:
    relation: :hasMother
    target: Thyra_of_Denmark
    source: Alexandra_of_Hanover
  AssignClass (13d8d022-79d2-4153-8cb7-9422aec8d1df)
 Call ID: 13d8d022-79d2-4153-8cb7-9422aec8d1df
  Args:
    type: :Woman
    source: Thyra_sister_of_Christian_Louis
  AssignClass (3c834715-bc62-49ab-a1a6-e8f41c7e4eef)
 Call ID: 3c834715-bc62-49ab-a1a6-e8f41c7e4eef
  Args:
    type: :Person
    source: Thyra_sister_of_Christian_Louis
  AddTriple (d8a10365-7533-43bc-bead-af1461298225)
 Call ID: d8a10365-7533-43bc-bead-af1461298225
  Args:
    source: Christian_Louis_of_Mecklenburg
    target: Thyra_sister_of_Christian_Louis
    relation: :isSiblingOf
  AssignClass (ca05e834-ed93-4f16-92d2-0ad95a7117ed)
 Call ID: ca05e834-ed93-4f16-92d2-0ad95a7117ed
  Args:
    type: :Woman
    source: Barbara_of_Prussia
  AssignClass (1e17244e-0f21-400e-b4d3-4474a204361a)
 Call ID: 1e17244e-0f21-400e-b4d3-4474a204361a
  Args:
    type: :Person
    source: Barbara_of_Prussia
  AddLiteral (c739bf05-56c4-45b7-8112-7d65cd359ef2)
 Call ID: c739bf05-56c4-45b7-8112-7d65cd359ef2
  Args:
    source: Barbara_of_Prussia
    literal_type: xsd:integer
    literal_value: 1920
    relation: :hasBirthYear
  AddLiteral (29b112d9-e79d-4615-84b8-863b77aa3933)
 Call ID: 29b112d9-e79d-4615-84b8-863b77aa3933
  Args:
    relation: :hasDeathYear
    literal_value: 1994
    literal_type: xsd:integer
    source: Barbara_of_Prussia
  AddTriple (fbaae8b8-0f4a-464c-81f7-991df9d6ca9d)
 Call ID: fbaae8b8-0f4a-464c-81f7-991df9d6ca9d
  Args:
    relation: :hasRelation
    target: Barbara_of_Prussia
    source: Christian_Louis_of_Mecklenburg
  AddLiteral (faadf038-cf78-4878-92d2-c5accf56f303)
 Call ID: faadf038-cf78-4878-92d2-c5accf56f303
  Args:
    literal_type: xsd:integer
    source: Christian_Louis_of_Mecklenburg
    relation: :hasMarriageYear
    literal_value: 1954
  AssignClass (4e673098-0a3f-4d1c-ba51-af710ef12ec8)
 Call ID: 4e673098-0a3f-4d1c-ba51-af710ef12ec8
  Args:
    type: :Man
    source: Sigismund_of_Prussia
  AssignClass (d1059811-4c08-4ea3-a6ce-47245c71585e)
 Call ID: d1059811-4c08-4ea3-a6ce-47245c71585e
  Args:
    type: :Person
    source: Sigismund_of_Prussia
  AddTriple (dc49acad-4d17-499f-aed6-c16c928afa9a)
 Call ID: dc49acad-4d17-499f-aed6-c16c928afa9a
  Args:
    target: Sigismund_of_Prussia
    source: Barbara_of_Prussia
    relation: :hasFather
  AssignClass (4a079c0c-4f11-43cf-8455-90649ea96ca5)
 Call ID: 4a079c0c-4f11-43cf-8455-90649ea96ca5
  Args:
    type: :Woman
    source: Charlotte_of_Saxe_Altenburg
  AssignClass (f921cb88-302b-40b2-a80d-fcf62c1225e5)
 Call ID: f921cb88-302b-40b2-a80d-fcf62c1225e5
  Args:
    type: :Person
    source: Charlotte_of_Saxe_Altenburg
  AddTriple (f36afcf8-a157-4880-a891-7133bbad201b)
 Call ID: f36afcf8-a157-4880-a891-7133bbad201b
  Args:
    source: Barbara_of_Prussia
    target: Charlotte_of_Saxe_Altenburg
    relation: :hasMother
  Finish (1fe792f7-c0e7-41e8-9e12-2a4c5729843c)
 Call ID: 1fe792f7-c0e7-41e8-9e12-2a4c5729843c
  Args:
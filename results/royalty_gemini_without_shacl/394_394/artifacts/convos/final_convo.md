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
Prince Bernhard of Lippe (Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard; 26 August 1872 – 19 June 1934) was a member of the Lippe-Biesterfeld line of the House of Lippe.
He was the father of Prince Bernhard of Lippe-Biesterfeld, the prince consort of Queen Juliana of the Netherlands.
Biography

Prince Bernhard of Lippe, born as Count of Lippe-Biesterfeld in Oberkassel on 26 August 1872, was the 2nd son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of Principality of Lippe, and his wife Countess Karoline von Wartensleben.
He was a younger brother of Leopold IV, Prince of Lippe, who succeeded as reigning Prince of Lippe in 1905.
The Lippe-Biesterfeld family had lived at Oberkassel, Bonn, ever since 1770, when count Frederick William (1737–1803) had married Elisabeth Johanna, Edle von Meinertzhagen (1752–1811), who inherited a small manor house at Oberkassel where the couple moved from Biesterfeld in 1770, and which became the home to the family for the following 209 years.
The manor house and farm at Biesterfeld were demolished around 1820.
Prince Bernhard acquired the Reckenwalde castle in eastern Brandenburg (today Wojnowo, Poland), the family's new estate, where his children grew up.
On 4 March 1909, Bernhard entered into a morganatic marriage with Baroness Armgard von Sierstorpff-Cramm, widowed Countess von Oeynhausen.
Before this marriage, his wife was granted the title Countess of Biesterfeld (Gräfin von Biesterfeld) on 8 February 1909.
She and her two sons Bernhard and Aschwin were created Princess (Prince) of Lippe-Biesterfeld (Prinzessin (Prinz) zur Lippe-Biesterfeld) on 24 February 1916 with the style Serene Highness, which brought their children into a more senior place in the line of succession, in which they hitherto had been the very last.
The suffix Biesterfeld was revived to mark the beginning of a new cadet line.
Bernhard died in Munich, aged 61.



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
  AssignClass (af69023d-ed28-4c45-a71d-7593fd8e8e36)
 Call ID: af69023d-ed28-4c45-a71d-7593fd8e8e36
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe
  AssignClass (8b23141f-fff8-4dc3-9768-43d6d44cf682)
 Call ID: 8b23141f-fff8-4dc3-9768-43d6d44cf682
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe
  AddLiteral (d5f7d13a-535c-4afd-91b3-a504991c293c)
 Call ID: d5f7d13a-535c-4afd-91b3-a504991c293c
  Args:
    relation: :hasBirthYear
    literal_value: 1872
    source: Prince_Bernhard_of_Lippe
    literal_type: xsd:integer
  AddLiteral (5afdbcb8-64d3-4cc5-9064-679d2937ab39)
 Call ID: 5afdbcb8-64d3-4cc5-9064-679d2937ab39
  Args:
    relation: :hasDeathYear
    literal_value: 1934
    source: Prince_Bernhard_of_Lippe
    literal_type: xsd:integer
  AssignClass (15719acb-7e77-4e23-ad8f-a4ada2a617e1)
 Call ID: 15719acb-7e77-4e23-ad8f-a4ada2a617e1
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (5a6eeba8-2296-4b41-b23c-fa4bbe63da52)
 Call ID: 5a6eeba8-2296-4b41-b23c-fa4bbe63da52
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (b4c95fb8-51ba-40f2-8950-d3a31088d2c9)
 Call ID: b4c95fb8-51ba-40f2-8950-d3a31088d2c9
  Args:
    relation: :hasFather
    target: Prince_Bernhard_of_Lippe
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (ca9fc0e8-75f7-42cb-abdd-5d83a18efbf2)
 Call ID: ca9fc0e8-75f7-42cb-abdd-5d83a18efbf2
  Args:
    source: Ernest_II_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (5bfbc2c3-d774-48fd-9212-ee726265782a)
 Call ID: 5bfbc2c3-d774-48fd-9212-ee726265782a
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (6623f7db-d033-45e3-bd2c-8f2aa026fead)
 Call ID: 6623f7db-d033-45e3-bd2c-8f2aa026fead
  Args:
    type: :Woman
    source: Countess_Karoline_von_Wartensleben
  AssignClass (ab8960e4-ed63-4dda-9d95-83e5ecd12af6)
 Call ID: ab8960e4-ed63-4dda-9d95-83e5ecd12af6
  Args:
    source: Countess_Karoline_von_Wartensleben
    type: :Person
  AddTriple (d3363357-4a6f-463d-b9f3-8e282e0cc75e)
 Call ID: d3363357-4a6f-463d-b9f3-8e282e0cc75e
  Args:
    source: Prince_Bernhard_of_Lippe
    target: Ernest_II_Count_of_Lippe-Biesterfeld
    relation: :hasFather
  AddTriple (abcfb64c-d75c-48ff-abd1-68653bd34935)
 Call ID: abcfb64c-d75c-48ff-abd1-68653bd34935
  Args:
    relation: :hasMother
    target: Countess_Karoline_von_Wartensleben
    source: Prince_Bernhard_of_Lippe
  AssignClass (b0ef785d-49a7-4f7c-8fae-d05a5dca65f5)
 Call ID: b0ef785d-49a7-4f7c-8fae-d05a5dca65f5
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Man
  AssignClass (92d53ad7-eea1-428a-99a7-1d2a99b4ac1a)
 Call ID: 92d53ad7-eea1-428a-99a7-1d2a99b4ac1a
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Person
  AddTriple (a7258e2f-3e04-439c-a146-eebffa78dd6e)
 Call ID: a7258e2f-3e04-439c-a146-eebffa78dd6e
  Args:
    source: Prince_Bernhard_of_Lippe
    target: Leopold_IV_Prince_of_Lippe
    relation: :hasBrother
  AssignClass (9907f796-a988-4bdf-8bc7-d5d2cdc35164)
 Call ID: 9907f796-a988-4bdf-8bc7-d5d2cdc35164
  Args:
    type: :Man
    source: Frederick_William_Count_of_Lippe-Biesterfeld
  AssignClass (b6c756f2-b741-4185-a16a-87a6cb4cc8e0)
 Call ID: b6c756f2-b741-4185-a16a-87a6cb4cc8e0
  Args:
    source: Frederick_William_Count_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (f7de67de-39f1-4715-96c0-cff533e21ef6)
 Call ID: f7de67de-39f1-4715-96c0-cff533e21ef6
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Woman
  AssignClass (3b4459db-7906-4d66-b81b-ff1c832a2c62)
 Call ID: 3b4459db-7906-4d66-b81b-ff1c832a2c62
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Person
  AddLiteral (973c52a5-888d-4515-8d3a-44836d68c42b)
 Call ID: 973c52a5-888d-4515-8d3a-44836d68c42b
  Args:
    source: Frederick_William_Count_of_Lippe-Biesterfeld
    literal_value: 1770
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (c5990ea2-096a-42cb-9700-233d9ef61165)
 Call ID: c5990ea2-096a-42cb-9700-233d9ef61165
  Args:
    source: Baroness_Armgard_von_Sierstorpff-Cramm
    type: :Woman
  AssignClass (3ec507d4-b28d-4bae-9581-72666748cc62)
 Call ID: 3ec507d4-b28d-4bae-9581-72666748cc62
  Args:
    source: Baroness_Armgard_von_Sierstorpff-Cramm
    type: :Person
  AddLiteral (5273e346-b468-4986-bd74-bde2f3d526bf)
 Call ID: 5273e346-b468-4986-bd74-bde2f3d526bf
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    relation: :hasMarriageYear
    source: Prince_Bernhard_of_Lippe
  AssignClass (e2746f23-ef17-435b-ae9c-d0f26a0ce4cc)
 Call ID: e2746f23-ef17-435b-ae9c-d0f26a0ce4cc
  Args:
    type: :Man
    source: Aschwin_of_Lippe-Biesterfeld
  AssignClass (3daa14ac-ba0a-41d7-be1d-dffb6e767f98)
 Call ID: 3daa14ac-ba0a-41d7-be1d-dffb6e767f98
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    type: :Person
  AddTriple (cda31496-be22-45b6-8321-24694eb8b549)
 Call ID: cda31496-be22-45b6-8321-24694eb8b549
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasFather
    target: Prince_Bernhard_of_Lippe
  AddTriple (99715f46-de43-492f-a70b-950f5fd7d405)
 Call ID: 99715f46-de43-492f-a70b-950f5fd7d405
  Args:
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMother
    target: Baroness_Armgard_von_Sierstorpff-Cramm
  AddTriple (95c3cfd4-0787-4dca-b14a-07ffc160a00c)
 Call ID: 95c3cfd4-0787-4dca-b14a-07ffc160a00c
  Args:
    target: Baroness_Armgard_von_Sierstorpff-Cramm
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  Finish (033f2103-b694-43fa-8936-82b4d3200093)
 Call ID: 033f2103-b694-43fa-8936-82b4d3200093
  Args:
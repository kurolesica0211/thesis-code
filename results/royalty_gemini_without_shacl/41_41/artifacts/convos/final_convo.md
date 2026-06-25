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
Infante Alfonso of Spain, Prince of the Two Sicilies, Duke of Calabria (30 November 1901 – 3 February 1964) was one of two claimants to the title of the head of the House of Bourbon-Two Sicilies from 1960 until his death in 1964.
He was the son of Prince Carlos of Bourbon-Two Sicilies and María de las Mercedes, Princess of Asturias.
He was born and died in Madrid, Spain.
Alfonso's mother was María de las Mercedes, Princess of Asturias, but she died in childbirth in 1904.
Alfonso XIII, King of Spain, was unmarried at the time so as the Princess of the Asturias's eldest son, the young infante became heir presumptive to the Spanish crown, though, unlike his mother, he never held the title of Prince of Asturias.
He was heir presumptive until the birth of his cousin, Alfonso, to Alfonso XIII and Queen Victoria Eugenie in 1907.
Marriage and issue

Alfonso married Princess Alice of Bourbon-Parma (1917–2017), his second cousin, daughter of Elias, Duke of Parma and Piacenza, and Archduchess Maria Anna of Austria, on 16 April 1936 in Vienna, Austria.



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
  AssignClass (36a94e17-76ed-4f37-9928-de06016ed5c4)
 Call ID: 36a94e17-76ed-4f37-9928-de06016ed5c4
  Args:
    type: :Man
    source: :Alfonso_of_Spain
  AssignClass (d26459d6-3a95-40cd-a9cf-633042ee477a)
 Call ID: d26459d6-3a95-40cd-a9cf-633042ee477a
  Args:
    type: :Person
    source: :Alfonso_of_Spain
  AddLiteral (68816ce6-e376-4c9e-a500-24bb8d81e4fc)
 Call ID: 68816ce6-e376-4c9e-a500-24bb8d81e4fc
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Alfonso_of_Spain
  AddLiteral (feaaaf38-44f6-429d-8331-9aa4baa01c67)
 Call ID: feaaaf38-44f6-429d-8331-9aa4baa01c67
  Args:
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Alfonso_of_Spain
  AssignClass (f32897c4-608f-4194-a9d3-bc8b065ad61f)
 Call ID: f32897c4-608f-4194-a9d3-bc8b065ad61f
  Args:
    source: :Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (fd8ae96c-c309-4ff3-8286-05d0ceda7cc5)
 Call ID: fd8ae96c-c309-4ff3-8286-05d0ceda7cc5
  Args:
    source: :Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (5e08b638-c45b-4ead-9aad-3ad66b88870d)
 Call ID: 5e08b638-c45b-4ead-9aad-3ad66b88870d
  Args:
    type: :Woman
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (666cc78f-b2a7-4c22-8e4a-0d2a231a5d74)
 Call ID: 666cc78f-b2a7-4c22-8e4a-0d2a231a5d74
  Args:
    type: :Person
    source: :Maria_de_las_Mercedes_Princess_of_Asturias
  AddTriple (f9a8cfc5-0d70-47df-836f-6599878d6618)
 Call ID: f9a8cfc5-0d70-47df-836f-6599878d6618
  Args:
    target: :Carlos_of_Bourbon-Two_Sicilies
    source: :Alfonso_of_Spain
    relation: :hasFather
  AddTriple (be08fa5b-962e-4fe1-a53c-4ecad380fdad)
 Call ID: be08fa5b-962e-4fe1-a53c-4ecad380fdad
  Args:
    target: :Maria_de_las_Mercedes_Princess_of_Asturias
    source: :Alfonso_of_Spain
    relation: :hasMother
  AssignClass (825a8c42-027d-4c6d-98f4-20326df6e72e)
 Call ID: 825a8c42-027d-4c6d-98f4-20326df6e72e
  Args:
    type: :Woman
    source: :Alice_of_Bourbon-Parma
  AssignClass (fabd03da-bc6e-4d42-8a9d-f8e25cd3a510)
 Call ID: fabd03da-bc6e-4d42-8a9d-f8e25cd3a510
  Args:
    type: :Person
    source: :Alice_of_Bourbon-Parma
  AddLiteral (0660d001-cb12-486b-8aa1-da92df7c4cb0)
 Call ID: 0660d001-cb12-486b-8aa1-da92df7c4cb0
  Args:
    source: :Alfonso_of_Spain
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1936
  AddTriple (dea38ecb-ca67-4098-8515-ef418e7809af)
 Call ID: dea38ecb-ca67-4098-8515-ef418e7809af
  Args:
    relation: :hasRelation
    source: :Alfonso_of_Spain
    target: :Alice_of_Bourbon-Parma
  AssignClass (78986b57-5656-471f-868d-912667c9c2c4)
 Call ID: 78986b57-5656-471f-868d-912667c9c2c4
  Args:
    type: :Man
    source: :Elias_Duke_of_Parma_and_Piacenza
  AssignClass (7af18ecf-1104-43bc-a525-03fd2148a290)
 Call ID: 7af18ecf-1104-43bc-a525-03fd2148a290
  Args:
    source: :Elias_Duke_of_Parma_and_Piacenza
    type: :Person
  AssignClass (2c326211-9289-4133-ba9b-129d037714c5)
 Call ID: 2c326211-9289-4133-ba9b-129d037714c5
  Args:
    source: :Maria_Anna_of_Austria
    type: :Woman
  AssignClass (1c5ae06e-59fb-4f0b-ab86-c4c2c64955d9)
 Call ID: 1c5ae06e-59fb-4f0b-ab86-c4c2c64955d9
  Args:
    type: :Person
    source: :Maria_Anna_of_Austria
  AddTriple (e2512cba-1c3f-48dc-9073-8ebd7c68246c)
 Call ID: e2512cba-1c3f-48dc-9073-8ebd7c68246c
  Args:
    target: :Elias_Duke_of_Parma_and_Piacenza
    source: :Alice_of_Bourbon-Parma
    relation: :hasFather
  AddTriple (b9c0528c-932b-4eb6-9eda-6515178a72a0)
 Call ID: b9c0528c-932b-4eb6-9eda-6515178a72a0
  Args:
    source: :Alice_of_Bourbon-Parma
    relation: :hasMother
    target: :Maria_Anna_of_Austria
  AssignClass (5ea67fb6-8cae-4f7d-93c6-1802ee86ce09)
 Call ID: 5ea67fb6-8cae-4f7d-93c6-1802ee86ce09
  Args:
    type: :Man
    source: :Alfonso_XIII_King_of_Spain
  AssignClass (36107558-1d1c-4ac2-b266-ba1054a36a8b)
 Call ID: 36107558-1d1c-4ac2-b266-ba1054a36a8b
  Args:
    type: :Person
    source: :Alfonso_XIII_King_of_Spain
  AssignClass (2dc5e0c1-7981-4ed2-89d2-91cd941b7c74)
 Call ID: 2dc5e0c1-7981-4ed2-89d2-91cd941b7c74
  Args:
    type: :Woman
    source: :Victoria_Eugenie_Queen_of_Spain
  AssignClass (f6b9fec6-8f89-4a9a-a56f-809ac5ef5ef9)
 Call ID: f6b9fec6-8f89-4a9a-a56f-809ac5ef5ef9
  Args:
    type: :Person
    source: :Victoria_Eugenie_Queen_of_Spain
  AssignClass (424a0243-9c0a-41ab-9219-168980161280)
 Call ID: 424a0243-9c0a-41ab-9219-168980161280
  Args:
    type: :Man
    source: :Alfonso_cousin_of_Infante_Alfonso
  AssignClass (a5802326-2aff-4960-8513-3bb21a34ab9b)
 Call ID: a5802326-2aff-4960-8513-3bb21a34ab9b
  Args:
    source: :Alfonso_cousin_of_Infante_Alfonso
    type: :Person
  AddTriple (8e2e187b-9d0a-479e-af2b-215caed0a211)
 Call ID: 8e2e187b-9d0a-479e-af2b-215caed0a211
  Args:
    target: :Alfonso_XIII_King_of_Spain
    relation: :hasFather
    source: :Alfonso_cousin_of_Infante_Alfonso
  AddTriple (4ebcd071-968c-4db6-9588-bd550c9c679d)
 Call ID: 4ebcd071-968c-4db6-9588-bd550c9c679d
  Args:
    target: :Victoria_Eugenie_Queen_of_Spain
    relation: :hasMother
    source: :Alfonso_cousin_of_Infante_Alfonso
  Finish (0cf733d8-844f-4b7c-a2f4-537160aafb44)
 Call ID: 0cf733d8-844f-4b7c-a2f4-537160aafb44
  Args:
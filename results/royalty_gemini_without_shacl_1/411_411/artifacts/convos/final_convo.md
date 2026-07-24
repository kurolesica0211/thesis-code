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
  AssignClass (077264f2-ac7d-442d-bb00-1d80d7c697b9)
 Call ID: 077264f2-ac7d-442d-bb00-1d80d7c697b9
  Args:
    source: Christian_Louis_of_Mecklenburg
    type: :Man
  AssignClass (1054e898-d9d8-49f8-8fe8-59355d56ac26)
 Call ID: 1054e898-d9d8-49f8-8fe8-59355d56ac26
  Args:
    type: :Person
    source: Christian_Louis_of_Mecklenburg
  AddLiteral (2cd218d2-abc6-4141-9d78-25d00b4f68b4)
 Call ID: 2cd218d2-abc6-4141-9d78-25d00b4f68b4
  Args:
    relation: :hasBirthYear
    source: Christian_Louis_of_Mecklenburg
    literal_value: 1912
    literal_type: xsd:integer
  AddLiteral (4a0a3e59-3408-4f16-9887-068e63546da1)
 Call ID: 4a0a3e59-3408-4f16-9887-068e63546da1
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Christian_Louis_of_Mecklenburg
    literal_value: 1996
  AssignClass (f9e3df3c-cf56-4b50-90b6-14d60631c87d)
 Call ID: f9e3df3c-cf56-4b50-90b6-14d60631c87d
  Args:
    source: Frederick_Francis_IV
    type: :Man
  AssignClass (50bb52d0-2b05-4b79-9008-8b4860a7f695)
 Call ID: 50bb52d0-2b05-4b79-9008-8b4860a7f695
  Args:
    type: :Person
    source: Frederick_Francis_IV
  AddTriple (2d3ed472-502f-4102-86f1-c32223b76cc7)
 Call ID: 2d3ed472-502f-4102-86f1-c32223b76cc7
  Args:
    source: Christian_Louis_of_Mecklenburg
    relation: :hasFather
    target: Frederick_Francis_IV
  AssignClass (e094837d-3c65-42c7-b59b-e01f0ab7e5c7)
 Call ID: e094837d-3c65-42c7-b59b-e01f0ab7e5c7
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AssignClass (1954d5f6-5d78-4c16-9550-b1c3a200ed32)
 Call ID: 1954d5f6-5d78-4c16-9550-b1c3a200ed32
  Args:
    source: Alexandra_of_Hanover
    type: :Person
  AddTriple (334a2613-0f16-4fa9-81d4-af904c36f123)
 Call ID: 334a2613-0f16-4fa9-81d4-af904c36f123
  Args:
    relation: :hasMother
    target: Alexandra_of_Hanover
    source: Christian_Louis_of_Mecklenburg
  AssignClass (4822410b-a41c-4f2d-8deb-170725e18898)
 Call ID: 4822410b-a41c-4f2d-8deb-170725e18898
  Args:
    type: :Woman
    source: Thyra_of_Mecklenburg
  AssignClass (04d5d5c8-c997-48bb-9d25-33f6dba07a36)
 Call ID: 04d5d5c8-c997-48bb-9d25-33f6dba07a36
  Args:
    source: Thyra_of_Mecklenburg
    type: :Person
  AddTriple (f7eb48f3-fe9e-4b3c-b43c-257db0108eab)
 Call ID: f7eb48f3-fe9e-4b3c-b43c-257db0108eab
  Args:
    target: Thyra_of_Mecklenburg
    relation: :hasSister
    source: Christian_Louis_of_Mecklenburg
  AssignClass (0e7f8787-06a9-4f44-8674-bb317c2a1840)
 Call ID: 0e7f8787-06a9-4f44-8674-bb317c2a1840
  Args:
    type: :Man
    source: Ernest_Augustus_of_Hanover
  AssignClass (3f58ae5e-5f16-4b34-b38e-0f793bb52128)
 Call ID: 3f58ae5e-5f16-4b34-b38e-0f793bb52128
  Args:
    type: :Person
    source: Ernest_Augustus_of_Hanover
  AssignClass (3ec78c8c-36a6-4f44-95f1-4ab84855a24a)
 Call ID: 3ec78c8c-36a6-4f44-95f1-4ab84855a24a
  Args:
    type: :Woman
    source: Thyra_of_Denmark
  AssignClass (9a04a717-16ff-43d7-ab83-2c0b3afbdcdb)
 Call ID: 9a04a717-16ff-43d7-ab83-2c0b3afbdcdb
  Args:
    source: Thyra_of_Denmark
    type: :Person
  AddTriple (19782465-63cb-4f49-8184-596ab3d9b880)
 Call ID: 19782465-63cb-4f49-8184-596ab3d9b880
  Args:
    source: Alexandra_of_Hanover
    target: Ernest_Augustus_of_Hanover
    relation: :hasFather
  AddTriple (0df660c1-744f-4140-a6e5-1498bd5db97f)
 Call ID: 0df660c1-744f-4140-a6e5-1498bd5db97f
  Args:
    source: Alexandra_of_Hanover
    relation: :hasMother
    target: Thyra_of_Denmark
  AssignClass (55a8de96-2e31-4283-8ef1-24c3df406321)
 Call ID: 55a8de96-2e31-4283-8ef1-24c3df406321
  Args:
    source: Barbara_of_Prussia
    type: :Woman
  AssignClass (6fe6b184-76fc-4afd-b40a-7ebfff7ed169)
 Call ID: 6fe6b184-76fc-4afd-b40a-7ebfff7ed169
  Args:
    source: Barbara_of_Prussia
    type: :Person
  AddLiteral (d0f9728c-8b7c-49f8-9503-dd17e58dab65)
 Call ID: d0f9728c-8b7c-49f8-9503-dd17e58dab65
  Args:
    relation: :hasBirthYear
    literal_value: 1920
    source: Barbara_of_Prussia
    literal_type: xsd:integer
  AddLiteral (2d2b41ef-3c5c-4713-9879-278cff0d10ac)
 Call ID: 2d2b41ef-3c5c-4713-9879-278cff0d10ac
  Args:
    literal_type: xsd:integer
    source: Barbara_of_Prussia
    literal_value: 1994
    relation: :hasDeathYear
  AddLiteral (40b702e3-0896-46c7-9546-f9ec50d2b546)
 Call ID: 40b702e3-0896-46c7-9546-f9ec50d2b546
  Args:
    source: Christian_Louis_of_Mecklenburg
    literal_value: 1954
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (50271c96-7de8-4c94-a294-d786d8db0437)
 Call ID: 50271c96-7de8-4c94-a294-d786d8db0437
  Args:
    relation: :hasRelation
    target: Barbara_of_Prussia
    source: Christian_Louis_of_Mecklenburg
  AssignClass (bf75aef2-80c3-4b3e-b7f9-de1d099ee2d3)
 Call ID: bf75aef2-80c3-4b3e-b7f9-de1d099ee2d3
  Args:
    type: :Man
    source: Sigismund_of_Prussia
  AssignClass (f7394750-b229-4964-9d4d-fe2750f8cd7a)
 Call ID: f7394750-b229-4964-9d4d-fe2750f8cd7a
  Args:
    source: Sigismund_of_Prussia
    type: :Person
  AssignClass (489bdf09-312c-4467-ab46-cb0c54d6dcec)
 Call ID: 489bdf09-312c-4467-ab46-cb0c54d6dcec
  Args:
    type: :Woman
    source: Charlotte_of_Saxe-Altenburg
  AssignClass (3486de9f-7074-416b-9782-6176bf83f441)
 Call ID: 3486de9f-7074-416b-9782-6176bf83f441
  Args:
    type: :Person
    source: Charlotte_of_Saxe-Altenburg
  AddTriple (2f67bb33-1b0f-4b67-acf2-63c8ce98c301)
 Call ID: 2f67bb33-1b0f-4b67-acf2-63c8ce98c301
  Args:
    target: Sigismund_of_Prussia
    relation: :hasFather
    source: Barbara_of_Prussia
  AddTriple (5df78abb-c0ec-4edd-996a-fa373ff236be)
 Call ID: 5df78abb-c0ec-4edd-996a-fa373ff236be
  Args:
    target: Charlotte_of_Saxe-Altenburg
    relation: :hasMother
    source: Barbara_of_Prussia
  Finish (9b62a8ef-fdfe-43be-b7ad-3d9817b9f2a1)
 Call ID: 9b62a8ef-fdfe-43be-b7ad-3d9817b9f2a1
  Args:
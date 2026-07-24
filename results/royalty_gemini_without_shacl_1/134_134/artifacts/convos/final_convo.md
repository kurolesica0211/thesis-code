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
Friedrich Franz, Hereditary Grand Duke of Mecklenburg-Schwerin (German: Friedrich Franz Erbgroßherzog von Mecklenburg-Schwerin; 22 April 1910 – 31 July 2001) was the heir apparent to the throne of Mecklenburg-Schwerin and a member of the Waffen-SS.
Early life

He was born in Schwerin, the eldest child of the reigning Grand Duke of Mecklenburg-Schwerin, Frederick Francis IV, and his wife Princess Alexandra of Hanover, a daughter of Crown Prince Ernest Augustus of Hanover (a first-cousin once removed of Queen Victoria) and Princess Thyra of Denmark, the youngest daughter of King Christian IX of Denmark.
He did not succeed to the throne, as the Grand Duchy was replaced with the Free State of Mecklenburg-Schwerin.
Upon the promulgation of the Weimar Constitution on 11 August 1919, titles of sovereigns such as emperor/empress, king/queen, grand duke/grand duchess, etc. were abolished.
He therefore became known as Friedrich Franz Herzog von Mecklenburg-Schwerin (or Friedrich Franz, Duke of Mecklenburg-Schwerin) de facto since the establishment of the Free State of Mecklenburg-Schwerin.
Post monarchy

In May 1931 against the will of his father, Friedrich Franz joined the SS and by 1936 he had been promoted to the rank of Hauptsturmführer (Captain).
In May 1943, a family council was called by the Grand Ducal family and Friedrich Franz was passed over as heir (of the family estates) in favour of his younger brother Duke Christian Louis, who would instead inherit the family property.
Friedrich Franz married Karin Elisabeth von Schaper (1920–2012), the daughter of Walter von Schaper and his wife Baroness Louise von Münchhausen, on 11 June 1941 at Schloß Wiligrad, near the Lake Schwerin.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e47e8181-05e3-45d7-b4f9-2ee8eeb45a54)
 Call ID: e47e8181-05e3-45d7-b4f9-2ee8eeb45a54
  Args:
    type: :Person
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AssignClass (82cfef49-8599-44be-89e3-fd97ee67cf83)
 Call ID: 82cfef49-8599-44be-89e3-fd97ee67cf83
  Args:
    source: Friedrich_Franz_Mecklenburg_Schwerin
    type: :Man
  AddLiteral (003f9b4f-a5f2-4e7a-aa15-483cfd23fee9)
 Call ID: 003f9b4f-a5f2-4e7a-aa15-483cfd23fee9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Friedrich_Franz_Mecklenburg_Schwerin
    literal_value: 1910
  AddLiteral (d4e9c8f5-cc0c-462f-becb-daa5b28f016d)
 Call ID: d4e9c8f5-cc0c-462f-becb-daa5b28f016d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Friedrich_Franz_Mecklenburg_Schwerin
    literal_value: 2001
  AssignClass (76cf7b09-291f-4e2c-8eb8-9c696fc97be1)
 Call ID: 76cf7b09-291f-4e2c-8eb8-9c696fc97be1
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AssignClass (c589a318-9fb2-4dbf-944d-a78b39b7a509)
 Call ID: c589a318-9fb2-4dbf-944d-a78b39b7a509
  Args:
    source: Frederick_Francis_IV
    type: :Man
  AssignClass (cb7f20d3-693d-4bc2-8ec2-fc77091e64a0)
 Call ID: cb7f20d3-693d-4bc2-8ec2-fc77091e64a0
  Args:
    type: :Person
    source: Princess_Alexandra_Hanover
  AssignClass (09ebeb95-1bd5-4366-8c20-4aa3f95eaea7)
 Call ID: 09ebeb95-1bd5-4366-8c20-4aa3f95eaea7
  Args:
    source: Princess_Alexandra_Hanover
    type: :Woman
  AddTriple (6f2ed00a-e7dc-42b9-b6eb-7b705290b551)
 Call ID: 6f2ed00a-e7dc-42b9-b6eb-7b705290b551
  Args:
    source: Friedrich_Franz_Mecklenburg_Schwerin
    relation: :hasFather
    target: Frederick_Francis_IV
  AddTriple (cc836cc4-0cc4-4eee-afef-2b10adc621d5)
 Call ID: cc836cc4-0cc4-4eee-afef-2b10adc621d5
  Args:
    target: Princess_Alexandra_Hanover
    relation: :hasMother
    source: Friedrich_Franz_Mecklenburg_Schwerin
  AssignClass (4e3b0461-cb02-4127-afa5-01364e210e5d)
 Call ID: 4e3b0461-cb02-4127-afa5-01364e210e5d
  Args:
    source: Ernest_Augustus_Hanover
    type: :Person
  AssignClass (47bdd6f0-d89d-4650-ae4a-b4dfde77b67e)
 Call ID: 47bdd6f0-d89d-4650-ae4a-b4dfde77b67e
  Args:
    type: :Man
    source: Ernest_Augustus_Hanover
  AssignClass (27dde9fd-79ad-4eec-8701-d3861012d5fb)
 Call ID: 27dde9fd-79ad-4eec-8701-d3861012d5fb
  Args:
    type: :Person
    source: Princess_Thyra_Denmark
  AssignClass (517f7c4b-85ac-4cf3-9d48-ebb6df6233e4)
 Call ID: 517f7c4b-85ac-4cf3-9d48-ebb6df6233e4
  Args:
    type: :Woman
    source: Princess_Thyra_Denmark
  AddTriple (00ac7650-ad96-4151-aef4-c67ba2f52703)
 Call ID: 00ac7650-ad96-4151-aef4-c67ba2f52703
  Args:
    target: Ernest_Augustus_Hanover
    relation: :hasFather
    source: Princess_Alexandra_Hanover
  AddTriple (dfe9c172-6c91-4cda-8031-8b31317f3333)
 Call ID: dfe9c172-6c91-4cda-8031-8b31317f3333
  Args:
    source: Princess_Alexandra_Hanover
    relation: :hasMother
    target: Princess_Thyra_Denmark
  AssignClass (bcd3ffb9-d03b-4b22-ac33-70cfd9378a1c)
 Call ID: bcd3ffb9-d03b-4b22-ac33-70cfd9378a1c
  Args:
    type: :Person
    source: Christian_IX_Denmark
  AssignClass (621cbcfa-dd78-4e23-8f8a-89ac01cbd089)
 Call ID: 621cbcfa-dd78-4e23-8f8a-89ac01cbd089
  Args:
    type: :Man
    source: Christian_IX_Denmark
  AddTriple (3ebaa1cd-9861-47d4-9013-4aec0d7e481b)
 Call ID: 3ebaa1cd-9861-47d4-9013-4aec0d7e481b
  Args:
    source: Princess_Thyra_Denmark
    relation: :hasFather
    target: Christian_IX_Denmark
  AssignClass (a76eb6ae-6f0b-4a2e-872a-55a631a89a61)
 Call ID: a76eb6ae-6f0b-4a2e-872a-55a631a89a61
  Args:
    type: :Person
    source: Christian_Louis
  AssignClass (3b6a0309-955c-4a04-bbb9-45da4e6b4f8c)
 Call ID: 3b6a0309-955c-4a04-bbb9-45da4e6b4f8c
  Args:
    source: Christian_Louis
    type: :Man
  AddTriple (057ee938-dde4-4182-b5f6-fc56d7e440cd)
 Call ID: 057ee938-dde4-4182-b5f6-fc56d7e440cd
  Args:
    source: Christian_Louis
    relation: :isBrotherOf
    target: Friedrich_Franz_Mecklenburg_Schwerin
  AssignClass (aca4670e-33a1-44ce-b8bb-159c624b8687)
 Call ID: aca4670e-33a1-44ce-b8bb-159c624b8687
  Args:
    source: Karin_Elisabeth_von_Schaper
    type: :Person
  AssignClass (fe2c77b8-d54e-454b-810c-04d373959ec1)
 Call ID: fe2c77b8-d54e-454b-810c-04d373959ec1
  Args:
    type: :Woman
    source: Karin_Elisabeth_von_Schaper
  AddLiteral (4b4d9c74-1e5a-4722-9c4a-8ac9ee4c9675)
 Call ID: 4b4d9c74-1e5a-4722-9c4a-8ac9ee4c9675
  Args:
    source: Karin_Elisabeth_von_Schaper
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (da0ac8fa-b9c7-4359-ad45-4e1367224039)
 Call ID: da0ac8fa-b9c7-4359-ad45-4e1367224039
  Args:
    source: Karin_Elisabeth_von_Schaper
    literal_value: 2012
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (44e2d38c-c965-4963-af59-bd1a3642fd92)
 Call ID: 44e2d38c-c965-4963-af59-bd1a3642fd92
  Args:
    literal_value: 1941
    source: Friedrich_Franz_Mecklenburg_Schwerin
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (abe9cd6f-7290-4b5b-8712-31ca27494ad6)
 Call ID: abe9cd6f-7290-4b5b-8712-31ca27494ad6
  Args:
    target: Karin_Elisabeth_von_Schaper
    source: Friedrich_Franz_Mecklenburg_Schwerin
    relation: :hasRelation
  AssignClass (b56e07fb-4ee3-475c-9f4f-e80e3eccc9f1)
 Call ID: b56e07fb-4ee3-475c-9f4f-e80e3eccc9f1
  Args:
    source: Walter_von_Schaper
    type: :Person
  AssignClass (50245d6b-0830-4155-89cc-c7d811c7ab18)
 Call ID: 50245d6b-0830-4155-89cc-c7d811c7ab18
  Args:
    type: :Man
    source: Walter_von_Schaper
  AssignClass (6e3005e5-829e-4bed-a9d1-922abb3a2e55)
 Call ID: 6e3005e5-829e-4bed-a9d1-922abb3a2e55
  Args:
    source: Louise_von_Münchhausen
    type: :Person
  AssignClass (2445f674-067d-40f0-b05d-5448a79295fd)
 Call ID: 2445f674-067d-40f0-b05d-5448a79295fd
  Args:
    source: Louise_von_Münchhausen
    type: :Woman
  AddTriple (9b7d1f08-d15c-4c48-a112-e961e6c5f96f)
 Call ID: 9b7d1f08-d15c-4c48-a112-e961e6c5f96f
  Args:
    source: Karin_Elisabeth_von_Schaper
    relation: :hasFather
    target: Walter_von_Schaper
  AddTriple (e18dbf28-0d14-49eb-9822-29c64f0f2930)
 Call ID: e18dbf28-0d14-49eb-9822-29c64f0f2930
  Args:
    source: Karin_Elisabeth_von_Schaper
    relation: :hasMother
    target: Louise_von_Münchhausen
  Finish (4e908b74-31df-4462-96a4-c943c36cc79c)
 Call ID: 4e908b74-31df-4462-96a4-c943c36cc79c
  Args:
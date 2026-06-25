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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Floris Frederik Martijn of Orange-Nassau, van Vollenhoven (born 10 April 1975) is the fourth and youngest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Prince Floris has three older brothers: Prince Maurits, Prince Bernhard, Prince Pieter-Christiaan


Marriage and children

Prince Floris announced his engagement to Aimée Söhngen, the daughter of Hans Söhngen and Eleonoor Stammeijer, on 25 February 2005.
Prince Floris had been 10th in the line of succession to the Dutch throne but decided not to seek parliamentary approval for his marriage, as would be required in the Netherlands.
Prince Floris and Princess Aimée's first child, Magali Margriet Eleonoor van Vollenhoven, was born at VU University Medical Center in Amsterdam on 9 October 2007.
She is named for Aimée's sister, Magali Söhngen, and her mother Eleonoor, as well as Princess Margriet.
Their second child, Eliane Sophia Carolina van Vollenhoven, was born at VU University Medical Center in Amsterdam on 5 July 2009.
Their third child, a son named Willem Jan Johannes Pieter Floris, was born at HMC Bronovo  in The Hague on 1 July 2013.
Ancestry

References

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (ca316f2f-8152-4552-bcc3-e144c7a0e50e)
 Call ID: ca316f2f-8152-4552-bcc3-e144c7a0e50e
  Args:
    type: :Man
    source: :Prince_Floris
  AssignClass (6848c04b-6b08-45b1-b567-726c62449dbd)
 Call ID: 6848c04b-6b08-45b1-b567-726c62449dbd
  Args:
    source: :Prince_Floris
    type: :Person
  AddLiteral (8612a0fc-427e-444c-8604-1c04d86aece2)
 Call ID: 8612a0fc-427e-444c-8604-1c04d86aece2
  Args:
    literal_value: 1975
    literal_type: xsd:integer
    source: :Prince_Floris
    relation: :hasBirthYear
  AssignClass (d85842e7-347b-41af-8da9-d1c951143116)
 Call ID: d85842e7-347b-41af-8da9-d1c951143116
  Args:
    source: :Princess_Margriet
    type: :Woman
  AssignClass (b6fec13d-64c8-4a6d-9817-913684cd3f72)
 Call ID: b6fec13d-64c8-4a6d-9817-913684cd3f72
  Args:
    source: :Princess_Margriet
    type: :Person
  AssignClass (fa738696-2d8f-4919-b19a-c1546560003a)
 Call ID: fa738696-2d8f-4919-b19a-c1546560003a
  Args:
    type: :Man
    source: :Pieter_van_Vollenhoven
  AssignClass (4ddb023f-ab0f-43fb-b9ff-2fccd5154808)
 Call ID: 4ddb023f-ab0f-43fb-b9ff-2fccd5154808
  Args:
    source: :Pieter_van_Vollenhoven
    type: :Person
  AddTriple (658914fa-125b-4a8a-8d3f-cbdb361e5b2c)
 Call ID: 658914fa-125b-4a8a-8d3f-cbdb361e5b2c
  Args:
    relation: :hasMother
    target: :Princess_Margriet
    source: :Prince_Floris
  AddTriple (ecb017d5-09b1-4e09-bdd0-8a6226a335f3)
 Call ID: ecb017d5-09b1-4e09-bdd0-8a6226a335f3
  Args:
    relation: :hasFather
    target: :Pieter_van_Vollenhoven
    source: :Prince_Floris
  AssignClass (96fea2b8-12c8-4081-b8dc-e5551c104632)
 Call ID: 96fea2b8-12c8-4081-b8dc-e5551c104632
  Args:
    type: :Man
    source: :Prince_Maurits
  AssignClass (f0447580-6b07-4d14-afd9-21cacdf73d20)
 Call ID: f0447580-6b07-4d14-afd9-21cacdf73d20
  Args:
    source: :Prince_Maurits
    type: :Person
  AssignClass (a4c09a03-7bed-43a7-bf0d-10ea33976b91)
 Call ID: a4c09a03-7bed-43a7-bf0d-10ea33976b91
  Args:
    type: :Man
    source: :Prince_Bernhard
  AssignClass (6fae13e3-b68d-4fad-b7fe-3731fdb6ff0d)
 Call ID: 6fae13e3-b68d-4fad-b7fe-3731fdb6ff0d
  Args:
    type: :Person
    source: :Prince_Bernhard
  AssignClass (f203e887-ba2f-4651-b3c2-a1c3c2bf52ad)
 Call ID: f203e887-ba2f-4651-b3c2-a1c3c2bf52ad
  Args:
    type: :Man
    source: :Prince_Pieter-Christiaan
  AssignClass (50f4b2fe-f174-4b86-9ca4-d24b4b3fe6a6)
 Call ID: 50f4b2fe-f174-4b86-9ca4-d24b4b3fe6a6
  Args:
    type: :Person
    source: :Prince_Pieter-Christiaan
  AddTriple (03289e94-0af7-41cb-9ac2-4c34f127508d)
 Call ID: 03289e94-0af7-41cb-9ac2-4c34f127508d
  Args:
    source: :Prince_Floris
    relation: :hasBrother
    target: :Prince_Maurits
  AddTriple (4a6b9fd8-2792-4d41-abde-99c35412ce68)
 Call ID: 4a6b9fd8-2792-4d41-abde-99c35412ce68
  Args:
    target: :Prince_Bernhard
    relation: :hasBrother
    source: :Prince_Floris
  AddTriple (4eda3897-4603-4a41-b0a8-0614b563e4e6)
 Call ID: 4eda3897-4603-4a41-b0a8-0614b563e4e6
  Args:
    source: :Prince_Floris
    target: :Prince_Pieter-Christiaan
    relation: :hasBrother
  AssignClass (169814d8-5b00-48c6-8f10-a1bc7f5b2379)
 Call ID: 169814d8-5b00-48c6-8f10-a1bc7f5b2379
  Args:
    source: :Princess_Aimée
    type: :Woman
  AssignClass (c31caf61-a6d7-4c05-a130-bba421764025)
 Call ID: c31caf61-a6d7-4c05-a130-bba421764025
  Args:
    source: :Princess_Aimée
    type: :Person
  AssignClass (ab909ba0-2eee-4c4b-986e-1ba1e181e06b)
 Call ID: ab909ba0-2eee-4c4b-986e-1ba1e181e06b
  Args:
    source: :Hans_Söhngen
    type: :Man
  AssignClass (236107a4-7f74-44a2-b6ba-17eb8c34ca53)
 Call ID: 236107a4-7f74-44a2-b6ba-17eb8c34ca53
  Args:
    type: :Person
    source: :Hans_Söhngen
  AssignClass (06cfbe8e-19ac-4c90-9a15-d7ad5ff225b3)
 Call ID: 06cfbe8e-19ac-4c90-9a15-d7ad5ff225b3
  Args:
    type: :Woman
    source: :Eleonoor_Stammeijer
  AssignClass (d80b3516-ac23-45fb-a72f-6369cbcf5bca)
 Call ID: d80b3516-ac23-45fb-a72f-6369cbcf5bca
  Args:
    source: :Eleonoor_Stammeijer
    type: :Person
  AddTriple (bf39e351-910d-4d45-b484-00b941180ab9)
 Call ID: bf39e351-910d-4d45-b484-00b941180ab9
  Args:
    source: :Princess_Aimée
    relation: :hasFather
    target: :Hans_Söhngen
  AddTriple (d7a4782c-ed21-4369-b5dc-031cd241f810)
 Call ID: d7a4782c-ed21-4369-b5dc-031cd241f810
  Args:
    relation: :hasMother
    target: :Eleonoor_Stammeijer
    source: :Princess_Aimée
  AssignClass (2b645408-e273-40c7-b888-27fe2eeb866c)
 Call ID: 2b645408-e273-40c7-b888-27fe2eeb866c
  Args:
    type: :Woman
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
  AssignClass (fb9ed75d-124c-4f26-88db-c873290fa1cc)
 Call ID: fb9ed75d-124c-4f26-88db-c873290fa1cc
  Args:
    type: :Person
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
  AddTriple (3bd99c90-37de-4cc1-b0ea-1a98165deca7)
 Call ID: 3bd99c90-37de-4cc1-b0ea-1a98165deca7
  Args:
    target: :Prince_Floris
    relation: :hasFather
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
  AddTriple (e893fa42-af3a-4342-b167-3cb4e8205355)
 Call ID: e893fa42-af3a-4342-b167-3cb4e8205355
  Args:
    source: :Magali_Margriet_Eleonoor_van_Vollenhoven
    relation: :hasMother
    target: :Princess_Aimée
  AssignClass (4fef4e0e-0269-49b7-b768-29dc667c6cc3)
 Call ID: 4fef4e0e-0269-49b7-b768-29dc667c6cc3
  Args:
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
    type: :Woman
  AssignClass (b91e226a-cf6f-44cf-8b33-171d58a4432b)
 Call ID: b91e226a-cf6f-44cf-8b33-171d58a4432b
  Args:
    type: :Person
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
  AddTriple (83dd5c83-9e7e-4b76-b9ac-16ceac88d495)
 Call ID: 83dd5c83-9e7e-4b76-b9ac-16ceac88d495
  Args:
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
    target: :Prince_Floris
    relation: :hasFather
  AddTriple (ca24c56b-8717-4574-a397-76a1d27f8e76)
 Call ID: ca24c56b-8717-4574-a397-76a1d27f8e76
  Args:
    source: :Eliane_Sophia_Carolina_van_Vollenhoven
    relation: :hasMother
    target: :Princess_Aimée
  AssignClass (6d37047e-84bd-4d6f-bc26-015a034f580b)
 Call ID: 6d37047e-84bd-4d6f-bc26-015a034f580b
  Args:
    type: :Man
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AssignClass (de48ad5c-3c4e-46cc-b3ed-e7d786f3812a)
 Call ID: de48ad5c-3c4e-46cc-b3ed-e7d786f3812a
  Args:
    type: :Person
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AddTriple (7dd47d8e-e7d1-4be4-ae18-256267d39580)
 Call ID: 7dd47d8e-e7d1-4be4-ae18-256267d39580
  Args:
    relation: :hasFather
    target: :Prince_Floris
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AddTriple (a70db64a-4a9c-4b95-9286-0ed81585f3d5)
 Call ID: a70db64a-4a9c-4b95-9286-0ed81585f3d5
  Args:
    target: :Princess_Aimée
    relation: :hasMother
    source: :Willem_Jan_Johannes_Pieter_Floris_van_Vollenhoven
  AssignClass (59b4ba04-21a0-4f21-a50d-647ee2242632)
 Call ID: 59b4ba04-21a0-4f21-a50d-647ee2242632
  Args:
    type: :Woman
    source: :Magali_Söhngen
  AssignClass (30448de8-0ecb-4587-a943-ca980f00bf8b)
 Call ID: 30448de8-0ecb-4587-a943-ca980f00bf8b
  Args:
    source: :Magali_Söhngen
    type: :Person
  AddTriple (895c493b-eda6-4e7d-aeef-4ee9cd65218a)
 Call ID: 895c493b-eda6-4e7d-aeef-4ee9cd65218a
  Args:
    source: :Princess_Aimée
    target: :Magali_Söhngen
    relation: :hasSister
  Finish (10caa01c-16ea-4e2c-9665-481c9b4da568)
 Call ID: 10caa01c-16ea-4e2c-9665-481c9b4da568
  Args: